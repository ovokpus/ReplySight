import React from 'react';
import { 
  MessageSquareIcon, 
  BookOpenIcon, 
  ZapIcon, 
  TrendingUpIcon,
  ClockIcon,
  CheckCircleIcon,
  ServerIcon,
  UsersIcon,
} from 'lucide-react';
import { StatCardProps, ColorVariant } from '@/types';

// Icon mapping for string-based icon props
export const iconMap = {
  MessageSquare: MessageSquareIcon,
  BookOpen: BookOpenIcon,
  Zap: ZapIcon,
  TrendingUp: TrendingUpIcon,
  Clock: ClockIcon,
  CheckCircle: CheckCircleIcon,
  Server: ServerIcon,
  Users: UsersIcon,
} as const;

export type IconName = keyof typeof iconMap;

// Color variant mapping
const colorVariants: Record<ColorVariant, string> = {
  blue: 'bg-blue-100 text-blue-600',
  green: 'bg-green-100 text-green-600',
  purple: 'bg-purple-100 text-purple-600',
  yellow: 'bg-yellow-100 text-yellow-600',
  red: 'bg-red-100 text-red-600',
};

interface StatCardComponentProps extends Omit<StatCardProps, 'icon'> {
  icon: IconName;
}

const StatCard: React.FC<StatCardComponentProps> = ({ 
  icon, 
  label, 
  value, 
  color 
}) => {
  const IconComponent = iconMap[icon];
  const colorClass = colorVariants[color];

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
      <div className="flex items-center">
        <div className={`p-2 rounded-lg ${colorClass}`}>
          <IconComponent className="w-6 h-6" />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{label}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  );
};

export default StatCard; 