"""Embedding generation and mathematical document chunking package."""

from .chunker import MathDocumentChunker, chunk_document
from .models import ChunkMetadata, EmbeddedChunk, TextChunk
from .pipeline import EmbeddingPipeline, process_parsed_document
from .provider import EmbeddingProvider, SentenceTransformerEmbeddingProvider

__all__ = [
    "ChunkMetadata",
    "TextChunk",
    "EmbeddedChunk",
    "EmbeddingProvider",
    "SentenceTransformerEmbeddingProvider",
    "MathDocumentChunker",
    "chunk_document",
    "EmbeddingPipeline",
    "process_parsed_document",
]
