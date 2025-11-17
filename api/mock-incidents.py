"""
Vercel serverless function to get mock incidents for testing.
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from copilot.sources import mock as mock_source
except ImportError:
    mock_source = None


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Get mock incidents for demonstration."""
        try:
            if mock_source is None:
                # Fallback mock data
                incidents_data = [
                    {
                        'id': 'demo-ec2-cpu-spike',
                        'title': 'EC2 CPU Spike Detected',
                        'severity': 'HIGH',
                        'resource': 'i-1234567890abcdef0',
                        'description': 'CPU usage exceeded 95% for more than 10 minutes',
                        'detected_at': '2024-01-15T10:30:00Z'
                    },
                    {
                        'id': 'demo-lambda-errors',
                        'title': 'Lambda Function Errors',
                        'severity': 'MEDIUM',
                        'resource': 'my-lambda-function',
                        'description': 'Multiple invocation errors detected',
                        'detected_at': '2024-01-15T10:25:00Z'
                    }
                ]
            else:
                # Use actual mock source
                incidents = mock_source.load_all()
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

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = {
                'success': True,
                'incidents': incidents_data,
                'is_mock': True
            }

            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
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
