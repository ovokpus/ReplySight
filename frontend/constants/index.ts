// API Endpoints
export const API_ENDPOINTS = {
  RESPOND: '/api/respond',
  WORKFLOW_GRAPH: '/api/workflow/graph',
} as const;

// App Configuration
export const APP_CONFIG = {
  DEFAULT_CUSTOMER_ID: 'demo-user',
  DEFAULT_PRIORITY: 'normal',
  MIN_COMPLAINT_LENGTH: 1,
  TEXTAREA_MIN_HEIGHT: 120,
  GRAPH_MIN_HEIGHT: 600,
  GRAPH_MAX_HEIGHT: 800,
  BACKEND_PORT: 8000,
} as const;

// UI Constants
export const UI_CONSTANTS = {
  LOADING_MESSAGES: {
    GENERATING: 'Generating Response...',
    LOADING_GRAPH: 'Loading Workflow Graph...',
    LOADING_LIBRARY: 'Loading diagram library...',
  },
  BUTTON_LABELS: {
    GENERATE: 'Generate Response',
    CLEAR: 'Clear',
    COPY: 'Copy Response',
    REFRESH: 'Refresh',
    TRY_AGAIN: 'Try Again',
    GENERATE_NEW: 'Generate New',
    VIEW_WORKFLOW: 'View Workflow',
  },
  PLACEHOLDERS: {
    COMPLAINT: 'Paste the customer complaint here...',
  },
  STATUS_LABELS: {
    ACTIVE: 'Active',
    ERROR: 'Error',
    SUCCESS: 'Success',
  },
} as const;

// Stats Cards Data
export const STATS_CARDS = [
  {
    icon: 'MessageSquare',
    label: 'AI-Powered',
    value: 'GPT-4o',
    color: 'blue' as const,
  },
  {
    icon: 'BookOpen',
    label: 'Research Sources',
    value: 'ArXiv + Web',
    color: 'green' as const,
  },
  {
    icon: 'Zap',
    label: 'Avg Response',
    value: '~2s',
    color: 'purple' as const,
  },
  {
    icon: 'TrendingUp',
    label: 'Quality Score',
    value: '92%',
    color: 'yellow' as const,
  },
] as const;

// Mermaid Configuration
export const MERMAID_CONFIG = {
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
    fontSize: '16px',
    fontFamily: 'Inter, system-ui, sans-serif',
  },
  flowchart: {
    useMaxWidth: true,
    htmlLabels: true,
    curve: 'cardinal',
    nodeSpacing: 80,
    rankSpacing: 100,
    padding: 20,
  },
  securityLevel: 'loose',
  maxTextSize: 50000,
  maxEdges: 500,
  fontSize: 16,
} as const;

// Error Messages
export const ERROR_MESSAGES = {
  API_ERROR: 'API Error',
  NETWORK_ERROR: 'Network error occurred',
  UNKNOWN_ERROR: 'An unknown error occurred',
  BACKEND_CONNECTION: 'Make sure the backend server is running on port 8000',
  GRAPH_LOAD_FAILED: 'Unable to Load Graph',
  DIAGRAM_RENDER_FAILED: 'Failed to render diagram',
  DIAGRAM_LIBRARY_FAILED: 'Failed to load diagram library',
} as const;

// Page Metadata
export const PAGE_METADATA = {
  MAIN: {
    title: 'ReplySight',
    description: 'Research-backed customer service response generation',
    sections: {
      GENERATE: {
        title: 'Generate Response',
        description: 'Enter a customer complaint to generate an empathetic, research-backed response',
      },
      RESPONSE: {
        title: 'Generated Response',
        description: 'AI-powered empathetic customer service response',
      },
    },
  },
  GRAPH: {
    title: 'Workflow Diagram',
    description: 'Interactive visualization of your Smart Study Buddy workflow',
  },
} as const; 