"""PDF report generator using WeasyPrint."""

from pathlib import Path

from eval_fw.reporting.base import Reporter, TestReport
from eval_fw.reporting.html_report import HTMLReporter


class PDFReporter(Reporter):
    """Generate PDF format reports via HTML conversion."""

    def __init__(self, html_template: str | None = None) -> None:
        """
        Initialize the PDF reporter.

        Args:
            html_template: Custom Jinja2 template string for HTML (optional).
        """
        self.html_reporter = HTMLReporter(template=html_template)

    def generate(self, report: TestReport, output_path: Path) -> Path:
        """
        Generate a PDF report file.

        Args:
            report: The test report data.
            output_path: Path to write the report to.

        Returns:
            Path to the generated report file.

        Note:
            Requires WeasyPrint and its dependencies (cairo, pango, etc.)
            to be installed on the system.
        """
        try:
            from weasyprint import HTML
        except ImportError as e:
            raise ImportError(
                "WeasyPrint is required for PDF generation. "
                "Install it with: pip install weasyprint"
            ) from e

        output_path = output_path.with_suffix(".pdf")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate HTML first
        html_path = output_path.with_suffix(".html")
        self.html_reporter.generate(report, html_path)

        # Convert to PDF
        HTML(filename=str(html_path)).write_pdf(str(output_path))

        # Clean up intermediate HTML
        html_path.unlink()

        return output_path
