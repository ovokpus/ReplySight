/**
 * ReplySight frontend - Main chat interface for customer service responses
 * 
 * This component provides a clean interface for CS agents to input complaints
 * and receive research-backed responses with citations and latency metrics.
 */

'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { LoaderIcon, ClockIcon, BookOpenIcon } from 'lucide-react'
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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            ReplySight
          </h1>
          <p className="text-gray-600">
            Research-backed customer service response generation
          </p>
        </div>

        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpenIcon className="h-5 w-5" />
              Customer Complaint
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Textarea
                value={complaint}
                onChange={(e) => setComplaint(e.target.value)}
                placeholder="Paste the customer complaint here..."
                className="min-h-[120px] resize-none"
                disabled={loading}
              />
              <div className="flex gap-2">
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
                    'Generate Response'
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
          </CardContent>
        </Card>

        {/* Error Display */}
        {error && (
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-700">{error}</p>
            </CardContent>
          </Card>
        )}

        {/* Response Display */}
        {response && (
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Generated Response</CardTitle>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="flex items-center gap-1">
                    <ClockIcon className="h-3 w-3" />
                    {response.latency_ms}ms
                  </Badge>
                  <Badge variant="outline">
                    {response.citations.length} citation{response.citations.length !== 1 ? 's' : ''}
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Response Text */}
                <div className="prose max-w-none">
                  <ReactMarkdown>{response.reply}</ReactMarkdown>
                </div>

                {/* Citations */}
                {response.citations.length > 0 && (
                  <div className="border-t pt-4">
                    <h4 className="font-semibold mb-2">Citations & Sources:</h4>
                    <ul className="space-y-1">
                      {response.citations.map((citation, index) => (
                        <li key={index} className="text-sm text-gray-600">
                          {citation.startsWith('http') ? (
                            <a
                              href={citation}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:underline"
                            >
                              {citation}
                            </a>
                          ) : (
                            citation
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Copy Button */}
                <div className="flex justify-end">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigator.clipboard.writeText(response.reply)}
                  >
                    Copy Response
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}