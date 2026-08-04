"""Unit tests for Day 5 Step 2, Step 2.5 & Step 2.6 Retrieval Engine, Scoring Abstraction, Explainability, and Statistics."""

from __future__ import annotations

from typing import Any, Sequence
import pytest

from config.retrieval_config import RetrievalConfig
from src.embeddings.models import ChunkMetadata, EmbeddedChunk
from src.embeddings.provider import EmbeddingProvider
from src.graph.models import GraphEdge, GraphNode, RelationType, ResearchGraph
from src.graph.service import GraphService
from src.rag.query_processing import QueryAnalysis, QueryIntent, QueryProcessor, ReferencedEntity
from src.rag.retrieval import (
    BaseRetriever,
    BaseScoringEngine,
    HybridRetriever,
    HybridScoringWeights,
    RankingReasonGenerator,
    RetrievalEngine,
    RetrievalExplanation,
    RetrievalResponse,
    RetrievalResult,
    RetrievalStatistics,
    RetrievalStatisticsCalculator,
    WeightedScoringEngine,
)
from src.rag.vector_store import FAISSVectorStore


class MockEmbeddingProvider(EmbeddingProvider):
    """Fast, deterministic mock embedding provider for unit tests."""

    @property
    def model_name(self) -> str:
        return "mock-embedding-model"

    @property
    def embedding_dimension(self) -> int:
        return 384

    def embed_text(self, text: str) -> list[float]:
        v = [0.0] * 384
        val = (len(text) % 50 + 1) / 50.0
        v[0] = val
        v[1] = 0.5
        return v

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        return [self.embed_text(t) for t in texts]


@pytest.fixture(scope="module")
def sample_retrieval_setup() -> tuple[EmbeddingProvider, FAISSVectorStore, GraphService]:
    """Fixture providing populated mock embedding provider, FAISS vector store, and GraphService."""
    provider = MockEmbeddingProvider()
    vector_store = FAISSVectorStore(dimension=384)

    # Chunks
    chunks_data = [
        {
            "chunk_id": "c_def_2.1",
            "text": "Definition 2.1 (Compact Operator). A linear operator T is compact if bounded sets map to relatively compact sets.",
            "section_title": "2. Definitions",
            "section_type": "definition",
        },
        {
            "chunk_id": "c_thm_3",
            "text": "Theorem 3 (Spectral Decomposition). Every compact operator T has a discrete spectrum of eigenvalues.",
            "section_title": "3. Main Theorems",
            "section_type": "theorem",
        },
        {
            "chunk_id": "c_lem_3.1",
            "text": "Lemma 3 (Approximation Lemma). Compact operators are limits of finite rank operators, proving Theorem 3.",
            "section_title": "3. Main Theorems",
            "section_type": "lemma",
        },
    ]

    embedded: list[EmbeddedChunk] = []
    for item in chunks_data:
        v = provider.embed_text(item["text"])
        meta = ChunkMetadata(
            paper_id="paper1",
            paper_title="Compact Operators",
            section_id="sec1",
            section_title=item["section_title"],
            section_type=item["section_type"],
            page_start=1,
            page_end=1,
            entity_type=item["section_type"],
        )
        embedded.append(EmbeddedChunk(chunk_id=item["chunk_id"], text=item["text"], embedding=v, metadata=meta))

    vector_store.add_chunks(embedded)

    # Graph
    graph = ResearchGraph()
    for item in chunks_data:
        graph.add_node(
            GraphNode(
                node_id=item["chunk_id"],
                node_type=item["section_type"],
                label=item["section_title"],
                text=item["text"],
                paper_id="paper1",
            )
        )
    graph.add_edge(
        GraphEdge(
            edge_id="e_lem_thm",
            source_id="c_lem_3.1",
            target_id="c_thm_3",
            relation_type=RelationType.PROVES,
        )
    )

    graph_service = GraphService(graph=graph)
    return provider, vector_store, graph_service


class TestScoringEngineAbstraction:
    """Test suite for Day 5 Step 2.6 BaseScoringEngine & WeightedScoringEngine."""

    def test_weighted_scoring_engine_computation(self) -> None:
        """Test WeightedScoringEngine produces exact linear combination score."""
        weights = HybridScoringWeights(
            semantic_weight=0.45,
            entity_weight=0.20,
            intent_weight=0.15,
            graph_weight=0.10,
            boost_weight=0.10,
        )
        engine = WeightedScoringEngine(weights=weights)

        score = engine.compute_score(
            semantic_score=1.0,
            entity_score=1.0,
            intent_score=1.0,
            graph_score=1.0,
            boost_score=1.0,
        )
        assert score == 1.0

        partial_score = engine.compute_score(
            semantic_score=0.8,
            entity_score=0.5,
            intent_score=0.0,
            graph_score=0.0,
            boost_score=1.0,
        )
        # 0.45*0.8 + 0.20*0.5 + 0.10*1.0 = 0.36 + 0.10 + 0.10 = 0.56
        assert abs(partial_score - 0.56) < 1e-4

    def test_custom_scoring_engine_injection(
        self, sample_retrieval_setup: tuple[EmbeddingProvider, FAISSVectorStore, GraphService]
    ) -> None:
        """Test injecting a custom BaseScoringEngine implementation into HybridRetriever."""
        class MockCustomScoringEngine(BaseScoringEngine):
            def compute_score(
                self,
                semantic_score: float,
                entity_score: float,
                intent_score: float,
                graph_score: float,
                boost_score: float,
                candidate_metadata: dict[str, Any] | None = None,
            ) -> float:
                # Custom scoring rule: pure semantic score multiplier
                return round(semantic_score * 0.99, 4)

        provider, vector_store, graph_service = sample_retrieval_setup
        custom_engine = MockCustomScoringEngine()

        retriever = HybridRetriever(
            provider=provider,
            vector_store=vector_store,
            graph_service=graph_service,
            scoring_engine=custom_engine,
        )

        query_proc = QueryProcessor()
        analysis = query_proc.process("What is Definition 2.1?")
        results = retriever.retrieve(analysis, top_k=1)

        assert len(results) == 1
        assert abs(results[0].final_score - round(results[0].semantic_score * 0.99, 4)) < 1e-4


class TestRetrievalResultSerialization:
    """Test suite for RetrievalResult and RetrievalExplanation models."""

    def test_to_dict_and_from_dict(self) -> None:
        """Test roundtrip dictionary serialization of RetrievalResult and RetrievalExplanation."""
        exp = RetrievalExplanation(
            semantic_score=0.90,
            entity_score=1.0,
            intent_score=1.0,
            graph_score=0.5,
            boost_score=0.8,
            final_score=0.88,
            matched_entities=["Definition 2.1"],
            boost_reason="Definition section boost",
            ranking_reason="Matched Definition 2.1 | High semantic similarity",
        )
        res = RetrievalResult(
            chunk_id="chunk_101",
            text="Definition 2.1 is compact.",
            paper_id="paper_1",
            paper_title="Functional Analysis",
            section_title="2. Definitions",
            section_type="definition",
            semantic_score=0.90,
            entity_score=1.0,
            intent_score=1.0,
            graph_score=0.5,
            boost_score=0.8,
            final_score=0.88,
            matched_entities=["Definition 2.1"],
            rank=1,
            explanation=exp,
        )

        data = res.to_dict()
        assert data["chunk_id"] == "chunk_101"
        assert data["rank"] == 1
        assert data["explanation"]["ranking_reason"] == "Matched Definition 2.1 | High semantic similarity"

        reconstructed = RetrievalResult.from_dict(data)
        assert reconstructed.chunk_id == res.chunk_id
        assert reconstructed.rank == 1
        assert reconstructed.explanation is not None
        assert reconstructed.explanation.matched_entities == ["Definition 2.1"]


class TestRetrievalConfig:
    """Test suite for RetrievalConfig settings."""

    def test_default_config(self) -> None:
        """Test default retrieval configuration values."""
        cfg = RetrievalConfig()
        assert cfg.semantic_weight == 0.45
        assert cfg.top_k == 5
        weights = cfg.get_scoring_weights()
        assert isinstance(weights, HybridScoringWeights)

    def test_custom_config(self) -> None:
        """Test custom RetrievalConfig values and serialization."""
        cfg = RetrievalConfig(semantic_weight=0.6, entity_weight=0.4, top_k=10)
        data = cfg.to_dict()
        assert data["top_k"] == 10

        restored = RetrievalConfig.from_dict(data)
        assert restored.semantic_weight == 0.6
        assert restored.top_k == 10

    def test_invalid_config(self) -> None:
        """Test invalid configuration parameters raise ValueError."""
        with pytest.raises(ValueError):
            RetrievalConfig(top_k=0)


class TestRankingReasonGenerator:
    """Test suite for rule-based RankingReasonGenerator."""

    def test_generate_reason(self) -> None:
        """Test generating human-readable ranking reasons."""
        res = RetrievalResult(
            chunk_id="c1",
            text="Definition 2.1 text",
            semantic_score=0.89,
            entity_score=1.0,
            intent_score=1.0,
            final_score=0.92,
            matched_entities=["Definition 2.1"],
            section_type="definition",
        )
        exp = RankingReasonGenerator.generate_explanation(
            result=res,
            matched_symbols=["λ"],
            boost_reason="Definition section boost",
        )
        assert "Matched Definition 2.1" in exp.ranking_reason
        assert "High semantic similarity" in exp.ranking_reason
        assert "Definition section boost" in exp.ranking_reason


class TestRetrievalStatistics:
    """Test suite for RetrievalStatisticsCalculator."""

    def test_statistics_calculation(self) -> None:
        """Test statistics calculation across candidate results."""
        c1 = RetrievalResult(chunk_id="c1", text="t1", semantic_score=0.9, entity_score=1.0, intent_score=1.0, final_score=0.95, matched_entities=["Definition 2.1"], section_type="definition")
        c2 = RetrievalResult(chunk_id="c2", text="t2", semantic_score=0.7, entity_score=0.0, intent_score=0.5, final_score=0.65, section_type="theorem")

        stats = RetrievalStatisticsCalculator.calculate([c1, c2], retrieval_time_ms=12.5)
        assert stats.number_of_candidates == 2
        assert stats.highest_score == 0.95
        assert stats.lowest_score == 0.65
        assert stats.average_semantic_score == 0.8
        assert stats.retrieval_time_ms == 12.5


class TestHybridRetrieverEngine:
    """Test suite for HybridRetriever and RetrievalEngine integration."""

    def test_semantic_retrieval(
        self, sample_retrieval_setup: tuple[EmbeddingProvider, FAISSVectorStore, GraphService]
    ) -> None:
        """Test semantic retrieval generates candidate chunks and returns scores."""
        provider, vector_store, graph_service = sample_retrieval_setup
        retriever = HybridRetriever(provider=provider, vector_store=vector_store, graph_service=graph_service)

        query_proc = QueryProcessor()
        analysis = query_proc.process("What is Definition 2.1?")

        results = retriever.retrieve(analysis, top_k=3)
        assert len(results) > 0
        assert results[0].semantic_score >= 0.0
        assert results[0].rank == 1
        assert results[0].explanation is not None

    def test_retrieve_with_response(
        self, sample_retrieval_setup: tuple[EmbeddingProvider, FAISSVectorStore, GraphService]
    ) -> None:
        """Test RetrievalEngine.retrieve_with_response returns full response container."""
        provider, vector_store, graph_service = sample_retrieval_setup
        retriever = HybridRetriever(provider=provider, vector_store=vector_store, graph_service=graph_service)
        engine = RetrievalEngine(retriever=retriever)

        response = engine.retrieve_with_response("What is Definition 2.1?", top_k=3)
        assert isinstance(response, RetrievalResponse)
        assert len(response.results) == 3
        assert response.statistics.number_of_candidates == 3
        assert response.results[0].explanation is not None
        assert response.results[0].rank == 1

    def test_top_k_ordering_and_explanations(
        self, sample_retrieval_setup: tuple[EmbeddingProvider, FAISSVectorStore, GraphService]
    ) -> None:
        """Test candidate results are strictly ordered by rank and carry explanations."""
        provider, vector_store, graph_service = sample_retrieval_setup
        retriever = HybridRetriever(provider=provider, vector_store=vector_store, graph_service=graph_service)
        engine = RetrievalEngine(retriever=retriever)

        results = engine.retrieve("Which lemma proves theorem 3?", top_k=3)
        for i, res in enumerate(results):
            assert res.rank == i + 1
            assert res.explanation is not None
            assert res.explanation.ranking_reason != ""
            if i > 0:
                assert results[i - 1].final_score >= results[i].final_score
