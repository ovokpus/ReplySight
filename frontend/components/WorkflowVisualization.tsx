'use client';

import React, { useEffect, useState, useRef } from 'react';
import mermaid from 'mermaid';

interface WorkflowVisualizationProps {
  /** API endpoint to fetch workflow data from */
  apiEndpoint?: string;
  /** Pre-loaded workflow data */
  workflowData?: any;
  /** Component height */
  height?: string;
  /** Whether to show metadata alongside the diagram */
  showMetadata?: boolean;
  /** Theme for the diagram */
  theme?: 'default' | 'dark' | 'forest' | 'base';
}

interface WorkflowMetadata {
  workflow_name: string;
  mermaid_diagram: string;
  node_count: number;
  edge_count: number;
  nodes: string[];
  edges: string[];
  execution_flow: string[];
  has_cycles: boolean;
  visualization_url: string;
  status: string;
}

const WorkflowVisualization: React.FC<WorkflowVisualizationProps> = ({
  apiEndpoint = '/api/workflow/graph',
  workflowData,
  height = '400px',
  showMetadata = true,
  theme = 'default'
}) => {
  const [metadata, setMetadata] = useState<WorkflowMetadata | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const diagramRef = useRef<HTMLDivElement>(null);

  // Initialize Mermaid
  useEffect(() => {
    mermaid.initialize({ 
      startOnLoad: true,
      theme: theme,
      securityLevel: 'loose',
      fontFamily: 'Inter, sans-serif'
    });
  }, [theme]);

  // Fetch workflow data
  useEffect(() => {
    if (workflowData) {
      setMetadata(workflowData);
      return;
    }

    const fetchWorkflowData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await fetch(apiEndpoint);
        if (!response.ok) {
          throw new Error(`Failed to fetch workflow data: ${response.statusText}`);
        }
        
        const data = await response.json();
        setMetadata(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchWorkflowData();
  }, [apiEndpoint, workflowData]);

  // Render Mermaid diagram
  useEffect(() => {
    if (metadata?.mermaid_diagram && diagramRef.current) {
      const renderDiagram = async () => {
        try {
          // Clear previous diagram
          diagramRef.current!.innerHTML = '';
          
          // Generate unique ID for this diagram
          const diagramId = `workflow-diagram-${Date.now()}`;
          
          // Render new diagram
          const { svg } = await mermaid.render(diagramId, metadata.mermaid_diagram);
          diagramRef.current!.innerHTML = svg;
        } catch (err) {
          console.error('Error rendering Mermaid diagram:', err);
          diagramRef.current!.innerHTML = `
            <div class="flex items-center justify-center h-full bg-red-50 border border-red-200 rounded-lg">
              <p class="text-red-600">Error rendering workflow diagram</p>
            </div>
          `;
        }
      };

      renderDiagram();
    }
  }, [metadata?.mermaid_diagram]);

  if (loading) {
    return (
      <div className="flex items-center justify-center" style={{ height }}>
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2 text-gray-600">Loading workflow visualization...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <h3 className="text-red-800 font-medium">Error Loading Workflow</h3>
        <p className="text-red-600 mt-1">{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-2 px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!metadata) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <p className="text-gray-600">No workflow data available</p>
      </div>
    );
  }

  return (
    <div className="workflow-visualization">
      {/* Header */}
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-900">
          {metadata.workflow_name}
        </h2>
        <div className="flex items-center mt-1 space-x-4">
          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
            metadata.status === 'active' 
              ? 'bg-green-100 text-green-800' 
              : 'bg-gray-100 text-gray-800'
          }`}>
            {metadata.status}
          </span>
          <span className="text-sm text-gray-500">
            {metadata.node_count} nodes • {metadata.edge_count} edges
          </span>
        </div>
      </div>

      {/* Main content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Diagram */}
        <div className="lg:col-span-2">
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-lg font-medium text-gray-900">Workflow Diagram</h3>
              <a
                href={`${metadata.visualization_url}/?state=${encodeURIComponent(JSON.stringify({ code: metadata.mermaid_diagram }))}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 text-sm underline"
              >
                Open in Mermaid Live
              </a>
            </div>
            <div 
              ref={diagramRef}
              className="workflow-diagram border border-gray-100 rounded bg-gray-50 p-4 overflow-auto"
              style={{ height, minHeight: '300px' }}
            />
          </div>
        </div>

        {/* Metadata sidebar */}
        {showMetadata && (
          <div className="space-y-4">
            {/* Execution Flow */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="text-lg font-medium text-gray-900 mb-3">Execution Flow</h3>
              <div className="space-y-2">
                {metadata.execution_flow.map((step, index) => (
                  <div key={index} className="flex items-start">
                    <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center text-xs font-medium mr-3">
                      {index + 1}
                    </span>
                    <span className="text-sm text-gray-700">{step}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Nodes */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="text-lg font-medium text-gray-900 mb-3">Workflow Nodes</h3>
              <div className="space-y-1">
                {metadata.nodes.map((node, index) => (
                  <div key={index} className="flex items-center">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                    <span className="text-sm text-gray-700 font-mono">{node}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Edges */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="text-lg font-medium text-gray-900 mb-3">Connections</h3>
              <div className="space-y-1">
                {metadata.edges.map((edge, index) => (
                  <div key={index} className="flex items-center">
                    <div className="w-2 h-2 bg-gray-400 rounded-full mr-3"></div>
                    <span className="text-sm text-gray-700 font-mono">{edge}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Properties */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="text-lg font-medium text-gray-900 mb-3">Properties</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Has Cycles</span>
                  <span className={`text-sm font-medium ${
                    metadata.has_cycles ? 'text-orange-600' : 'text-green-600'
                  }`}>
                    {metadata.has_cycles ? 'Yes' : 'No'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Complexity</span>
                  <span className="text-sm font-medium text-gray-900">
                    {metadata.node_count + metadata.edge_count} points
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Raw Mermaid Code (collapsible) */}
      <details className="mt-6">
        <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
          View Raw Mermaid Code
        </summary>
        <div className="mt-2 bg-gray-50 border border-gray-200 rounded-lg p-4">
          <pre className="text-xs text-gray-700 overflow-x-auto">
            <code>{metadata.mermaid_diagram}</code>
          </pre>
          <button
            onClick={() => navigator.clipboard.writeText(metadata.mermaid_diagram)}
            className="mt-2 px-3 py-1 bg-gray-600 text-white rounded text-xs hover:bg-gray-700"
          >
            Copy to Clipboard
          </button>
        </div>
      </details>
    </div>
  );
};

export default WorkflowVisualization; 