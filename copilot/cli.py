from __future__ import annotations

import typer
import time
from typing import Optional
from rich.console import Console
from rich.table import Table

from copilot.sources import mock as mock_source
from copilot.sources.cloudwatch import CloudWatchSource
from copilot.sources.cloudtrail import CloudTrailSource
from copilot.detectors import run_all_detectors
from copilot.evidence import EvidenceCollector
from copilot.alerts import AlertManager
from copilot.config import settings

app = typer.Typer(
    no_args_is_help=True,
    help="AWS Incident Co-Pilot - Real-time AWS incident detection and response",
)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    incident: Optional[str] = typer.Option(
        None,
        "--incident",
        help="Specific incident slug (default command: diagnose)",
    ),
):
    """
    If no subcommand is provided, behave like `diagnose` so you can run
    `copilot` or `copilot --incident <slug>` directly.
    """
    if ctx.invoked_subcommand is None:
        if incident:
            inc = mock_source.load_incident(incident)
            _print_incidents([inc], title="Detected Incidents (mock)")
        else:
            incs = mock_source.load_all()
            _print_incidents(incs, title="Detected Incidents (mock)")


@app.command()
def diagnose(
    incident: Optional[str] = typer.Option(
        None, "--incident", help="Specific incident slug"
    )
):
    """Diagnose incidents from mock JSON files."""
    if incident:
        inc = mock_source.load_incident(incident)
        _print_incidents([inc], title="Detected Incidents (mock)")
    else:
        incs = mock_source.load_all()
        _print_incidents(incs, title="Detected Incidents (mock)")


@app.command("diag")
def diag(
    incident: Optional[str] = typer.Option(
        None, "--incident", help="Specific incident slug"
    )
):
    """Alias for `diagnose`."""
    return diagnose(incident=incident)


@app.command()
def monitor(
    continuous: bool = typer.Option(
        False, "--continuous", "-c", help="Run continuously with polling"
    ),
    collect_evidence: bool = typer.Option(
        True, "--evidence/--no-evidence", help="Collect evidence for incidents"
    ),
    enable_alerts: bool = typer.Option(
        False, "--alerts", "-a", help="Send alerts for HIGH/CRITICAL incidents"
    ),
    region: Optional[str] = typer.Option(
        None, "--region", "-r", help="AWS region (default from config)"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="AWS profile name"
    ),
):
    """Monitor AWS resources for incidents in real-time."""
    region = region or settings.aws_region

    console.print("[bold cyan]Starting AWS Incident Monitor[/bold cyan]")
    console.print(f"Region: {region}")
    console.print(f"Continuous: {continuous}")
    console.print(f"Evidence Collection: {collect_evidence}")
    console.print(f"Alerting: {enable_alerts}")
    console.print()

    # Initialize AWS clients
    try:
        cloudwatch = CloudWatchSource(region=region, profile=profile)
        cloudtrail = CloudTrailSource(region=region, profile=profile)
        console.print("[green]✓[/green] Connected to AWS services")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to connect to AWS: {e}")
        raise typer.Exit(1)

    # Initialize optional services
    evidence_collector = None
    alert_manager = None

    if collect_evidence:
        evidence_collector = EvidenceCollector(cloudwatch, cloudtrail)
        console.print(
            f"[green]✓[/green] Evidence collection enabled (output: {settings.evidence_output_dir})"
        )

    if enable_alerts:
        alert_manager = AlertManager(region=region, profile=profile)
        console.print("[green]✓[/green] Alerting enabled")

    console.print()

    def scan_for_incidents():
        """Run a single scan for incidents."""
        console.print("[yellow]Scanning for incidents...[/yellow]")

        # Run all detectors
        incidents = run_all_detectors(cloudwatch, cloudtrail)

        if not incidents:
            console.print("[green]✓[/green] No incidents detected")
            return

        # Print incidents
        _print_incidents(incidents, title="Active Incidents")

        # Collect evidence if enabled
        if collect_evidence and evidence_collector:
            console.print()
            console.print("[yellow]Collecting evidence...[/yellow]")
            for incident in incidents:
                try:
                    evidence_paths = evidence_collector.collect_for_incident(incident)
                    console.print(
                        f"[green]✓[/green] Evidence collected for {incident.id}: {len(evidence_paths)} files"
                    )
                except Exception as e:
                    console.print(
                        f"[red]✗[/red] Failed to collect evidence for {incident.id}: {e}"
                    )

        # Send alerts if enabled
        if enable_alerts and alert_manager:
            console.print()
            console.print("[yellow]Sending alerts...[/yellow]")
            alert_manager.alert_on_incidents(incidents, use_sns=True, use_email=True)
            high_critical = [i for i in incidents if i.severity in ["HIGH", "CRITICAL"]]
            if high_critical:
                console.print(
                    f"[green]✓[/green] Alerts sent for {len(high_critical)} HIGH/CRITICAL incidents"
                )

    # Run monitoring
    try:
        if continuous:
            console.print(
                f"[cyan]Monitoring continuously (polling every {settings.poll_interval_seconds}s)...[/cyan]"
            )
            console.print("[dim]Press Ctrl+C to stop[/dim]")
            console.print()

            while True:
                scan_for_incidents()
                console.print()
                console.print(
                    f"[dim]Next scan in {settings.poll_interval_seconds} seconds...[/dim]"
                )
                console.print()
                time.sleep(settings.poll_interval_seconds)
        else:
            scan_for_incidents()
    except KeyboardInterrupt:
        console.print()
        console.print("[yellow]Monitoring stopped by user[/yellow]")


def _print_incidents(incidents, title="Detected Incidents"):
    """Print incidents in a formatted table."""
    table = Table(title=title, show_lines=True)
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Severity", style="red")
    table.add_column("Resource", style="magenta")
    table.add_column("Description", style="yellow", max_width=50)

    for inc in incidents:
        # Color code severity
        severity_color = {
            "LOW": "green",
            "MEDIUM": "yellow",
            "HIGH": "red",
            "CRITICAL": "bold red",
        }.get(inc.severity, "white")

        table.add_row(
            inc.id,
            inc.title,
            f"[{severity_color}]{inc.severity}[/{severity_color}]",
            inc.resource,
            (
                inc.description[:100] + "..."
                if len(inc.description) > 100
                else inc.description
            ),
        )

    console.print(table)


if __name__ == "__main__":
    app()
