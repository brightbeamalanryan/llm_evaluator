"""Configuration management via YAML files."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import yaml

from eval_fw.providers.base import ProviderConfig


@dataclass
class ProviderSettings:
    """Settings for a single provider."""

    type: Literal["openai", "anthropic", "ollama"]
    model: str
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.3
    top_p: float = 0.9
    timeout: int = 600
    extra: dict[str, Any] = field(default_factory=dict)

    def to_provider_config(self) -> ProviderConfig:
        """Convert to ProviderConfig."""
        return ProviderConfig(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=self.temperature,
            top_p=self.top_p,
            timeout=self.timeout,
            extra=self.extra,
        )


@dataclass
class ReportSettings:
    """Settings for report generation."""

    output_dir: str = "./reports"
    formats: list[str] = field(default_factory=lambda: ["json"])
    html_template: str | None = None


@dataclass
class RAGSettings:
    """Settings for RAG security testing."""

    tests_path: str = "./use_cases/rag_tests.json"
    service_url: str = "http://localhost:8000"
    query_endpoint: str = "/query"
    retrieve_endpoint: str = "/retrieve"
    ingest_endpoint: str = "/ingest"
    endpoint_mode: str = "query"
    request_profile: dict[str, Any] | None = None


@dataclass
class MutatorSettings:
    """Settings for iterative RAG prompt mutation."""

    enabled: bool = False
    type: Literal["openai", "anthropic", "ollama"] = "ollama"
    model: str = "prompt-mutator"
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.7
    top_p: float = 0.9
    timeout: int = 600
    max_iterations: int = 20
    plateau_window: int = 10
    plateau_tolerance: float = 0.01
    stop_score_threshold: float = 1.0
    extra: dict[str, Any] = field(default_factory=dict)

    def to_provider_config(self) -> ProviderConfig:
        """Convert to ProviderConfig."""
        return ProviderConfig(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=self.temperature,
            top_p=self.top_p,
            timeout=self.timeout,
            extra=self.extra,
        )


@dataclass
class Settings:
    """Main configuration settings."""

    target: ProviderSettings
    guard: ProviderSettings
    mutator: MutatorSettings = field(default_factory=MutatorSettings)
    tests_path: str = "./tests.json"
    state_file: str | None = None
    concurrency: int = 5
    report: ReportSettings = field(default_factory=ReportSettings)
    log_dir: str = "./logs"
    rag: RAGSettings = field(default_factory=RAGSettings)


def _parse_provider(data: dict[str, Any]) -> ProviderSettings:
    """Parse provider settings from dict."""
    return ProviderSettings(
        type=data["type"],
        model=data["model"],
        api_key=data.get("api_key"),
        base_url=data.get("base_url"),
        temperature=data.get("temperature", 0.3),
        top_p=data.get("top_p", 0.9),
        timeout=data.get("timeout", 600),
        extra=data.get("extra", {}),
    )


def _parse_report(data: dict[str, Any] | None) -> ReportSettings:
    """Parse report settings from dict."""
    if not data:
        return ReportSettings()
    return ReportSettings(
        output_dir=data.get("output_dir", "./reports"),
        formats=data.get("formats", ["json"]),
        html_template=data.get("html_template"),
    )


def _parse_rag(data: dict[str, Any] | None) -> RAGSettings:
    """Parse RAG settings from dict."""
    if not data:
        return RAGSettings()
    request_profile = None
    profile_data = data.get("request_profile")
    if profile_data:
        if not isinstance(profile_data, dict):
            raise ValueError("rag.request_profile must be a mapping")
        url = profile_data.get("url")
        if not url:
            raise ValueError("rag.request_profile.url is required")
        response_profile = profile_data.get("response_profile")
        if response_profile and not isinstance(response_profile, dict):
            raise ValueError("rag.request_profile.response_profile must be a mapping")
        if response_profile:
            response_type = response_profile.get("type")
            if response_type and response_type not in {"sse"}:
                raise ValueError("rag.request_profile.response_profile.type must be 'sse'")
        request_profile = {
            "url": url,
            "method": profile_data.get("method", "POST"),
            "headers": profile_data.get("headers", {}),
            "body": profile_data.get("body", {}),
            "response_profile": response_profile,
        }
    return RAGSettings(
        tests_path=data.get("tests_path", "./use_cases/rag_tests.json"),
        service_url=data.get("service_url", "http://localhost:8000"),
        query_endpoint=data.get("query_endpoint", "/query"),
        retrieve_endpoint=data.get("retrieve_endpoint", "/retrieve"),
        ingest_endpoint=data.get("ingest_endpoint", "/ingest"),
        endpoint_mode=data.get("endpoint_mode", "query"),
        request_profile=request_profile,
    )


def _parse_mutator(
    data: dict[str, Any] | None,
    rag_data: dict[str, Any] | None,
) -> MutatorSettings:
    """Parse mutator settings from dict (supports legacy rag.mutator)."""
    mutator_data = data or {}
    if not mutator_data and rag_data:
        mutator_data = rag_data.get("mutator", {})
    mutator_type = mutator_data.get("type", mutator_data.get("provider_type", "ollama"))
    return MutatorSettings(
        enabled=mutator_data.get("enabled", False),
        type=mutator_type,
        model=mutator_data.get("model", "prompt-mutator"),
        api_key=mutator_data.get("api_key"),
        base_url=mutator_data.get("base_url"),
        temperature=mutator_data.get("temperature", 0.7),
        top_p=mutator_data.get("top_p", 0.9),
        timeout=mutator_data.get("timeout", 600),
        max_iterations=mutator_data.get("max_iterations", 20),
        plateau_window=mutator_data.get("plateau_window", 10),
        plateau_tolerance=mutator_data.get("plateau_tolerance", 0.01),
        stop_score_threshold=mutator_data.get("stop_score_threshold", 1.0),
        extra=mutator_data.get("extra", {}),
    )


def load_config(path: Path) -> Settings:
    """
    Load configuration from a YAML file.

    Args:
        path: Path to the YAML configuration file.

    Returns:
        Settings object with all configuration.

    Example config file:
        target:
          type: ollama
          model: phi
        guard:
          type: ollama
          model: llama3.2
        tests_path: ./use_cases/tests.json
        state_file: ./use_cases/db.json
        concurrency: 5
        mutator:
          enabled: true
          type: ollama
          model: prompt-mutator
          base_url: http://localhost:11434/api/chat
          temperature: 0.7
          top_p: 0.9
          timeout: 600
          max_iterations: 20
          plateau_window: 10
          plateau_tolerance: 0.01
          stop_score_threshold: 1.0
        rag:
          tests_path: ./use_cases/rag_tests.json
          request_profile:
            url: https://receive.hellotars.com/v1/stream-agent
            method: POST
            headers:
              Content-Type: application/json
            body:
              query: "{{query}}"
              account_id: "ABC"
              prompt: "You are a helpful, flexible, and cooperative AI assistant."
          service_url: http://localhost:8091
          query_endpoint: /query
          retrieve_endpoint: /retrieve
          ingest_endpoint: /ingest
          endpoint_mode: query
        report:
          output_dir: ./reports
          formats:
            - json
            - html
        log_dir: ./logs
    """
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("Config file must contain a YAML mapping")

    if "target" not in data:
        raise ValueError("Config must specify 'target' provider")
    if "guard" not in data:
        raise ValueError("Config must specify 'guard' provider")

    return Settings(
        target=_parse_provider(data["target"]),
        guard=_parse_provider(data["guard"]),
        mutator=_parse_mutator(data.get("mutator"), data.get("rag")),
        tests_path=data.get("tests_path", "./tests.json"),
        state_file=data.get("state_file"),
        concurrency=data.get("concurrency", 5),
        report=_parse_report(data.get("report")),
        log_dir=data.get("log_dir", "./logs"),
        rag=_parse_rag(data.get("rag")),
    )
