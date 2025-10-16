from __future__ import annotations
import typer
from rich.console import Console

app = typer.Typer(no_args_is_help=True, help="AWS Incident Co-Pilot CLI (mock-first demo)")
console = Console()

@app.command()
def diagnose():
    """
    First version: just say hello so we prove the CLI wiring works.
    """
    console.print("[bold green]Hello from Incident Co-Pilot![/bold green] (Lesson 2)")
    console.print("Next: we’ll load mock incident JSONs and show a table.")

if __name__ == "__main__":
    app()
