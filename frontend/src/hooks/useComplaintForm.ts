import { useState, useCallback } from 'react';
import { generateResponse, ResponseOutput } from '@/services/api';
import { APP_CONFIG } from '@/constants';

export interface UseComplaintFormReturn {
  // State
  complaint: string;
  response: ResponseOutput | null;
  loading: boolean;
  error: string;
  
  // Actions
  setComplaint: (complaint: string) => void;
  handleSubmit: (e: React.FormEvent) => Promise<void>;
  clearForm: () => void;
}

export const useComplaintForm = (): UseComplaintFormReturn => {
  const [complaint, setComplaint] = useState('');
  const [response, setResponse] = useState<ResponseOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!complaint.trim() || complaint.trim().length < APP_CONFIG.MIN_COMPLAINT_LENGTH) {
      return;
    }

    setLoading(true);
    setError('');
    setResponse(null);

    try {
      const data = await generateResponse(complaint);
      setResponse(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [complaint]);

  const clearForm = useCallback(() => {
    setComplaint('');
    setResponse(null);
    setError('');
  }, []);

  return {
    complaint,
    response,
    loading,
    error,
    setComplaint,
    handleSubmit,
    clearForm,
  };
}; 