"""Verification test for Day 3 Step 6 Semantic Retriever."""

import unittest
from pathlib import Path

from src.embeddings.pipeline import process_parsed_document
from src.embeddings.provider import SentenceTransformerEmbeddingProvider
from src.rag.retriever import SemanticRetriever
from src.rag.vector_store import FAISSVectorStore


class TestSemanticRetriever(unittest.TestCase):
    """Test suite for SemanticRetriever verification."""

    @classmethod
    def setUpClass(cls) -> None:
        sample_path = Path("exports/parser_outputs/paper_6cd768c13674.json")
        if not sample_path.is_file():
            raise unittest.SkipTest(f"Sample parsed JSON not found at {sample_path}")

        cls.provider = SentenceTransformerEmbeddingProvider("all-MiniLM-L6-v2")
        cls.embedded_chunks = process_parsed_document(
            sample_path, provider=cls.provider
        )
        cls.vector_store = FAISSVectorStore(dimension=cls.provider.embedding_dimension)
        cls.vector_store.add_chunks(cls.embedded_chunks)
        cls.retriever = SemanticRetriever(
            provider=cls.provider, vector_store=cls.vector_store
        )


    def test_retrieve_scibert(self) -> None:
        results = self.retriever.retrieve("SciBERT", top_k=3)
        self.assertGreaterEqual(len(results), 1)
        top_result = results[0]
        self.assertIn("score", top_result)
        self.assertIn("text", top_result)
        self.assertIn("chunk_id", top_result)
        self.assertIn("paper_title", top_result)
        self.assertGreater(top_result["score"], 0.0)

    def test_retrieve_queries(self) -> None:
        queries = ["definition of compactness", "main theorem", "proof", "SciBERT"]
        for q in queries:
            results = self.retriever.retrieve(q, top_k=3)
            self.assertGreaterEqual(len(results), 1)
            self.assertIn("chunk_id", results[0])
            self.assertIn("score", results[0])
            self.assertIn("section_title", results[0])


if __name__ == "__main__":
    unittest.main()
