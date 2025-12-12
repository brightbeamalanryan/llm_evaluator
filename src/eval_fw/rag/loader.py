"""RAG test case loader."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class InjectedDocument:
    """A document to inject into the RAG pipeline for testing."""

    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RAGTestCase:
    """A RAG security test case."""

    id: str
    description: str
    attack_type: str
    query: str
    expectation: str
    injected_doc: InjectedDocument | None = None
    expected_fail: bool = True
    severity: str = "medium"
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, id: str, data: dict[str, Any]) -> "RAGTestCase":
        """Create a RAGTestCase from a dictionary."""
        injected_doc = None
        if "injected_doc" in data:
            doc_data = data["injected_doc"]
            injected_doc = InjectedDocument(
                content=doc_data.get("content", ""),
                metadata=doc_data.get("metadata", {}),
            )

        return cls(
            id=id,
            description=data.get("description", ""),
            attack_type=data.get("attack_type", "unknown"),
            query=data.get("query", ""),
            expectation=data.get("expectation", ""),
            injected_doc=injected_doc,
            expected_fail=data.get("expected_fail", True),
            severity=data.get("severity", "medium"),
            tags=data.get("tags", []),
        )


class RAGTestLoader:
    """Loader for RAG security test cases from JSON files."""

    def __init__(self, path: Path | None = None) -> None:
        """Initialize the loader.

        Args:
            path: Path to the JSON file containing test cases.
                  Defaults to use_cases/rag_tests.json.
        """
        if path is None:
            path = Path(__file__).parent.parent.parent.parent / "use_cases" / "rag_tests.json"
        self.path = path
        self._tests: list[RAGTestCase] = []

    def load(self) -> list[RAGTestCase]:
        """Load test cases from the JSON file."""
        if not self.path.exists():
            return []

        with self.path.open() as f:
            data = json.load(f)

        self._tests = [RAGTestCase.from_dict(id, tc_data) for id, tc_data in data.items()]
        return self._tests

    @property
    def tests(self) -> list[RAGTestCase]:
        """Get loaded test cases."""
        return self._tests

    def filter_by_attack_type(self, attack_type: str) -> list[RAGTestCase]:
        """Filter test cases by attack type."""
        return [t for t in self._tests if t.attack_type == attack_type]

    def filter_by_severity(self, severity: str) -> list[RAGTestCase]:
        """Filter test cases by severity level."""
        return [t for t in self._tests if t.severity == severity]

    def filter_by_tag(self, tag: str) -> list[RAGTestCase]:
        """Filter test cases by tag."""
        return [t for t in self._tests if tag in t.tags]
