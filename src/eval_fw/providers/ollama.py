"""Ollama provider adapter - for local LLM models."""

import httpx

from eval_fw.providers.base import LLMProvider, LLMResponse, ProviderConfig

DEFAULT_OLLAMA_URL = "http://localhost:11434/api/chat"


class OllamaProvider(LLMProvider):
    """Provider for local Ollama models."""

    @property
    def name(self) -> str:
        return "ollama"

    def _get_base_url(self) -> str:
        return self.config.base_url or DEFAULT_OLLAMA_URL

    def _build_payload(self, system_prompt: str, user_prompt: str) -> dict:
        return {
            "model": self.config.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "options": {
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
            },
        }

    def _parse_response(self, data: dict) -> LLMResponse:
        msg = data.get("message", {})
        content = (msg.get("content") or "").strip()
        return LLMResponse(
            content=content,
            model=data.get("model", self.config.model),
            usage={
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0),
            },
            raw=data,
        )

    def chat(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Send a synchronous chat request to Ollama."""
        payload = self._build_payload(system_prompt, user_prompt)
        with httpx.Client(timeout=self.config.timeout) as client:
            response = client.post(self._get_base_url(), json=payload)
            response.raise_for_status()
            return self._parse_response(response.json())

    async def achat(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Send an async chat request to Ollama."""
        payload = self._build_payload(system_prompt, user_prompt)
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(self._get_base_url(), json=payload)
            response.raise_for_status()
            return self._parse_response(response.json())
