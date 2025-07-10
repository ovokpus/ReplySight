// API Response Types
export interface ApiResponse {
  reply: string;
  citations: string[];
  latency_ms: number;
}

export interface ComplaintRequest {
  complaint: string;
  customer_id: string;
  priority: string;
}

// Graph Data Types
export interface GraphData {
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

// Component Props Types
export interface GraphVisualizationProps {
  apiUrl?: string;
}

export interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  color: 'blue' | 'green' | 'purple' | 'yellow' | 'red';
}

export interface LoadingStateProps {
  message?: string;
  description?: string;
  variant?: 'default' | 'graph';
}

export interface ErrorStateProps {
  error: string;
  onRetry?: () => void;
  variant?: 'default' | 'graph';
}

// Mermaid Types
export type MermaidType = typeof import('mermaid').default;

// Form Types
export interface FormState {
  complaint: string;
  response: ApiResponse | null;
  loading: boolean;
  error: string;
}

// Common Types
export type ColorVariant = 'blue' | 'green' | 'purple' | 'yellow' | 'red';
export type ComponentSize = 'sm' | 'md' | 'lg';
export type ComponentVariant = 'default' | 'outline' | 'secondary'; 