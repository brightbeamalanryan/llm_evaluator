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
class Settings:
    """Main configuration settings."""

    target: ProviderSettings
    guard: ProviderSettings
    tests_path: str = "./tests.json"
    state_file: str | None = None
    concurrency: int = 5
    report: ReportSettings = field(default_factory=ReportSettings)
    log_dir: str = "./logs"


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
        tests_path=data.get("tests_path", "./tests.json"),
        state_file=data.get("state_file"),
        concurrency=data.get("concurrency", 5),
        report=_parse_report(data.get("report")),
        log_dir=data.get("log_dir", "./logs"),
    )
