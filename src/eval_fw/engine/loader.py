"""Test case loading and validation - refactored from baseline_injection.py."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class TestCase:
    """A single security test case."""

    id: str
    description: str
    system_prompt: str
    user_prompt: str
    expectation: str  # what "good" behaviour looks like


class TestLoader:
    """Load test cases from JSON or YAML files."""

    def __init__(self, state_file: Path | None = None) -> None:
        """
        Initialize the loader.

        Args:
            state_file: Optional path to track which tests have been run.
        """
        self._state_file = state_file
        self._ran_ids: set[str] = set()
        if state_file and state_file.exists():
            self._load_state()

    def _load_state(self) -> None:
        """Load previously run test IDs from state file."""
        if not self._state_file:
            return
        with self._state_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            self._ran_ids = set(data.get("ran", []))

    def _save_state(self, new_ids: list[str]) -> None:
        """Save run test IDs to state file."""
        if not self._state_file:
            return
        self._ran_ids.update(new_ids)
        with self._state_file.open("w", encoding="utf-8") as f:
            json.dump({"ran": list(self._ran_ids)}, f, indent=2)

    def _parse_test_case(self, test_id: str, payload: dict[str, Any]) -> TestCase:
        """Parse a single test case from dict."""
        required = ["description", "system_prompt", "user_prompt", "expectation"]
        for field in required:
            if field not in payload:
                raise ValueError(f"Test {test_id} is missing required field: {field}")
        return TestCase(
            id=test_id,
            description=payload["description"],
            system_prompt=payload["system_prompt"],
            user_prompt=payload["user_prompt"],
            expectation=payload["expectation"],
        )

    def load_json(self, path: Path, skip_ran: bool = False) -> list[TestCase]:
        """
        Load test cases from a JSON file.

        Args:
            path: Path to JSON file with test definitions.
            skip_ran: If True, skip tests that have already been run.

        Returns:
            List of TestCase objects.
        """
        if not path.exists():
            raise FileNotFoundError(f"Test file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("JSON test file must contain an object keyed by test id")

        cases = []
        for test_id, payload in data.items():
            if skip_ran and test_id in self._ran_ids:
                continue
            cases.append(self._parse_test_case(test_id, payload))

        if skip_ran and cases:
            self._save_state([c.id for c in cases])

        return cases

    def load_yaml(self, path: Path, skip_ran: bool = False) -> list[TestCase]:
        """
        Load test cases from a YAML file.

        Args:
            path: Path to YAML file with test definitions.
            skip_ran: If True, skip tests that have already been run.

        Returns:
            List of TestCase objects.
        """
        if not path.exists():
            raise FileNotFoundError(f"Test file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise ValueError("YAML test file must contain a mapping keyed by test id")

        cases = []
        for test_id, payload in data.items():
            if skip_ran and test_id in self._ran_ids:
                continue
            cases.append(self._parse_test_case(test_id, payload))

        if skip_ran and cases:
            self._save_state([c.id for c in cases])

        return cases

    def load(self, path: Path, skip_ran: bool = False) -> list[TestCase]:
        """
        Load test cases from a file (auto-detect format).

        Args:
            path: Path to test file (JSON or YAML).
            skip_ran: If True, skip tests that have already been run.

        Returns:
            List of TestCase objects.
        """
        suffix = path.suffix.lower()
        if suffix == ".json":
            return self.load_json(path, skip_ran)
        elif suffix in (".yaml", ".yml"):
            return self.load_yaml(path, skip_ran)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
