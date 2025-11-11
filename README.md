# AWS Incident Co-Pilot

A real-time AWS incident detection and response CLI tool that monitors your AWS infrastructure, detects incidents, collects evidence, and sends alerts.

## Features

- **Real-time Monitoring**: Continuously monitor AWS resources for incidents
- **Multiple Incident Types**:
  - EC2 CPU spikes
  - Lambda function errors and timeouts
  - Bedrock token usage spikes
  - S3 access denied errors
  - DynamoDB throttling (coming soon)
- **Evidence Collection**: Automatically collect and package CloudWatch metrics and CloudTrail logs
- **Alerting**: Send notifications via SNS or email for HIGH/CRITICAL incidents
- **Configurable Thresholds**: Customize detection thresholds via environment variables
- **Mock Mode**: Test with mock data before connecting to AWS

## Installation

### Prerequisites

- Python 3.9 or higher
- AWS credentials configured (via `~/.aws/credentials` or environment variables)
- Appropriate IAM permissions (see [Required Permissions](#required-permissions))

### Install from Source

```bash
# Clone the repository
git clone https://github.com/JavierHernandezVantuyl/aws-incident-copilot.git
cd aws-incident-copilot

# Install dependencies
pip install -e .

# For development (includes testing tools)
pip install -e ".[dev]"
```

## Quick Start

### 1. Mock Mode (No AWS Required)

Test the CLI with mock incident data:

```bash
# List all mock incidents
copilot diagnose

# View specific incident
copilot diagnose --incident ec2-cpu-spike
```

### 2. Real AWS Monitoring

Monitor your AWS resources for incidents:

```bash
# Run a single scan
copilot monitor

# Run continuous monitoring (polls every 5 minutes)
copilot monitor --continuous

# Enable alerting for HIGH/CRITICAL incidents
copilot monitor --continuous --alerts

# Monitor specific region
copilot monitor --region us-west-2

# Use specific AWS profile
copilot monitor --profile production
```

## Configuration

Configure the tool via environment variables or a `.env` file:

```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
nano .env
```

### AWS Configuration

```bash
COPILOT_AWS_REGION=us-east-1
COPILOT_AWS_PROFILE=default  # Optional: AWS profile name
```

### Detection Thresholds

```bash
# EC2 CPU Spike Detection
COPILOT_EC2_CPU_THRESHOLD=95.0                # CPU percentage threshold
COPILOT_EC2_CPU_DURATION_MINUTES=10           # Sustained duration

# Lambda Error Detection
COPILOT_LAMBDA_ERROR_THRESHOLD=5              # Number of errors
COPILOT_LAMBDA_TIMEOUT_THRESHOLD_MS=25000     # Timeout threshold

# Bedrock Token Usage
COPILOT_BEDROCK_TOKEN_THRESHOLD=100000        # Token count threshold
COPILOT_BEDROCK_TOKEN_WINDOW_MINUTES=60       # Time window

# DynamoDB Throttling
COPILOT_DYNAMODB_THROTTLE_THRESHOLD=10        # Throttle event count

# RDS Connections
COPILOT_RDS_CONNECTION_THRESHOLD=90           # Connection percentage
```

### Monitoring Configuration

```bash
COPILOT_LOOKBACK_MINUTES=60              # How far back to check metrics
COPILOT_POLL_INTERVAL_SECONDS=300        # Polling interval for continuous mode
```

### Alerting Configuration

```bash
COPILOT_ENABLE_ALERTING=true
COPILOT_SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:incident-alerts
COPILOT_ALERT_EMAIL=alerts@example.com
```

### Evidence Configuration

```bash
COPILOT_EVIDENCE_OUTPUT_DIR=./evidence   # Where to store evidence files
COPILOT_MAX_EVIDENCE_AGE_DAYS=30         # Auto-cleanup threshold
```

## Usage Examples

### Basic Monitoring

```bash
# Single scan of all AWS resources
copilot monitor

# Continuous monitoring (Ctrl+C to stop)
copilot monitor --continuous

# Disable evidence collection (faster)
copilot monitor --no-evidence
```

### Advanced Monitoring

```bash
# Production setup: continuous monitoring with alerts
copilot monitor \
  --continuous \
  --alerts \
  --region us-east-1 \
  --profile production

# Quick check without evidence collection
copilot monitor --no-evidence
```

### Working with Mock Data

```bash
# List all mock incidents
copilot diagnose

# View specific incident types
copilot diagnose --incident ec2-cpu-spike
copilot diagnose --incident s3-access-denied

# Alias for diagnose
copilot diag
```

## Required Permissions

Create an IAM policy with these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "cloudtrail:LookupEvents",
        "ec2:DescribeInstances",
        "lambda:ListFunctions",
        "lambda:GetFunction",
        "sns:Publish",
        "ses:SendEmail"
      ],
      "Resource": "*"
    }
  ]
}
```

## Architecture

```
aws-incident-copilot/
├── copilot/
│   ├── cli.py              # CLI commands
│   ├── config.py           # Configuration management
│   ├── incidents/          # Incident data models
│   ├── sources/            # Data sources (CloudWatch, CloudTrail)
│   │   ├── cloudwatch.py
│   │   ├── cloudtrail.py
│   │   └── mock.py
│   ├── detectors/          # Incident detection logic
│   ├── evidence.py         # Evidence collection
│   └── alerts.py           # Alerting system
├── tests/                  # Test suite
└── .env.example           # Configuration template
```

## Detected Incident Types

### 1. EC2 CPU Spike
- **Detection**: CPU > 95% for 10+ minutes (configurable)
- **Severity**: MEDIUM to HIGH
- **Evidence**: CloudWatch CPU metrics, instance details

### 2. Lambda Function Errors
- **Detection**: 5+ errors in lookback window (configurable)
- **Severity**: MEDIUM to HIGH (HIGH if also timing out)
- **Evidence**: Error metrics, duration metrics, CloudWatch logs

### 3. Bedrock Token Usage Spike
- **Detection**: >100K tokens in 60 minutes (configurable)
- **Severity**: HIGH
- **Evidence**: Token metrics, invocation counts

### 4. S3 Access Denied
- **Detection**: AccessDenied errors in CloudTrail
- **Severity**: HIGH
- **Evidence**: CloudTrail events, bucket policies

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=copilot --cov-report=html

# Run specific test file
pytest tests/test_detectors.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Lint code
ruff check .

# Format code
black .

# Check formatting without modifying
black --check .
```

### CI/CD

GitHub Actions automatically runs on all PRs:
- Linting with ruff and black
- Test suite with pytest
- Python 3.11 on Ubuntu

## Troubleshooting

### No incidents detected

- Verify AWS credentials: `aws sts get-caller-identity`
- Check IAM permissions
- Verify resources exist in the specified region
- Adjust detection thresholds in `.env`

### CloudTrail events not found

- Ensure CloudTrail is enabled in your AWS account
- CloudTrail has a delay of up to 15 minutes
- Verify `COPILOT_LOOKBACK_MINUTES` is sufficient

### Alerting not working

- Verify SNS topic exists and you have publish permissions
- For email alerts, verify sender email is verified in SES
- Check `COPILOT_ENABLE_ALERTING=true` is set

## Roadmap

- [ ] Additional incident types (RDS, DynamoDB, API Gateway)
- [ ] Web UI dashboard
- [ ] Slack/Teams integration
- [ ] Custom detection rules
- [ ] Machine learning for anomaly detection
- [ ] Multi-account support
- [ ] Historical incident tracking
- [ ] Automated remediation actions

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass and code is formatted
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Author

Javier Hernandez Vantuyl

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues).
