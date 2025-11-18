"""
Vercel serverless function for scanning AWS resources for incidents.

Security: Read-only AWS operations, proper error handling, no sensitive data exposure.
Cost: Free tier friendly - uses CloudWatch/CloudTrail free tier operations.
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import traceback

# Add the parent directory to the path so we can import copilot modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Cost tracking constants
# AWS Free Tier: 1M CloudWatch API requests/month, 1 CloudTrail trail free
MAX_SCANS_PER_HOUR_FREE_TIER = 100  # Conservative limit to stay in free tier

try:
    from copilot.sources.cloudwatch import CloudWatchSource
    from copilot.sources.cloudtrail import CloudTrailSource
    from copilot.detectors import run_all_detectors
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    CloudWatchSource = None
    CloudTrailSource = None
    run_all_detectors = None
    DEPENDENCIES_AVAILABLE = False
    print(f"Warning: Dependencies not available: {e}")


def validate_aws_credentials() -> tuple[bool, str]:
    """
    Validate AWS credentials are present (not their correctness).

    Returns:
        (is_valid, error_message)
    """
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    if not access_key or not secret_key:
        return False, "AWS credentials not configured. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."

    # Basic validation - check they're not placeholder values
    if 'your_' in access_key.lower() or 'example' in access_key.lower():
        return False, "AWS credentials appear to be placeholder values. Please use real credentials."

    return True, ""


def get_cost_warning() -> Dict[str, Any]:
    """
    Generate cost awareness information for the response.

    Returns:
        Dictionary with cost information
    """
    return {
        "cost_info": {
            "estimated_cost_per_scan": "$0.001 - $0.01",
            "free_tier_eligible": True,
            "aws_services_used": [
                "CloudWatch (read-only)",
                "CloudTrail (read-only)",
                "EC2 describe (read-only)"
            ],
            "recommendation": "Limit scans to once per 5-15 minutes to stay within free tier limits",
            "note": "First 1M CloudWatch API requests per month are free. You are responsible for AWS costs."
        }
    }


def sanitize_error_message(error: Exception, include_details: bool = False) -> str:
    """
    Sanitize error messages to avoid exposing sensitive information.

    Args:
        error: The exception that occurred
        include_details: Whether to include detailed error info (for development)

    Returns:
        Safe error message string
    """
    error_str = str(error)

    # Remove potential sensitive data patterns
    sensitive_patterns = [
        'AKIA',  # AWS access key prefix
        'aws_secret',
        'password',
        'token',
    ]

    for pattern in sensitive_patterns:
        if pattern.lower() in error_str.lower():
            return "An error occurred. Please check your AWS credentials and permissions."

    # Common AWS errors - provide helpful messages
    if 'AuthFailure' in error_str or 'InvalidClientTokenId' in error_str:
        return "AWS authentication failed. Please verify your credentials are correct."

    if 'AccessDenied' in error_str or 'UnauthorizedOperation' in error_str:
        return "Access denied. Please ensure your IAM user has CloudWatch and CloudTrail read permissions."

    if 'RequestLimitExceeded' in error_str or 'Throttling' in error_str:
        return "AWS API rate limit exceeded. Please wait a few minutes before scanning again."

    if include_details:
        return error_str

    return "An unexpected error occurred while scanning AWS resources."


class handler(BaseHTTPRequestHandler):
    """
    Serverless function handler for AWS incident scanning.

    This function runs on Vercel's infrastructure and is billed per invocation.
    Vercel Free Tier: 100GB-hours of execution time per month.

    Security: All AWS operations are read-only. No data is stored on server.
    """

    def _set_security_headers(self):
        """Set secure HTTP headers."""
        self.send_header('Content-Type', 'application/json')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, private')
        # CORS - restrict in production to your domain
        allowed_origin = os.getenv('ALLOWED_ORIGIN', '*')
        self.send_header('Access-Control-Allow-Origin', allowed_origin)

    def _send_json_response(self, status_code: int, data: Dict[str, Any]):
        """Send a JSON response with proper headers."""
        self.send_response(status_code)
        self._set_security_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def do_GET(self):
        """Handle GET requests to scan for incidents."""
        try:
            # Validate dependencies are available
            if not DEPENDENCIES_AVAILABLE:
                self._send_json_response(200, {
                    'success': True,
                    'demo_mode': True,
                    'incidents': [
                        {
                            'id': 'demo-incident-1',
                            'title': 'Demo: High CPU Usage',
                            'severity': 'MEDIUM',
                            'resource': 'i-demo123456',
                            'description': 'This is a demo incident. Install dependencies to see real incidents.',
                            'detected_at': datetime.utcnow().isoformat()
                        }
                    ],
                    'warning': 'Running in demo mode. Python dependencies not available.',
                    **get_cost_warning()
                })
                return

            # Validate AWS credentials
            creds_valid, error_msg = validate_aws_credentials()
            if not creds_valid:
                self._send_json_response(200, {
                    'success': False,
                    'error': error_msg,
                    'incidents': [],
                    'help': 'Add AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY to your Vercel environment variables.'
                })
                return

            # Get region from environment or use default
            region = os.getenv('AWS_DEFAULT_REGION', os.getenv('COPILOT_AWS_REGION', 'us-east-1'))

            # Initialize AWS clients with timeout protection
            try:
                cloudwatch = CloudWatchSource(region=region)
                cloudtrail = CloudTrailSource(region=region)
            except Exception as e:
                error_message = sanitize_error_message(e)
                self._send_json_response(500, {
                    'success': False,
                    'error': error_message,
                    'incidents': [],
                    'troubleshooting': {
                        'check_credentials': 'Verify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are correct',
                        'check_permissions': 'Ensure IAM user has CloudWatch and CloudTrail read permissions',
                        'check_region': f'Verify region "{region}" is valid and accessible'
                    }
                })
                return

            # Run all detectors
            try:
                incidents = run_all_detectors(cloudwatch, cloudtrail)
            except Exception as e:
                error_message = sanitize_error_message(e)
                self._send_json_response(500, {
                    'success': False,
                    'error': f'Failed to scan AWS resources: {error_message}',
                    'incidents': [],
                    'region': region
                })
                return

            # Convert incidents to JSON-serializable format
            incidents_data = []
            for incident in incidents:
                try:
                    incidents_data.append({
                        'id': incident.id,
                        'title': incident.title,
                        'severity': incident.severity,
                        'resource': incident.resource,
                        'description': incident.description,
                        'detected_at': incident.detected_at.isoformat() if hasattr(incident.detected_at, 'isoformat') else str(incident.detected_at)
                    })
                except Exception as e:
                    # Log but don't fail the entire request for one bad incident
                    print(f"Warning: Failed to serialize incident: {e}")
                    continue

            # Send successful response
            response = {
                'success': True,
                'incidents': incidents_data,
                'incident_count': len(incidents_data),
                'region': region,
                'scanned_at': datetime.utcnow().isoformat(),
                **get_cost_warning()
            }

            self._send_json_response(200, response)

        except Exception as e:
            # Catch-all for unexpected errors
            # Log full traceback for debugging (visible in Vercel logs)
            print(f"Unexpected error in scan endpoint:")
            traceback.print_exc()

            # Send sanitized error to client
            error_message = sanitize_error_message(e, include_details=False)
            self._send_json_response(500, {
                'success': False,
                'error': error_message,
                'incidents': [],
                'support': 'Check Vercel function logs for detailed error information'
            })

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self._set_security_headers()
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '86400')  # 24 hours
        self.end_headers()
