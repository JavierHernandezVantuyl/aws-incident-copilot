"""Tests for configuration management."""

from copilot.config import Settings


def test_settings_defaults():
    """Test default settings values."""
    settings = Settings()

    # Test AWS defaults
    assert settings.aws_region == "us-east-1"
    assert settings.aws_profile is None

    # Test threshold defaults
    assert settings.ec2_cpu_threshold == 95.0
    assert settings.ec2_cpu_duration_minutes == 10
    assert settings.lambda_error_threshold == 5

    # Test monitoring defaults
    assert settings.lookback_minutes == 60
    assert settings.poll_interval_seconds == 300

    # Test alerting defaults
    assert settings.enable_alerting is False
    assert settings.sns_topic_arn is None


def test_settings_from_env(monkeypatch):
    """Test loading settings from environment variables."""
    monkeypatch.setenv("COPILOT_AWS_REGION", "us-west-2")
    monkeypatch.setenv("COPILOT_EC2_CPU_THRESHOLD", "90.0")
    monkeypatch.setenv("COPILOT_ENABLE_ALERTING", "true")

    settings = Settings()

    assert settings.aws_region == "us-west-2"
    assert settings.ec2_cpu_threshold == 90.0
    assert settings.enable_alerting is True


def test_settings_evidence_config():
    """Test evidence configuration settings."""
    settings = Settings()

    assert settings.evidence_output_dir == "./evidence"
    assert settings.max_evidence_age_days == 30


def test_settings_bedrock_config():
    """Test Bedrock-specific configuration."""
    settings = Settings()

    assert settings.bedrock_token_threshold == 100000
    assert settings.bedrock_token_window_minutes == 60
