'use client'

import { useState, Suspense } from 'react'
import { signIn } from 'next-auth/react'
import { useRouter, useSearchParams } from 'next/navigation'
import { AlertCircle, Cloud, Key, Lock, User, Globe } from 'lucide-react'

function LoginForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showAwsConfig, setShowAwsConfig] = useState(false)

  const [formData, setFormData] = useState({
    username: '',
    password: '',
    awsAccessKeyId: '',
    awsSecretAccessKey: '',
    awsRegion: 'us-east-1',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const result = await signIn('credentials', {
        redirect: false,
        username: formData.username,
        password: formData.password,
        awsAccessKeyId: formData.awsAccessKeyId,
        awsSecretAccessKey: formData.awsSecretAccessKey,
        awsRegion: formData.awsRegion,
      })

      if (result?.error) {
        setError('Invalid credentials')
      } else {
        // Redirect to the page they were trying to access, or home
        const callbackUrl = searchParams.get('callbackUrl') || '/'
        router.push(callbackUrl)
        router.refresh()
      }
    } catch (err) {
      setError('An error occurred during sign in')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-8">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <Cloud className="h-12 w-12 text-blue-600" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">AWS Incident Co-Pilot</h1>
          <p className="text-gray-600 mt-2">Sign in to access your dashboard</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-800">
            <AlertCircle className="h-5 w-5 flex-shrink-0" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Username */}
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <User className="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="username"
                type="text"
                required
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter your username"
              />
            </div>
          </div>

          {/* Password */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock className="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="password"
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter your password"
              />
            </div>
          </div>

          {/* AWS Configuration Toggle */}
          <div className="border-t border-gray-200 pt-4">
            <button
              type="button"
              onClick={() => setShowAwsConfig(!showAwsConfig)}
              className="flex items-center justify-between w-full text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors"
            >
              <span>AWS Configuration {showAwsConfig ? '(Click to hide)' : '(Optional - Click to configure)'}</span>
              <Key className="h-4 w-4" />
            </button>
          </div>

          {/* AWS Credentials (collapsible) */}
          {showAwsConfig && (
            <div className="space-y-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-xs text-gray-600">
                Configure your AWS credentials now, or skip and add them later in Settings.
              </p>

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
              </div>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-gray-600">
          <p>First time here? Just create any username and password to get started.</p>
          <p className="mt-2 text-xs">Your credentials are stored securely in your browser session.</p>
        </div>
      </div>
    </div>
  )
}

export default function LoginPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    }>
      <LoginForm />
    </Suspense>
  )
}
