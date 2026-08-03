"""Embedding provider interfaces and implementations."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Sequence

logger = logging.getLogger(__name__)


class EmbeddingProvider(ABC):
    """Abstract base class for text embedding providers."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the identifier of the underlying embedding model."""
        raise NotImplementedError

    @property
    @abstractmethod
    def embedding_dimension(self) -> int:
        """Return the vector dimension produced by this embedding provider."""
        raise NotImplementedError

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """Generate a vector embedding for a single string.

        Args:
            text: Input text string to embed.

        Returns:
            List of floats representing the vector embedding.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        """Generate vector embeddings for a sequence of text strings.

        Args:
            texts: Sequence of input text strings to embed.

        Returns:
            List of vector embeddings (list of lists of floats).
        """
        raise NotImplementedError


class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    """SentenceTransformers-backed embedding provider implementation."""

    DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        device: str | None = None,
        normalize_embeddings: bool = True,
    ) -> None:
        """Initialize the SentenceTransformer embedding provider.

        Args:
            model_name: Name or path of the SentenceTransformer model.
            device: Device for model inference ('cpu', 'cuda', etc.).
            normalize_embeddings: Whether to normalize embedding vectors.
        """
        self._model_name = model_name
        self._device = device
        self._normalize_embeddings = normalize_embeddings
        self._model: Any = None

    @property
    def model_name(self) -> str:
        """Return the name of the active SentenceTransformer model."""
        return self._model_name

    @property
    def embedding_dimension(self) -> int:
        """Return the vector dimension of the active model."""
        model = self._load_model()
        if hasattr(model, "get_embedding_dimension"):
            dim = model.get_embedding_dimension()
        else:
            dim = model.get_sentence_embedding_dimension()
        return int(dim) if dim is not None else 384

    def _load_model(self) -> Any:
        """Lazy-load the SentenceTransformer model on first invocation."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer

                logger.info(
                    "Loading SentenceTransformer model: %s (device=%s)",
                    self._model_name,
                    self._device or "default",
                )
                if self._device:
                    self._model = SentenceTransformer(
                        self._model_name, device=self._device
                    )
                else:
                    self._model = SentenceTransformer(self._model_name)
                logger.info(
                    "Successfully loaded model %s",
                    self._model_name,
                )
            except Exception as exc:
                logger.error(
                    "Failed to load SentenceTransformer model '%s': %s",
                    self._model_name,
                    exc,
                )
                raise RuntimeError(
                    f"Could not load embedding model '{self._model_name}': {exc}"
                ) from exc
        return self._model

    def embed_text(self, text: str) -> list[float]:
        """Generate a vector embedding for a single text string."""
        if not isinstance(text, str):
            raise TypeError(f"Expected text to be a string, got {type(text)}")

        results = self.embed_texts([text])
        if not results:
            raise RuntimeError("Embedding generation produced no results")
        return results[0]

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        """Generate vector embeddings for a sequence of text strings."""
        if not texts:
            return []

        text_list = list(texts)
        for idx, item in enumerate(text_list):
            if not isinstance(item, str):
                raise TypeError(
                    f"Item at index {idx} is not a string (got {type(item)})"
                )

        model = self._load_model()
        try:
            embeddings = model.encode(
                text_list,
                normalize_embeddings=self._normalize_embeddings,
                show_progress_bar=False,
            )
            return [
                [float(val) for val in row] for row in embeddings
            ]
        except Exception as exc:
            logger.error("Error during embedding generation: %s", exc)
            raise RuntimeError(
                f"Embedding generation failed for batch of size {len(texts)}: {exc}"
            ) from exc
