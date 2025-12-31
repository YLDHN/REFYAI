import React from 'react';
import { GlassCard } from '@/components/ui/GlassCard';

export const MetricsPreview = () => {
  const metrics = [
    { label: 'TRI Projet', value: '15.4%', trend: '+2.1%', color: 'text-emerald-400' },
    { label: 'Marge Nette', value: '235k€', trend: 'High', color: 'text-blue-400' },
    { label: 'DSCR', value: '1.45', trend: 'Safe', color: 'text-purple-400' },
  ];

  return (
    <div className="relative w-full max-w-sm mx-auto perspective-1000">
      <div className="absolute -top-10 -right-10 w-32 h-32 bg-purple-500 rounded-full blur-[50px] opacity-40 animate-pulse" />
      <div className="absolute -bottom-10 -left-10 w-32 h-32 bg-blue-500 rounded-full blur-[50px] opacity-40 animate-pulse delay-700" />
      
      <GlassCard className="relative z-10 border-t border-l border-white/20">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-white font-semibold">Performance</h3>
          <span className="text-xs text-blue-200 bg-blue-500/20 px-2 py-1 rounded-full border border-blue-500/30">
            Live Analysis
          </span>
        </div>

        <div className="space-y-4">
          {metrics.map((m, i) => (
            <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
              <div>
                <p className="text-gray-400 text-xs">{m.label}</p>
                <p className={`font-bold ${m.color}`}>{m.value}</p>
              </div>
              <div className="text-xs text-gray-400 text-right">
                <span className="block mb-1 opacity-50">Trend</span>
                <span className="text-white">{m.trend}</span>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 pt-4 border-t border-white/10">
          <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 w-3/4" />
          </div>
          <div className="flex justify-between mt-2 text-xs text-gray-500">
            <span>Score de faisabilité</span>
            <span className="text-white">85/100</span>
          </div>
        </div>
      </GlassCard>
    </div>
  );
};
