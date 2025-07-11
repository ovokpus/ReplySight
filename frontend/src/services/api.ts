import { API_BASE_URL, API_ENDPOINTS, UI_CONFIG } from '@/constants';

export interface ComplaintRequest {
  complaint: string;
  customer_info?: Record<string, any>;
}

export interface ResponseOutput {
  response: string;
  latency_ms: number;
  status: string;
  citations?: Array<{
    title: string;
    url: string;
    source: string;
  }>;
}

export interface WorkflowGraphResponse {
  mermaid: string;
  metadata: {
    version: string;
    status: string;
    note?: string;
  };
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