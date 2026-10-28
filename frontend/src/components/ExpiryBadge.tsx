import React from 'react';

interface ExpiryBadgeProps {
  days: number;
}

export const ExpiryBadge: React.FC<ExpiryBadgeProps> = ({ days }) => {
  if (days <= 2) {
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-red-100 text-red-800 border border-red-300">
        <span className="w-1.5 h-1.5 mr-1.5 bg-red-600 rounded-full animate-pulse"></span>
        {days <= 0 ? 'Expired Today' : `${days}d left (Use Now!)`}
      </span>
    );
  } else if (days <= 4) {
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-300">
        <span className="w-1.5 h-1.5 mr-1.5 bg-amber-600 rounded-full"></span>
        {days}d left (Use soon)
      </span>
    );
  } else {
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-300">
        <span className="w-1.5 h-1.5 mr-1.5 bg-emerald-500 rounded-full"></span>
        {days}d fresh
      </span>
    );
  }
};
