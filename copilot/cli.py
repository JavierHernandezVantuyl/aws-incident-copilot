from __future__ import annotations

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table

from copilot.sources import mock as mock_source

app = typer.Typer(no_args_is_help=True, help="AWS Incident Co-Pilot CLI (mock-first demo)")
console = Console()

def _print_incidents(incidents):
    table = Table(title="Detected Incidents (mock)", show_lines=True)
    table.add_column("Slug", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Severity", style="red")
    table.add_column("Resource", style="magenta")
    table.add_column("Suggested Fix", style="green")
    for inc in incidents:
        table.add_row(inc.id, inc.title, inc.severity, inc.resource, inc.suggested_fix)
    console.print(table)

@app.command()
def diagnose(incident: Optional[str] = typer.Option(None, "--incident", help="Specific incident slug")):
    """Diagnose incidents from mock JSON files."""
    if incident:
        inc = mock_source.load_incident(incident)
        _print_incidents([inc])
    else:
        incs = mock_source.load_all()
        _print_incidents(incs)

if __name__ == "__main__":
    app()