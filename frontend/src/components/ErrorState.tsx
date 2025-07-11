import React from 'react';
import { ErrorStateProps } from '@/types';
import { UI_CONSTANTS, ERROR_MESSAGES } from '@/constants';

const ErrorState: React.FC<ErrorStateProps> = ({ 
  error, 
  onRetry, 
  variant = 'default' 
}) => {
  const gradientClass = variant === 'graph' 
    ? 'bg-gradient-to-br from-red-50 to-pink-100' 
    : 'bg-gradient-to-br from-slate-50 to-blue-50';

  const isGraphError = variant === 'graph';

  return (
    <div className={`flex items-center justify-center min-h-screen ${gradientClass}`}>
      <div className="text-center max-w-md">
        <div className="bg-red-100 rounded-full p-4 inline-block mb-4">
          <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 className="text-xl font-semibold text-gray-700 mb-2">
          {isGraphError ? ERROR_MESSAGES.GRAPH_LOAD_FAILED : 'Error'}
        </h2>
        <p className="text-gray-600 mb-4">{error}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
          >
            {UI_CONSTANTS.BUTTON_LABELS.TRY_AGAIN}
          </button>
        )}
        {isGraphError && (
          <p className="text-sm text-gray-500 mt-4">
            {ERROR_MESSAGES.BACKEND_CONNECTION}
          </p>
        )}
      </div>
    </div>
  );
};

export default ErrorState; 