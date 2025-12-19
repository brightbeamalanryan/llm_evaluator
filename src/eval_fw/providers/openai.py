"""OpenAI provider adapter."""

import os

from openai import AsyncOpenAI, OpenAI

from eval_fw.providers.base import LLMProvider, LLMResponse, ProviderConfig


class OpenAIProvider(LLMProvider):
    """Provider for OpenAI models (GPT-4, GPT-3.5, etc.)."""

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        api_key = config.api_key or os.environ.get("OPENAI_API_KEY")
        self._client = OpenAI(api_key=api_key, base_url=config.base_url)
        self._async_client = AsyncOpenAI(api_key=api_key, base_url=config.base_url)

    @property
    def name(self) -> str:
        return "openai"

    def _parse_response(self, response) -> LLMResponse:
        choice = response.choices[0]
        content = (choice.message.content or "").strip()
        usage = None
        if response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
            }
        return LLMResponse(
            content=content,
            model=response.model,
            usage=usage,
            raw=response.model_dump(),
        )

    def chat(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Send a synchronous chat request to OpenAI."""
        response = self._client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            timeout=self.config.timeout,
        )
        return self._parse_response(response)

    async def achat(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Send an async chat request to OpenAI."""
        response = await self._async_client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            timeout=self.config.timeout,
        )
        return self._parse_response(response)
