"""CloudWatch data source for metrics monitoring."""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class CloudWatchSource:
    """CloudWatch metrics data source."""

    def __init__(self, region: str = "us-east-1", profile: Optional[str] = None):
        """Initialize CloudWatch client.

        Args:
            region: AWS region to connect to
            profile: AWS profile name (optional)
        """
        session_kwargs = {"region_name": region}
        if profile:
            session_kwargs["profile_name"] = profile

        session = boto3.Session(**session_kwargs)
        self.cloudwatch = session.client("cloudwatch")
        self.ec2 = session.client("ec2")
        self.lambda_client = session.client("lambda")
        self.region = region

    def get_ec2_cpu_metrics(
        self, instance_id: str, lookback_minutes: int = 60
    ) -> List[Dict[str, Any]]:
        """Get CPU utilization metrics for an EC2 instance.

        Args:
            instance_id: EC2 instance ID
            lookback_minutes: How far back to look for metrics

        Returns:
            List of datapoints with timestamp and value
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=lookback_minutes)

            response = self.cloudwatch.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,  # 5 minutes
                Statistics=["Average", "Maximum"],
            )

            return sorted(response.get("Datapoints", []), key=lambda x: x["Timestamp"])
        except (ClientError, NoCredentialsError) as e:
            print(f"Error fetching EC2 CPU metrics: {e}")
            return []

    def get_all_ec2_instances(self) -> List[str]:
        """Get all running EC2 instance IDs in the region.

        Returns:
            List of instance IDs
        """
        try:
            response = self.ec2.describe_instances(
                Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
            )

            instances = []
            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances.append(instance["InstanceId"])

            return instances
        except (ClientError, NoCredentialsError) as e:
            print(f"Error fetching EC2 instances: {e}")
            return []

    def get_lambda_error_metrics(
        self, function_name: str, lookback_minutes: int = 60
    ) -> List[Dict[str, Any]]:
        """Get error metrics for a Lambda function.

        Args:
            function_name: Lambda function name
            lookback_minutes: How far back to look for metrics

        Returns:
            List of datapoints with timestamp and value
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=lookback_minutes)

            response = self.cloudwatch.get_metric_statistics(
                Namespace="AWS/Lambda",
                MetricName="Errors",
                Dimensions=[{"Name": "FunctionName", "Value": function_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=["Sum"],
            )

            return sorted(response.get("Datapoints", []), key=lambda x: x["Timestamp"])
        except (ClientError, NoCredentialsError) as e:
            print(f"Error fetching Lambda error metrics: {e}")
            return []

    def get_lambda_duration_metrics(
        self, function_name: str, lookback_minutes: int = 60
    ) -> List[Dict[str, Any]]:
        """Get duration metrics for a Lambda function.

        Args:
            function_name: Lambda function name
            lookback_minutes: How far back to look for metrics

        Returns:
            List of datapoints with timestamp and value
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=lookback_minutes)

            response = self.cloudwatch.get_metric_statistics(
                Namespace="AWS/Lambda",
                MetricName="Duration",
                Dimensions=[{"Name": "FunctionName", "Value": function_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=["Average", "Maximum"],
            )

            return sorted(response.get("Datapoints", []), key=lambda x: x["Timestamp"])
        except (ClientError, NoCredentialsError) as e:
            print(f"Error fetching Lambda duration metrics: {e}")
            return []

    def get_all_lambda_functions(self) -> List[str]:
        """Get all Lambda function names in the region.

        Returns:
            List of function names
        """
        try:
            functions = []
            paginator = self.lambda_client.get_paginator("list_functions")

            for page in paginator.paginate():
                for func in page.get("Functions", []):
                    functions.append(func["FunctionName"])

            return functions
        except (ClientError, NoCredentialsError) as e:
            print(f"Error fetching Lambda functions: {e}")
            return []

    def get_bedrock_invocation_metrics(
        self, model_id: str, lookback_minutes: int = 60
    ) -> List[Dict[str, Any]]:
        """Get invocation metrics for a Bedrock model.

        Args:
            model_id: Bedrock model ID
            lookback_minutes: How far back to look for metrics

        Returns:
            List of datapoints with timestamp and value
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=lookback_minutes)

            response = self.cloudwatch.get_metric_statistics(
                Namespace="AWS/Bedrock",
                MetricName="Invocations",
                Dimensions=[{"Name": "ModelId", "Value": model_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=["Sum"],
            )

            return sorted(response.get("Datapoints", []), key=lambda x: x["Timestamp"])
        except (ClientError, NoCredentialsError) as e:
            print(f"Error fetching Bedrock invocation metrics: {e}")
            return []

    def get_bedrock_input_tokens(
        self, model_id: str, lookback_minutes: int = 60
    ) -> List[Dict[str, Any]]:
        """Get input token count for a Bedrock model.

        Args:
            model_id: Bedrock model ID
            lookback_minutes: How far back to look for metrics

        Returns:
            List of datapoints with timestamp and value
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=lookback_minutes)

            response = self.cloudwatch.get_metric_statistics(
                Namespace="AWS/Bedrock",
                MetricName="InputTokenCount",
                Dimensions=[{"Name": "ModelId", "Value": model_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=["Sum"],
            )

            return sorted(response.get("Datapoints", []), key=lambda x: x["Timestamp"])
        except (ClientError, NoCredentialsError) as e:
            print(f"Error fetching Bedrock input tokens: {e}")
            return []

    def get_dynamodb_throttle_metrics(
        self, table_name: str, lookback_minutes: int = 60
    ) -> List[Dict[str, Any]]:
        """Get throttle events for a DynamoDB table.

        Args:
            table_name: DynamoDB table name
            lookback_minutes: How far back to look for metrics

        Returns:
            List of datapoints with timestamp and value
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=lookback_minutes)

            response = self.cloudwatch.get_metric_statistics(
                Namespace="AWS/DynamoDB",
                MetricName="UserErrors",
                Dimensions=[{"Name": "TableName", "Value": table_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=["Sum"],
            )

            return sorted(response.get("Datapoints", []), key=lambda x: x["Timestamp"])
        except (ClientError, NoCredentialsError) as e:
            print(f"Error fetching DynamoDB throttle metrics: {e}")
            return []
