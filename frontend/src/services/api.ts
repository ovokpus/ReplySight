import { API_BASE_URL, API_ENDPOINTS, UI_CONFIG } from '@/constants';

export interface ComplaintRequest {
  complaint: string;
  customer_info?: Record<string, any>;
}

export interface ResponseOutput {
  reply: string;
  citations: string[];
  latency_ms: number;
}

export interface WorkflowGraphResponse {
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

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async generateResponse(complaint: string): Promise<ResponseOutput> {
    const request: ComplaintRequest = {
      complaint: complaint.trim(),
      customer_info: {}
    };

    const response = await fetch(`${this.baseUrl}${API_ENDPOINTS.respond}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async getWorkflowGraph(): Promise<WorkflowGraphResponse> {
    const response = await fetch(`${this.baseUrl}${API_ENDPOINTS.workflowGraph}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<{ status: string; service: string; version: string }> {
    const response = await fetch(`${this.baseUrl}${API_ENDPOINTS.health}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return response.json();
  }

  // Utility method to check if API is available
  async isApiAvailable(): Promise<boolean> {
    try {
      await this.healthCheck();
      return true;
    } catch {
      return false;
    }
  }

  // Get current API base URL (useful for debugging)
  getApiBaseUrl(): string {
    return this.baseUrl;
  }
}

export const apiService = new ApiService();

// Standalone functions for hooks that expect them
export const generateResponse = async (complaint: string): Promise<ResponseOutput> => {
  return apiService.generateResponse(complaint);
};

export const fetchGraphData = async (): Promise<WorkflowGraphResponse> => {
  return apiService.getWorkflowGraph();
}; 