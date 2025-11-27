'use client'

import { useState, useEffect } from 'react'
import { useSession, signOut } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { Settings, Key, Globe, CheckCircle, AlertCircle, LogOut, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function SettingsPage() {
  const { data: session, status, update } = useSession()
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  const [formData, setFormData] = useState({
    awsAccessKeyId: '',
    awsSecretAccessKey: '',
    awsRegion: 'us-east-1',
  })

  // Redirect to login if not authenticated
  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/login')
    } else if (session?.user) {
      // Load current AWS credentials
      setFormData({
        awsAccessKeyId: (session.user as any).awsAccessKeyId || '',
        awsSecretAccessKey: (session.user as any).awsSecretAccessKey || '',
        awsRegion: (session.user as any).awsRegion || 'us-east-1',
      })
    }
  }, [session, status, router])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess(false)

    try {
      // Update session with new credentials by signing in again
      const result = await fetch('/api/update-credentials', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (!result.ok) {
        throw new Error('Failed to update credentials')
      }

      // Force session refresh
      await update({
        ...session,
        user: {
          ...session?.user,
          awsAccessKeyId: formData.awsAccessKeyId,
          awsSecretAccessKey: formData.awsSecretAccessKey,
          awsRegion: formData.awsRegion,
        },
      })

      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError('Failed to update AWS credentials')
    } finally {
      setLoading(false)
    }
  }

  const handleSignOut = async () => {
    await signOut({ callbackUrl: '/login' })
  }

  if (status === 'loading') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              href="/"
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft className="h-5 w-5" />
              <span>Back to Dashboard</span>
            </Link>
          </div>
          <button
            onClick={handleSignOut}
            className="flex items-center gap-2 text-gray-600 hover:text-red-600 transition-colors"
          >
            <LogOut className="h-5 w-5" />
            <span>Sign Out</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-6">
            <Settings className="h-6 w-6 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
          </div>

          {/* User Info */}
          <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-sm text-gray-700">
              <span className="font-medium">Logged in as:</span> {session?.user?.name}
            </p>
          </div>

          {/* Success/Error Messages */}
          {success && (
            <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2 text-green-800">
              <CheckCircle className="h-5 w-5 flex-shrink-0" />
              <span className="text-sm">AWS credentials updated successfully!</span>
            </div>
          )}

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-800">
              <AlertCircle className="h-5 w-5 flex-shrink-0" />
              <span className="text-sm">{error}</span>
            </div>
          )}

          {/* AWS Configuration Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Key className="h-5 w-5 text-gray-600" />
                AWS Credentials
              </h2>

              <div className="space-y-4">
                <div>
                  <label htmlFor="awsAccessKeyId" className="block text-sm font-medium text-gray-700 mb-1">
                    AWS Access Key ID
                  </label>
                  <input
                    id="awsAccessKeyId"
                    type="text"
                    value={formData.awsAccessKeyId}
                    onChange={(e) => setFormData({ ...formData, awsAccessKeyId: e.target.value })}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="AKIA..."
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Your AWS access key ID for API authentication
                  </p>
                </div>

                <div>
                  <label htmlFor="awsSecretAccessKey" className="block text-sm font-medium text-gray-700 mb-1">
                    AWS Secret Access Key
                  </label>
                  <input
                    id="awsSecretAccessKey"
                    type="password"
                    value={formData.awsSecretAccessKey}
                    onChange={(e) => setFormData({ ...formData, awsSecretAccessKey: e.target.value })}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter secret key"
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Your AWS secret access key (stored securely in your session)
                  </p>
                </div>

                <div>
                  <label htmlFor="awsRegion" className="block text-sm font-medium text-gray-700 mb-1">
                    AWS Region
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Globe className="h-5 w-5 text-gray-400" />
                    </div>
                    <select
                      id="awsRegion"
                      value={formData.awsRegion}
                      onChange={(e) => setFormData({ ...formData, awsRegion: e.target.value })}
                      className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="us-east-1">US East (N. Virginia)</option>
                      <option value="us-east-2">US East (Ohio)</option>
                      <option value="us-west-1">US West (N. California)</option>
                      <option value="us-west-2">US West (Oregon)</option>
                      <option value="eu-west-1">EU (Ireland)</option>
                      <option value="eu-central-1">EU (Frankfurt)</option>
                      <option value="ap-southeast-1">Asia Pacific (Singapore)</option>
                      <option value="ap-northeast-1">Asia Pacific (Tokyo)</option>
                    </select>
                  </div>
                  <p className="mt-1 text-xs text-gray-500">
                    The primary AWS region to monitor
                  </p>
                </div>
              </div>
            </div>

            {/* Security Note */}
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-900">
                <strong>Security Note:</strong> Your AWS credentials are stored in an encrypted JWT session cookie
                and are never saved to any database. They are only accessible during your current session.
              </p>
            </div>

            {/* Save Button */}
            <div className="flex justify-end gap-3">
              <Link
                href="/"
                className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium rounded-lg transition-colors"
              >
                {loading ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
