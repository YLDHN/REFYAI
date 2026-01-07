'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { GlassCard } from '@/components/ui/GlassCard';
import { apiClient } from '@/lib/api';

interface Typologie {
  key: string;
  label: string;
  description: string;
  icon: string;
}

interface CAPEXEstimate {
  typologie: string;
  surface_m2: number;
  cost_per_m2: number;
  project_capex: {
    base_costs: {
      min: number;
      avg: number;
      max: number;
    };
    total_with_contingency: {
      min: number;
      avg: number;
      max: number;
    };
  };
  items_detail: Array<{
    item: string;
    unit: string;
    quantity: number;
    total_costs: {
      min: number;
      avg: number;
      max: number;
    };
  }>;
}

export default function CAPEXPage() {
  const params = useParams();
  const projectId = params?.id as string;

  const [typologies, setTypologies] = useState<Typologie[]>([]);
  const [selectedTypologie, setSelectedTypologie] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [estimate, setEstimate] = useState<CAPEXEstimate | null>(null);
  
  // Form inputs
  const [surface, setSurface] = useState(500);
  const [cityTier, setCityTier] = useState(1);
  const [constructionYear, setConstructionYear] = useState(1990);
  const [description, setDescription] = useState('');

  useEffect(() => {
    loadTypologies();
  }, []);

  const loadTypologies = async () => {
    try {
      const response = await apiClient.get('/capex/typologies');
      setTypologies(response.data.typologies);
    } catch (error) {
      console.error('Erreur chargement typologies:', error);
    }
  };

  const handleEstimate = async () => {
    if (!selectedTypologie) return;

    setLoading(true);
    try {
      const response = await apiClient.post('/capex/typologies/estimate', {
        typologie: selectedTypologie,
        surface: surface,
        city_tier: cityTier,
        construction_year: constructionYear,
        project_description: description
      });

      setEstimate(response.data);
    } catch (error) {
      console.error('Erreur estimation:', error);
      alert('Erreur lors de l\'estimation CAPEX');
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(price);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Estimation CAPEX</h1>
            <p className="text-slate-400">Estimation automatique par typologie selon Business Plan</p>
          </div>
          <Link
            href={`/projects/${projectId}`}
            className="px-4 py-2 rounded-lg bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-all text-sm font-medium"
          >
            ← Retour
          </Link>
        </div>

        {/* Typologie Selection */}
        <GlassCard className="p-6">
          <h2 className="text-xl font-bold text-white mb-4">1. Sélectionnez la typologie du projet</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {typologies.map((typo) => (
              <button
                key={typo.key}
                onClick={() => setSelectedTypologie(typo.key)}
                className={`p-6 rounded-xl border-2 transition-all text-left ${
                  selectedTypologie === typo.key
                    ? 'bg-blue-600/20 border-blue-500 shadow-[0_0_20px_rgba(59,130,246,0.3)]'
                    : 'bg-white/5 border-white/10 hover:bg-white/10 hover:border-white/20'
                }`}
              >
                <div className="text-4xl mb-3">{typo.icon}</div>
                <h3 className="text-lg font-bold text-white mb-2">{typo.label}</h3>
                <p className="text-sm text-slate-400">{typo.description}</p>
              </button>
            ))}
          </div>
        </GlassCard>

        {/* Parameters */}
        {selectedTypologie && (
          <GlassCard className="p-6">
            <h2 className="text-xl font-bold text-white mb-4">2. Paramètres du projet</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Surface (m²)
                </label>
                <input
                  type="number"
                  value={surface}
                  onChange={(e) => setSurface(Number(e.target.value))}
                  className="w-full px-4 py-3 rounded-xl glass-input text-white"
                  min="10"
                  step="10"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Zone géographique
                </label>
                <select
                  value={cityTier}
                  onChange={(e) => setCityTier(Number(e.target.value))}
                  className="w-full px-4 py-3 rounded-xl glass-input text-white appearance-none bg-no-repeat bg-[right_1rem_center]"
                  style={{ backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e")` }}
                >
                  <option value={1} className="bg-slate-900">Tier 1 (Paris, Lyon, Marseille)</option>
                  <option value={2} className="bg-slate-900">Tier 2 (Grandes villes)</option>
                  <option value={3} className="bg-slate-900">Tier 3 (Province)</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Année de construction
                </label>
                <input
                  type="number"
                  value={constructionYear}
                  onChange={(e) => setConstructionYear(Number(e.target.value))}
                  className="w-full px-4 py-3 rounded-xl glass-input text-white"
                  min="1800"
                  max={new Date().getFullYear()}
                />
              </div>
            </div>

            <div className="mt-6">
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Description additionnelle (optionnel)
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-4 py-3 rounded-xl glass-input text-white resize-none"
                rows={3}
                placeholder="Ex: Immeuble haussmannien avec façade pierre de taille..."
              />
            </div>

            <button
              onClick={handleEstimate}
              disabled={loading}
              className="mt-6 w-full md:w-auto px-8 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-blue-500 text-white font-semibold shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {loading ? 'Calcul en cours...' : '🤖 Estimer automatiquement'}
            </button>
          </GlassCard>
        )}

        {/* Results */}
        {estimate && (
          <>
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <GlassCard className="p-6 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 border-blue-500/20">
                <p className="text-blue-300 text-sm mb-1">Budget Minimum</p>
                <p className="text-3xl font-bold text-white">
                  {formatPrice(estimate.project_capex.total_with_contingency.min)}
                </p>
              </GlassCard>

              <GlassCard className="p-6 bg-gradient-to-br from-emerald-500/10 to-teal-500/10 border-emerald-500/20">
                <p className="text-emerald-300 text-sm mb-1">Budget Moyen (recommandé)</p>
                <p className="text-3xl font-bold text-white">
                  {formatPrice(estimate.project_capex.total_with_contingency.avg)}
                </p>
                <p className="text-sm text-emerald-400 mt-1">
                  {formatPrice(estimate.cost_per_m2)}/m²
                </p>
              </GlassCard>

              <GlassCard className="p-6 bg-gradient-to-br from-amber-500/10 to-orange-500/10 border-amber-500/20">
                <p className="text-amber-300 text-sm mb-1">Budget Maximum</p>
                <p className="text-3xl font-bold text-white">
                  {formatPrice(estimate.project_capex.total_with_contingency.max)}
                </p>
              </GlassCard>
            </div>

            {/* Detailed Items List */}
            <GlassCard className="p-6">
              <h2 className="text-xl font-bold text-white mb-4">
                Détail des postes - {typologies.find(t => t.key === estimate.typologie)?.label}
              </h2>
              <p className="text-sm text-slate-400 mb-6">
                Format liste (sans astérisques) - {estimate.items_detail.length} postes identifiés
              </p>

              <div className="space-y-3">
                {estimate.items_detail.map((item, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-4 rounded-lg bg-white/5 hover:bg-white/10 transition-colors border border-white/5"
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 text-xs font-bold">
                          {index + 1}
                        </span>
                        <span className="text-white font-medium">{item.item.replace(/_/g, ' ')}</span>
                      </div>
                      <div className="ml-9 mt-1 flex items-center gap-4 text-sm">
                        <span className="text-slate-400">
                          {item.quantity} {item.unit}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-white font-bold">{formatPrice(item.total_costs.avg)}</div>
                      <div className="text-xs text-slate-500">
                        {formatPrice(item.total_costs.min)} - {formatPrice(item.total_costs.max)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6 pt-6 border-t border-white/10">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-slate-400">Sous-total travaux</span>
                  <span className="text-lg font-semibold text-white">
                    {formatPrice(estimate.project_capex.base_costs.avg)}
                  </span>
                </div>
                <div className="flex justify-between items-center mb-3">
                  <span className="text-slate-400">Aléas (10%)</span>
                  <span className="text-lg font-semibold text-white">
                    {formatPrice(estimate.project_capex.total_with_contingency.avg - estimate.project_capex.base_costs.avg)}
                  </span>
                </div>
                <div className="flex justify-between items-center pt-3 border-t border-white/10">
                  <span className="text-white font-bold text-lg">TOTAL avec aléas</span>
                  <span className="text-2xl font-bold text-emerald-400">
                    {formatPrice(estimate.project_capex.total_with_contingency.avg)}
                  </span>
                </div>
              </div>
            </GlassCard>

            {/* Info Note */}
            <GlassCard className="p-4 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border-blue-500/20">
              <div className="flex items-start gap-3">
                <div className="text-2xl">💡</div>
                <div className="text-sm text-slate-300">
                  <p className="font-semibold text-white mb-1">Note importante</p>
                  <p>Cette estimation est générée automatiquement par l'IA selon la typologie sélectionnée et les paramètres saisis. Les quantités sont calculées selon les standards du marché français. Nous recommandons de valider ces estimations avec des devis réels avant financement.</p>
                </div>
              </div>
            </GlassCard>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
