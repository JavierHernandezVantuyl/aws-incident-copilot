'use client'

/**
 * AWS Incident Co-Pilot - Main Dashboard
 *
 * Production-ready dashboard with proper error handling, cost awareness,
 * and security best practices.
 *
 * Cost: Vercel free tier includes 100GB-hours/month of function execution.
 * Each scan costs ~$0.001-0.01 in AWS API calls (free tier eligible).
 */

import { useState, useEffect, useCallback } from 'react'
import {
  Activity,
  AlertTriangle,
  CheckCircle,
  XCircle,
  RefreshCw,
  Play,
  Pause,
  CloudIcon,
  Shield,
  Zap,
  DollarSign,
  Info
} from 'lucide-react'
import type { Incident, ScanResponse, AWSTestResponse } from './types'

const SCAN_COOLDOWN_MS = 30000 // 30 seconds minimum between scans
const CONTINUOUS_SCAN_INTERVAL_MS = 5 * 60 * 1000 // 5 minutes

export default function Home() {
  // State management
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(false)
  const [monitoring, setMonitoring] = useState(false)
  const [lastScan, setLastScan] = useState<Date | null>(null)
  const [awsConfigured, setAwsConfigured] = useState(false)
  const [awsConnected, setAwsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [scanCooldown, setScanCooldown] = useState(false)
  const [costInfo, setCostInfo] = useState<string | null>(null)
  const [permissionWarning, setPermissionWarning] = useState<string | null>(null)

  // Check AWS configuration on mount
  useEffect(() => {
    checkAwsConfig()
  }, [])

  // Continuous monitoring effect
  useEffect(() => {
    if (!monitoring) return

    const interval = setInterval(() => {
      if (!scanCooldown) {
        scanForIncidents()
      }
    }, CONTINUOUS_SCAN_INTERVAL_MS)

    return () => clearInterval(interval)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [monitoring, scanCooldown])

  const checkAwsConfig = async () => {
    try {
      const response = await fetch('/api/test-aws', {
        headers: {
          'Accept': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data: AWSTestResponse = await response.json()

      setAwsConfigured(data.configured)
      setAwsConnected(data.connected || false)

      // Show permission warnings if any
      if (data.permissions && !data.all_permissions_ok) {
        const failedServices = Object.entries(data.permissions)
          .filter(([_, status]) => status !== 'OK')
          .map(([service, _]) => service)

        if (failedServices.length > 0) {
          setPermissionWarning(
            `Limited permissions detected for: ${failedServices.join(', ')}. Some incident types may not be detected.`
          )
        }
      }

      // Show cost info
      if (data.cost_info) {
        setCostInfo(data.cost_info.free_tier || null)
      }
    } catch (error) {
      console.error('Failed to check AWS config:', error)
      setAwsConfigured(false)
      setAwsConnected(false)
      setError('Failed to connect to API. Please refresh the page.')
    }
  }

  const scanForIncidents = useCallback(async () => {
    // Prevent rapid scanning (cost control)
    if (scanCooldown) {
      setError(`Please wait ${SCAN_COOLDOWN_MS / 1000} seconds between scans to stay within free tier limits.`)
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/scan', {
        headers: {
          'Accept': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data: ScanResponse = await response.json()

      if (data.success) {
        setIncidents(data.incidents || [])
        setLastScan(new Date())

        // Store cost info for display
        if (data.cost_info) {
          setCostInfo(data.cost_info.recommendation || null)
        }

        // Clear any previous errors
        setError(null)
      } else {
        setError(data.error || 'Failed to scan for incidents')

        // Show help if available
        if (data.help && typeof data.help === 'string') {
          setError(`${data.error || 'Error'}: ${data.help}`)
        }
      }

      // Activate cooldown
      setScanCooldown(true)
      setTimeout(() => setScanCooldown(false), SCAN_COOLDOWN_MS)

    } catch (error) {
      console.error('Scan error:', error)
      const errorMessage = error instanceof Error ? error.message : 'Unknown error'
      setError(`Failed to scan: ${errorMessage}. Check your AWS credentials and network connection.`)
      setIncidents([])
    } finally {
      setLoading(false)
    }
  }, [scanCooldown])

  const toggleMonitoring = () => {
    if (!monitoring) {
      // Start monitoring
      scanForIncidents()
    }
    setMonitoring(!monitoring)
  }

  const getSeverityColor = (severity: string): string => {
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
            <div className="flex items-center space-x-4">
              {awsConnected ? (
                <span className="flex items-center text-sm text-green-600">
                  <CheckCircle className="w-4 h-4 mr-1" />
                  AWS Connected
                </span>
              ) : awsConfigured ? (
                <span className="flex items-center text-sm text-yellow-600">
                  <AlertTriangle className="w-4 h-4 mr-1" />
                  Configured (not verified)
                </span>
              ) : (
                <span className="flex items-center text-sm text-red-600">
                  <XCircle className="w-4 h-4 mr-1" />
                  Not Configured
                </span>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Cost Awareness Banner */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 flex items-start space-x-3">
          <DollarSign className="w-5 h-5 text-blue-600 mt-0.5" />
          <div className="flex-1">
            <h3 className="text-sm font-semibold text-blue-900 mb-1">Cost Information</h3>
            <p className="text-sm text-blue-800">
              <strong>Free Tier Friendly:</strong> This dashboard uses AWS free tier eligible operations.
              Estimated cost: $0.001-0.01 per scan. Limit scans to 5-15 minute intervals to stay within free tier.
              {costInfo && ` ${costInfo}`}
            </p>
            <p className="text-xs text-blue-700 mt-1">
              Vercel hosting: Free tier includes 100GB-hours/month. You are responsible for AWS costs.
            </p>
          </div>
        </div>

        {/* Permission Warning */}
        {permissionWarning && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6 flex items-start space-x-3">
            <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
            <div className="flex-1">
              <h3 className="text-sm font-semibold text-yellow-900 mb-1">Permission Warning</h3>
              <p className="text-sm text-yellow-800">{permissionWarning}</p>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start space-x-3">
            <XCircle className="w-5 h-5 text-red-600 mt-0.5" />
            <div className="flex-1">
              <h3 className="text-sm font-semibold text-red-900 mb-1">Error</h3>
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        )}

        {/* Welcome Section for unconfigured AWS */}
        {!awsConfigured && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
            <div className="flex items-start space-x-4">
              <div className="bg-blue-500 p-2 rounded-lg">
                <CloudIcon className="w-6 h-6 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-lg font-semibold text-blue-900 mb-2">
                  Welcome! Let&apos;s get you set up
                </h2>
                <p className="text-blue-800 mb-4">
                  To start monitoring your AWS infrastructure, you&apos;ll need to configure your AWS credentials.
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
                  <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
                    <strong>Security:</strong> Use IAM user with read-only permissions (CloudWatchReadOnlyAccess, AWSCloudTrailReadOnlyAccess, AmazonEC2ReadOnlyAccess).
                  </div>
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
              <div className="text-right">
                <span className="text-sm text-gray-500">Last scan:</span>
                <br />
                <span className="text-sm font-medium text-gray-900">
                  {lastScan.toLocaleTimeString()}
                </span>
              </div>
            )}
          </div>

          <div className="flex flex-wrap gap-4">
            <button
              onClick={scanForIncidents}
              disabled={loading || !awsConfigured || scanCooldown}
              className="flex items-center px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors shadow-sm"
              aria-label="Scan for incidents now"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
                  Scanning...
                </>
              ) : scanCooldown ? (
                <>
                  <RefreshCw className="w-5 h-5 mr-2" />
                  Cooldown Active
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
              aria-label={monitoring ? 'Stop continuous monitoring' : 'Start continuous monitoring'}
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

            <button
              onClick={checkAwsConfig}
              disabled={loading}
              className="flex items-center px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors shadow-sm"
              aria-label="Test AWS connection"
            >
              <Shield className="w-5 h-5 mr-2" />
              Test Connection
            </button>
          </div>

          {monitoring && (
            <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm text-green-800 flex items-center">
                <Activity className="w-4 h-4 mr-2 animate-pulse" />
                Continuous monitoring active - Scanning every 5 minutes
              </p>
              <p className="text-xs text-green-700 mt-1">
                <Info className="w-3 h-3 inline mr-1" />
                Automatic scanning helps you catch issues early while staying within free tier limits
              </p>
            </div>
          )}

          {scanCooldown && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800 flex items-center">
                <AlertTriangle className="w-4 h-4 mr-2" />
                Scan cooldown active ({SCAN_COOLDOWN_MS / 1000}s) - This prevents excessive AWS API costs
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
                      <p className="text-sm text-gray-600 mb-3">
                        {incident.description}
                      </p>

                      {/* Recommendations */}
                      {incident.recommendations && incident.recommendations.length > 0 && (
                        <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                          <p className="text-xs font-semibold text-blue-900 mb-2">Recommendations:</p>
                          <ul className="text-xs text-blue-800 space-y-1">
                            {incident.recommendations.map((rec, idx) => (
                              <li key={idx} className="flex items-start">
                                <span className="mr-2">•</span>
                                <span>{rec}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Cost Impact */}
                      {incident.cost_impact && (
                        <div className="mt-2 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
                          <strong>Cost Impact:</strong> {incident.cost_impact}
                        </div>
                      )}
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
          <div className="text-center">
            <p className="text-gray-500 text-sm mb-2">
              AWS Incident Co-Pilot - Powered by AWS CloudWatch & CloudTrail
            </p>
            <p className="text-gray-400 text-xs">
              <strong>Security:</strong> All AWS operations are read-only. No data is stored on servers.
              <br />
              <strong>Cost:</strong> Uses AWS free tier eligible operations. You are responsible for AWS costs.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
