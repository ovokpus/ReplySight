/**
 * ReplySight frontend - Main chat interface for customer service responses
 * 
 * This component provides a clean interface for CS agents to input complaints
 * and receive research-backed responses with citations and latency metrics.
 */

'use client'

import React from 'react';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { LoaderIcon, MessageSquareIcon, ClockIcon, BookOpenIcon, CheckCircleIcon } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

// Custom hooks and components
import { useComplaintForm } from '@/hooks/useComplaintForm';
import PageHeader from '@/components/PageHeader';
import StatsGrid from '@/components/StatsGrid';

// Constants and types
import { UI_CONSTANTS, APP_CONFIG, PAGE_METADATA } from '@/constants';

export default function ReplySight() {
  const {
    complaint,
    response,
    loading,
    error,
    setComplaint,
    handleSubmit,
    clearForm,
  } = useComplaintForm();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <PageHeader
        title={PAGE_METADATA.MAIN.title}
        description={PAGE_METADATA.MAIN.description}
        showWorkflowButton={true}
      />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Stats Cards */}
        <StatsGrid />

        {/* Main Interface */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mb-8">
          <div className="px-6 py-4 border-b border-gray-100">
            <h2 className="text-xl font-semibold text-gray-900">
              {PAGE_METADATA.MAIN.sections.GENERATE.title}
            </h2>
            <p className="text-gray-600 text-sm mt-1">
              {PAGE_METADATA.MAIN.sections.GENERATE.description}
            </p>
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
                  placeholder={UI_CONSTANTS.PLACEHOLDERS.COMPLAINT}
                  className="resize-none"
                  style={{ minHeight: `${APP_CONFIG.TEXTAREA_MIN_HEIGHT}px` }}
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
                      {UI_CONSTANTS.LOADING_MESSAGES.GENERATING}
                    </>
                  ) : (
                    <>
                      <MessageSquareIcon className="h-4 w-4 mr-2" />
                      {UI_CONSTANTS.BUTTON_LABELS.GENERATE}
                    </>
                  )}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={clearForm}
                  disabled={loading}
                >
                  {UI_CONSTANTS.BUTTON_LABELS.CLEAR}
                </Button>
              </div>
            </form>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-white rounded-xl shadow-sm border border-red-200 overflow-hidden mb-8">
            <div className="px-6 py-4 border-b border-red-200 bg-red-50">
              <h2 className="text-xl font-semibold text-red-800">
                {UI_CONSTANTS.STATUS_LABELS.ERROR}
              </h2>
              <p className="text-red-600 text-sm mt-1">
                Something went wrong while generating the response
              </p>
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
                  <h2 className="text-xl font-semibold text-gray-900">
                    {PAGE_METADATA.MAIN.sections.RESPONSE.title}
                  </h2>
                  <p className="text-gray-600 text-sm mt-1">
                    {PAGE_METADATA.MAIN.sections.RESPONSE.description}
                  </p>
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
                    {UI_CONSTANTS.BUTTON_LABELS.COPY}
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={clearForm}
                  >
                    {UI_CONSTANTS.BUTTON_LABELS.GENERATE_NEW}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}