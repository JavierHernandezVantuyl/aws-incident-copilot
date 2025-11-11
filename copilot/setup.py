"""Interactive setup wizard for AWS Incident Co-Pilot."""

import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()


def run_setup_wizard():
    """Run the interactive setup wizard."""
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]Welcome to AWS Incident Co-Pilot Setup! 🚀[/bold cyan]\n\n"
            "This wizard will help you configure the tool in just a few steps.\n"
            "Don't worry - we'll guide you through everything!",
            border_style="cyan",
        )
    )
    console.print()

    # Show important warnings
    console.print(
        Panel(
            "[bold yellow]⚠️  Important Information[/bold yellow]\n\n"
            "[bold]Security:[/bold]\n"
            "• This tool is READ-ONLY - it won't modify your AWS resources\n"
            "• Keep your AWS access keys private (never share or commit to Git)\n"
            "• We'll save credentials to ~/.aws/credentials (standard AWS location)\n\n"
            "[bold]Costs:[/bold]\n"
            "• AWS API calls may incur small charges (~$1-2/month for hourly checks)\n"
            "• CloudWatch & CloudTrail usage typically covered by free tier\n\n"
            "[bold]Permissions:[/bold]\n"
            "• You need read access to CloudWatch, CloudTrail, EC2, and Lambda\n"
            "• IAM user with proper permissions required (not root account)",
            border_style="yellow",
            padding=(1, 2),
        )
    )
    console.print()

    if not Confirm.ask(
        "[bold]Do you understand and want to continue?[/bold]", default=True
    ):
        console.print(
            "\n[yellow]Setup cancelled. Run 'copilot setup' when ready![/yellow]"
        )
        raise typer.Exit()

    console.print()

    # Step 1: Check for existing AWS credentials
    console.print("[bold]Step 1: AWS Credentials[/bold]")
    console.print("We need to connect to your AWS account to monitor for incidents.\n")

    has_aws_cli = check_aws_cli_installed()

    if has_aws_cli:
        console.print("✓ AWS CLI is installed!", style="green")
        if check_aws_credentials():
            console.print("✓ AWS credentials are already configured!", style="green")
            console.print()
            if not Confirm.ask("Would you like to use a different AWS profile?"):
                profile = None
            else:
                profile = prompt_aws_profile()
        else:
            console.print(
                "⚠ No AWS credentials found. Let's set them up!", style="yellow"
            )
            profile = setup_aws_credentials()
    else:
        console.print("⚠ AWS CLI is not installed", style="yellow")
        console.print("\nTo install AWS CLI, visit:")
        console.print(
            "[link]https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html[/link]"
        )
        console.print()
        if Confirm.ask(
            "Do you have AWS access keys ready? (We can configure them manually)"
        ):
            profile = setup_aws_credentials_manual()
        else:
            console.print(
                "\n[yellow]Please install AWS CLI and get your access keys, then run:[/yellow]"
            )
            console.print("[cyan]copilot setup[/cyan]")
            return

    # Step 2: Choose AWS region
    console.print("\n[bold]Step 2: AWS Region[/bold]")
    region = prompt_aws_region()

    # Step 3: Configure detection settings
    console.print("\n[bold]Step 3: Detection Settings[/bold]")
    console.print("Let's configure when you want to be alerted about incidents.\n")

    use_defaults = Confirm.ask(
        "Use recommended default settings? (You can change these later)",
        default=True,
    )

    if use_defaults:
        config = get_default_config(region, profile)
        console.print("✓ Using recommended defaults", style="green")
    else:
        config = prompt_custom_settings(region, profile)

    # Step 4: Test connection
    console.print("\n[bold]Step 4: Test Connection[/bold]")
    if Confirm.ask("Would you like to test the AWS connection now?", default=True):
        test_aws_connection(region, profile)

    # Step 5: Save configuration
    console.print("\n[bold]Step 5: Save Configuration[/bold]")
    save_configuration(config)

    # Success!
    console.print()
    console.print(
        Panel.fit(
            "[bold green]🎉 Setup Complete![/bold green]\n\n"
            "You're all set to start monitoring your AWS infrastructure!\n\n"
            "Quick Start:\n"
            "  • [cyan]copilot monitor[/cyan]     - Run a single scan\n"
            "  • [cyan]copilot monitor -c[/cyan]  - Continuous monitoring\n"
            "  • [cyan]copilot test[/cyan]        - Test AWS connection\n"
            "  • [cyan]copilot help[/cyan]        - Get help",
            border_style="green",
        )
    )


def check_aws_cli_installed() -> bool:
    """Check if AWS CLI is installed."""
    import shutil

    return shutil.which("aws") is not None


def check_aws_credentials() -> bool:
    """Check if AWS credentials are configured."""
    # Check environment variables
    if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
        return True

    # Check credentials file
    creds_file = Path.home() / ".aws" / "credentials"
    return creds_file.exists()


def prompt_aws_profile() -> Optional[str]:
    """Prompt for AWS profile name."""
    profile = Prompt.ask("Enter AWS profile name (leave empty for default)", default="")
    return profile if profile else None


def setup_aws_credentials() -> Optional[str]:
    """Guide user through AWS credentials setup."""
    console.print("\nLet's configure your AWS credentials.")
    console.print("You'll need your AWS Access Key ID and Secret Access Key.\n")
    console.print("Where to find these:")
    console.print(
        "1. Log into AWS Console → IAM → Users → Your User → Security Credentials"
    )
    console.print("2. Click 'Create access key'\n")

    if Confirm.ask("Do you have your access keys ready?"):
        console.print("\nRun this command in your terminal:")
        console.print("[cyan]aws configure[/cyan]")
        console.print(
            "\nThen paste your access keys when prompted, and come back here.\n"
        )
        Prompt.ask("Press Enter when you've completed AWS configuration...")
        return None
    else:
        console.print(
            "\n[yellow]Please get your AWS access keys first, then run:[/yellow]"
        )
        console.print("[cyan]copilot setup[/cyan]")
        raise typer.Exit()


def setup_aws_credentials_manual() -> Optional[str]:
    """Manually configure AWS credentials."""
    access_key = Prompt.ask("AWS Access Key ID")
    secret_key = Prompt.ask("AWS Secret Access Key", password=True)
    region = Prompt.ask("Default region", default="us-east-1")

    # Create .aws directory
    aws_dir = Path.home() / ".aws"
    aws_dir.mkdir(exist_ok=True)

    # Write credentials
    creds_file = aws_dir / "credentials"
    with open(creds_file, "a") as f:
        f.write("\n[default]\n")
        f.write(f"aws_access_key_id = {access_key}\n")
        f.write(f"aws_secret_access_key = {secret_key}\n")

    # Write config
    config_file = aws_dir / "config"
    with open(config_file, "a") as f:
        f.write("\n[default]\n")
        f.write(f"region = {region}\n")

    console.print("✓ AWS credentials saved!", style="green")
    return None


def prompt_aws_region() -> str:
    """Prompt for AWS region."""
    console.print("Select your AWS region (where your resources are):\n")

    regions = {
        "1": ("us-east-1", "US East (N. Virginia)"),
        "2": ("us-west-2", "US West (Oregon)"),
        "3": ("eu-west-1", "EU (Ireland)"),
        "4": ("ap-southeast-1", "Asia Pacific (Singapore)"),
        "5": ("other", "Enter custom region"),
    }

    table = Table(show_header=False, box=None)
    for num, (code, name) in regions.items():
        if code != "other":
            table.add_row(f"[cyan]{num}[/cyan]", f"{name} ({code})")
        else:
            table.add_row(f"[cyan]{num}[/cyan]", name)

    console.print(table)
    console.print()

    choice = Prompt.ask("Choose a region", choices=list(regions.keys()), default="1")

    if regions[choice][0] == "other":
        return Prompt.ask("Enter AWS region code", default="us-east-1")
    else:
        return regions[choice][0]


def get_default_config(region: str, profile: Optional[str]) -> dict:
    """Get default configuration."""
    return {
        "COPILOT_AWS_REGION": region,
        "COPILOT_AWS_PROFILE": profile or "",
        "COPILOT_EC2_CPU_THRESHOLD": "95.0",
        "COPILOT_EC2_CPU_DURATION_MINUTES": "10",
        "COPILOT_LAMBDA_ERROR_THRESHOLD": "5",
        "COPILOT_BEDROCK_TOKEN_THRESHOLD": "100000",
        "COPILOT_LOOKBACK_MINUTES": "60",
        "COPILOT_POLL_INTERVAL_SECONDS": "300",
        "COPILOT_ENABLE_ALERTING": "false",
    }


def prompt_custom_settings(region: str, profile: Optional[str]) -> dict:
    """Prompt for custom settings."""
    config = {"COPILOT_AWS_REGION": region, "COPILOT_AWS_PROFILE": profile or ""}

    console.print("Configure detection thresholds:\n")

    config["COPILOT_EC2_CPU_THRESHOLD"] = Prompt.ask(
        "EC2 CPU threshold (%)", default="95.0"
    )
    config["COPILOT_LAMBDA_ERROR_THRESHOLD"] = Prompt.ask(
        "Lambda error threshold (count)", default="5"
    )
    config["COPILOT_LOOKBACK_MINUTES"] = Prompt.ask(
        "How far back to check (minutes)", default="60"
    )

    config["COPILOT_ENABLE_ALERTING"] = str(
        Confirm.ask("Enable alerting?", default=False)
    ).lower()

    return config


def test_aws_connection(region: str, profile: Optional[str]):
    """Test AWS connection."""
    console.print("Testing connection to AWS...", style="yellow")

    try:
        import boto3

        session_kwargs = {"region_name": region}
        if profile:
            session_kwargs["profile_name"] = profile

        session = boto3.Session(**session_kwargs)
        sts = session.client("sts")

        # Get caller identity
        identity = sts.get_caller_identity()

        console.print("✓ Successfully connected to AWS!", style="green")
        console.print(f"  Account: {identity['Account']}")
        console.print(f"  User: {identity['Arn']}")
        console.print(f"  Region: {region}")

    except Exception as e:
        console.print(f"✗ Connection failed: {e}", style="red")
        console.print(
            "\n[yellow]Please check your AWS credentials and try again.[/yellow]"
        )


def save_configuration(config: dict):
    """Save configuration to .env file."""
    env_file = Path.cwd() / ".env"

    console.print(f"Saving configuration to {env_file}...")

    with open(env_file, "w") as f:
        f.write("# AWS Incident Co-Pilot Configuration\n")
        f.write("# Generated by setup wizard\n\n")

        for key, value in config.items():
            if value:  # Only write non-empty values
                f.write(f"{key}={value}\n")

    console.print("✓ Configuration saved!", style="green")
