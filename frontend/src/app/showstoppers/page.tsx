'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useShowstoppers } from '@/lib/hooks';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { GlassCard } from '@/components/ui/GlassCard';

interface Showstopper {
  category: string;
  type: string;
  severity: string;
  description: string;
  impact: string;
  recommendation: string;
  estimated_cost?: number;
  estimated_delay_days?: number;
}

interface ActionPlanItem {
  priority: number;
  showstopper: Showstopper;
  action: string;
  timeline: string;
  estimated_cost: number;
}

export default function ShowstoppersPage() {
  const { detectShowstoppers, getActionPlan } = useShowstoppers();
  const [showstoppers, setShowstoppers] = useState<Showstopper[]>([]);
  const [actionPlan, setActionPlan] = useState<ActionPlanItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'list' | 'plan'>('list');

  useEffect(() => {
    loadShowstoppers();
  }, []);

  const loadShowstoppers = async () => {
    setLoading(true);
    try {
      // Mock data remains same as before until real backend hookup
      const mockShowstoppers: Showstopper[] = [
        {
          category: 'regulatory',
          type: 'zone_non_constructible',
          severity: 'CRITICAL',
          description: 'Zone non constructible (Zone N)',
          impact: 'Projet impossible en l\'état actuel',
          recommendation: 'Demander modification PLU ou changer de terrain',
          estimated_delay_days: 180
        },
        {
          category: 'regulatory',
          type: 'abf_required',
          severity: 'HIGH',
          description: 'Avis ABF obligatoire',
          impact: 'Délais administratifs prolongés (+3-6 mois)',
          recommendation: 'Prévoir consultation ABF en amont du dépôt PC',
          estimated_delay_days: 120
        },
        {
          category: 'technical',
          type: 'structure_risk',
          severity: 'HIGH',
          description: 'Risque structurel majeur',
          impact: 'Travaux de reprise importants requis',
          recommendation: 'Étude structure BET + devis détaillé',
          estimated_cost: 80000
        },
        {
          category: 'financial',
          type: 'tri_insufficient',
          severity: 'MEDIUM',
          description: 'TRI insuffisant (7.2% < 10%)',
          impact: 'Rentabilité faible',
          recommendation: 'Renégocier prix achat ou revoir budget travaux',
          estimated_cost: 50000
        }
      ];

      setShowstoppers(mockShowstoppers);

      const mockPlan: ActionPlanItem[] = mockShowstoppers.map((s, i) => ({
        priority: i + 1,
        showstopper: s,
        action: s.recommendation,
        timeline: s.estimated_delay_days ? `${Math.floor(s.estimated_delay_days / 30)} mois` : '2-4 semaines',
        estimated_cost: s.estimated_cost || 0
      }));

      setActionPlan(mockPlan);
    } catch (error) {
      console.error('Erreur:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityStyle = (severity: string) => {
    switch (severity) {
      case 'CRITICAL':
        return 'bg-red-500/10 border-red-500/30 text-red-400';
      case 'HIGH':
        return 'bg-orange-500/10 border-orange-500/30 text-orange-400';
      case 'MEDIUM':
        return 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400';
      case 'LOW':
        return 'bg-blue-500/10 border-blue-500/30 text-blue-400';
      default:
        return 'bg-slate-500/10 border-slate-500/30 text-slate-400';
    }
  };

  const getSeverityBadge = (severity: string) => {
    const labels = {
      CRITICAL: 'Critique',
      HIGH: 'Élevé',
      MEDIUM: 'Moyen',
      LOW: 'Faible'
    };
    return labels[severity as keyof typeof labels] || severity;
  };

  const totalCost = actionPlan.reduce((sum, item) => sum + item.estimated_cost, 0);
  const criticalCount = showstoppers.filter(s => s.severity === 'CRITICAL').length;
  const highCount = showstoppers.filter(s => s.severity === 'HIGH').length;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Points Bloquants</h1>
            <p className="text-slate-400">Analyse des risques et showstoppers du projet</p>
          </div>
          <Link
            href="/analyses"
            className="px-4 py-2 rounded-lg bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-all text-sm font-medium"
          >
            ← Retour
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <GlassCard className="p-4">
            <p className="text-slate-400 text-sm mb-1">Total Détecté</p>
            <p className="text-2xl font-bold text-white">{showstoppers.length}</p>
          </GlassCard>
          <GlassCard className="p-4 bg-red-500/5 border-red-500/20">
            <p className="text-red-400 text-sm mb-1">Critiques</p>
            <p className="text-2xl font-bold text-white">{criticalCount}</p>
          </GlassCard>
           <GlassCard className="p-4 bg-orange-500/5 border-orange-500/20">
            <p className="text-orange-400 text-sm mb-1">Élevés</p>
            <p className="text-2xl font-bold text-white">{highCount}</p>
          </GlassCard>
          <GlassCard className="p-4">
            <p className="text-slate-400 text-sm mb-1">Coût Estimé</p>
            <p className="text-2xl font-bold text-white">{(totalCost / 1000).toFixed(0)}k€</p>
          </GlassCard>
        </div>

        {/* Tabs */}
        <div className="flex space-x-2 border-b border-white/10 pb-1">
          <button
            onClick={() => setActiveTab('list')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
              activeTab === 'list' 
                ? 'bg-blue-500/20 text-blue-300 shadow-[0_0_20px_rgba(59,130,246,0.1)]' 
                : 'text-slate-400 hover:text-white hover:bg-white/5'
            }`}
          >
            Liste des Risques
          </button>
          <button
            onClick={() => setActiveTab('plan')}
             className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
              activeTab === 'plan' 
                ? 'bg-blue-500/20 text-blue-300 shadow-[0_0_20px_rgba(59,130,246,0.1)]' 
                : 'text-slate-400 hover:text-white hover:bg-white/5'
            }`}
          >
            Plan d'Action
          </button>
        </div>

        {/* Content */}
        {activeTab === 'list' && (
          <div className="grid grid-cols-1 gap-4">
            {showstoppers.map((showstopper, index) => (
              <GlassCard key={index} className={`p-6 border-l-4 ${
                  showstopper.severity === 'CRITICAL' ? 'border-l-red-500' : 
                  showstopper.severity === 'HIGH' ? 'border-l-orange-500' : 
                  'border-l-yellow-500'
              }`}>
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-4">
                    <div>
                        <div className="flex items-center gap-3 mb-2">
                             <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium border ${getSeverityStyle(showstopper.severity)}`}>
                                {getSeverityBadge(showstopper.severity)}
                             </span>
                            <span className="text-sm text-slate-400 uppercase tracking-wider">{showstopper.category}</span>
                        </div>
                        <h3 className="text-xl font-bold text-white">{showstopper.description}</h3>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                    <div className="space-y-2">
                         <div className="flex gap-2">
                            <span className="text-slate-400 w-24 flex-shrink-0">Impact:</span>
                            <span className="text-slate-200">{showstopper.impact}</span>
                         </div>
                         <div className="flex gap-2">
                            <span className="text-slate-400 w-24 flex-shrink-0">Recommandation:</span>
                            <span className="text-emerald-400">{showstopper.recommendation}</span>
                         </div>
                    </div>
                    <div className="space-y-2">
                        {showstopper.estimated_cost && (
                             <div className="flex gap-2">
                                <span className="text-slate-400 w-24 flex-shrink-0">Coût estimé:</span>
                                <span className="text-white font-medium">{(showstopper.estimated_cost / 1000).toFixed(0)}k€</span>
                             </div>
                        )}
                         {showstopper.estimated_delay_days && (
                             <div className="flex gap-2">
                                <span className="text-slate-400 w-24 flex-shrink-0">Délai estimé:</span>
                                <span className="text-white font-medium">{Math.floor(showstopper.estimated_delay_days / 30)} mois</span>
                             </div>
                        )}
                    </div>
                </div>
              </GlassCard>
            ))}
          </div>
        )}

        {activeTab === 'plan' && (
          <GlassCard className="overflow-hidden">
             <div className="p-6 border-b border-white/10">
                <h2 className="text-lg font-semibold text-white">Actions Recommandées</h2>
                <p className="text-slate-400 text-sm mt-1">Plan priorisé pour débloquer le projet</p>
             </div>
             
             <div className="divide-y divide-white/5">
                {actionPlan.map((item) => (
                    <div key={item.priority} className="p-6 hover:bg-white/5 transition-colors group">
                        <div className="flex items-start gap-4">
                            <div className="w-10 h-10 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-lg border border-blue-500/10 flex-shrink-0">
                                {item.priority}
                            </div>
                            <div className="flex-1">
                                <div className="flex items-center justify-between mb-2">
                                    <h3 className="text-white font-medium text-lg">{item.action}</h3>
                                     <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getSeverityStyle(item.showstopper.severity)}`}>
                                        {getSeverityBadge(item.showstopper.severity)}
                                     </span>
                                </div>
                                <p className="text-slate-400 text-sm mb-3">Pour résoudre : <span className="text-slate-300 italic">{item.showstopper.description}</span></p>
                                
                                <div className="flex items-center gap-6 text-sm">
                                    <div className="flex items-center gap-2 text-slate-500">
                                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                                        {item.timeline}
                                    </div>
                                    {item.estimated_cost > 0 && (
                                        <div className="flex items-center gap-2 text-slate-500">
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                                            {(item.estimated_cost / 1000).toFixed(0)}k€
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
             </div>
          </GlassCard>
        )}
      </div>
    </DashboardLayout>
  );
}
