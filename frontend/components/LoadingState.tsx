import React from 'react';
import { LoadingStateProps } from '@/types';
import { UI_CONSTANTS } from '@/constants';

const LoadingState: React.FC<LoadingStateProps> = ({ 
  message, 
  description, 
  variant = 'default' 
}) => {
  const gradientClass = variant === 'graph' 
    ? 'bg-gradient-to-br from-blue-50 to-indigo-100' 
    : 'bg-gradient-to-br from-slate-50 to-blue-50';

  return (
    <div className={`flex items-center justify-center min-h-screen ${gradientClass}`}>
      <div className="text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mx-auto mb-4"></div>
        <h2 className="text-xl font-semibold text-gray-700">
          {message || UI_CONSTANTS.LOADING_MESSAGES.LOADING_LIBRARY}
        </h2>
        <p className="text-gray-500 mt-2">
          {description || 'Fetching your beautiful visualization'}
        </p>
      </div>
    </div>
  );
};

export default LoadingState; 