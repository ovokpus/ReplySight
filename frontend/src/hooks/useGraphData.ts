import { useState, useEffect, useCallback } from 'react';
import { GraphData } from '@/types';
import { fetchGraphData } from '@/services/api';
import { API_ENDPOINTS } from '@/constants';

export interface UseGraphDataReturn {
  // State
  graphData: GraphData | null;
  loading: boolean;
  error: string | null;
  
  // Actions
  refresh: () => void;
  setError: (error: string | null) => void;
}

export const useGraphData = (apiUrl: string = API_ENDPOINTS.WORKFLOW_GRAPH): UseGraphDataReturn => {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const data = await fetchGraphData();
      setGraphData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  }, []);

  const refresh = useCallback(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return {
    graphData,
    loading,
    error,
    refresh,
    setError,
  };
}; 