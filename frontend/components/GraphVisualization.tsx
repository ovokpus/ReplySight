'use client';

import React, { useEffect, useState, useRef } from 'react';

// Proper type for mermaid
type MermaidType = typeof import('mermaid').default;

interface GraphData {
  workflow_name: string;
  mermaid_diagram: string;
  node_count: number;
  edge_count: number;
  nodes: string[];
  edges: string[];
  execution_flow: string[];
  has_cycles: boolean;
  status: string;
}

interface GraphVisualizationProps {
  apiUrl?: string;
}

export default function GraphVisualization({ apiUrl = '/api/workflow/graph' }: GraphVisualizationProps) {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [mermaidLoaded, setMermaidLoaded] = useState(false);
  const [mermaid, setMermaid] = useState<MermaidType | null>(null);
  const mermaidRef = useRef<HTMLDivElement>(null);

  // Dynamic import of mermaid to avoid SSR issues
  useEffect(() => {
    const loadMermaid = async () => {
      try {
        const mermaidModule = await import('mermaid');
        const mermaidInstance = mermaidModule.default;
        
        // Initialize Mermaid with beautiful theme
        mermaidInstance.initialize({
          startOnLoad: false,
          theme: 'default',
          themeVariables: {
            primaryColor: '#4F46E5',
            primaryTextColor: '#1F2937',
            primaryBorderColor: '#6366F1',
            lineColor: '#6366F1',
            secondaryColor: '#F3F4F6',
            tertiaryColor: '#E5E7EB',
            background: '#FFFFFF',
            mainBkg: '#F8FAFC',
            secondaryBkg: '#F1F5F9',
            primaryDark: '#312E81',
            edgeLabelBackground: '#FFFFFF',
            clusterBkg: '#F8FAFC',
            clusterBorder: '#D1D5DB',
          },
          flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            curve: 'cardinal',
          },
          securityLevel: 'loose',
        });
        
        setMermaid(mermaidInstance);
        setMermaidLoaded(true);
        return mermaidInstance;
      } catch (error) {
        console.error('Failed to load Mermaid:', error);
        setError('Failed to load diagram library');
        return null;
      }
    };

    loadMermaid();
  }, []);

  const fetchGraphData = async () => {
    try {
      setLoading(true);
      const response = await fetch(apiUrl);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch graph data: ${response.status}`);
      }
      
      const data: GraphData = await response.json();
      setGraphData(data);
      
      // Render the mermaid diagram only after mermaid is loaded
      if (data.mermaid_diagram && mermaidRef.current && mermaidLoaded && mermaid) {
        renderMermaidDiagram(data.mermaid_diagram);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  const renderMermaidDiagram = async (diagramCode: string) => {
    try {
      if (!mermaid || !mermaidRef.current) {
        return;
      }
      
      // Clear any existing content
      mermaidRef.current.innerHTML = '';
      
      // Generate unique ID for this diagram
      const diagramId = `mermaid-diagram-${Date.now()}`;
      
      try {
        const { svg } = await mermaid.render(diagramId, diagramCode);
        if (mermaidRef.current) {
          mermaidRef.current.innerHTML = svg;
        }
      } catch (mermaidError) {
        console.error('Mermaid rendering error:', mermaidError);
        setError('Failed to render diagram');
      }
    } catch (error) {
      console.error('Failed to render diagram:', error);
      setError('Failed to render diagram');
    }
  };

  // Fetch data when mermaid is loaded
  useEffect(() => {
    if (mermaidLoaded && mermaid) {
      fetchGraphData();
    }
  }, [mermaidLoaded, mermaid, apiUrl]);

  // Re-render diagram when data changes and mermaid is loaded
  useEffect(() => {
    if (graphData?.mermaid_diagram && mermaidRef.current && mermaidLoaded && mermaid) {
      renderMermaidDiagram(graphData.mermaid_diagram);
    }
  }, [graphData, mermaidLoaded, mermaid]);

  const handleRefresh = () => {
    setError(null);
    fetchGraphData();
  };

  if (loading || !mermaidLoaded) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-700">
            {!mermaidLoaded ? 'Loading diagram library...' : 'Loading Workflow Graph...'}
          </h2>
          <p className="text-gray-500 mt-2">Fetching your beautiful visualization</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-red-50 to-pink-100">
        <div className="text-center max-w-md">
          <div className="bg-red-100 rounded-full p-4 inline-block mb-4">
            <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">Unable to Load Graph</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={handleRefresh}
            className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
          >
            Try Again
          </button>
          <p className="text-sm text-gray-500 mt-4">
            Make sure the backend server is running on port 8000
          </p>
        </div>
      </div>
    );
  }

  if (!graphData) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{graphData.workflow_name}</h1>
              <p className="text-gray-600 mt-1">Interactive workflow visualization</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                {graphData.status}
              </div>
              <button
                onClick={handleRefresh}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Refresh
              </button>
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
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Nodes</p>
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
                <p className="text-sm font-medium text-gray-600">Total Edges</p>
                <p className="text-2xl font-bold text-gray-900">{graphData.edge_count}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Has Cycles</p>
                <p className="text-2xl font-bold text-gray-900">{graphData.has_cycles ? 'Yes' : 'No'}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Flow Steps</p>
                <p className="text-2xl font-bold text-gray-900">{graphData.execution_flow.length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Graph Visualization */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-100">
            <h2 className="text-xl font-semibold text-gray-900">Workflow Diagram</h2>
            <p className="text-gray-600 text-sm mt-1">Interactive visualization of your Smart Study Buddy workflow</p>
          </div>
          
          <div className="p-8 flex justify-center">
            <div 
              ref={mermaidRef}
              className="w-full max-w-full overflow-x-auto"
              style={{ minHeight: '400px' }}
            />
          </div>
        </div>

        {/* Execution Flow */}
        <div className="mt-8 bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="px-6 py-4 border-b border-gray-100">
            <h2 className="text-xl font-semibold text-gray-900">Execution Flow</h2>
            <p className="text-gray-600 text-sm mt-1">Step-by-step workflow execution path</p>
          </div>
          
          <div className="p-6">
            <div className="space-y-4">
              {graphData.execution_flow.map((step, index) => (
                <div key={index} className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-indigo-100 text-indigo-700 rounded-full flex items-center justify-center text-sm font-semibold">
                    {index + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{step}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 