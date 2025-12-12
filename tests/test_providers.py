"""Unit tests for LLM provider adapters."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from eval_fw.providers.base import LLMResponse, ProviderConfig
from eval_fw.providers.ollama import OllamaProvider
from eval_fw.providers.openai import OpenAIProvider
from eval_fw.providers.anthropic import AnthropicProvider


@pytest.fixture
def provider_config():
    """Create a basic provider config for testing."""
    return ProviderConfig(
        model="test-model",
        api_key="test-key",
        temperature=0.5,
        top_p=0.9,
    )


class TestOllamaProvider:
    """Tests for OllamaProvider."""

    def test_name(self, provider_config):
        """Test provider name property."""
        provider = OllamaProvider(provider_config)
        assert provider.name == "ollama"

    def test_build_payload(self, provider_config):
        """Test payload construction."""
        provider = OllamaProvider(provider_config)
        payload = provider._build_payload("system", "user")

        assert payload["model"] == "test-model"
        assert payload["stream"] is False
        assert len(payload["messages"]) == 2
        assert payload["messages"][0]["role"] == "system"
        assert payload["messages"][1]["role"] == "user"
        assert payload["options"]["temperature"] == 0.5

    def test_parse_response(self, provider_config):
        """Test response parsing."""
        provider = OllamaProvider(provider_config)
        data = {
            "message": {"content": "  test response  "},
            "model": "test-model",
            "prompt_eval_count": 10,
            "eval_count": 20,
        }

        response = provider._parse_response(data)

        assert response.content == "test response"
        assert response.model == "test-model"
        assert response.usage["prompt_tokens"] == 10
        assert response.usage["completion_tokens"] == 20

    @patch("httpx.Client")
    def test_chat(self, mock_client_class, provider_config):
        """Test synchronous chat method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "message": {"content": "Hello!"},
            "model": "test-model",
        }

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        provider = OllamaProvider(provider_config)
        response = provider.chat("system prompt", "user prompt")

        assert response.content == "Hello!"
        mock_client.post.assert_called_once()


class TestOpenAIProvider:
    """Tests for OpenAIProvider."""

    @patch("eval_fw.providers.openai.OpenAI")
    @patch("eval_fw.providers.openai.AsyncOpenAI")
    def test_name(self, mock_async, mock_sync, provider_config):
        """Test provider name property."""
        provider = OpenAIProvider(provider_config)
        assert provider.name == "openai"

    @patch("eval_fw.providers.openai.OpenAI")
    @patch("eval_fw.providers.openai.AsyncOpenAI")
    def test_chat(self, mock_async, mock_sync, provider_config):
        """Test synchronous chat method."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello from OpenAI!"
        mock_response.model = "gpt-4"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 20
        mock_response.model_dump.return_value = {}

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_sync.return_value = mock_client

        provider = OpenAIProvider(provider_config)
        response = provider.chat("system", "user")

        assert response.content == "Hello from OpenAI!"
        assert response.model == "gpt-4"


class TestAnthropicProvider:
    """Tests for AnthropicProvider."""

    @patch("eval_fw.providers.anthropic.Anthropic")
    @patch("eval_fw.providers.anthropic.AsyncAnthropic")
    def test_name(self, mock_async, mock_sync, provider_config):
        """Test provider name property."""
        provider = AnthropicProvider(provider_config)
        assert provider.name == "anthropic"

    @patch("eval_fw.providers.anthropic.Anthropic")
    @patch("eval_fw.providers.anthropic.AsyncAnthropic")
    def test_chat(self, mock_async, mock_sync, provider_config):
        """Test synchronous chat method."""
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = "Hello from Claude!"

        mock_response = MagicMock()
        mock_response.content = [mock_block]
        mock_response.model = "claude-3"
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 20
        mock_response.model_dump.return_value = {}

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_sync.return_value = mock_client

        provider = AnthropicProvider(provider_config)
        response = provider.chat("system", "user")

        assert response.content == "Hello from Claude!"
        assert response.model == "claude-3"
