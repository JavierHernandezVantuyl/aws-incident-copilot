"""Configuration management for AWS Incident Co-Pilot."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="COPILOT_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_profile: Optional[str] = None

    # Detection Thresholds
    ec2_cpu_threshold: float = 95.0
    ec2_cpu_duration_minutes: int = 10
    lambda_error_threshold: int = 5
    lambda_timeout_threshold_ms: int = 25000
    bedrock_token_threshold: int = 100000
    bedrock_token_window_minutes: int = 60
    dynamodb_throttle_threshold: int = 10
    rds_connection_threshold: int = 90

    # Monitoring Configuration
    lookback_minutes: int = 60
    poll_interval_seconds: int = 300

    # Alerting Configuration
    enable_alerting: bool = False
    sns_topic_arn: Optional[str] = None
    alert_email: Optional[str] = None

    # Evidence Configuration
    evidence_output_dir: str = "./evidence"
    max_evidence_age_days: int = 30


# Global settings instance
settings = Settings()
