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


# Process-wide singleton model cache to avoid re-downloading or reloading model weights
_MODEL_CACHE: dict[str, Any] = {}


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
        if self._model is not None:
            if hasattr(self._model, "get_embedding_dimension"):
                dim = self._model.get_embedding_dimension()
            else:
                dim = self._model.get_sentence_embedding_dimension()
            return int(dim) if dim is not None else 384
        return 384

    def _load_model(self) -> Any:
        """Lazy-load the SentenceTransformer model on first invocation with global caching."""
        if self._model is not None:
            return self._model

        cache_key = f"{self._model_name}:{self._device or 'cpu'}"
        if cache_key in _MODEL_CACHE:
            self._model = _MODEL_CACHE[cache_key]
            return self._model

        try:
            import os
            import warnings
            
            # Configure HuggingFace authentication token & environment defaults
            os.environ.setdefault("HF_HUB_DISABLE_IMPLICIT_TOKEN_WARNING", "1")
            os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
            warnings.filterwarnings("ignore", message=".*unauthenticated requests to the HF Hub.*")
            warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub")

            hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")

            from sentence_transformers import SentenceTransformer

            logger.info(
                "Loading SentenceTransformer model: %s (device=%s)",
                self._model_name,
                self._device or "default",
            )
            
            kwargs: dict[str, Any] = {}
            if self._device:
                kwargs["device"] = self._device
            if hf_token:
                kwargs["token"] = hf_token

            loaded_model = SentenceTransformer(self._model_name, **kwargs)

            _MODEL_CACHE[cache_key] = loaded_model
            self._model = loaded_model
            logger.info(
                "Successfully loaded model %s into process cache",
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


class MockEmbeddingProvider(EmbeddingProvider):
    """Lightweight mock embedding provider for fast unit testing."""

    def __init__(self, dimension: int = 384, model_name: str = "mock-mini-l6") -> None:
        self._dimension = dimension
        self._model_name = model_name

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def embedding_dimension(self) -> int:
        return self._dimension

    def embed_text(self, text: str) -> list[float]:
        return [0.0] * self._dimension

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        return [[0.0] * self._dimension for _ in texts]

