import React from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  hoverEffect?: boolean;
}

export const GlassCard = ({ children, className = '', hoverEffect = false }: GlassCardProps) => {
  return (
    <div className={`
      glass-card rounded-2xl p-6 
      transition-all duration-300
      ${hoverEffect ? 'hover:shadow-sky-500/10 hover:border-sky-500/30 hover:-translate-y-1' : ''}
      ${className}
    `}>
      {children}
    </div>
  );
};
