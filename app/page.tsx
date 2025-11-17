'use client'

import { useState, useEffect } from 'react'
import {
  Activity,
  AlertTriangle,
  CheckCircle,
  XCircle,
  RefreshCw,
  Settings,
  Play,
  Pause,
  CloudIcon,
  Shield,
  Zap
} from 'lucide-react'

interface Incident {
  id: string
  title: string
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  resource: string
  description: string
  detected_at: string
}

export default function Home() {
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(false)
  const [monitoring, setMonitoring] = useState(false)
  const [lastScan, setLastScan] = useState<Date | null>(null)
  const [awsConfigured, setAwsConfigured] = useState(false)

  // Check AWS configuration on mount
  useEffect(() => {
    checkAwsConfig()
  }, [])

  const checkAwsConfig = async () => {
    try {
      const response = await fetch('/api/test-aws')
      const data = await response.json()
      setAwsConfigured(data.configured)
    } catch (error) {
      console.error('Failed to check AWS config:', error)
      setAwsConfigured(false)
    }
  }

  const scanForIncidents = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/scan')
      const data = await response.json()
      setIncidents(data.incidents || [])
      setLastScan(new Date())
    } catch (error) {
      console.error('Failed to scan:', error)
      alert('Failed to scan for incidents. Please check your AWS credentials.')
    } finally {
      setLoading(false)
    }
  }

  const toggleMonitoring = () => {
    setMonitoring(!monitoring)
    if (!monitoring) {
      scanForIncidents()
      // Poll every 5 minutes
      const interval = setInterval(scanForIncidents, 5 * 60 * 1000)
      return () => clearInterval(interval)
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL':
        return 'bg-red-100 text-red-800 border-red-300'
      case 'HIGH':
        return 'bg-orange-100 text-orange-800 border-orange-300'
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'LOW':
        return 'bg-green-100 text-green-800 border-green-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-lg">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  AWS Incident Co-Pilot
                </h1>
                <p className="text-sm text-gray-500">
                  Monitor and respond to AWS incidents automatically
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              {awsConfigured ? (
                <span className="flex items-center text-sm text-green-600">
                  <CheckCircle className="w-4 h-4 mr-1" />
                  AWS Connected
                </span>
              ) : (
                <span className="flex items-center text-sm text-red-600">
                  <XCircle className="w-4 h-4 mr-1" />
                  AWS Not Configured
                </span>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        {!awsConfigured && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
            <div className="flex items-start space-x-4">
              <div className="bg-blue-500 p-2 rounded-lg">
                <CloudIcon className="w-6 h-6 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-lg font-semibold text-blue-900 mb-2">
                  Welcome! Let's get you set up
                </h2>
                <p className="text-blue-800 mb-4">
                  To start monitoring your AWS infrastructure, you'll need to configure your AWS credentials.
                </p>
                <div className="bg-white rounded-lg p-4 border border-blue-200">
                  <h3 className="font-medium text-gray-900 mb-2">Quick Setup:</h3>
                  <ol className="list-decimal list-inside space-y-2 text-sm text-gray-700">
                    <li>Go to your Vercel project settings</li>
                    <li>Add environment variables:
                      <ul className="ml-6 mt-1 space-y-1 text-xs">
                        <li><code className="bg-gray-100 px-2 py-0.5 rounded">AWS_ACCESS_KEY_ID</code></li>
                        <li><code className="bg-gray-100 px-2 py-0.5 rounded">AWS_SECRET_ACCESS_KEY</code></li>
                        <li><code className="bg-gray-100 px-2 py-0.5 rounded">AWS_DEFAULT_REGION</code></li>
                      </ul>
                    </li>
                    <li>Redeploy your application</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Control Panel */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center">
              <Activity className="w-6 h-6 mr-2 text-blue-500" />
              Monitoring Control
            </h2>
            {lastScan && (
              <span className="text-sm text-gray-500">
                Last scan: {lastScan.toLocaleTimeString()}
              </span>
            )}
          </div>

          <div className="flex flex-wrap gap-4">
            <button
              onClick={scanForIncidents}
              disabled={loading || !awsConfigured}
              className="flex items-center px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors shadow-sm"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
                  Scanning...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5 mr-2" />
                  Scan Now
                </>
              )}
            </button>

            <button
              onClick={toggleMonitoring}
              disabled={!awsConfigured}
              className={`flex items-center px-6 py-3 rounded-lg transition-colors shadow-sm ${
                monitoring
                  ? 'bg-orange-500 text-white hover:bg-orange-600'
                  : 'bg-green-500 text-white hover:bg-green-600'
              } disabled:bg-gray-300 disabled:cursor-not-allowed`}
            >
              {monitoring ? (
                <>
                  <Pause className="w-5 h-5 mr-2" />
                  Stop Monitoring
                </>
              ) : (
                <>
                  <Play className="w-5 h-5 mr-2" />
                  Start Continuous Monitoring
                </>
              )}
            </button>
          </div>

          {monitoring && (
            <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm text-green-800 flex items-center">
                <Activity className="w-4 h-4 mr-2 animate-pulse" />
                Continuous monitoring active - Scanning every 5 minutes
              </p>
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Total Incidents</p>
                <p className="text-3xl font-bold text-gray-900">{incidents.length}</p>
              </div>
              <AlertTriangle className="w-10 h-10 text-blue-500 opacity-20" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Critical</p>
                <p className="text-3xl font-bold text-red-600">
                  {incidents.filter(i => i.severity === 'CRITICAL').length}
                </p>
              </div>
              <XCircle className="w-10 h-10 text-red-500 opacity-20" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">High Priority</p>
                <p className="text-3xl font-bold text-orange-600">
                  {incidents.filter(i => i.severity === 'HIGH').length}
                </p>
              </div>
              <AlertTriangle className="w-10 h-10 text-orange-500 opacity-20" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Medium/Low</p>
                <p className="text-3xl font-bold text-yellow-600">
                  {incidents.filter(i => ['MEDIUM', 'LOW'].includes(i.severity)).length}
                </p>
              </div>
              <CheckCircle className="w-10 h-10 text-yellow-500 opacity-20" />
            </div>
          </div>
        </div>

        {/* Incidents List */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <AlertTriangle className="w-6 h-6 mr-2 text-orange-500" />
            Active Incidents
          </h2>

          {incidents.length === 0 ? (
            <div className="text-center py-12">
              <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
              <p className="text-xl font-medium text-gray-900 mb-2">
                No incidents detected
              </p>
              <p className="text-gray-500">
                {awsConfigured
                  ? "Your AWS infrastructure is running smoothly!"
                  : "Configure AWS credentials to start monitoring"
                }
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {incidents.map((incident) => (
                <div
                  key={incident.id}
                  className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <span
                          className={`px-3 py-1 text-xs font-semibold rounded-full border ${getSeverityColor(
                            incident.severity
                          )}`}
                        >
                          {incident.severity}
                        </span>
                        <span className="text-xs text-gray-500">
                          {incident.resource}
                        </span>
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">
                        {incident.title}
                      </h3>
                      <p className="text-sm text-gray-600">
                        {incident.description}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-100">
                    <span>ID: {incident.id}</span>
                    <span>Detected: {new Date(incident.detected_at).toLocaleString()}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            AWS Incident Co-Pilot - Powered by AWS CloudWatch & CloudTrail
          </p>
        </div>
      </footer>
    </div>
  )
}
