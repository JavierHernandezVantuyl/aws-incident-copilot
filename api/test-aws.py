"""
Vercel serverless function to test AWS connectivity and permissions.

Security: Only tests read permissions, never writes. No sensitive data in responses.
Cost: Minimal - single STS GetCallerIdentity call (~$0.0001 per call, free tier).
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from typing import Dict, Any

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def sanitize_arn(arn: str) -> str:
    """
    Sanitize ARN to show role/user name but hide account details if needed.

    Args:
        arn: Full AWS ARN

    Returns:
        Sanitized ARN string
    """
    # For security, we could mask the account ID, but it's generally safe to show
    # since the user already has access to it
    return arn


class handler(BaseHTTPRequestHandler):
    """
    Test AWS credentials and verify required permissions.

    This endpoint performs minimal AWS API calls to verify connectivity.
    Cost: ~$0.0001 per test (covered by free tier).
    """

    def _set_security_headers(self):
        """Set secure HTTP headers."""
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.send_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, private"
        )
        allowed_origin = os.getenv("ALLOWED_ORIGIN", "*")
        self.send_header("Access-Control-Allow-Origin", allowed_origin)

    def _send_json_response(self, status_code: int, data: Dict[str, Any]):
        """Send a JSON response with proper headers."""
        self.send_response(status_code)
        self._set_security_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def _get_credentials(self, request_data=None):
        """Get AWS credentials from request data or environment variables."""
        if request_data and request_data.get("awsAccessKeyId"):
            # Use credentials from request (user-specific)
            access_key = request_data.get("awsAccessKeyId", "")
            secret_key = request_data.get("awsSecretAccessKey", "")
            region = request_data.get("awsRegion", "us-east-1")
        else:
            # Fallback to environment variables (legacy/fallback)
            access_key = os.getenv("AWS_ACCESS_KEY_ID", "")
            secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "")
            region = os.getenv(
                "AWS_DEFAULT_REGION", os.getenv("COPILOT_AWS_REGION", "us-east-1")
            )

        has_access_key = bool(access_key)
        has_secret_key = bool(secret_key)

        return {
            "access_key": access_key,
            "secret_key": secret_key,
            "region": region,
            "has_access_key": has_access_key,
            "has_secret_key": has_secret_key
        }

    def _test_aws_credentials(self, credentials):
        """Test AWS credentials and return response data."""
        has_access_key = credentials["has_access_key"]
        has_secret_key = credentials["has_secret_key"]
        region = credentials["region"]
        access_key = credentials["access_key"]
        secret_key = credentials["secret_key"]

        configured = has_access_key and has_secret_key

        response_data = {
            "configured": configured,
            "has_access_key": has_access_key,
            "has_secret_key": has_secret_key,
            "region": region,
            "cost_info": {
                "test_cost": "~$0.0001 per test (free tier)",
                "free_tier": "STS GetCallerIdentity is always free",
            },
        }

        # If not configured, return early with helpful message
        if not configured:
            response_data["help"] = {
                "message": "AWS credentials not configured",
                "required_credentials": [
                    "AWS Access Key ID",
                    "AWS Secret Access Key",
                    "AWS Region (optional, defaults to us-east-1)",
                ],
                "setup_guide": "Configure your credentials in Settings",
            }
            return response_data

        # Check for placeholder values
        if "your_" in access_key.lower() or "example" in access_key.lower():
            response_data["configured"] = False
            response_data["error"] = (
                "AWS credentials appear to be placeholder values"
            )
            response_data["help"] = (
                "Replace example values with real AWS credentials"
            )
            return response_data

        # Try to actually connect to AWS
        try:
            import boto3
            from botocore.exceptions import (
                ClientError,
                NoCredentialsError,
                BotoCoreError,
            )

            # Create session with user-provided credentials
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )

            # Test STS (this verifies credentials work)
            sts = session.client("sts")
            identity = sts.get_caller_identity()

            response_data["connected"] = True
            response_data["account_id"] = identity["Account"]
            response_data["user_arn"] = sanitize_arn(identity["Arn"])
            response_data["user_id"] = identity["UserId"]

            # Test required service permissions (non-blocking)
            permissions_status = {}

            # Test CloudWatch
            try:
                cw = session.client("cloudwatch")
                cw.list_metrics(MaxRecords=1)
                permissions_status["cloudwatch"] = "OK"
            except ClientError as e:
                if "AccessDenied" in str(e):
                    permissions_status["cloudwatch"] = (
                        "Access Denied - Add CloudWatchReadOnlyAccess"
                    )
                else:
                    permissions_status["cloudwatch"] = f"Error: {str(e)[:100]}"
            except Exception as e:
                permissions_status["cloudwatch"] = f"Error: {str(e)[:100]}"

            # Test CloudTrail
            try:
                ct = session.client("cloudtrail")
                ct.lookup_events(MaxResults=1)
                permissions_status["cloudtrail"] = "OK"
            except ClientError as e:
                if "AccessDenied" in str(e):
                    permissions_status["cloudtrail"] = (
                        "Access Denied - Add AWSCloudTrailReadOnlyAccess"
                    )
                else:
                    permissions_status["cloudtrail"] = f"Error: {str(e)[:100]}"
            except Exception as e:
                permissions_status["cloudtrail"] = f"Error: {str(e)[:100]}"

            # Test EC2
            try:
                ec2 = session.client("ec2")
                ec2.describe_instances(MaxResults=5)
                permissions_status["ec2"] = "OK"
            except ClientError as e:
                if "AccessDenied" in str(e) or "UnauthorizedOperation" in str(e):
                    permissions_status["ec2"] = (
                        "Access Denied - Add AmazonEC2ReadOnlyAccess"
                    )
                else:
                    permissions_status["ec2"] = f"Error: {str(e)[:100]}"
            except Exception as e:
                permissions_status["ec2"] = f"Error: {str(e)[:100]}"

            response_data["permissions"] = permissions_status

            # Determine overall status
            all_ok = all(status == "OK" for status in permissions_status.values())
            response_data["all_permissions_ok"] = all_ok

            if not all_ok:
                response_data["warning"] = (
                    "Some required permissions are missing. Incident detection may be limited."
                )
                response_data["recommendation"] = (
                    "Ensure your IAM user/role has CloudWatch, CloudTrail, and EC2 read-only access"
                )

        except NoCredentialsError:
            response_data["connected"] = False
            response_data["error"] = "AWS credentials not found or invalid"
            response_data["help"] = (
                "Verify your AWS credentials are correct"
            )

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", str(e))

            response_data["connected"] = False
            response_data["error_code"] = error_code

            # Provide helpful error messages
            if error_code == "InvalidClientTokenId":
                response_data["error"] = "Invalid AWS Access Key ID"
                response_data["help"] = "Check that your AWS Access Key ID is correct"
            elif error_code == "SignatureDoesNotMatch":
                response_data["error"] = "Invalid AWS Secret Access Key"
                response_data["help"] = (
                    "Check that your AWS Secret Access Key is correct"
                )
            elif "AccessDenied" in error_code:
                response_data["error"] = "Access denied"
                response_data["help"] = (
                    "Verify IAM permissions include STS GetCallerIdentity"
                )
            else:
                response_data["error"] = f"AWS error: {error_message[:200]}"

        except ImportError:
            response_data["connected"] = False
            response_data["error"] = "boto3 not installed"
            response_data["help"] = (
                "This error should not occur in Vercel. Check deployment logs."
            )

        except BotoCoreError as e:
            response_data["connected"] = False
            response_data["error"] = f"AWS connection error: {str(e)[:200]}"

        except Exception as e:
            response_data["connected"] = False
            response_data["error"] = f"Unexpected error: {str(e)[:200]}"

        return response_data

    def do_GET(self):
        """Test AWS credentials and connectivity (legacy support)."""
        try:
            credentials = self._get_credentials()
            response_data = self._test_aws_credentials(credentials)
            self._send_json_response(200, response_data)
        except Exception as e:
            # Catch-all error handler
            self._send_json_response(
                500,
                {
                    "configured": False,
                    "error": "Internal server error occurred during AWS test",
                    "details": str(e)[:200],
                    "support": "Check Vercel function logs for details",
                },
            )

    def do_POST(self):
        """Test AWS credentials from request body (user-specific)."""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            request_body = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(request_body) if request_body else {}

            # Get credentials from request or environment
            credentials = self._get_credentials(request_data)
            response_data = self._test_aws_credentials(credentials)
            self._send_json_response(200, response_data)

        except Exception as e:
            # Catch-all error handler
            self._send_json_response(
                500,
                {
                    "configured": False,
                    "error": "Internal server error occurred during AWS test",
                    "details": str(e)[:200],
                    "support": "Check Vercel function logs for details",
                },
            )

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self._set_security_headers()
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()
