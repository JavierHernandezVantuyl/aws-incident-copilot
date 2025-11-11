"""Tests for CloudWatch data source."""

import pytest
from datetime import datetime, timedelta
from moto import mock_aws
import boto3
from copilot.sources.cloudwatch import CloudWatchSource


@mock_aws
def test_get_ec2_cpu_metrics():
    """Test getting EC2 CPU metrics."""
    # Create CloudWatch client and put metric data
    cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

    # Put some test metric data
    cloudwatch.put_metric_data(
        Namespace="AWS/EC2",
        MetricData=[
            {
                "MetricName": "CPUUtilization",
                "Dimensions": [{"Name": "InstanceId", "Value": "i-test123"}],
                "Value": 98.5,
                "Timestamp": datetime.utcnow(),
            }
        ],
    )

    # Test CloudWatch source
    source = CloudWatchSource(region="us-east-1")
    metrics = source.get_ec2_cpu_metrics("i-test123", lookback_minutes=60)

    # Verify metrics were retrieved
    assert isinstance(metrics, list)


@mock_aws
def test_get_all_ec2_instances():
    """Test getting all EC2 instances."""
    # Create EC2 client and launch instance
    ec2 = boto3.client("ec2", region_name="us-east-1")
    ec2.run_instances(ImageId="ami-12345", MinCount=1, MaxCount=1)

    # Test CloudWatch source
    source = CloudWatchSource(region="us-east-1")
    instances = source.get_all_ec2_instances()

    # Verify instances were retrieved
    assert isinstance(instances, list)
    assert len(instances) > 0


@mock_aws
def test_get_lambda_error_metrics():
    """Test getting Lambda error metrics."""
    # Create CloudWatch client and put metric data
    cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

    cloudwatch.put_metric_data(
        Namespace="AWS/Lambda",
        MetricData=[
            {
                "MetricName": "Errors",
                "Dimensions": [{"Name": "FunctionName", "Value": "test-function"}],
                "Value": 5,
                "Timestamp": datetime.utcnow(),
            }
        ],
    )

    # Test CloudWatch source
    source = CloudWatchSource(region="us-east-1")
    metrics = source.get_lambda_error_metrics("test-function", lookback_minutes=60)

    # Verify metrics were retrieved
    assert isinstance(metrics, list)


@mock_aws
def test_get_all_lambda_functions():
    """Test getting all Lambda functions."""
    # Create IAM role first
    iam = boto3.client("iam", region_name="us-east-1")
    iam.create_role(
        RoleName="lambda-role",
        AssumeRolePolicyDocument="{}",
        Path="/",
    )

    # Create Lambda client and function
    lambda_client = boto3.client("lambda", region_name="us-east-1")
    lambda_client.create_function(
        FunctionName="test-function",
        Runtime="python3.9",
        Role="arn:aws:iam::123456789012:role/lambda-role",
        Handler="index.handler",
        Code={"ZipFile": b"fake code"},
    )

    # Test CloudWatch source
    source = CloudWatchSource(region="us-east-1")
    functions = source.get_all_lambda_functions()

    # Verify functions were retrieved
    assert isinstance(functions, list)
    assert "test-function" in functions
