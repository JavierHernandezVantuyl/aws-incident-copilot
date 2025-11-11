"""Incident detection system."""

from typing import List
from copilot.incidents import Incident
from copilot.sources.cloudwatch import CloudWatchSource
from copilot.sources.cloudtrail import CloudTrailSource
from copilot.config import settings


class IncidentDetector:
    """Base class for incident detectors."""

    def __init__(self, cloudwatch: CloudWatchSource, cloudtrail: CloudTrailSource):
        """Initialize detector with data sources.

        Args:
            cloudwatch: CloudWatch data source
            cloudtrail: CloudTrail data source
        """
        self.cloudwatch = cloudwatch
        self.cloudtrail = cloudtrail
        self.settings = settings

    def detect(self) -> List[Incident]:
        """Detect incidents. Must be implemented by subclasses.

        Returns:
            List of detected incidents
        """
        raise NotImplementedError


class EC2CPUSpikeDetector(IncidentDetector):
    """Detector for EC2 CPU spikes."""

    def detect(self) -> List[Incident]:
        """Detect EC2 instances with sustained high CPU usage.

        Returns:
            List of EC2 CPU spike incidents
        """
        incidents = []
        instances = self.cloudwatch.get_all_ec2_instances()

        for instance_id in instances:
            metrics = self.cloudwatch.get_ec2_cpu_metrics(
                instance_id=instance_id, lookback_minutes=self.settings.lookback_minutes
            )

            if not metrics:
                continue

            # Check if CPU has been consistently high
            high_cpu_count = sum(
                1
                for m in metrics
                if m.get("Maximum", 0) > self.settings.ec2_cpu_threshold
            )

            # If more than N datapoints show high CPU (each datapoint is 5 min)
            required_datapoints = self.settings.ec2_cpu_duration_minutes // 5
            if high_cpu_count >= required_datapoints:
                max_cpu = max(m.get("Maximum", 0) for m in metrics)
                avg_cpu = sum(m.get("Average", 0) for m in metrics) / len(metrics)

                incidents.append(
                    Incident(
                        id=f"ec2-cpu-spike-{instance_id}",
                        title=f"EC2 CPU Spike on {instance_id}",
                        severity="HIGH" if max_cpu > 98 else "MEDIUM",
                        resource=instance_id,
                        description=(
                            f"Instance {instance_id} has sustained CPU usage above "
                            f"{self.settings.ec2_cpu_threshold}% for over "
                            f"{self.settings.ec2_cpu_duration_minutes} minutes. "
                            f"Max CPU: {max_cpu:.1f}%, Avg CPU: {avg_cpu:.1f}%"
                        ),
                        suggested_fix=(
                            "1. Check running processes with 'top' or 'htop'\n"
                            "2. Consider right-sizing instance type\n"
                            "3. Review application logs for performance issues\n"
                            "4. Set up Auto Scaling if load is variable"
                        ),
                        evidence_files=[
                            f"cloudwatch-metrics-{instance_id}.json",
                            f"ec2-instance-details-{instance_id}.json",
                        ],
                    )
                )

        return incidents


class LambdaErrorDetector(IncidentDetector):
    """Detector for Lambda function errors."""

    def detect(self) -> List[Incident]:
        """Detect Lambda functions with high error rates.

        Returns:
            List of Lambda error incidents
        """
        incidents = []
        functions = self.cloudwatch.get_all_lambda_functions()

        for function_name in functions:
            error_metrics = self.cloudwatch.get_lambda_error_metrics(
                function_name=function_name,
                lookback_minutes=self.settings.lookback_minutes,
            )

            if not error_metrics:
                continue

            total_errors = sum(m.get("Sum", 0) for m in error_metrics)

            if total_errors >= self.settings.lambda_error_threshold:
                # Also check duration for timeouts
                duration_metrics = self.cloudwatch.get_lambda_duration_metrics(
                    function_name=function_name,
                    lookback_minutes=self.settings.lookback_minutes,
                )

                max_duration = 0
                if duration_metrics:
                    max_duration = max(m.get("Maximum", 0) for m in duration_metrics)

                timeout_warning = ""
                severity = "MEDIUM"
                if max_duration > self.settings.lambda_timeout_threshold_ms:
                    timeout_warning = f" Function is also experiencing long execution times (max: {max_duration:.0f}ms)."
                    severity = "HIGH"

                incidents.append(
                    Incident(
                        id=f"lambda-errors-{function_name}",
                        title=f"Lambda Errors: {function_name}",
                        severity=severity,
                        resource=f"function:{function_name}",
                        description=(
                            f"Function '{function_name}' has {total_errors:.0f} errors "
                            f"in the last {self.settings.lookback_minutes} minutes."
                            f"{timeout_warning}"
                        ),
                        suggested_fix=(
                            "1. Check CloudWatch Logs for error stack traces\n"
                            "2. Review recent code deployments\n"
                            "3. Verify function configuration (memory, timeout)\n"
                            "4. Check for dependency or permission issues"
                        ),
                        evidence_files=[
                            f"lambda-error-metrics-{function_name}.json",
                            f"lambda-logs-{function_name}.txt",
                        ],
                    )
                )

        return incidents


class BedrockTokenUsageDetector(IncidentDetector):
    """Detector for excessive Bedrock token usage."""

    def detect(self) -> List[Incident]:
        """Detect Bedrock models with excessive token usage.

        Returns:
            List of Bedrock token usage incidents
        """
        incidents = []
        # Common Bedrock model IDs - in production, you'd list actual models in use
        model_ids = [
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-v2:1",
            "amazon.titan-text-express-v1",
        ]

        for model_id in model_ids:
            token_metrics = self.cloudwatch.get_bedrock_input_tokens(
                model_id=model_id,
                lookback_minutes=self.settings.bedrock_token_window_minutes,
            )

            if not token_metrics:
                continue

            total_tokens = sum(m.get("Sum", 0) for m in token_metrics)

            if total_tokens >= self.settings.bedrock_token_threshold:
                invocation_metrics = self.cloudwatch.get_bedrock_invocation_metrics(
                    model_id=model_id,
                    lookback_minutes=self.settings.bedrock_token_window_minutes,
                )

                total_invocations = sum(m.get("Sum", 0) for m in invocation_metrics)
                avg_tokens_per_call = (
                    total_tokens / total_invocations if total_invocations > 0 else 0
                )

                incidents.append(
                    Incident(
                        id=f"bedrock-token-usage-{model_id.replace(':', '-').replace('.', '-')}",
                        title=f"Excessive Bedrock Token Usage: {model_id}",
                        severity="HIGH",
                        resource=f"model:{model_id}",
                        description=(
                            f"Model '{model_id}' has consumed {total_tokens:.0f} tokens "
                            f"in the last {self.settings.bedrock_token_window_minutes} minutes. "
                            f"Total invocations: {total_invocations:.0f}, "
                            f"Avg tokens/call: {avg_tokens_per_call:.0f}"
                        ),
                        suggested_fix=(
                            "1. Review application logic for unnecessary API calls\n"
                            "2. Check for retry loops or error conditions\n"
                            "3. Consider implementing caching for common requests\n"
                            "4. Review prompt engineering to reduce token usage\n"
                            "5. Set up CloudWatch alarms for token thresholds"
                        ),
                        evidence_files=[
                            f"bedrock-token-metrics-{model_id.replace(':', '-')}.json",
                            f"bedrock-invocation-metrics-{model_id.replace(':', '-')}.json",
                        ],
                    )
                )

        return incidents


class S3AccessDeniedDetector(IncidentDetector):
    """Detector for S3 access denied errors."""

    def detect(self) -> List[Incident]:
        """Detect S3 access denied errors from CloudTrail.

        Returns:
            List of S3 access denied incidents
        """
        incidents = []
        access_denied_events = self.cloudtrail.get_s3_access_denied_events(
            lookback_minutes=self.settings.lookback_minutes
        )

        # Group by resource (bucket/object)
        resource_errors = {}
        for event in access_denied_events:
            resources = event.get("resources", [])
            for resource in resources:
                resource_name = resource.get("ResourceName", "unknown")
                if resource_name not in resource_errors:
                    resource_errors[resource_name] = []
                resource_errors[resource_name].append(event)

        for resource_name, events in resource_errors.items():
            if len(events) >= 1:  # At least one access denied event
                usernames = set(e.get("username", "unknown") for e in events)

                incidents.append(
                    Incident(
                        id=f"s3-access-denied-{resource_name.replace(':', '-').replace('/', '-')[:50]}",
                        title=f"S3 Access Denied: {resource_name}",
                        severity="HIGH",
                        resource=resource_name,
                        description=(
                            f"S3 resource '{resource_name}' has {len(events)} access denied "
                            f"error(s) in the last {self.settings.lookback_minutes} minutes. "
                            f"Affected users: {', '.join(usernames)}"
                        ),
                        suggested_fix=(
                            "1. Review S3 bucket policy for required permissions\n"
                            "2. Check IAM role/user permissions for s3:GetObject\n"
                            "3. Verify bucket ACLs and Block Public Access settings\n"
                            "4. Ensure correct AWS account is being used"
                        ),
                        evidence_files=[
                            f"cloudtrail-s3-access-denied-{resource_name.replace(':', '-')[:30]}.json",
                            f"s3-bucket-policy-{resource_name.split(':::')[-1].split('/')[0]}.json",
                        ],
                    )
                )

        return incidents


class DynamoDBThrottleDetector(IncidentDetector):
    """Detector for DynamoDB throttling events."""

    def detect(self) -> List[Incident]:
        """Detect DynamoDB tables experiencing throttling.

        Returns:
            List of DynamoDB throttling incidents
        """
        incidents = []
        # In production, you'd get list of tables from DynamoDB API
        # For now, we'll skip this as it requires additional implementation
        return incidents


def run_all_detectors(
    cloudwatch: CloudWatchSource, cloudtrail: CloudTrailSource
) -> List[Incident]:
    """Run all incident detectors.

    Args:
        cloudwatch: CloudWatch data source
        cloudtrail: CloudTrail data source

    Returns:
        List of all detected incidents
    """
    detectors = [
        EC2CPUSpikeDetector(cloudwatch, cloudtrail),
        LambdaErrorDetector(cloudwatch, cloudtrail),
        BedrockTokenUsageDetector(cloudwatch, cloudtrail),
        S3AccessDeniedDetector(cloudwatch, cloudtrail),
        DynamoDBThrottleDetector(cloudwatch, cloudtrail),
    ]

    all_incidents = []
    for detector in detectors:
        try:
            incidents = detector.detect()
            all_incidents.extend(incidents)
        except Exception as e:
            print(f"Error in {detector.__class__.__name__}: {e}")

    return all_incidents
