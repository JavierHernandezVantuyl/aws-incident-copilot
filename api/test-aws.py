"""
Vercel serverless function to test AWS connectivity.
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Test AWS credentials and connectivity."""
        try:
            # Check if basic AWS credentials are present
            has_access_key = bool(os.getenv('AWS_ACCESS_KEY_ID'))
            has_secret_key = bool(os.getenv('AWS_SECRET_ACCESS_KEY'))

            configured = has_access_key and has_secret_key

            response_data = {
                'configured': configured,
                'has_access_key': has_access_key,
                'has_secret_key': has_secret_key,
                'region': os.getenv('AWS_DEFAULT_REGION', os.getenv('COPILOT_AWS_REGION', 'us-east-1'))
            }

            # If configured, try to actually connect to AWS
            if configured:
                try:
                    import boto3
                    from botocore.exceptions import ClientError, NoCredentialsError

                    region = response_data['region']
                    session = boto3.Session(region_name=region)

                    # Test STS (this verifies credentials)
                    sts = session.client('sts')
                    identity = sts.get_caller_identity()

                    response_data['connected'] = True
                    response_data['account_id'] = identity['Account']
                    response_data['user_arn'] = identity['Arn']

                except (ClientError, NoCredentialsError) as e:
                    response_data['connected'] = False
                    response_data['error'] = str(e)
                except ImportError:
                    response_data['connected'] = False
                    response_data['error'] = 'boto3 not installed'

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            error_response = {
                'configured': False,
                'error': str(e)
            }

            self.wfile.write(json.dumps(error_response).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
