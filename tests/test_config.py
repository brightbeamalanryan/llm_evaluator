"""Unit tests for configuration management."""

import tempfile
from pathlib import Path

import pytest
import yaml

from eval_fw.config.settings import Settings, load_config, ProviderSettings


@pytest.fixture
def sample_config(tmp_path):
    """Create a sample configuration file."""
    config = {
        "target": {
            "type": "ollama",
            "model": "phi",
            "temperature": 0.3,
        },
        "guard": {
            "type": "ollama",
            "model": "llama3.2",
        },
        "tests_path": "./tests.json",
        "state_file": "./db.json",
        "concurrency": 10,
        "report": {
            "output_dir": "./reports",
            "formats": ["json", "html"],
        },
        "log_dir": "./logs",
    }
    path = tmp_path / "config.yaml"
    with path.open("w") as f:
        yaml.dump(config, f)
    return path


@pytest.fixture
def minimal_config(tmp_path):
    """Create a minimal configuration file."""
    config = {
        "target": {
            "type": "openai",
            "model": "gpt-4",
        },
        "guard": {
            "type": "anthropic",
            "model": "claude-3-haiku-20240307",
        },
    }
    path = tmp_path / "minimal.yaml"
    with path.open("w") as f:
        yaml.dump(config, f)
    return path


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_full_config(self, sample_config):
        """Test loading a full configuration file."""
        settings = load_config(sample_config)

        assert settings.target.type == "ollama"
        assert settings.target.model == "phi"
        assert settings.target.temperature == 0.3

        assert settings.guard.type == "ollama"
        assert settings.guard.model == "llama3.2"

        assert settings.tests_path == "./tests.json"
        assert settings.state_file == "./db.json"
        assert settings.concurrency == 10

        assert settings.report.output_dir == "./reports"
        assert settings.report.formats == ["json", "html"]

    def test_load_minimal_config(self, minimal_config):
        """Test loading a minimal configuration with defaults."""
        settings = load_config(minimal_config)

        assert settings.target.type == "openai"
        assert settings.guard.type == "anthropic"

        # Check defaults
        assert settings.tests_path == "./tests.json"
        assert settings.state_file is None
        assert settings.concurrency == 5
        assert settings.report.formats == ["json"]

    def test_missing_target(self, tmp_path):
        """Test error when target is missing."""
        config = {"guard": {"type": "ollama", "model": "phi"}}
        path = tmp_path / "bad.yaml"
        with path.open("w") as f:
            yaml.dump(config, f)

        with pytest.raises(ValueError, match="target"):
            load_config(path)

    def test_missing_guard(self, tmp_path):
        """Test error when guard is missing."""
        config = {"target": {"type": "ollama", "model": "phi"}}
        path = tmp_path / "bad.yaml"
        with path.open("w") as f:
            yaml.dump(config, f)

        with pytest.raises(ValueError, match="guard"):
            load_config(path)

    def test_file_not_found(self, tmp_path):
        """Test error when config file doesn't exist."""
        path = tmp_path / "nonexistent.yaml"

        with pytest.raises(FileNotFoundError):
            load_config(path)


class TestProviderSettings:
    """Tests for ProviderSettings."""

    def test_to_provider_config(self):
        """Test conversion to ProviderConfig."""
        settings = ProviderSettings(
            type="openai",
            model="gpt-4",
            api_key="test-key",
            temperature=0.7,
            extra={"max_tokens": 1000},
        )

        config = settings.to_provider_config()

        assert config.model == "gpt-4"
        assert config.api_key == "test-key"
        assert config.temperature == 0.7
        assert config.extra["max_tokens"] == 1000

    def test_defaults(self):
        """Test default values."""
        settings = ProviderSettings(
            type="ollama",
            model="phi",
        )

        assert settings.api_key is None
        assert settings.base_url is None
        assert settings.temperature == 0.3
        assert settings.top_p == 0.9
        assert settings.timeout == 600
