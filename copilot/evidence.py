"""Evidence collection and packaging system."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict
from copilot.incidents import Incident
from copilot.sources.cloudwatch import CloudWatchSource
from copilot.sources.cloudtrail import CloudTrailSource
from copilot.config import settings


class EvidenceCollector:
    """Collects and packages evidence for incidents."""

    def __init__(
        self,
        cloudwatch: CloudWatchSource,
        cloudtrail: CloudTrailSource,
        output_dir: str = None,
    ):
        """Initialize evidence collector.

        Args:
            cloudwatch: CloudWatch data source
            cloudtrail: CloudTrail data source
            output_dir: Directory to save evidence files
        """
        self.cloudwatch = cloudwatch
        self.cloudtrail = cloudtrail
        self.output_dir = output_dir or settings.evidence_output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def collect_for_incident(self, incident: Incident) -> Dict[str, str]:
        """Collect evidence for a specific incident.

        Args:
            incident: The incident to collect evidence for

        Returns:
            Dictionary mapping evidence file names to their paths
        """
        evidence_paths = {}
        incident_dir = Path(self.output_dir) / incident.id
        incident_dir.mkdir(parents=True, exist_ok=True)

        # Determine incident type and collect appropriate evidence
        if "ec2-cpu-spike" in incident.id:
            evidence_paths.update(self._collect_ec2_evidence(incident, incident_dir))
        elif "lambda-errors" in incident.id:
            evidence_paths.update(self._collect_lambda_evidence(incident, incident_dir))
        elif "bedrock-token-usage" in incident.id:
            evidence_paths.update(
                self._collect_bedrock_evidence(incident, incident_dir)
            )
        elif "s3-access-denied" in incident.id:
            evidence_paths.update(self._collect_s3_evidence(incident, incident_dir))

        # Save incident details
        incident_file = incident_dir / "incident.json"
        with open(incident_file, "w") as f:
            json.dump(incident.model_dump(), f, indent=2, default=str)
        evidence_paths["incident.json"] = str(incident_file)

        return evidence_paths

    def _collect_ec2_evidence(
        self, incident: Incident, output_dir: Path
    ) -> Dict[str, str]:
        """Collect EC2-specific evidence.

        Args:
            incident: The incident
            output_dir: Directory to save evidence

        Returns:
            Dictionary of evidence file paths
        """
        evidence = {}
        instance_id = incident.resource

        # Collect CPU metrics
        metrics = self.cloudwatch.get_ec2_cpu_metrics(
            instance_id=instance_id, lookback_minutes=settings.lookback_minutes
        )

        metrics_file = output_dir / f"cloudwatch-metrics-{instance_id}.json"
        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=2, default=str)
        evidence[f"cloudwatch-metrics-{instance_id}.json"] = str(metrics_file)

        return evidence

    def _collect_lambda_evidence(
        self, incident: Incident, output_dir: Path
    ) -> Dict[str, str]:
        """Collect Lambda-specific evidence.

        Args:
            incident: The incident
            output_dir: Directory to save evidence

        Returns:
            Dictionary of evidence file paths
        """
        evidence = {}
        function_name = incident.resource.replace("function:", "")

        # Collect error metrics
        error_metrics = self.cloudwatch.get_lambda_error_metrics(
            function_name=function_name, lookback_minutes=settings.lookback_minutes
        )

        metrics_file = output_dir / f"lambda-error-metrics-{function_name}.json"
        with open(metrics_file, "w") as f:
            json.dump(error_metrics, f, indent=2, default=str)
        evidence[f"lambda-error-metrics-{function_name}.json"] = str(metrics_file)

        # Collect duration metrics
        duration_metrics = self.cloudwatch.get_lambda_duration_metrics(
            function_name=function_name, lookback_minutes=settings.lookback_minutes
        )

        duration_file = output_dir / f"lambda-duration-metrics-{function_name}.json"
        with open(duration_file, "w") as f:
            json.dump(duration_metrics, f, indent=2, default=str)
        evidence[f"lambda-duration-metrics-{function_name}.json"] = str(duration_file)

        return evidence

    def _collect_bedrock_evidence(
        self, incident: Incident, output_dir: Path
    ) -> Dict[str, str]:
        """Collect Bedrock-specific evidence.

        Args:
            incident: The incident
            output_dir: Directory to save evidence

        Returns:
            Dictionary of evidence file paths
        """
        evidence = {}
        model_id = incident.resource.replace("model:", "")

        # Collect token metrics
        token_metrics = self.cloudwatch.get_bedrock_input_tokens(
            model_id=model_id, lookback_minutes=settings.bedrock_token_window_minutes
        )

        safe_model_id = model_id.replace(":", "-").replace(".", "-")
        metrics_file = output_dir / f"bedrock-token-metrics-{safe_model_id}.json"
        with open(metrics_file, "w") as f:
            json.dump(token_metrics, f, indent=2, default=str)
        evidence[f"bedrock-token-metrics-{safe_model_id}.json"] = str(metrics_file)

        # Collect invocation metrics
        invocation_metrics = self.cloudwatch.get_bedrock_invocation_metrics(
            model_id=model_id, lookback_minutes=settings.bedrock_token_window_minutes
        )

        invocation_file = (
            output_dir / f"bedrock-invocation-metrics-{safe_model_id}.json"
        )
        with open(invocation_file, "w") as f:
            json.dump(invocation_metrics, f, indent=2, default=str)
        evidence[f"bedrock-invocation-metrics-{safe_model_id}.json"] = str(
            invocation_file
        )

        return evidence

    def _collect_s3_evidence(
        self, incident: Incident, output_dir: Path
    ) -> Dict[str, str]:
        """Collect S3-specific evidence.

        Args:
            incident: The incident
            output_dir: Directory to save evidence

        Returns:
            Dictionary of evidence file paths
        """
        evidence = {}

        # Collect CloudTrail events
        access_denied_events = self.cloudtrail.get_s3_access_denied_events(
            lookback_minutes=settings.lookback_minutes
        )

        # Filter events for this specific resource
        resource_events = [
            e
            for e in access_denied_events
            if any(
                r.get("ResourceName") == incident.resource
                for r in e.get("resources", [])
            )
        ]

        safe_resource_name = incident.resource.replace(":", "-").replace("/", "-")[:30]
        events_file = (
            output_dir / f"cloudtrail-s3-access-denied-{safe_resource_name}.json"
        )
        with open(events_file, "w") as f:
            json.dump(resource_events, f, indent=2, default=str)
        evidence[f"cloudtrail-s3-access-denied-{safe_resource_name}.json"] = str(
            events_file
        )

        return evidence

    def package_evidence(self, incident: Incident) -> str:
        """Package all evidence for an incident into a tarball.

        Args:
            incident: The incident to package evidence for

        Returns:
            Path to the created tarball
        """
        import tarfile

        # Collect evidence first
        self.collect_for_incident(incident)

        # Create tarball
        incident_dir = Path(self.output_dir) / incident.id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tarball_name = f"{incident.id}_{timestamp}.tar.gz"
        tarball_path = Path(self.output_dir) / tarball_name

        with tarfile.open(tarball_path, "w:gz") as tar:
            tar.add(incident_dir, arcname=incident.id)

        return str(tarball_path)

    def cleanup_old_evidence(self):
        """Remove evidence files older than max_evidence_age_days."""
        max_age_seconds = settings.max_evidence_age_days * 24 * 60 * 60
        current_time = datetime.now().timestamp()

        evidence_dir = Path(self.output_dir)
        if not evidence_dir.exists():
            return

        for item in evidence_dir.iterdir():
            if item.is_dir():
                # Check directory age
                if current_time - item.stat().st_mtime > max_age_seconds:
                    import shutil

                    shutil.rmtree(item)
            elif item.suffix == ".gz":
                # Check tarball age
                if current_time - item.stat().st_mtime > max_age_seconds:
                    item.unlink()
