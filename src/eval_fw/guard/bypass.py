"""Guard bypass test suite - loader for bypass test cases from JSON/YAML."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

import json
import yaml

from eval_fw.engine.loader import TestCase


class BypassTechnique(str, Enum):
    """Categories of guard bypass techniques."""

    ENCODING = "encoding"  # Base64, ROT13, etc.
    ROLEPLAY = "roleplay"  # "Pretend you are..."
    JAILBREAK = "jailbreak"  # DAN, Developer Mode, etc.
    SPLITTING = "splitting"  # Split harmful content across messages
    OBFUSCATION = "obfuscation"  # Typos, leetspeak, etc.
    CONTEXT_MANIPULATION = "context_manipulation"  # Manipulate context window
    PROMPT_INJECTION = "prompt_injection"  # Inject into guard's prompt


@dataclass
class BypassTestCase(TestCase):
    """Extended test case for bypass testing."""

    technique: BypassTechnique
    expected_bypass: bool  # True if we expect this to bypass the guard
    difficulty: str = "medium"  # easy, medium, hard


class GuardBypassSuite:
    """
    Load and manage guard bypass test cases from JSON/YAML files.

    Test cases should follow this schema:
    {
        "test-id": {
            "description": "...",
            "system_prompt": "...",
            "user_prompt": "...",
            "expectation": "...",
            "technique": "encoding|roleplay|obfuscation|...",
            "expected_bypass": false,
            "difficulty": "easy|medium|hard"
        }
    }
    """

    def __init__(self, tests_path: Path | None = None) -> None:
        """
        Initialize the bypass suite.

        Args:
            tests_path: Path to bypass tests JSON/YAML file.
        """
        self.tests_path = tests_path
        self._tests: list[BypassTestCase] = []

    def _parse_test_case(self, test_id: str, data: dict[str, Any]) -> BypassTestCase:
        """Parse a single bypass test case from dict."""
        technique_str = data.get("technique", "prompt_injection")
        try:
            technique = BypassTechnique(technique_str)
        except ValueError:
            technique = BypassTechnique.PROMPT_INJECTION

        return BypassTestCase(
            id=test_id,
            description=data["description"],
            system_prompt=data["system_prompt"],
            user_prompt=data["user_prompt"],
            expectation=data["expectation"],
            technique=technique,
            expected_bypass=data.get("expected_bypass", False),
            difficulty=data.get("difficulty", "medium"),
        )

    def load(self, path: Path | None = None) -> list[BypassTestCase]:
        """
        Load bypass test cases from a JSON or YAML file.

        Args:
            path: Path to test file. Uses self.tests_path if not provided.

        Returns:
            List of BypassTestCase objects.
        """
        path = path or self.tests_path
        if not path or not path.exists():
            return []

        with path.open("r", encoding="utf-8") as f:
            if path.suffix == ".json":
                data = json.load(f)
            else:
                data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise ValueError("Bypass test file must contain a mapping keyed by test id")

        self._tests = [
            self._parse_test_case(test_id, payload)
            for test_id, payload in data.items()
        ]
        return self._tests

    def filter_by_technique(
        self, technique: BypassTechnique
    ) -> list[BypassTestCase]:
        """Filter loaded tests by technique."""
        return [t for t in self._tests if t.technique == technique]

    def filter_by_difficulty(self, difficulty: str) -> list[BypassTestCase]:
        """Filter loaded tests by difficulty."""
        return [t for t in self._tests if t.difficulty == difficulty]

    @property
    def tests(self) -> list[BypassTestCase]:
        """Get all loaded tests."""
        return self._tests
