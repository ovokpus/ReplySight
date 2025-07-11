'use client';

import React, { useEffect } from 'react';
import Link from 'next/link';
import { WorkflowVisualizationProps } from '@/types';
import { useGraphData } from '@/hooks/useGraphData';
import { useMermaid } from '@/hooks/useMermaid';
import { LoadingState, ErrorState } from '@/components';
import { UI_CONSTANTS, PAGE_METADATA } from '@/constants';

interface ExtendedWorkflowVisualizationProps extends WorkflowVisualizationProps {
  /** Component height */
  height?: string;
  /** Whether to show metadata alongside the diagram */
  showMetadata?: boolean;
  /** Theme for the diagram */
  theme?: 'default' | 'dark' | 'forest' | 'base';
}

const WorkflowVisualization: React.FC<ExtendedWorkflowVisualizationProps> = ({
  apiUrl,
  height = '600px',
  showMetadata = true,
  theme = 'default'
}) => {
  const { graphData, loading, error, refresh } = useGraphData(apiUrl);
  const { 
    mermaidLoaded, 
    error: mermaidError, 
    mermaidRef, 
    renderDiagram, 
    setError: setMermaidError 
  } = useMermaid();

  // Render diagram when both data and mermaid are ready
  useEffect(() => {
    if (graphData?.mermaid_diagram && mermaidLoaded && !mermaidError) {
      renderDiagram(graphData.mermaid_diagram);
    }
  }, [graphData, mermaidLoaded, mermaidError, renderDiagram]);

  // Handle refresh - reset mermaid errors and refetch data
  const handleRefresh = () => {
    setMermaidError(null);
    refresh();
  };

  // Show loading state
  if (loading || !mermaidLoaded) {
    const message = !mermaidLoaded 
      ? UI_CONSTANTS.LOADING_MESSAGES.LOADING_LIBRARY 
      : UI_CONSTANTS.LOADING_MESSAGES.LOADING_GRAPH;
    
    return (
      <LoadingState 
        message={message} 
        variant="graph" 
      />
    );
  }

  // Show error state
  if (error || mermaidError) {
    return (
      <ErrorState 
        error={error || mermaidError || 'Unknown error'} 
        onRetry={handleRefresh}
        variant="graph" 
      />
    );
  }

  // Show diagram
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                {graphData?.workflow_name || PAGE_METADATA.GRAPH.title}
              </h1>
              <p className="text-gray-600 mt-1">{PAGE_METADATA.GRAPH.description}</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                {graphData?.status || UI_CONSTANTS.STATUS_LABELS.ACTIVE}
              </div>
              <Link href="/">
                <button className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm font-medium">
                  ← Home
                </button>
              </Link>
              <button
                onClick={handleRefresh}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium"
              >
                {UI_CONSTANTS.BUTTON_LABELS.REFRESH}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Workflow Stats */}
        {graphData && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Nodes</p>
                  <p className="text-2xl font-bold text-gray-900">{graphData.node_count}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Edges</p>
                  <p className="text-2xl font-bold text-gray-900">{graphData.edge_count}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Flow Steps</p>
                  <p className="text-2xl font-bold text-gray-900">{graphData.execution_flow.length}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
              <div className="flex items-center">
                <div className={`p-2 rounded-lg ${graphData.has_cycles ? 'bg-red-100' : 'bg-green-100'}`}>
                  <svg className={`w-6 h-6 ${graphData.has_cycles ? 'text-red-600' : 'text-green-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Cycles</p>
                  <p className={`text-2xl font-bold ${graphData.has_cycles ? 'text-red-600' : 'text-green-600'}`}>
                    {graphData.has_cycles ? 'Yes' : 'No'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Main content grid */}
        <div className={`grid ${showMetadata ? 'grid-cols-1 lg:grid-cols-3' : 'grid-cols-1'} gap-6`}>
          {/* Diagram */}
          <div className={showMetadata ? 'lg:col-span-2' : 'col-span-1'}>
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-100">
                <h3 className="text-lg font-semibold text-gray-900">Workflow Diagram</h3>
                <p className="text-gray-600 text-sm mt-1">Interactive visualization of the workflow</p>
              </div>
              <div className="p-6">
                <div 
                  ref={mermaidRef}
                  className="w-full flex items-center justify-center p-4 bg-gray-50 rounded-lg border border-gray-200"
                  style={{ 
                    height,
                    minHeight: '400px',
                    background: 'linear-gradient(45deg, #f8fafc 25%, transparent 25%), linear-gradient(-45deg, #f8fafc 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #f8fafc 75%), linear-gradient(-45deg, transparent 75%, #f8fafc 75%)',
                    backgroundSize: '20px 20px',
                    backgroundPosition: '0 0, 0 10px, 10px -10px, -10px 0px'
                  }}
                >
                  {/* Loading state for diagram rendering */}
                  {graphData && !mermaidRef.current?.innerHTML && (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                      <span className="ml-3 text-gray-600">Rendering diagram...</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Metadata sidebar */}
          {showMetadata && graphData && (
            <div className="space-y-6">
              {/* Execution Flow */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-100">
                <div className="px-6 py-4 border-b border-gray-100">
                  <h3 className="text-lg font-semibold text-gray-900">Execution Flow</h3>
                  <p className="text-gray-600 text-sm mt-1">Step-by-step workflow execution</p>
                </div>
                <div className="p-6">
                  <div className="space-y-3">
                    {graphData.execution_flow.map((step, index) => (
                      <div key={index} className="flex items-start">
                        <div className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center text-xs font-semibold mr-3">
                          {index + 1}
                        </div>
                        <span className="text-sm text-gray-700">{step}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Workflow Nodes */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-100">
                <div className="px-6 py-4 border-b border-gray-100">
                  <h3 className="text-lg font-semibold text-gray-900">Workflow Nodes</h3>
                  <p className="text-gray-600 text-sm mt-1">All nodes in the workflow</p>
                </div>
                <div className="p-6">
                  <div className="space-y-2">
                    {graphData.nodes.map((node, index) => (
                      <div key={index} className="flex items-center">
                        <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                        <span className="text-sm text-gray-700">{node}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Workflow Edges */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-100">
                <div className="px-6 py-4 border-b border-gray-100">
                  <h3 className="text-lg font-semibold text-gray-900">Workflow Edges</h3>
                  <p className="text-gray-600 text-sm mt-1">All connections in the workflow</p>
                </div>
                <div className="p-6">
                  <div className="space-y-2">
                    {graphData.edges.map((edge, index) => (
                      <div key={index} className="flex items-center">
                        <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                        <span className="text-sm text-gray-700">{edge}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default WorkflowVisualization; 