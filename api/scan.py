"""
Vercel serverless function for scanning AWS resources for incidents.
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import copilot modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from copilot.sources.cloudwatch import CloudWatchSource
    from copilot.sources.cloudtrail import CloudTrailSource
    from copilot.detectors import run_all_detectors
except ImportError:
    # Fallback for when dependencies aren't available
    CloudWatchSource = None
    CloudTrailSource = None
    run_all_detectors = None


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests to scan for incidents."""
        try:
            # Check if AWS is configured
            if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'AWS credentials not configured',
                    'incidents': []
                }).encode())
                return

            # Get region from environment or use default
            region = os.getenv('AWS_DEFAULT_REGION', os.getenv('COPILOT_AWS_REGION', 'us-east-1'))

            # Initialize AWS clients
            if CloudWatchSource is None or CloudTrailSource is None:
                # Return mock data if dependencies aren't available
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'incidents': [
                        {
                            'id': 'demo-incident-1',
                            'title': 'Demo: High CPU Usage',
                            'severity': 'MEDIUM',
                            'resource': 'i-demo123456',
                            'description': 'This is a demo incident. Configure AWS credentials to see real incidents.',
                            'detected_at': datetime.utcnow().isoformat()
                        }
                    ],
                    'region': region
                }).encode())
                return

            cloudwatch = CloudWatchSource(region=region)
            cloudtrail = CloudTrailSource(region=region)

            # Run all detectors
            incidents = run_all_detectors(cloudwatch, cloudtrail)

            # Convert incidents to JSON-serializable format
            incidents_data = []
            for incident in incidents:
                incidents_data.append({
                    'id': incident.id,
                    'title': incident.title,
                    'severity': incident.severity,
                    'resource': incident.resource,
                    'description': incident.description,
                    'detected_at': incident.detected_at.isoformat() if hasattr(incident.detected_at, 'isoformat') else str(incident.detected_at)
                })

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = {
                'success': True,
                'incidents': incidents_data,
                'region': region,
                'scanned_at': datetime.utcnow().isoformat()
            }

            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            # Handle errors gracefully
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            error_response = {
                'success': False,
                'error': str(e),
                'incidents': []
            }

            self.wfile.write(json.dumps(error_response).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
