"""FAISS-backed vector store for document embeddings."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Sequence

import faiss
import numpy as np

from src.embeddings.models import EmbeddedChunk

logger = logging.getLogger(__name__)


class FAISSVectorStore:
    """FAISS-based vector store for indexing and retrieving embedded chunks."""

    DEFAULT_STORE_DIR = Path("exports/vector_store")

    def __init__(self, dimension: int = 384) -> None:
        """Initialize FAISS vector store with given vector dimension.

        Args:
            dimension: Vector embedding dimension (default: 384).
        """
        if dimension <= 0:
            raise ValueError("Vector dimension must be a positive integer")

        self.dimension = dimension
        self.index: faiss.IndexFlatIP = faiss.IndexFlatIP(dimension)
        self._chunk_ids: list[str] = []
        self._metadata_store: dict[str, dict[str, Any]] = {}

    def number_of_vectors(self) -> int:
        """Return the total number of vectors indexed in the store."""
        return self.index.ntotal

    def add_chunks(self, embedded_chunks: Sequence[EmbeddedChunk]) -> None:
        """Add embedded chunks to the FAISS index and metadata store.

        Args:
            embedded_chunks: Sequence of EmbeddedChunk objects to index.
        """
        if not embedded_chunks:
            logger.warning("No embedded chunks provided to add_chunks")
            return

        vectors: list[list[float]] = []
        for chunk in embedded_chunks:
            if not isinstance(chunk, EmbeddedChunk):
                raise TypeError(f"Expected EmbeddedChunk, got {type(chunk)}")
            if len(chunk.embedding) != self.dimension:
                raise ValueError(
                    f"Vector dimension mismatch: expected {self.dimension}, "
                    f"got {len(chunk.embedding)}"
                )

            vectors.append(chunk.embedding)
            self._chunk_ids.append(chunk.chunk_id)
            self._metadata_store[chunk.chunk_id] = {
                "chunk_id": chunk.chunk_id,
                "text": getattr(chunk, "text", ""),
                "metadata": chunk.metadata.to_dict(),
            }

        vector_matrix = np.array(vectors, dtype=np.float32)
        faiss.normalize_L2(vector_matrix)

        self.index.add(vector_matrix)
        logger.info(
            "Added %d vector(s) to FAISS index. Total index size: %d",
            len(embedded_chunks),
            self.index.ntotal,
        )

    def search(
        self, query_embedding: Sequence[float], top_k: int = 5
    ) -> list[dict[str, Any]]:
        """Search nearest neighbor vectors using Cosine Similarity.

        Args:
            query_embedding: Query embedding vector.
            top_k: Number of nearest neighbors to retrieve.

        Returns:
            List of result dictionaries containing chunk_id, score, text, and metadata,
            sorted by similarity score in descending order.
        """
        if self.index.ntotal == 0:
            logger.warning("Search called on an empty vector store")
            return []
        if len(query_embedding) != self.dimension:
            raise ValueError(
                f"Query vector dimension mismatch: expected {self.dimension}, "
                f"got {len(query_embedding)}"
            )

        query_matrix = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_matrix)

        actual_k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_matrix, actual_k)

        results: list[dict[str, Any]] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self._chunk_ids):
                continue

            chunk_id = self._chunk_ids[idx]
            chunk_data = self._metadata_store.get(chunk_id, {})
            results.append(
                {
                    "chunk_id": chunk_id,
                    "score": float(score),
                    "text": chunk_data.get("text", ""),
                    "metadata": chunk_data.get("metadata", {}),
                }
            )

        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def get_chunk(self, chunk_id: str) -> dict[str, Any] | None:
        """Retrieve stored metadata for a specific chunk_id."""
        return self._metadata_store.get(chunk_id)

    def save(self, directory: str | Path | None = None) -> Path:
        """Save FAISS index and metadata store to disk.

        Args:
            directory: Target directory path (default: exports/vector_store/).

        Returns:
            Path to saved directory.
        """
        dir_path = Path(directory) if directory else self.DEFAULT_STORE_DIR
        dir_path.mkdir(parents=True, exist_ok=True)

        index_path = dir_path / "index.faiss"
        meta_path = dir_path / "metadata.json"

        try:
            faiss.write_index(self.index, str(index_path))
            payload = {
                "dimension": self.dimension,
                "chunk_ids": self._chunk_ids,
                "metadata_store": self._metadata_store,
            }
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)

            logger.info("Saved FAISS index and metadata to: %s", dir_path)
            return dir_path
        except Exception as exc:
            logger.error("Failed to save vector store to '%s': %s", dir_path, exc)
            raise RuntimeError(f"Could not save vector store: {exc}") from exc

    def load(self, directory: str | Path | None = None) -> None:
        """Load FAISS index and metadata store from disk.

        Args:
            directory: Source directory path (default: exports/vector_store/).
        """
        dir_path = Path(directory) if directory else self.DEFAULT_STORE_DIR
        index_path = dir_path / "index.faiss"
        meta_path = dir_path / "metadata.json"

        if not index_path.is_file():
            raise FileNotFoundError(f"FAISS index file not found: {index_path}")
        if not meta_path.is_file():
            raise FileNotFoundError(f"Metadata store file not found: {meta_path}")

        try:
            self.index = faiss.read_index(str(index_path))
            with open(meta_path, "r", encoding="utf-8") as f:
                payload = json.load(f)

            self.dimension = int(payload.get("dimension", self.dimension))
            self._chunk_ids = list(payload.get("chunk_ids", []))
            self._metadata_store = dict(payload.get("metadata_store", {}))

            logger.info(
                "Loaded FAISS vector store from '%s' (%d vectors, dim=%d)",
                dir_path,
                self.index.ntotal,
                self.dimension,
            )
        except Exception as exc:
            logger.error("Failed to load vector store from '%s': %s", dir_path, exc)
            raise RuntimeError(f"Could not load vector store: {exc}") from exc
