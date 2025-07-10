import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { UI_CONSTANTS } from '@/constants';

interface PageHeaderProps {
  title: string;
  description: string;
  status?: string;
  showWorkflowButton?: boolean;
  onRefresh?: () => void;
}

const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  description,
  status = UI_CONSTANTS.STATUS_LABELS.ACTIVE,
  showWorkflowButton = false,
  onRefresh,
}) => {
  return (
    <div className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
            <p className="text-gray-600 mt-1">{description}</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              {status}
            </div>
            {showWorkflowButton && (
              <Link href="/workflow">
                <Button variant="outline">
                  {UI_CONSTANTS.BUTTON_LABELS.VIEW_WORKFLOW}
                </Button>
              </Link>
            )}
            {onRefresh && (
              <Button onClick={onRefresh}>
                {UI_CONSTANTS.BUTTON_LABELS.REFRESH}
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PageHeader; 