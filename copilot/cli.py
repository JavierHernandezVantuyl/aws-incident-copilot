from __future__ import annotations

import typer
import time
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from copilot.sources import mock as mock_source
from copilot.sources.cloudwatch import CloudWatchSource
from copilot.sources.cloudtrail import CloudTrailSource
from copilot.detectors import run_all_detectors
from copilot.evidence import EvidenceCollector
from copilot.alerts import AlertManager
from copilot.config import settings

app = typer.Typer(
    no_args_is_help=False,
    help="🚀 AWS Incident Co-Pilot - Monitor and respond to AWS incidents with ease",
)
console = Console()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """AWS Incident Co-Pilot - Your friendly AWS monitoring assistant."""
    if ctx.invoked_subcommand is None:
        # Show welcome message
        console.print()
        console.print(
            Panel.fit(
                "[bold cyan]AWS Incident Co-Pilot 🚀[/bold cyan]\n\n"
                "Monitor your AWS infrastructure and respond to incidents quickly!\n\n"
                "[dim]Quick Start:[/dim]\n"
                "  [cyan]copilot setup[/cyan]        - First time? Run this to get started\n"
                "  [cyan]copilot monitor[/cyan]      - Scan your AWS account for incidents\n"
                "  [cyan]copilot test[/cyan]         - Test your AWS connection\n\n"
                "[dim]Need help?[/dim] Run [cyan]copilot --help[/cyan]",
                border_style="cyan",
            )
        )
        console.print()


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
        False, "--continuous", "-c", help="Keep monitoring (poll every 5 minutes)"
    ),
    collect_evidence: bool = typer.Option(
        True, "--evidence/--no-evidence", help="Save evidence files"
    ),
    enable_alerts: bool = typer.Option(
        False, "--alerts", "-a", help="Send email/SNS alerts for HIGH/CRITICAL"
    ),
    region: Optional[str] = typer.Option(
        None, "--region", "-r", help="AWS region (default from config)"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="AWS profile name"
    ),
):
    """📊 Monitor your AWS account for incidents.

    This scans your AWS resources (EC2, Lambda, S3, Bedrock) for issues like:
    • High CPU usage on EC2 instances
    • Lambda function errors
    • Excessive Bedrock token usage
    • S3 access denied errors

    Examples:
      copilot monitor                 # Run once
      copilot monitor --continuous    # Keep monitoring
      copilot monitor --alerts        # Enable alerts
    """
    region = region or settings.aws_region

    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]🔍 AWS Incident Monitor[/bold cyan]\n\n"
            f"Region: [yellow]{region}[/yellow]\n"
            f"Mode: {'[green]Continuous[/green]' if continuous else '[yellow]Single Scan[/yellow]'}\n"
            f"Evidence: {'[green]Enabled[/green]' if collect_evidence else '[dim]Disabled[/dim]'}\n"
            f"Alerts: {'[green]Enabled[/green]' if enable_alerts else '[dim]Disabled[/dim]'}",
            border_style="cyan",
        )
    )
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


@app.command()
def setup():
    """🛠️  Run the interactive setup wizard (recommended for first-time users)."""
    from copilot.setup import run_setup_wizard

    run_setup_wizard()


@app.command()
def test(
    region: Optional[str] = typer.Option(
        None, "--region", "-r", help="AWS region to test"
    ),
    profile: Optional[str] = typer.Option(
        None, "--profile", "-p", help="AWS profile to use"
    ),
):
    """🔍 Test your AWS connection and verify credentials."""
    region = region or settings.aws_region
    profile = profile or settings.aws_profile

    console.print()
    console.print("[bold]Testing AWS Connection...[/bold]")
    console.print()

    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError

        # Create session
        session_kwargs = {"region_name": region}
        if profile:
            session_kwargs["profile_name"] = profile

        session = boto3.Session(**session_kwargs)

        # Test STS (this verifies credentials)
        console.print("[yellow]→[/yellow] Verifying AWS credentials...")
        sts = session.client("sts")
        identity = sts.get_caller_identity()

        console.print("[green]✓[/green] AWS credentials are valid!")
        console.print(f"  Account ID: {identity['Account']}")
        console.print(f"  User ARN: {identity['Arn']}")
        console.print()

        # Test CloudWatch access
        console.print("[yellow]→[/yellow] Testing CloudWatch access...")
        cloudwatch = session.client("cloudwatch")
        cloudwatch.list_metrics(MaxRecords=1)
        console.print("[green]✓[/green] CloudWatch access confirmed")

        # Test CloudTrail access
        console.print("[yellow]→[/yellow] Testing CloudTrail access...")
        cloudtrail = session.client("cloudtrail")
        cloudtrail.lookup_events(MaxResults=1)
        console.print("[green]✓[/green] CloudTrail access confirmed")

        # Test EC2 access
        console.print("[yellow]→[/yellow] Testing EC2 access...")
        ec2 = session.client("ec2")
        ec2.describe_instances(MaxResults=5)
        console.print("[green]✓[/green] EC2 access confirmed")

        console.print()
        console.print(
            Panel.fit(
                "[bold green]✅ All tests passed![/bold green]\n\n"
                "Your AWS connection is working perfectly.\n"
                f"Region: [cyan]{region}[/cyan]\n"
                + (f"Profile: [cyan]{profile}[/cyan]\n" if profile else "")
                + "\nYou're ready to start monitoring!",
                border_style="green",
            )
        )

    except NoCredentialsError:
        console.print()
        console.print(
            Panel.fit(
                "[bold red]❌ No AWS Credentials Found[/bold red]\n\n"
                "We couldn't find your AWS credentials.\n\n"
                "[yellow]To fix this:[/yellow]\n"
                "1. Run [cyan]copilot setup[/cyan] to configure credentials\n"
                "2. Or manually run [cyan]aws configure[/cyan]",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    except ClientError as e:
        console.print()
        console.print(
            Panel.fit(
                f"[bold red]❌ AWS Error[/bold red]\n\n"
                f"{str(e)}\n\n"
                "[yellow]Possible causes:[/yellow]\n"
                "• Incorrect credentials\n"
                "• Insufficient IAM permissions\n"
                "• Invalid region\n\n"
                "[cyan]Try running:[/cyan] copilot setup",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    except Exception as e:
        console.print()
        console.print(
            Panel.fit(
                f"[bold red]❌ Unexpected Error[/bold red]\n\n{str(e)}",
                border_style="red",
            )
        )
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
