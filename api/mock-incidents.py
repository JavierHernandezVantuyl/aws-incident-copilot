"""
Vercel serverless function to get mock incidents for testing and demonstration.

Security: Returns static mock data only, no AWS API calls.
Cost: Free - no external API calls, minimal compute time.
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from copilot.sources import mock as mock_source

    MOCK_SOURCE_AVAILABLE = True
except ImportError:
    MOCK_SOURCE_AVAILABLE = False


def generate_fallback_mock_incidents() -> List[Dict[str, Any]]:
    """
    Generate realistic mock incidents for demonstration.

    Returns:
        List of incident dictionaries
    """
    now = datetime.utcnow()
    return [
        {
            "id": "demo-ec2-cpu-spike-001",
            "title": "EC2 CPU Spike Detected",
            "severity": "HIGH",
            "resource": "i-1234567890abcdef0",
            "description": "CPU usage exceeded 95% for more than 10 minutes. This may indicate a need for instance resizing or application optimization.",
            "detected_at": (now - timedelta(minutes=5)).isoformat() + "Z",
            "recommendations": [
                "Check application logs for unusual activity",
                "Consider scaling up instance size",
                "Review recent deployments",
            ],
        },
        {
            "id": "demo-lambda-errors-002",
            "title": "Lambda Function Errors",
            "severity": "MEDIUM",
            "resource": "my-lambda-function",
            "description": "Detected 8 invocation errors in the last hour. Common causes include timeout issues, permission errors, or runtime exceptions.",
            "detected_at": (now - timedelta(minutes=15)).isoformat() + "Z",
            "recommendations": [
                "Review CloudWatch logs for error details",
                "Check IAM role permissions",
                "Verify function timeout configuration",
            ],
        },
        {
            "id": "demo-s3-access-denied-003",
            "title": "S3 Access Denied Errors",
            "severity": "CRITICAL",
            "resource": "my-application-bucket",
            "description": "Multiple AccessDenied errors detected when attempting to access S3 bucket. This indicates a permissions issue that may be blocking critical functionality.",
            "detected_at": (now - timedelta(minutes=30)).isoformat() + "Z",
            "recommendations": [
                "Review bucket policy and IAM permissions",
                "Check if bucket encryption settings changed",
                "Verify requester identity in CloudTrail",
            ],
        },
        {
            "id": "demo-bedrock-tokens-004",
            "title": "Bedrock Token Usage Spike",
            "severity": "HIGH",
            "resource": "anthropic.claude-v2",
            "description": "Token usage exceeded 100,000 tokens in the last hour. This may result in higher than expected AWS bills.",
            "detected_at": (now - timedelta(minutes=45)).isoformat() + "Z",
            "cost_impact": "Estimated $2-5 per hour at current rate",
            "recommendations": [
                "Review application for token optimization",
                "Check for unexpected loops or retries",
                "Consider implementing rate limiting",
            ],
        },
    ]


class handler(BaseHTTPRequestHandler):
    """
    Return mock incident data for demonstration and testing.

    This endpoint is useful for:
    - Testing the UI without AWS credentials
    - Demonstrating incident types
    - Development and testing

    Cost: Free - no AWS API calls, minimal compute
    """

    def _set_security_headers(self):
        """Set secure HTTP headers."""
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.send_header("Cache-Control", "public, max-age=300")  # Cache for 5 minutes
        allowed_origin = os.getenv("ALLOWED_ORIGIN", "*")
        self.send_header("Access-Control-Allow-Origin", allowed_origin)

    def _send_json_response(self, status_code: int, data: Dict[str, Any]):
        """Send a JSON response with proper headers."""
        self.send_response(status_code)
        self._set_security_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        """Get mock incidents for demonstration."""
        try:
            incidents_data = []

            if MOCK_SOURCE_AVAILABLE:
                # Use actual mock source from codebase
                try:
                    incidents = mock_source.load_all()
                    for incident in incidents:
                        incident_dict = {
                            "id": incident.id,
                            "title": incident.title,
                            "severity": incident.severity,
                            "resource": incident.resource,
                            "description": incident.description,
                            "detected_at": (
                                incident.detected_at.isoformat()
                                if hasattr(incident.detected_at, "isoformat")
                                else str(incident.detected_at)
                            ),
                        }

                        # Add optional fields if available
                        if hasattr(incident, "recommendations"):
                            incident_dict["recommendations"] = incident.recommendations
                        if hasattr(incident, "cost_impact"):
                            incident_dict["cost_impact"] = incident.cost_impact

                        incidents_data.append(incident_dict)
                except Exception as e:
                    print(f"Warning: Failed to load mock incidents from source: {e}")
                    incidents_data = generate_fallback_mock_incidents()
            else:
                # Use fallback mock data
                incidents_data = generate_fallback_mock_incidents()

            response = {
                "success": True,
                "incidents": incidents_data,
                "incident_count": len(incidents_data),
                "is_mock": True,
                "demo_mode": True,
                "message": "These are demonstration incidents. Connect AWS credentials to see real incidents.",
                "cost_info": {
                    "endpoint_cost": "Free - no AWS API calls",
                    "vercel_cost": "Minimal - cached response",
                    "note": "Mock data is useful for testing without incurring AWS costs",
                },
                "generated_at": datetime.utcnow().isoformat() + "Z",
            }

            self._send_json_response(200, response)

        except Exception as e:
            # Catch-all error handler
            print(f"Error in mock-incidents endpoint: {e}")
            self._send_json_response(
                500,
                {
                    "success": False,
                    "error": "Failed to generate mock incidents",
                    "details": str(e)[:200],
                    "is_mock": True,
                },
            )

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self._set_security_headers()
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()
