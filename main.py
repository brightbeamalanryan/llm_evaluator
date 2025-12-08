import os

from rich.console import Console
import baseline_injection
from rich.table import Table

def main():
    os.makedirs(os.path.join(os.getcwd(), "logs"), exist_ok=True)
    log_file_path = os.path.join(os.getcwd(), "logs", "log.txt")

    # record=True lets us export everything printed
    console = Console(record=True)

    console.print("[bold yellow]Baseline Prompt Injection Test Harness[/bold yellow]\n")

    table = Table(title="Registered Test Cases")
    table.add_column("ID", style="cyan")
    table.add_column("Description", style="white", max_width=60)
    for tc in baseline_injection.TEST_CASES:
        table.add_row(tc.id, tc.description)

    console.print(table)
    # dump everything to log file as plain text
    with open(log_file_path, "w") as log_file:
        log_file.write(console.export_text())

    # run tests (they should also print via this console if you refactor)
    for tc in baseline_injection.TEST_CASES:
        _console = baseline_injection.run_test_case(tc)
        with open(log_file_path, "w") as log_file:
            log_file.write(_console.export_text())




if __name__ == "__main__":
    main()
