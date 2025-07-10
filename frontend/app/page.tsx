/**
 * ReplySight frontend - Main chat interface for customer service responses
 * 
 * This component provides a clean interface for CS agents to input complaints
 * and receive research-backed responses with citations and latency metrics.
 */

'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { LoaderIcon, ClockIcon, BookOpenIcon, MessageSquareIcon, TrendingUpIcon, ZapIcon, CheckCircleIcon } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface ApiResponse {
  reply: string
  citations: string[]
  latency_ms: number
}

export default function ReplySight() {
  const [complaint, setComplaint] = useState('')
  const [response, setResponse] = useState<ApiResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!complaint.trim()) return

    setLoading(true)
    setError('')
    setResponse(null)

    try {
      const res = await fetch('/api/respond', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          complaint: complaint.trim(),
          customer_id: 'demo-user',
          priority: 'normal'
        })
      })

      if (!res.ok) {
        throw new Error(`API Error: ${res.status}`)
      }

      const data: ApiResponse = await res.json()
      setResponse(data)
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const clearForm = () => {
    setComplaint('')
    setResponse(null)
    setError('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">ReplySight</h1>
              <p className="text-gray-600 mt-1">Research-backed customer service response generation</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                Active
              </div>
              <Link href="/workflow">
                <Button variant="outline">
                  View Workflow
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <MessageSquareIcon className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">AI-Powered</p>
                <p className="text-2xl font-bold text-gray-900">GPT-4o</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <BookOpenIcon className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Research Sources</p>
                <p className="text-2xl font-bold text-gray-900">ArXiv + Web</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <ZapIcon className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg Response</p>
                <p className="text-2xl font-bold text-gray-900">~2s</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <TrendingUpIcon className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Quality Score</p>
                <p className="text-2xl font-bold text-gray-900">92%</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Interface */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mb-8">
          <div className="px-6 py-4 border-b border-gray-100">
            <h2 className="text-xl font-semibold text-gray-900">Generate Response</h2>
            <p className="text-gray-600 text-sm mt-1">Enter a customer complaint to generate an empathetic, research-backed response</p>
          </div>
          
          <div className="p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="complaint" className="block text-sm font-medium text-gray-700 mb-2">
                  Customer Complaint
                </label>
                <Textarea
                  id="complaint"
                  value={complaint}
                  onChange={(e) => setComplaint(e.target.value)}
                  placeholder="Paste the customer complaint here..."
                  className="min-h-[120px] resize-none"
                  disabled={loading}
                />
              </div>
              
              <div className="flex gap-3">
                <Button
                  type="submit"
                  disabled={loading || !complaint.trim()}
                  className="flex-1"
                >
                  {loading ? (
                    <>
                      <LoaderIcon className="h-4 w-4 mr-2 animate-spin" />
                      Generating Response...
                    </>
                  ) : (
                    <>
                      <MessageSquareIcon className="h-4 w-4 mr-2" />
                      Generate Response
                    </>
                  )}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={clearForm}
                  disabled={loading}
                >
                  Clear
                </Button>
              </div>
            </form>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-white rounded-xl shadow-sm border border-red-200 overflow-hidden mb-8">
            <div className="px-6 py-4 border-b border-red-200 bg-red-50">
              <h2 className="text-xl font-semibold text-red-800">Error</h2>
              <p className="text-red-600 text-sm mt-1">Something went wrong while generating the response</p>
            </div>
            <div className="p-6">
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        )}

        {/* Response Display */}
        {response && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Generated Response</h2>
                  <p className="text-gray-600 text-sm mt-1">AI-powered empathetic customer service response</p>
                </div>
                <div className="flex items-center space-x-3">
                  <Badge variant="secondary" className="flex items-center gap-1">
                    <ClockIcon className="h-3 w-3" />
                    {response.latency_ms}ms
                  </Badge>
                  <Badge variant="outline" className="flex items-center gap-1">
                    <BookOpenIcon className="h-3 w-3" />
                    {response.citations.length} source{response.citations.length !== 1 ? 's' : ''}
                  </Badge>
                  <Badge variant="outline" className="flex items-center gap-1">
                    <CheckCircleIcon className="h-3 w-3" />
                    Research-backed
                  </Badge>
                </div>
              </div>
            </div>
            
            <div className="p-6">
              <div className="space-y-6">
                {/* Response Text */}
                <div className="prose max-w-none">
                  <ReactMarkdown>{response.reply}</ReactMarkdown>
                </div>

                {/* Citations */}
                {response.citations.length > 0 && (
                  <div className="border-t pt-6">
                    <h4 className="font-semibold mb-3 text-gray-900">Citations & Sources</h4>
                    <div className="space-y-2">
                      {response.citations.map((citation, index) => (
                        <div key={index} className="flex items-start space-x-3">
                          <div className="flex-shrink-0 w-6 h-6 bg-indigo-100 text-indigo-700 rounded-full flex items-center justify-center text-xs font-semibold">
                            {index + 1}
                          </div>
                          <div className="flex-1 min-w-0">
                            {citation.startsWith('http') ? (
                              <a
                                href={citation}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-600 hover:underline text-sm break-all"
                              >
                                {citation}
                              </a>
                            ) : (
                              <p className="text-sm text-gray-700">{citation}</p>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex justify-end space-x-3 pt-4 border-t">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigator.clipboard.writeText(response.reply)}
                  >
                    Copy Response
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={clearForm}
                  >
                    Generate New
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}