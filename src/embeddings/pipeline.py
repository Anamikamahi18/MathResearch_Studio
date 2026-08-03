"""Embedding pipeline orchestrator module."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from .chunker import MathDocumentChunker
from .models import EmbeddedChunk, TextChunk
from .provider import EmbeddingProvider, SentenceTransformerEmbeddingProvider

logger = logging.getLogger(__name__)


class EmbeddingPipeline:
    """Orchestrates document chunking and vector embedding generation."""

    def __init__(
        self,
        chunker: MathDocumentChunker | None = None,
        provider: EmbeddingProvider | None = None,
        batch_size: int = 32,
    ) -> None:
        """Initialize embedding pipeline with chunker and provider.

        Args:
            chunker: Optional MathDocumentChunker instance. Defaults to default chunker.
            provider: Optional EmbeddingProvider instance. Defaults to SentenceTransformer.
            batch_size: Number of text chunks to embed in a single batch.
        """
        if batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")

        self.chunker = chunker or MathDocumentChunker()
        self.provider = provider or SentenceTransformerEmbeddingProvider()
        self.batch_size = batch_size

    def process_document(
        self, document: dict[str, Any]
    ) -> list[EmbeddedChunk]:
        """Process a parsed document dictionary into a list of EmbeddedChunk objects.

        Args:
            document: Parsed document dictionary adhering to Schema v1.0.

        Returns:
            List of EmbeddedChunk instances containing vector embeddings and metadata.
        """
        if not isinstance(document, dict):
            logger.error(
                "Invalid document input: expected dict, got %s", type(document)
            )
            raise TypeError(f"Document must be a dictionary, got {type(document)}")

        # 1. Chunk document
        text_chunks: list[TextChunk] = self.chunker.chunk_document(document)
        if not text_chunks:
            logger.warning(
                "No text chunks generated for document '%s'",
                document.get("paper_id"),
            )
            return []

        # 2. Extract texts and batch generate embeddings
        embedded_chunks: list[EmbeddedChunk] = []
        total_chunks = len(text_chunks)
        logger.info(
            "Generating embeddings for %d chunk(s) using model '%s' (batch_size=%d)",
            total_chunks,
            self.provider.model_name,
            self.batch_size,
        )

        for i in range(0, total_chunks, self.batch_size):
            batch_text_chunks = text_chunks[i : i + self.batch_size]
            batch_texts = [chunk.text for chunk in batch_text_chunks]

            try:
                batch_embeddings = self.provider.embed_texts(batch_texts)
            except Exception as exc:
                logger.error(
                    "Embedding generation failed for batch [%d:%d]: %s",
                    i,
                    i + len(batch_texts),
                    exc,
                )
                raise RuntimeError(
                    f"Failed to generate embeddings for batch starting at index {i}: {exc}"
                ) from exc

            if len(batch_embeddings) != len(batch_text_chunks):
                raise RuntimeError(
                    f"Embedding count mismatch: expected {len(batch_text_chunks)}, got {len(batch_embeddings)}"
                )

            for text_chunk, vector in zip(batch_text_chunks, batch_embeddings):
                embedded_chunks.append(
                    EmbeddedChunk(
                        chunk_id=text_chunk.chunk_id,
                        text=text_chunk.text,
                        embedding=vector,
                        metadata=text_chunk.metadata,
                    )
                )

        logger.info(
            "Successfully created %d EmbeddedChunk(s) for paper '%s'",
            len(embedded_chunks),
            document.get("paper_id"),
        )
        return embedded_chunks

    def process_file(
        self, file_path: str | Path
    ) -> list[EmbeddedChunk]:
        """Load a parsed JSON file from disk and process it into EmbeddedChunks.

        Args:
            file_path: Path to parsed document JSON file.

        Returns:
            List of EmbeddedChunk objects.
        """
        path = Path(file_path)
        if not path.is_file():
            logger.error("Parsed JSON file not found: %s", path)
            raise FileNotFoundError(f"Parsed JSON file not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                document = json.load(f)
        except Exception as exc:
            logger.error("Failed to read JSON file '%s': %s", path, exc)
            raise RuntimeError(
                f"Could not load JSON from file '{path}': {exc}"
            ) from exc

        return self.process_document(document)


def process_parsed_document(
    document_or_path: dict[str, Any] | str | Path,
    chunker: MathDocumentChunker | None = None,
    provider: EmbeddingProvider | None = None,
    batch_size: int = 32,
) -> list[EmbeddedChunk]:
    """Convenience function to process a parsed document dictionary or file path."""
    pipeline = EmbeddingPipeline(
        chunker=chunker,
        provider=provider,
        batch_size=batch_size,
    )
    if isinstance(document_or_path, (str, Path)):
        return pipeline.process_file(document_or_path)
    return pipeline.process_document(document_or_path)
