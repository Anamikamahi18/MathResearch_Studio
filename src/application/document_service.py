"""DocumentService application service for paper upload, parsing, storing, and library management."""

from __future__ import annotations

import json
import logging
import shutil
from pathlib import Path
from typing import Any

from src.embeddings.pipeline import EmbeddingPipeline
from src.embeddings.provider import EmbeddingProvider
from src.graph.service import GraphService as BackendGraphService
from src.parser.pipeline import parse_pdf
from src.rag.vector_store import FAISSVectorStore

logger = logging.getLogger(__name__)


class DocumentService:
    """Application service for managing PDF paper uploads, parsing, indexing, and library state."""

    def __init__(
        self,
        upload_dir: str | Path = "uploads",
        parsed_dir: str | Path = "exports/parser_outputs",
        vector_store: FAISSVectorStore | None = None,
        graph_service: BackendGraphService | None = None,
        embedding_provider: EmbeddingProvider | None = None,
    ) -> None:
        """Initialize DocumentService with directory paths and service dependencies.

        Args:
            upload_dir: Directory for storing raw PDF uploads.
            parsed_dir: Directory where parsed JSON outputs are stored.
            vector_store: Optional FAISSVectorStore instance.
            graph_service: Optional backend GraphService instance.
            embedding_provider: Optional EmbeddingProvider instance.
        """
        self.upload_dir = Path(upload_dir)
        self.parsed_dir = Path(parsed_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.parsed_dir.mkdir(parents=True, exist_ok=True)

        self.vector_store = vector_store or FAISSVectorStore()
        self.graph_service = graph_service or BackendGraphService()
        self.embedding_pipeline = EmbeddingPipeline(provider=embedding_provider)

        self._paper_library: dict[str, dict[str, Any]] = {}

    def upload_paper(
        self,
        file_source: str | Path | bytes,
        filename: str | None = None,
    ) -> Path:
        """Upload and save a paper PDF to the library upload directory.

        Args:
            file_source: File path (str/Path) or raw PDF bytes.
            filename: Target file name if bytes or overriding name.

        Returns:
            Path to the saved PDF file in the upload directory.
        """
        if isinstance(file_source, (str, Path)):
            source_path = Path(file_source)
            if not source_path.exists():
                raise FileNotFoundError(f"Upload source file not found: {source_path}")
            target_name = filename or source_path.name
            target_path = self.upload_dir / target_name
            if source_path.resolve() != target_path.resolve():
                shutil.copy2(source_path, target_path)
            logger.info("Uploaded paper file saved to: %s", target_path)
            return target_path

        elif isinstance(file_source, bytes):
            if not filename:
                raise ValueError("Filename must be provided when uploading bytes")
            target_path = self.upload_dir / filename
            target_path.write_bytes(file_source)
            logger.info("Uploaded paper bytes saved to: %s", target_path)
            return target_path

        else:
            raise TypeError(
                f"Unsupported file_source type: {type(file_source)}. Expected str, Path, or bytes."
            )

    def parse_paper(
        self,
        file_path: str | Path,
        output_dir: str | Path | None = None,
    ) -> dict[str, Any]:
        """Parse a PDF paper into a structured JSON representation.

        Args:
            file_path: Path to the PDF paper file.
            output_dir: Optional custom output directory for parsed JSON.

        Returns:
            Parsed document dictionary conforming to Schema v1.0.
        """
        path = Path(file_path)
        out_dir = Path(output_dir) if output_dir else self.parsed_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        json_path = parse_pdf(path, out_dir)
        with open(json_path, "r", encoding="utf-8") as f:
            parsed_doc: dict[str, Any] = json.load(f)

        logger.info("Successfully parsed paper '%s' -> %s", path.name, json_path)
        return parsed_doc

    def store_paper(self, parsed_document: dict[str, Any]) -> dict[str, Any]:
        """Index a parsed paper into vector store, update Knowledge Graph, and library catalog.

        Args:
            parsed_document: Parsed paper dictionary conforming to Schema v1.0.

        Returns:
            Dictionary containing indexing metrics (paper_id, title, chunk_count, graph_node_count).
        """
        if not isinstance(parsed_document, dict):
            raise TypeError("parsed_document must be a dictionary")

        paper_id = parsed_document.get("paper_id") or "unknown_paper"
        metadata = parsed_document.get("metadata") or {}
        title = metadata.get("title") or paper_id

        # 1. Embed and index in vector store
        embedded_chunks = self.embedding_pipeline.process_document(parsed_document)
        if embedded_chunks:
            self.vector_store.add_chunks(embedded_chunks)

        # 2. Add to backend Knowledge Graph
        self.graph_service.build_from_document(parsed_document)

        # 3. Catalog paper in library index
        paper_summary = {
            "paper_id": paper_id,
            "title": title,
            "authors": metadata.get("authors", []),
            "year": metadata.get("year"),
            "section_count": len(parsed_document.get("sections", [])),
            "chunk_count": len(embedded_chunks),
            "equation_count": len(parsed_document.get("equations", [])),
            "reference_count": len(parsed_document.get("references", [])),
            "ingested_at": metadata.get("ingested_at"),
            "raw_document": parsed_document,
        }
        self._paper_library[paper_id] = paper_summary

        logger.info(
            "Stored paper '%s' (%s): %d chunks indexed into vector store",
            paper_id,
            title,
            len(embedded_chunks),
        )

        return {
            "paper_id": paper_id,
            "title": title,
            "chunk_count": len(embedded_chunks),
            "graph_node_count": len(self.graph_service.graph.nodes),
            "graph_edge_count": len(self.graph_service.graph.edges),
        }

    def refresh_library(self) -> list[dict[str, Any]]:
        """Rescan parsed_dir for parsed paper JSON files and refresh the library index.

        Returns:
            List of paper metadata summary dictionaries in the library.
        """
        if not self.parsed_dir.exists():
            return self.list_papers()

        json_files = sorted(self.parsed_dir.glob("*.json"))
        for jf in json_files:
            try:
                with open(jf, "r", encoding="utf-8") as f:
                    doc = json.load(f)
                if isinstance(doc, dict) and "paper_id" in doc:
                    paper_id = doc["paper_id"]
                    if paper_id not in self._paper_library:
                        self.store_paper(doc)
            except Exception as exc:
                logger.warning("Could not read/index parsed paper file '%s': %s", jf, exc)

        return self.list_papers()

    def list_papers(self) -> list[dict[str, Any]]:
        """Return a list of summary records for all papers currently in the library."""
        return list(self._paper_library.values())

    def get_paper(self, paper_id: str) -> dict[str, Any] | None:
        """Retrieve a paper record by its paper_id."""
        return self._paper_library.get(paper_id)
