"""Abstract base class for LLM providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProviderConfig:
    """Configuration for an LLM provider."""

    model: str
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.3
    top_p: float = 0.9
    timeout: int = 600
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    """Response from an LLM provider."""

    content: str
    model: str
    usage: dict[str, int] | None = None
    raw: dict[str, Any] | None = None


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""
        ...

    @abstractmethod
    def chat(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """
        Send a chat request with system and user prompts.

        Args:
            system_prompt: The system prompt to set context.
            user_prompt: The user's message.

        Returns:
            LLMResponse with the model's reply.
        """
        ...

    @abstractmethod
    async def achat(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """
        Async version of chat.

        Args:
            system_prompt: The system prompt to set context.
            user_prompt: The user's message.

        Returns:
            LLMResponse with the model's reply.
        """
        ...
