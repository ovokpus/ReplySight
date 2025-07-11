import { ApiResponse, ComplaintRequest, GraphData } from '@/types';
import { API_ENDPOINTS, APP_CONFIG, ERROR_MESSAGES } from '@/constants';

// Base API class with common functionality
class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = '') {
    // Use environment variable or default to current origin for Vercel deployment
    this.baseUrl = baseUrl || process.env.NEXT_PUBLIC_API_BASE_URL || '';
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      throw new Error(`${ERROR_MESSAGES.API_ERROR}: ${response.status}`);
    }
    return response.json();
  }

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    const finalOptions = { ...defaultOptions, ...options };

    try {
      const response = await fetch(url, finalOptions);
      return this.handleResponse<T>(response);
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error(ERROR_MESSAGES.UNKNOWN_ERROR);
    }
  }

  // Generate response from complaint
  async generateResponse(complaint: string): Promise<ApiResponse> {
    const request: ComplaintRequest = {
      complaint: complaint.trim(),
      customer_id: APP_CONFIG.DEFAULT_CUSTOMER_ID,
      priority: APP_CONFIG.DEFAULT_PRIORITY,
    };

    return this.makeRequest<ApiResponse>(API_ENDPOINTS.RESPOND, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Fetch workflow graph data
  async fetchGraphData(): Promise<GraphData> {
    return this.makeRequest<GraphData>(API_ENDPOINTS.WORKFLOW_GRAPH);
  }
}

// Export singleton instance
export const apiService = new ApiService();

// Export individual functions for convenience
export const generateResponse = (complaint: string) => 
  apiService.generateResponse(complaint);

export const fetchGraphData = () => 
  apiService.fetchGraphData();

// Export the class for testing or custom instances
export { ApiService }; 