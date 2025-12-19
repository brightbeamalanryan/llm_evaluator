"""Base reporter and data structures."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from eval_fw.engine.runner import RunResult, TestResult
from eval_fw.engine.scorer import Verdict


@dataclass
class TestReport:
    """Complete test report data."""

    run_result: RunResult
    target_model: str
    guard_model: str
    generated_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert report to dictionary for serialization."""
        return {
            "summary": {
                "total": self.run_result.total,
                "passed": self.run_result.passed,
                "failed": self.run_result.failed,
                "errors": self.run_result.errors,
                "pass_rate": round(self.run_result.pass_rate * 100, 2),
            },
            "target_model": self.target_model,
            "guard_model": self.guard_model,
            "generated_at": self.generated_at.isoformat(),
            "started_at": self.run_result.started_at.isoformat(),
            "completed_at": self.run_result.completed_at.isoformat(),
            "duration_seconds": (
                self.run_result.completed_at - self.run_result.started_at
            ).total_seconds(),
            "results": [self._result_to_dict(r) for r in self.run_result.results],
            "metadata": self.metadata,
        }

    def _result_to_dict(self, result: TestResult) -> dict[str, Any]:
        """Convert a single test result to dictionary."""
        return {
            "test_id": result.test_case.id,
            "description": result.test_case.description,
            "system_prompt": result.test_case.system_prompt,
            "user_prompt": result.test_case.user_prompt,
            "expectation": result.test_case.expectation,
            "target_response": (
                result.target_response.content if result.target_response else None
            ),
            "verdict": (
                result.scorer_result.verdict.value if result.scorer_result else None
            ),
            "guard_raw": (
                result.scorer_result.raw_output if result.scorer_result else None
            ),
            "passed": result.passed,
            "jailbroken": result.jailbroken,
            "error": result.error,
            "duration_seconds": result.duration_seconds,
        }


class Reporter(ABC):
    """Abstract base class for report generators."""

    @abstractmethod
    def generate(self, report: TestReport, output_path: Path) -> Path:
        """
        Generate a report file.

        Args:
            report: The test report data.
            output_path: Path to write the report to.

        Returns:
            Path to the generated report file.
        """
        ...
