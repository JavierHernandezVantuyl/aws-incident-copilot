"""CloudTrail data source for event analysis."""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class CloudTrailSource:
    """CloudTrail events data source."""

    def __init__(self, region: str = "us-east-1", profile: Optional[str] = None):
        """Initialize CloudTrail client.

        Args:
            region: AWS region to connect to
            profile: AWS profile name (optional)
        """
        session_kwargs = {"region_name": region}
        if profile:
            session_kwargs["profile_name"] = profile

        session = boto3.Session(**session_kwargs)
        self.cloudtrail = session.client("cloudtrail")
        self.region = region

    def lookup_events(
        self,
        lookback_minutes: int = 60,
        event_name: Optional[str] = None,
        resource_type: Optional[str] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """Look up CloudTrail events.

        Args:
            lookback_minutes: How far back to look for events
            event_name: Filter by event name (e.g., 'GetObject')
            resource_type: Filter by resource type (e.g., 'AWS::S3::Bucket')
            max_results: Maximum number of events to return

        Returns:
            List of CloudTrail events
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=lookback_minutes)

            lookup_attributes = []
            if event_name:
                lookup_attributes.append(
                    {"AttributeKey": "EventName", "AttributeValue": event_name}
                )
            if resource_type:
                lookup_attributes.append(
                    {"AttributeKey": "ResourceType", "AttributeValue": resource_type}
                )

            kwargs = {
                "StartTime": start_time,
                "EndTime": end_time,
                "MaxResults": max_results,
            }
            if lookup_attributes:
                kwargs["LookupAttributes"] = lookup_attributes

            response = self.cloudtrail.lookup_events(**kwargs)
            return response.get("Events", [])
        except (ClientError, NoCredentialsError) as e:
            print(f"Error looking up CloudTrail events: {e}")
            return []

    def get_s3_access_denied_events(
        self, lookback_minutes: int = 60
    ) -> List[Dict[str, Any]]:
        """Get S3 access denied events from CloudTrail.

        Args:
            lookback_minutes: How far back to look for events

        Returns:
            List of S3 access denied events with details
        """
        events = self.lookup_events(
            lookback_minutes=lookback_minutes, event_name="GetObject", max_results=100
        )

        access_denied_events = []
        for event in events:
            # Check if the event has an error
            cloud_trail_event = event.get("CloudTrailEvent", "{}")
            import json

            try:
                event_data = json.loads(cloud_trail_event)
                error_code = event_data.get("errorCode", "")
                if error_code == "AccessDenied":
                    access_denied_events.append(
                        {
                            "timestamp": event.get("EventTime"),
                            "event_name": event.get("EventName"),
                            "username": event.get("Username"),
                            "resources": event.get("Resources", []),
                            "error_code": error_code,
                            "error_message": event_data.get("errorMessage", ""),
                            "event_data": event_data,
                        }
                    )
            except json.JSONDecodeError:
                continue

        return access_denied_events

    def get_failed_api_calls(
        self, lookback_minutes: int = 60, service: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get failed API calls from CloudTrail.

        Args:
            lookback_minutes: How far back to look for events
            service: Filter by AWS service (e.g., 's3', 'lambda')

        Returns:
            List of failed API calls with details
        """
        events = self.lookup_events(lookback_minutes=lookback_minutes, max_results=100)

        failed_calls = []
        for event in events:
            cloud_trail_event = event.get("CloudTrailEvent", "{}")
            import json

            try:
                event_data = json.loads(cloud_trail_event)
                error_code = event_data.get("errorCode", "")

                # Filter by service if specified
                event_source = event_data.get("eventSource", "")
                if service and not event_source.startswith(service):
                    continue

                if error_code:  # Any error code indicates a failure
                    failed_calls.append(
                        {
                            "timestamp": event.get("EventTime"),
                            "event_name": event.get("EventName"),
                            "event_source": event_source,
                            "username": event.get("Username"),
                            "resources": event.get("Resources", []),
                            "error_code": error_code,
                            "error_message": event_data.get("errorMessage", ""),
                            "source_ip": event_data.get("sourceIPAddress", ""),
                            "user_agent": event_data.get("userAgent", ""),
                        }
                    )
            except json.JSONDecodeError:
                continue

        return failed_calls

    def get_iam_permission_errors(
        self, lookback_minutes: int = 60
    ) -> List[Dict[str, Any]]:
        """Get IAM permission-related errors from CloudTrail.

        Args:
            lookback_minutes: How far back to look for events

        Returns:
            List of IAM permission errors
        """
        events = self.lookup_events(lookback_minutes=lookback_minutes, max_results=100)

        permission_errors = []
        error_codes = ["AccessDenied", "UnauthorizedOperation", "AccessDeniedException"]

        for event in events:
            cloud_trail_event = event.get("CloudTrailEvent", "{}")
            import json

            try:
                event_data = json.loads(cloud_trail_event)
                error_code = event_data.get("errorCode", "")

                if error_code in error_codes:
                    permission_errors.append(
                        {
                            "timestamp": event.get("EventTime"),
                            "event_name": event.get("EventName"),
                            "event_source": event_data.get("eventSource", ""),
                            "username": event.get("Username"),
                            "resources": event.get("Resources", []),
                            "error_code": error_code,
                            "error_message": event_data.get("errorMessage", ""),
                            "request_parameters": event_data.get(
                                "requestParameters", {}
                            ),
                        }
                    )
            except json.JSONDecodeError:
                continue

        return permission_errors
