# tests/test_cli.py
from typer.testing import CliRunner
from copilot.cli import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "AWS Incident Co-Pilot" in result.stdout


def test_diagnose_list():
    result = runner.invoke(app, ["diagnose"])
    assert result.exit_code == 0
    assert "Detected Incidents" in result.stdout
