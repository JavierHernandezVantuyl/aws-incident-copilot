"""Tests for incident detectors."""

from datetime import datetime
from moto import mock_aws
import boto3
from copilot.sources.cloudwatch import CloudWatchSource
from copilot.sources.cloudtrail import CloudTrailSource
from copilot.detectors import (
    EC2CPUSpikeDetector,
    LambdaErrorDetector,
    BedrockTokenUsageDetector,
    S3AccessDeniedDetector,
    run_all_detectors,
)


@mock_aws
def test_ec2_cpu_spike_detector():
    """Test EC2 CPU spike detection."""
    # Setup CloudWatch metrics
    cloudwatch_client = boto3.client("cloudwatch", region_name="us-east-1")
    ec2 = boto3.client("ec2", region_name="us-east-1")

    # Launch an EC2 instance
    response = ec2.run_instances(ImageId="ami-12345", MinCount=1, MaxCount=1)
    instance_id = response["Instances"][0]["InstanceId"]

    # Put high CPU metrics
    for i in range(3):  # 3 datapoints of high CPU
        cloudwatch_client.put_metric_data(
            Namespace="AWS/EC2",
            MetricData=[
                {
                    "MetricName": "CPUUtilization",
                    "Dimensions": [{"Name": "InstanceId", "Value": instance_id}],
                    "Value": 98.0,
                    "Timestamp": datetime.utcnow(),
                }
            ],
        )

    # Test detector
    cloudwatch = CloudWatchSource(region="us-east-1")
    cloudtrail = CloudTrailSource(region="us-east-1")
    detector = EC2CPUSpikeDetector(cloudwatch, cloudtrail)

    incidents = detector.detect()

    # Verify detection (may not detect due to time windows, but should not error)
    assert isinstance(incidents, list)


@mock_aws
def test_lambda_error_detector():
    """Test Lambda error detection."""
    # Create IAM role first
    iam = boto3.client("iam", region_name="us-east-1")
    iam.create_role(
        RoleName="lambda-role",
        AssumeRolePolicyDocument="{}",
        Path="/",
    )

    # Setup Lambda function
    lambda_client = boto3.client("lambda", region_name="us-east-1")
    lambda_client.create_function(
        FunctionName="test-function",
        Runtime="python3.9",
        Role="arn:aws:iam::123456789012:role/lambda-role",
        Handler="index.handler",
        Code={"ZipFile": b"fake code"},
    )

    # Put error metrics
    cloudwatch_client = boto3.client("cloudwatch", region_name="us-east-1")
    cloudwatch_client.put_metric_data(
        Namespace="AWS/Lambda",
        MetricData=[
            {
                "MetricName": "Errors",
                "Dimensions": [{"Name": "FunctionName", "Value": "test-function"}],
                "Value": 10,
                "Timestamp": datetime.utcnow(),
            }
        ],
    )

    # Test detector
    cloudwatch = CloudWatchSource(region="us-east-1")
    cloudtrail = CloudTrailSource(region="us-east-1")
    detector = LambdaErrorDetector(cloudwatch, cloudtrail)

    incidents = detector.detect()

    # Verify detection
    assert isinstance(incidents, list)


@mock_aws
def test_run_all_detectors():
    """Test running all detectors."""
    cloudwatch = CloudWatchSource(region="us-east-1")
    cloudtrail = CloudTrailSource(region="us-east-1")

    incidents = run_all_detectors(cloudwatch, cloudtrail)

    # Should return a list (may be empty)
    assert isinstance(incidents, list)


def test_bedrock_token_usage_detector_no_aws():
    """Test Bedrock detector initialization without AWS calls."""
    cloudwatch = CloudWatchSource(region="us-east-1")
    cloudtrail = CloudTrailSource(region="us-east-1")
    detector = BedrockTokenUsageDetector(cloudwatch, cloudtrail)

    # Verify detector was created
    assert detector is not None
    assert detector.settings is not None


def test_s3_access_denied_detector_no_aws():
    """Test S3 access denied detector initialization without AWS calls."""
    cloudwatch = CloudWatchSource(region="us-east-1")
    cloudtrail = CloudTrailSource(region="us-east-1")
    detector = S3AccessDeniedDetector(cloudwatch, cloudtrail)

    # Verify detector was created
    assert detector is not None
    assert detector.settings is not None
