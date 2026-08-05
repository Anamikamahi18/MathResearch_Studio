"""ChatService application service for executing the complete RAG pipeline."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from src.embeddings.provider import EmbeddingProvider, SentenceTransformerEmbeddingProvider
from src.graph.service import GraphService as BackendGraphService
from src.rag.answer_generator import AnswerGenerator
from src.rag.citation_engine import CitationEngine
from src.rag.evidence import EvidenceMapper
from src.rag.grounding import GroundingVerifier
from src.rag.guardrails import FinalResearchResponse, GuardrailDecisionEngine
from src.rag.llm import BaseLLMAdapter
from src.rag.prompt_builder import PromptBuilder, PromptRequest
from src.rag.query_processing import QueryProcessor
from src.rag.retrieval import HybridRetriever, RetrievalResult
from src.rag.vector_store import FAISSVectorStore

logger = logging.getLogger(__name__)


class ChatService:
    """Application service executing the end-to-end RAG question-answering pipeline."""

    def __init__(
        self,
        vector_store: FAISSVectorStore | None = None,
        graph_service: BackendGraphService | None = None,
        embedding_provider: EmbeddingProvider | None = None,
        llm_adapter: BaseLLMAdapter | None = None,
    ) -> None:
        """Initialize ChatService with RAG pipeline components.

        Args:
            vector_store: Optional FAISSVectorStore instance.
            graph_service: Optional backend GraphService instance.
            embedding_provider: Optional EmbeddingProvider instance.
            llm_adapter: Optional custom BaseLLMAdapter instance.
        """
        self.vector_store = vector_store or FAISSVectorStore()
        self.graph_service = graph_service or BackendGraphService()
        self.embedding_provider = (
            embedding_provider or SentenceTransformerEmbeddingProvider()
        )

        # RAG pipeline stage engines
        self.query_processor = QueryProcessor()
        self.retriever = HybridRetriever(
            provider=self.embedding_provider,
            vector_store=self.vector_store,
            graph_service=self.graph_service,
        )
        self.prompt_builder = PromptBuilder()
        self.answer_generator = AnswerGenerator(llm_adapter=llm_adapter)
        self.evidence_mapper = EvidenceMapper()
        self.citation_engine = CitationEngine()
        self.grounding_verifier = GroundingVerifier()
        self.guardrail_engine = GuardrailDecisionEngine()

        self._chat_history: list[dict[str, Any]] = []

    def receive_question(
        self,
        question: str,
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> FinalResearchResponse:
        """Execute the complete 8-stage RAG pipeline for a researcher question.

        Pipeline Stages:
            1. Query Processing (`QueryProcessor`)
            2. Multi-signal Retrieval (`HybridRetriever`)
            3. Context & Prompt Assembly (`PromptBuilder`)
            4. LLM Answer Generation (`AnswerGenerator`)
            5. Evidence Mapping & Span Extraction (`EvidenceMapper`)
            6. Citation Generation & Formatting (`CitationEngine`)
            7. Grounding Verification & Claim Auditing (`GroundingVerifier`)
            8. Guardrail Decision Policy & Final Response (`GuardrailDecisionEngine`)

        Args:
            question: Natural language or mathematical question string.
            top_k: Top-K document chunks to retrieve as evidence candidates.
            filters: Optional metadata filters.

        Returns:
            FinalResearchResponse object evaluated through Guardrails policy.
        """
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question string cannot be empty")

        clean_question = question.strip()
        logger.info("Executing RAG pipeline for question: '%s'", clean_question)

        # 1. Query Processing
        query_analysis = self.query_processor.process(clean_question)

        # 2. Retrieval
        try:
            candidates: list[RetrievalResult] = self.retriever.retrieve(
                query_analysis=query_analysis,
                top_k=top_k,
            )
        except Exception as exc:
            logger.warning("HybridRetriever failed (%s), returning empty candidates", exc)
            candidates = []

        # Apply metadata filters if provided
        if filters and candidates:
            candidates = self._filter_candidates(candidates, filters)

        # 3. Prompt Building
        prompt_req = PromptRequest(
            query=query_analysis,
            retrieval_response=candidates,
        )
        prompt_resp = self.prompt_builder.build_prompt(prompt_req)

        # 4. Answer Generation
        ans_resp = self.answer_generator.generate_answer(prompt_resp)

        # 5. Evidence Mapping
        ev_bundle = self.evidence_mapper.map_evidence(
            answer_response=ans_resp,
            retrieval_response=candidates,
        )

        # 6. Citation Engine
        cit_bundle = self.citation_engine.generate_citations(
            answer_response=ans_resp,
            evidence_bundle=ev_bundle,
        )

        # 7. Grounding Verification
        gr_report = self.grounding_verifier.verify_grounding(
            answer_response=ans_resp,
            evidence_bundle=ev_bundle,
            citation_bundle=cit_bundle,
        )

        # 8. Guardrails Policy & Final Response
        final_response: FinalResearchResponse = self.guardrail_engine.process_and_build_response(
            answer_response=ans_resp,
            evidence_bundle=ev_bundle,
            citation_bundle=cit_bundle,
            grounding_report=gr_report,
        )

        # Append to chat history
        history_item = {
            "question": clean_question,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "decision": final_response.decision.value,
            "status": final_response.status.value,
            "answer_preview": final_response.answer_text[:150],
            "response": final_response,
        }
        self._chat_history.append(history_item)

        logger.info(
            "RAG pipeline completed for '%s' -> Decision: %s",
            clean_question,
            final_response.decision.value,
        )

        return final_response

    def _filter_candidates(
        self,
        candidates: list[RetrievalResult],
        filters: dict[str, Any],
    ) -> list[RetrievalResult]:
        """Filter retrieval candidate items based on filter criteria."""
        target_paper_id = filters.get("paper_id")
        target_section_type = filters.get("section_type")
        min_score = filters.get("min_score")

        filtered: list[RetrievalResult] = []
        for cand in candidates:
            if target_paper_id is not None:
                if isinstance(target_paper_id, list):
                    if cand.paper_id not in target_paper_id:
                        continue
                elif cand.paper_id != target_paper_id:
                    continue

            if target_section_type is not None:
                if cand.section_type.lower() != str(target_section_type).lower():
                    continue

            if min_score is not None:
                if cand.final_score < float(min_score):
                    continue

            filtered.append(cand)
        return filtered

    def get_chat_history(self) -> list[dict[str, Any]]:
        """Return full Q&A chat history."""
        return list(self._chat_history)

    def clear_chat_history(self) -> None:
        """Clear Q&A chat session history."""
        self._chat_history.clear()
