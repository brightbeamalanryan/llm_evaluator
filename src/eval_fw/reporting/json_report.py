"""JSON report generator."""

import json
from pathlib import Path

from eval_fw.reporting.base import Reporter, TestReport


class JSONReporter(Reporter):
    """Generate JSON format reports."""

    def __init__(self, indent: int = 2) -> None:
        """
        Initialize the JSON reporter.

        Args:
            indent: JSON indentation level.
        """
        self.indent = indent

    def generate(self, report: TestReport, output_path: Path) -> Path:
        """
        Generate a JSON report file.

        Args:
            report: The test report data.
            output_path: Path to write the report to.

        Returns:
            Path to the generated report file.
        """
        output_path = output_path.with_suffix(".json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=self.indent, ensure_ascii=False)

        return output_path
