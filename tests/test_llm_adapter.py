"""Unit tests for Day 5 Step 3.5 Provider-Agnostic LLM Adapter Layer."""

from __future__ import annotations

import os
import pytest

from config.llm_config import LLMConfig
from src.rag.llm import (
    BaseLLMAdapter,
    LLMAdapterFactory,
    LLMMetadata,
    LLMRequest,
    LLMResponse,
    MockLLMAdapter,
    ProviderConfig,
)
from src.rag.prompt_builder.models import PromptResponse


class CustomTestAdapter(BaseLLMAdapter):
    """Dummy custom adapter for testing factory registration."""

    def __init__(self, model_name: str = "custom-v1", **kwargs) -> None:
        self.model_name = model_name

    def generate(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            raw_text="Custom Output",
            request=request,
            metadata=LLMMetadata(provider="custom", model=self.model_name),
        )

    def health_check(self) -> bool:
        return True

    def supports_streaming(self) -> bool:
        return True


class TestLLMModels:
    """Test data models, serialization, and factory constructors."""

    def test_provider_config_serialization(self) -> None:
        config = ProviderConfig(
            provider_name="mock",
            model_name="mock-model",
            temperature=0.2,
            max_tokens=1024,
        )
        data = config.to_dict()
        assert data["provider_name"] == "mock"
        assert data["model_name"] == "mock-model"
        assert data["temperature"] == 0.2
        assert data["max_tokens"] == 1024

    def test_llm_request_from_prompt_response(self) -> None:
        prompt_resp = PromptResponse(
            system_prompt="System Prompt",
            user_prompt="User Prompt",
            full_prompt="Full Prompt",
            estimated_tokens=100,
            context_coverage=0.8,
            prompt_version="v1.0",
        )
        req = LLMRequest.from_prompt_response(
            prompt_response=prompt_resp,
            provider="mock",
            model="mock-math-v1",
        )
        assert req.prompt_text == "Full Prompt"
        assert req.system_prompt == "System Prompt"
        assert req.user_prompt == "User Prompt"
        assert req.metadata["estimated_prompt_tokens"] == 100
        assert req.metadata["context_coverage"] == 0.8
        assert req.to_dict()["has_prompt_response"] is True

    def test_llm_response_serialization(self) -> None:
        req = LLMRequest(prompt_text="Hello")
        meta = LLMMetadata(provider="mock", model="mock-model", total_tokens=10)
        resp = LLMResponse(raw_text="World", request=req, metadata=meta)

        dict_repr = resp.to_dict()
        assert dict_repr["raw_text"] == "World"
        assert dict_repr["metadata"]["provider"] == "mock"
        assert dict_repr["request"]["prompt_text"] == "Hello"


class TestMockLLMAdapter:
    """Test MockLLMAdapter behavior, health check, and capabilities."""

    def test_generate_response(self) -> None:
        adapter = MockLLMAdapter(model_name="test-mock-v1")
        assert adapter.health_check() is True
        assert adapter.supports_streaming() is False

        req = LLMRequest(prompt_text="Test prompt text for mock generation")
        resp = adapter.generate(req)

        assert isinstance(resp, LLMResponse)
        assert "[Mock LLM Response]" in resp.raw_text
        assert resp.metadata.provider == "mock"
        assert resp.metadata.model == "test-mock-v1"
        assert resp.metadata.total_tokens > 0
        assert resp.metadata.finish_reason == "stop"

    def test_generate_type_error(self) -> None:
        adapter = MockLLMAdapter()
        with pytest.raises(TypeError):
            adapter.generate("invalid_request")  # type: ignore


class TestLLMAdapterFactory:
    """Test LLMAdapterFactory registration and instantiation."""

    def test_get_mock_adapter(self) -> None:
        adapter = LLMAdapterFactory.get_adapter("mock", model_name="mock-model")
        assert isinstance(adapter, MockLLMAdapter)
        assert adapter.model_name == "mock-model"

    def test_unsupported_provider(self) -> None:
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            LLMAdapterFactory.get_adapter("unsupported_vendor")

    def test_custom_adapter_registration(self) -> None:
        LLMAdapterFactory.register_adapter("custom_test", CustomTestAdapter)
        assert "custom_test" in LLMAdapterFactory.list_supported_providers()

        custom_adapter = LLMAdapterFactory.get_adapter("custom_test", model_name="custom-model")
        assert isinstance(custom_adapter, CustomTestAdapter)
        assert custom_adapter.supports_streaming() is True

        req = LLMRequest(prompt_text="Test")
        resp = custom_adapter.generate(req)
        assert resp.raw_text == "Custom Output"

    def test_register_invalid_class(self) -> None:
        with pytest.raises(TypeError):
            LLMAdapterFactory.register_adapter("invalid", str)  # type: ignore


class TestLLMConfig:
    """Test configuration model and environment variable overrides."""

    def test_default_config(self) -> None:
        config = LLMConfig()
        assert config.default_provider == "mock"
        assert config.default_model == "mock-math-v1"
        assert config.temperature == 0.0
        assert config.max_tokens == 2048

    def test_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("LLM_DEFAULT_PROVIDER", "custom_env")
        monkeypatch.setenv("LLM_DEFAULT_MODEL", "custom-model-v2")
        monkeypatch.setenv("LLM_TEMPERATURE", "0.7")
        monkeypatch.setenv("LLM_MAX_TOKENS", "4096")

        config = LLMConfig.from_env()
        assert config.default_provider == "custom_env"
        assert config.default_model == "custom-model-v2"
        assert config.temperature == 0.7
        assert config.max_tokens == 4096
