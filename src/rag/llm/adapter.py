"""Mock LLM adapter implementation for testing and offline development."""

from __future__ import annotations

import logging
import time

from src.rag.llm.base import BaseLLMAdapter
from src.rag.llm.models import LLMMetadata, LLMRequest, LLMResponse

logger = logging.getLogger(__name__)


class MockLLMAdapter(BaseLLMAdapter):
    """Deterministic mock LLM adapter that operates offline without calling external APIs."""

    def __init__(self, model_name: str = "mock-math-v1") -> None:
        """Initialize MockLLMAdapter.

        Args:
            model_name: Default model identifier.
        """
        self.model_name = model_name
        logger.info("Initialized MockLLMAdapter (model='%s')", self.model_name)

    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a deterministic mock response string without calling any external LLM service.

        Args:
            request: LLMRequest container.

        Returns:
            LLMResponse containing deterministic text and metadata.

        Raises:
            TypeError: If request is not an instance of LLMRequest.
        """
        if not isinstance(request, LLMRequest):
            raise TypeError(f"Expected LLMRequest, got {type(request).__name__}")

        start_time = time.perf_counter()

        prompt_str = request.prompt_text or request.user_prompt or "No prompt provided"
        # Deterministic mock response generation
        mock_output = (
            f"[Mock LLM Response]\n"
            f"Based on the supplied mathematical context, the query is resolved as follows:\n"
            f"1. Direct Answer: Formal mathematical statement verified.\n"
            f"2. Context Analysis: Processed prompt of {len(prompt_str)} chars.\n"
            f"3. Note: Generated via MockLLMAdapter for testing pipeline integrity."
        )

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        prompt_tokens = len(prompt_str) // 4
        completion_tokens = len(mock_output) // 4
        total_tokens = prompt_tokens + completion_tokens

        metadata = LLMMetadata(
            provider="mock",
            model=request.model or self.model_name,
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            finish_reason="stop",
            extra_info={"mock_execution": True},
        )

        logger.info("MockLLMAdapter generated %d tokens in %.2f ms", total_tokens, latency_ms)

        return LLMResponse(
            raw_text=mock_output,
            request=request,
            metadata=metadata,
        )

    def health_check(self) -> bool:
        """Mock health check always succeeds."""
        return True

    def supports_streaming(self) -> bool:
        """Mock adapter does not implement streaming."""
        return False
