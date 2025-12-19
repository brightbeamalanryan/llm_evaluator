"""CLI entry point for the evaluation framework."""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from eval_fw import __version__
from eval_fw.config.settings import Settings, load_config
from eval_fw.engine.loader import TestCase, TestLoader
from eval_fw.engine.runner import RunResult, TestResult, TestRunner
from eval_fw.engine.scorer import GuardScorer, Verdict
from eval_fw.logging import setup_logging
from eval_fw.providers.anthropic import AnthropicProvider
from eval_fw.providers.base import LLMProvider, ProviderConfig
from eval_fw.providers.ollama import OllamaProvider
from eval_fw.providers.openai import OpenAIProvider
from eval_fw.reporting.base import TestReport
from eval_fw.reporting.html_report import HTMLReporter
from eval_fw.reporting.json_report import JSONReporter
from eval_fw.reporting.pdf_report import PDFReporter
from eval_fw.rag import (
    RAGClient,
    RAGTestLoader,
    RAGSeverityScorer,
    RAGSessionRunner,
)
from eval_fw.rag.runner import RAGMutatorConfig

app = typer.Typer(
    name="eval-fw",
    help="AI Security Evaluation Framework",
    add_completion=False,
)
console = Console(record=True)
logger = logging.getLogger(__name__)


def get_provider(provider_type: str, config: ProviderConfig) -> LLMProvider:
    """Create a provider instance from type string."""
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider,
    }
    if provider_type not in providers:
        raise ValueError(f"Unknown provider type: {provider_type}")
    return providers[provider_type](config)


def print_result(tc: TestCase, result: TestResult) -> None:
    """Print a single test result (progress callback)."""
    if result.error:
        status = "[bold yellow]ERROR[/bold yellow]"
    elif result.jailbroken:
        status = "[bold red]JAILBROKEN[/bold red]"
    else:
        status = "[bold green]SAFE[/bold green]"

    console.print(f"  {tc.id}: {status}")


def print_summary(run_result: RunResult) -> None:
    """Print run summary table."""
    table = Table(title="Test Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Total Tests", str(run_result.total))
    table.add_row("Passed (Safe)", f"[green]{run_result.passed}[/green]")
    table.add_row("Failed (Jailbroken)", f"[red]{run_result.failed}[/red]")
    table.add_row("Errors", f"[yellow]{run_result.errors}[/yellow]")
    table.add_row("Pass Rate", f"{run_result.pass_rate * 100:.1f}%")

    duration = (run_result.completed_at - run_result.started_at).total_seconds()
    table.add_row("Duration", f"{duration:.1f}s")

    console.print(table)


@app.command()
def run(
    config_file: Annotated[
        Path,
        typer.Option("--config", "-c", help="Path to YAML configuration file"),
    ],
    tests_file: Annotated[
        Optional[Path],
        typer.Option("--tests", "-t", help="Path to test cases file (overrides config)"),
    ] = None,
    output_dir: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Output directory for reports"),
    ] = None,
    formats: Annotated[
        Optional[str],
        typer.Option("--format", "-f", help="Report formats (comma-separated: json,html,pdf)"),
    ] = None,
    async_mode: Annotated[
        bool,
        typer.Option("--async", help="Run tests concurrently"),
    ] = False,
    skip_ran: Annotated[
        bool,
        typer.Option("--skip-ran", help="Skip previously run tests"),
    ] = False,
) -> None:
    """Run security evaluation tests."""
    console.print(Panel("[bold cyan]AI Security Evaluation Framework[/bold cyan]"))

    # Load configuration
    try:
        settings = load_config(config_file)
    except Exception as e:
        console.print(f"[bold red]Error loading config:[/bold red] {e}")
        raise typer.Exit(1)

    log_path = setup_logging(Path(settings.log_dir))
    logger.info("Initialized logging at %s", log_path)

    # Override settings from CLI
    tests_path = Path(tests_file or settings.tests_path)
    report_dir = Path(output_dir or settings.report.output_dir)
    report_formats = (formats.split(",") if formats else settings.report.formats)

    # Load test cases
    console.print(f"\n[dim]Loading tests from:[/dim] {tests_path}")
    logger.info("Loading %s tests from %s", "async" if async_mode else "sync", tests_path)
    state_file = Path(settings.state_file) if settings.state_file else None
    loader = TestLoader(state_file=state_file)

    try:
        test_cases = loader.load(tests_path, skip_ran=skip_ran)
    except Exception as e:
        console.print(f"[bold red]Error loading tests:[/bold red] {e}")
        raise typer.Exit(1)

    if not test_cases:
        console.print("[yellow]No test cases to run.[/yellow]")
        raise typer.Exit(0)

    # Show test cases
    table = Table(title=f"Loaded {len(test_cases)} Test Cases")
    table.add_column("ID", style="cyan")
    table.add_column("Description", style="white", max_width=60)
    for tc in test_cases:
        table.add_row(tc.id, tc.description[:60] + "..." if len(tc.description) > 60 else tc.description)
    console.print(table)

    # Create providers
    console.print(f"\n[dim]Target model:[/dim] {settings.target.type}/{settings.target.model}")
    console.print(f"[dim]Guard model:[/dim] {settings.guard.type}/{settings.guard.model}")

    target_provider = get_provider(
        settings.target.type,
        settings.target.to_provider_config(),
    )
    guard_provider = get_provider(
        settings.guard.type,
        settings.guard.to_provider_config(),
    )

    # Create scorer and runner
    scorer = GuardScorer(guard_provider)
    runner = TestRunner(target_provider, scorer, on_progress=print_result)

    # Run tests
    console.print("\n[bold]Running tests...[/bold]\n")
    logger.info("Starting run with %d test cases", len(test_cases))

    if async_mode:
        run_result = asyncio.run(
            runner.run_async(test_cases, concurrency=settings.concurrency)
        )
    else:
        run_result = runner.run(test_cases)

    # Print summary
    console.print()
    print_summary(run_result)
    logger.info(
        "Run complete total=%d passed=%d failed=%d errors=%d pass_rate=%.3f",
        run_result.total,
        run_result.passed,
        run_result.failed,
        run_result.errors,
        run_result.pass_rate,
    )

    # Generate reports
    report = TestReport(
        run_result=run_result,
        target_model=f"{settings.target.type}/{settings.target.model}",
        guard_model=f"{settings.guard.type}/{settings.guard.model}",
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"report_{timestamp}"

    console.print(f"\n[dim]Generating reports in:[/dim] {report_dir}")

    reporters = {
        "json": JSONReporter(),
        "html": HTMLReporter(),
        "pdf": PDFReporter(),
    }

    for fmt in report_formats:
        fmt = fmt.strip().lower()
        if fmt in reporters:
            try:
                output_path = reporters[fmt].generate(report, report_dir / base_name)
                console.print(f"  [green]✓[/green] {output_path}")
                logger.info("Generated report format=%s path=%s", fmt, output_path)
            except Exception as e:
                console.print(f"  [red]✗[/red] {fmt}: {e}")
                logger.exception("Failed to generate report format=%s", fmt)


@app.command()
def list_tests(
    tests_file: Annotated[
        Path,
        typer.Argument(help="Path to test cases file"),
    ],
) -> None:
    """List test cases from a file."""
    loader = TestLoader()
    try:
        test_cases = loader.load(tests_file)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

    table = Table(title=f"Test Cases ({len(test_cases)})")
    table.add_column("ID", style="cyan")
    table.add_column("Description", style="white", max_width=80)
    for tc in test_cases:
        table.add_row(tc.id, tc.description)
    console.print(table)


@app.command("rag-run")
def rag_run(
    tests_file: Annotated[
        Optional[Path],
        typer.Option("--tests", "-t", help="Path to RAG test cases file"),
    ] = None,
    config_file: Annotated[
        Optional[Path],
        typer.Option("--config", "-c", help="Path to YAML configuration file"),
    ] = None,
    service_url: Annotated[
        Optional[str],
        typer.Option("--service-url", help="RAG service base URL"),
    ] = None,
    query_endpoint: Annotated[
        Optional[str],
        typer.Option("--query-endpoint", help="RAG query endpoint path"),
    ] = None,
    retrieve_endpoint: Annotated[
        Optional[str],
        typer.Option("--retrieve-endpoint", help="RAG retrieve endpoint path"),
    ] = None,
    ingest_endpoint: Annotated[
        Optional[str],
        typer.Option("--ingest-endpoint", help="RAG ingest endpoint path"),
    ] = None,
    endpoint_mode: Annotated[
        Optional[str],
        typer.Option(
            "--endpoint-mode",
            help="Which endpoint to exercise: query, retrieve, or ingest",
        ),
    ] = None,
) -> None:
    """Run RAG security test cases against a RAG service."""
    settings = None
    if config_file:
        try:
            settings = load_config(config_file)
        except Exception as e:
            console.print(f"[bold red]Error loading config:[/bold red] {e}")
            raise typer.Exit(1)

    log_dir = Path(settings.log_dir) if settings else Path("./logs")
    log_path = setup_logging(log_dir)
    logger.info("Initialized logging at %s", log_path)

    default_tests_path = (
        Path(__file__).parent.parent.parent.parent / "use_cases" / "rag_tests.json"
    )
    tests_path = tests_file or Path(
        settings.rag.tests_path if settings else default_tests_path
    )
    resolved_service_url = (
        service_url or (settings.rag.service_url if settings else "http://localhost:8091")
    )
    resolved_query_endpoint = (
        query_endpoint or (settings.rag.query_endpoint if settings else "/query")
    )
    resolved_retrieve_endpoint = (
        retrieve_endpoint or (settings.rag.retrieve_endpoint if settings else "/retrieve")
    )
    resolved_ingest_endpoint = (
        ingest_endpoint or (settings.rag.ingest_endpoint if settings else "/ingest")
    )
    resolved_endpoint_mode = (
        endpoint_mode or (settings.rag.endpoint_mode if settings else "query")
    )

    console.print(Panel("[bold cyan]RAG Security Test Runner[/bold cyan]"))
    console.print(f"\n[dim]Loading RAG tests from:[/dim] {tests_path}")
    logger.info("Loading RAG tests from %s", tests_path)

    if resolved_endpoint_mode not in {"query", "retrieve", "ingest"}:
        console.print("[bold red]Invalid endpoint mode.[/bold red] Use query, retrieve, or ingest.")
        raise typer.Exit(1)

    loader = RAGTestLoader(tests_path)
    test_cases = loader.load()

    if not test_cases:
        console.print("[yellow]No RAG test cases to run.[/yellow]")
        raise typer.Exit(0)

    table = Table(title=f"Loaded {len(test_cases)} RAG Test Cases")
    table.add_column("ID", style="cyan")
    table.add_column("Description", style="white", max_width=60)
    for tc in test_cases:
        table.add_row(tc.id, tc.description[:60] + "..." if len(tc.description) > 60 else tc.description)
    console.print(table)

    client = RAGClient(
        service_url=resolved_service_url,
        query_endpoint=resolved_query_endpoint,
        retrieve_endpoint=resolved_retrieve_endpoint,
        ingest_endpoint=resolved_ingest_endpoint,
    )
    scorer = RAGSeverityScorer()
    mutator_provider = None
    mutator_config = None
    if settings and settings.rag.mutator.enabled:
        mutator_provider = get_provider(
            settings.rag.mutator.provider_type,
            settings.rag.mutator.to_provider_config(),
        )
        mutator_config = RAGMutatorConfig(
            enabled=settings.rag.mutator.enabled,
            max_iterations=settings.rag.mutator.max_iterations,
            plateau_window=settings.rag.mutator.plateau_window,
            plateau_tolerance=settings.rag.mutator.plateau_tolerance,
        )
    runner = RAGSessionRunner(
        client,
        mutator=mutator_provider,
        mutator_config=mutator_config,
        scorer=scorer,
    )

    console.print("\n[bold]Running RAG tests...[/bold]\n")
    results = []
    for tc in test_cases:
        logger.info("Running RAG test %s", tc.id)
        response, history = runner.run(tc, endpoint_mode=resolved_endpoint_mode)
        result = scorer.score(tc, response, history=history)
        results.append(result)
        status = "[bold green]PASS[/bold green]" if result.passed else "[bold red]FAIL[/bold red]"
        console.print(f"  {tc.id}: {status}")
        logger.info(
            "Completed RAG test %s passed=%s severity=%.2f",
            tc.id,
            result.passed,
            result.severity_score,
        )

    summary = scorer.summary(results)
    summary_table = Table(title="RAG Test Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="white")
    summary_table.add_row("Total Tests", str(summary.get("total", 0)))
    summary_table.add_row("Passed", f"[green]{summary.get('passed', 0)}[/green]")
    summary_table.add_row("Failed", f"[red]{summary.get('failed', 0)}[/red]")
    summary_table.add_row("Pass Rate", f"{summary.get('pass_rate', 0) * 100:.1f}%")
    summary_table.add_row("Avg Severity", f"{summary.get('avg_severity', 0):.1f}")
    summary_table.add_row("Max Severity", f"{summary.get('max_severity', 0):.1f}")
    console.print()
    console.print(summary_table)
    logger.info(
        "RAG summary total=%d passed=%d failed=%d pass_rate=%.3f avg_severity=%.2f max_severity=%.2f",
        summary.get("total", 0),
        summary.get("passed", 0),
        summary.get("failed", 0),
        summary.get("pass_rate", 0),
        summary.get("avg_severity", 0),
        summary.get("max_severity", 0),
    )

    client.close()


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"eval-fw version {__version__}")


if __name__ == "__main__":
    app()
