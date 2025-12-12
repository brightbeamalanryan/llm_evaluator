"""Anthropic provider adapter."""

import os

from anthropic import Anthropic, AsyncAnthropic

from eval_fw.providers.base import LLMProvider, LLMResponse, ProviderConfig


class AnthropicProvider(LLMProvider):
    """Provider for Anthropic models (Claude)."""

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        api_key = config.api_key or os.environ.get("ANTHROPIC_API_KEY")
        self._client = Anthropic(api_key=api_key, base_url=config.base_url)
        self._async_client = AsyncAnthropic(api_key=api_key, base_url=config.base_url)

    @property
    def name(self) -> str:
        return "anthropic"

    def _parse_response(self, response) -> LLMResponse:
        content = ""
        for block in response.content:
            if block.type == "text":
                content += block.text
        content = content.strip()
        usage = None
        if response.usage:
            usage = {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
            }
        return LLMResponse(
            content=content,
            model=response.model,
            usage=usage,
            raw=response.model_dump(),
        )

    def chat(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Send a synchronous chat request to Anthropic."""
        response = self._client.messages.create(
            model=self.config.model,
            max_tokens=self.config.extra.get("max_tokens", 4096),
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=self.config.temperature,
            top_p=self.config.top_p,
        )
        return self._parse_response(response)

    async def achat(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Send an async chat request to Anthropic."""
        response = await self._async_client.messages.create(
            model=self.config.model,
            max_tokens=self.config.extra.get("max_tokens", 4096),
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=self.config.temperature,
            top_p=self.config.top_p,
        )
        return self._parse_response(response)
