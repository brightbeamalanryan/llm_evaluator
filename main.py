from rich.console import Console
import baseline_injection

def main():
    console = Console()
    console.print("[bold yellow]Baseline Prompt Injection Test Harness[/bold yellow]\n")

    table = baseline_injection.Table(title="Registered Test Cases")
    table.add_column("ID", style="cyan")
    table.add_column("Description", style="white", max_width=60)
    for tc in baseline_injection.TEST_CASES:
        table.add_row(tc.id, tc.description)
    console.print(table)

    for tc in baseline_injection.TEST_CASES:
        baseline_injection.run_test_case(tc)

    console.print(
        "\n[bold]Next step (manual):[/bold] For each test, decide whether the "
        "model behaved securely or leaked/obeyed the injection."
    )




if __name__ == "__main__":
    main()
