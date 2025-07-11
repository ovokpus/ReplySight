import React from 'react';
import StatCard, { IconName } from './StatCard';
import { STATS_CARDS } from '@/constants';

interface StatsGridProps {
  statsData?: typeof STATS_CARDS;
}

const StatsGrid: React.FC<StatsGridProps> = ({ 
  statsData = STATS_CARDS 
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      {statsData.map((stat, index) => (
        <StatCard
          key={index}
          icon={stat.icon as IconName}
          label={stat.label}
          value={stat.value}
          color={stat.color}
        />
      ))}
    </div>
  );
};

export default StatsGrid; 