'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useShowstoppers } from '@/lib/hooks';

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
      // Appel API backend pour détecter showstoppers
      // Pour le moment, on utilise mock data car on a besoin de données de projet
      // TODO: Passer les vraies données du projet actif
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

      // Générer plan d'action
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

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL':
        return 'bg-red-500/10 text-red-400 border-red-500/30';
      case 'HIGH':
        return 'bg-orange-500/10 text-orange-400 border-orange-500/30';
      case 'MEDIUM':
        return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30';
      case 'LOW':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      default:
        return 'bg-gray-500/10 text-gray-400 border-gray-500/30';
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

  const getCategoryLabel = (category: string) => {
    const labels = {
      regulatory: 'Réglementaire',
      technical: 'Technique',
      financial: 'Financier',
      legal: 'Juridique'
    };
    return labels[category as keyof typeof labels] || category;
  };

  const totalCost = actionPlan.reduce((sum, item) => sum + item.estimated_cost, 0);
  const criticalCount = showstoppers.filter(s => s.severity === 'CRITICAL').length;
  const highCount = showstoppers.filter(s => s.severity === 'HIGH').length;

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Header */}
      <div className="bg-gray-900 border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">Points Bloquants</h1>
              <p className="text-gray-400 mt-1">Analyse des showstoppers du projet</p>
            </div>
            <Link
              href="/projects"
              className="px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition"
            >
              ← Retour
            </Link>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-gray-900 rounded-lg border border-gray-800 p-4">
            <div className="text-gray-400 text-sm">Total</div>
            <div className="text-3xl font-bold text-white mt-1">{showstoppers.length}</div>
          </div>
          <div className="bg-red-500/10 rounded-lg border border-red-500/30 p-4">
            <div className="text-red-400 text-sm">Critiques</div>
            <div className="text-3xl font-bold text-red-400 mt-1">{criticalCount}</div>
          </div>
          <div className="bg-orange-500/10 rounded-lg border border-orange-500/30 p-4">
            <div className="text-orange-400 text-sm">Élevés</div>
            <div className="text-3xl font-bold text-orange-400 mt-1">{highCount}</div>
          </div>
          <div className="bg-gray-900 rounded-lg border border-gray-800 p-4">
            <div className="text-gray-400 text-sm">Coût estimé</div>
            <div className="text-2xl font-bold text-white mt-1">
              {(totalCost / 1000).toFixed(0)}k€
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-6">
        <div className="border-b border-gray-800">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('list')}
              className={`pb-3 px-1 border-b-2 transition ${
                activeTab === 'list'
                  ? 'border-blue-600 text-white'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              Liste des Showstoppers
            </button>
            <button
              onClick={() => setActiveTab('plan')}
              className={`pb-3 px-1 border-b-2 transition ${
                activeTab === 'plan'
                  ? 'border-blue-600 text-white'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              Plan d'Action
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-6">
        {activeTab === 'list' && (
          <div className="space-y-4">
            {showstoppers.map((showstopper, index) => (
              <div
                key={index}
                className={`rounded-lg border p-6 ${getSeverityColor(showstopper.severity)}`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <span className="px-3 py-1 bg-gray-900 rounded-full text-sm">
                      {getCategoryLabel(showstopper.category)}
                    </span>
                    <span className="px-3 py-1 bg-gray-900 rounded-full text-sm font-semibold">
                      {getSeverityBadge(showstopper.severity)}
                    </span>
                  </div>
                </div>

                <h3 className="text-xl font-semibold text-white mb-2">
                  {showstopper.description}
                </h3>

                <div className="space-y-3 text-gray-300">
                  <div>
                    <span className="font-medium">Impact:</span> {showstopper.impact}
                  </div>
                  <div>
                    <span className="font-medium">Recommandation:</span> {showstopper.recommendation}
                  </div>
                  {showstopper.estimated_cost && (
                    <div>
                      <span className="font-medium">Coût estimé:</span>{' '}
                      {(showstopper.estimated_cost / 1000).toFixed(0)}k€
                    </div>
                  )}
                  {showstopper.estimated_delay_days && (
                    <div>
                      <span className="font-medium">Délai estimé:</span>{' '}
                      {Math.floor(showstopper.estimated_delay_days / 30)} mois
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'plan' && (
          <div className="bg-gray-900 rounded-lg border border-gray-800">
            <div className="p-6 border-b border-gray-800">
              <h2 className="text-xl font-bold text-white">Plan d'Action Priorisé</h2>
              <p className="text-gray-400 mt-1">Actions à entreprendre par ordre de priorité</p>
            </div>

            <div className="divide-y divide-gray-800">
              {actionPlan.map((item) => (
                <div key={item.priority} className="p-6 hover:bg-gray-800/50 transition">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0 w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center font-bold text-white">
                      {item.priority}
                    </div>

                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-lg font-semibold text-white">
                          {item.showstopper.description}
                        </h3>
                        <span className={`px-3 py-1 rounded-full text-sm ${getSeverityColor(item.showstopper.severity)}`}>
                          {getSeverityBadge(item.showstopper.severity)}
                        </span>
                      </div>

                      <p className="text-gray-400 mb-3">{item.action}</p>

                      <div className="flex items-center space-x-6 text-sm">
                        <div className="flex items-center space-x-2">
                          <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <span className="text-gray-400">{item.timeline}</span>
                        </div>
                        {item.estimated_cost > 0 && (
                          <div className="flex items-center space-x-2">
                            <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span className="text-gray-400">
                              {(item.estimated_cost / 1000).toFixed(0)}k€
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="p-6 bg-gray-800/50 border-t border-gray-800">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-gray-400 text-sm">Coût total estimé</div>
                  <div className="text-2xl font-bold text-white">{(totalCost / 1000).toFixed(0)}k€</div>
                </div>
                <div>
                  <div className="text-gray-400 text-sm">Durée estimée</div>
                  <div className="text-2xl font-bold text-white">6-12 mois</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
