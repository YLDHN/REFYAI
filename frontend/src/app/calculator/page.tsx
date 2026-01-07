'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { interestRateAPI } from '@/lib/api';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { GlassCard } from '@/components/ui/GlassCard';

interface RiskFactor {
  name: string;
  score: number;
  weight: number;
  description: string;
}

interface InterestRateResult {
  euribor_rate: number;
  risk_score: number;
  margin: number;
  final_rate: number;
  category: string;
  factors: RiskFactor[];
}

export default function CalculatorPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<InterestRateResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [city, setCity] = useState('Paris');
  const [ltv, setLtv] = useState(70);
  const [tri, setTri] = useState(12);
  const [showstoppers, setShowstoppers] = useState(0);
  const [experience, setExperience] = useState('intermediate');
  const [projectType, setProjectType] = useState('restructuration_lourde');
  const [complexity, setComplexity] = useState('moderate');

  useEffect(() => {
    calculateInterestRate();
  }, []);

  const calculateInterestRate = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await interestRateAPI.calculate({
        city,
        ltv,
        tri,
        showstoppers_count: showstoppers,
        company_experience: experience,
        project_type: projectType,
        complexity
      });

      setResult(response.data);
    } catch (err: any) {
      console.error('Erreur:', err);
      // Fallback vers données mockées en cas d'erreur
      const mockResult: InterestRateResult = {
        euribor_rate: 3.45,
        risk_score: 65,
        margin: 2.8,
        final_rate: 6.25,
        category: 'Moyen',
        factors: [
          { name: 'LTV', score: 70, weight: 20, description: `LTV de ${ltv}% considéré modéré` },
          { name: 'TRI', score: 80, weight: 25, description: `TRI de ${tri}% excellent` },
          { name: 'Showstoppers', score: showstoppers > 0 ? 40 : 100, weight: 15, description: `${showstoppers} point(s) bloquant(s)` },
          { name: 'Localisation', score: city === 'Paris' ? 90 : 70, weight: 15, description: `Marché ${city}` },
          { name: 'Expérience', score: experience === 'expert' ? 90 : experience === 'intermediate' ? 70 : 50, weight: 10, description: `Promoteur ${experience}` },
          { name: 'Type Projet', score: projectType === 'rehabilitation_legere' ? 80 : 60, weight: 10, description: projectType.replace(/_/g, ' ') },
          { name: 'Complexité', score: complexity === 'simple' ? 90 : complexity === 'moderate' ? 70 : 50, weight: 5, description: `Projet ${complexity}` }
        ]
      };
      setResult(mockResult);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'Excellent': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
      case 'Bon': return 'text-blue-400 bg-blue-500/10 border-blue-500/30';
      case 'Moyen': return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
      case 'Risqué': return 'text-red-400 bg-red-500/10 border-red-500/30';
      default: return 'text-slate-400 bg-slate-500/10 border-slate-500/30';
    }
  };

  const getRiskScoreColor = (score: number) => {
    if (score >= 80) return 'bg-emerald-500';
    if (score >= 60) return 'bg-blue-500';
    if (score >= 40) return 'bg-amber-500';
    return 'bg-red-500';
  };

  const getRiskTextColor = (score: number) => {
    if (score >= 80) return 'text-emerald-400';
    if (score >= 60) return 'text-blue-400';
    if (score >= 40) return 'text-amber-400';
    return 'text-red-400';
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Calculateur de Taux</h1>
            <p className="text-slate-400">Simulation du taux d'intérêt basé sur le profil de risque</p>
          </div>
          <Link
            href="/analyses"
            className="px-4 py-2 rounded-lg bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-all text-sm font-medium"
          >
            ← Retour
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Form */}
          <div className="lg:col-span-4 space-y-6">
            <GlassCard className="p-6">
              <h2 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                <span className="w-8 h-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center text-sm">⚙️</span>
                Paramètres
              </h2>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Ville</label>
                  <select
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-lg glass-input text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 appearance-none bg-no-repeat bg-[right_1rem_center]"
                    style={{ backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e")` }}
                  >
                    <option value="Paris" className="bg-slate-900">Paris</option>
                    <option value="Lyon" className="bg-slate-900">Lyon</option>
                    <option value="Marseille" className="bg-slate-900">Marseille</option>
                    <option value="Bordeaux" className="bg-slate-900">Bordeaux</option>
                    <option value="Toulouse" className="bg-slate-900">Toulouse</option>
                    <option value="Nice" className="bg-slate-900">Nice</option>
                  </select>
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-sm font-medium text-slate-300">LTV (Loan-to-Value)</label>
                    <span className="text-sm font-bold text-blue-400">{ltv}%</span>
                  </div>
                  <input
                    type="range"
                    min="40"
                    max="90"
                    step="5"
                    value={ltv}
                    onChange={(e) => setLtv(Number(e.target.value))}
                    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
                  />
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-sm font-medium text-slate-300">TRI Cible</label>
                    <span className="text-sm font-bold text-emerald-400">{tri}%</span>
                  </div>
                  <input
                    type="range"
                    min="5"
                    max="20"
                    step="0.5"
                    value={tri}
                    onChange={(e) => setTri(Number(e.target.value))}
                    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Points Bloquants</label>
                  <input
                    type="number"
                    min="0"
                    max="10"
                    value={showstoppers}
                    onChange={(e) => setShowstoppers(Number(e.target.value))}
                    className="w-full px-4 py-2.5 rounded-lg glass-input text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Expérience</label>
                  <select
                    value={experience}
                    onChange={(e) => setExperience(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-lg glass-input text-white appearance-none bg-no-repeat bg-[right_1rem_center]"
                    style={{ backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e")` }}
                  >
                    <option value="beginner" className="bg-slate-900">Débutant (&lt; 2 projets)</option>
                    <option value="intermediate" className="bg-slate-900">Intermédiaire (2-5 projets)</option>
                    <option value="expert" className="bg-slate-900">Expert (&gt; 5 projets)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Type de Projet</label>
                  <select
                    value={projectType}
                    onChange={(e) => setProjectType(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-lg glass-input text-white appearance-none bg-no-repeat bg-[right_1rem_center]"
                    style={{ backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e")` }}
                  >
                    <option value="rehabilitation_legere" className="bg-slate-900">Réhabilitation Légère</option>
                    <option value="restructuration_lourde" className="bg-slate-900">Restructuration Lourde</option>
                    <option value="construction_neuve" className="bg-slate-900">Construction Neuve</option>
                    <option value="marchand_de_biens" className="bg-slate-900">Marchand de Biens</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Complexité</label>
                  <select
                    value={complexity}
                    onChange={(e) => setComplexity(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-lg glass-input text-white appearance-none bg-no-repeat bg-[right_1rem_center]"
                    style={{ backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e")` }}
                  >
                    <option value="simple" className="bg-slate-900">Simple</option>
                    <option value="moderate" className="bg-slate-900">Modérée</option>
                    <option value="complex" className="bg-slate-900">Complexe</option>
                    <option value="very_complex" className="bg-slate-900">Très Complexe</option>
                  </select>
                </div>

                <button
                  onClick={calculateInterestRate}
                  disabled={loading}
                  className="w-full px-6 py-3 rounded-lg bg-gradient-to-r from-blue-600 to-blue-500 text-white font-medium shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                  {loading ? 'Calcul en cours...' : 'Recalculer'}
                </button>
              </div>
            </GlassCard>
          </div>

          {/* Results */}
          <div className="lg:col-span-8 space-y-6">
            {result && (
              <>
                <GlassCard className={`p-8 relative overflow-hidden ${getCategoryColor(result.category).split(' ')[1]}`}>
                  <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl -mr-32 -mt-32"></div>
                  
                  <div className="flex items-center justify-between mb-8 relative z-10">
                    <div>
                      <h2 className="text-sm font-medium text-slate-300 uppercase tracking-widest mb-1">Taux estimé</h2>
                      <div className="text-6xl font-bold text-white tracking-tight">
                        {result.final_rate.toFixed(2)}<span className="text-3xl text-slate-400 font-normal">%</span>
                      </div>
                    </div>
                    <div className={`px-4 py-2 rounded-xl border text-sm font-bold uppercase tracking-wider ${getCategoryColor(result.category)}`}>
                      {result.category}
                    </div>
                  </div>

                  <div className="flex items-center gap-8 relative z-10">
                    <div className="px-4 py-3 rounded-lg bg-black/20 backdrop-blur-sm border border-white/5">
                      <span className="block text-xs text-slate-400 mb-1">Euribor</span>
                      <span className="text-lg font-semibold text-white">{result.euribor_rate.toFixed(2)}%</span>
                    </div>
                    <div className="text-slate-500">+</div>
                    <div className="px-4 py-3 rounded-lg bg-black/20 backdrop-blur-sm border border-white/5">
                      <span className="block text-xs text-slate-400 mb-1">Marge de Risque</span>
                      <span className="text-lg font-semibold text-white">{result.margin.toFixed(2)}%</span>
                    </div>
                  </div>
                </GlassCard>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Risk Score */}
                  <GlassCard className="p-6">
                    <h3 className="text-lg font-semibold text-white mb-6">Score de Risque</h3>
                    
                    <div className="relative mb-8 pt-4">
                      <div className="h-4 bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className={`h-full transition-all duration-1000 ease-out ${getRiskScoreColor(result.risk_score)}`}
                          style={{ width: `${result.risk_score}%` }}
                        />
                      </div>
                      <div className="absolute top-0 right-0 -mt-8">
                         <span className={`text-2xl font-bold ${getRiskTextColor(result.risk_score)}`}>{result.risk_score}</span>
                         <span className="text-slate-500 text-sm">/100</span>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Détail des facteurs</p>
                      {result.factors.map((factor, index) => (
                        <div key={index} className="group">
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="text-sm text-slate-300">{factor.name}</span>
                            <span className={`text-sm font-medium ${getRiskTextColor(factor.score)}`}>{factor.score}</span>
                          </div>
                          <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                             <div 
                                className={`h-full ${getRiskScoreColor(factor.score)} opacity-50 group-hover:opacity-100 transition-opacity`}
                                style={{ width: `${factor.score}%` }}
                             />
                          </div>
                        </div>
                      ))}
                    </div>
                  </GlassCard>

                  {/* Recommendations */}
                  <GlassCard className="p-6">
                    <h3 className="text-lg font-semibold text-white mb-6">Recommandations</h3>
                    <ul className="space-y-4">
                      {result.category === 'Risqué' && (
                        <>
                          <li className="flex gap-3 text-sm text-slate-300">
                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-red-500/20 text-red-400 flex items-center justify-center">!</span>
                            Envisager de réduire le LTV pour améliorer le profil de risque.
                          </li>
                          <li className="flex gap-3 text-sm text-slate-300">
                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-red-500/20 text-red-400 flex items-center justify-center">!</span>
                            Résoudre les showstoppers critiques avant financement.
                          </li>
                        </>
                      )}
                      
                       {(result.category === 'Bon' || result.category === 'Excellent') && (
                        <>
                          <li className="flex gap-3 text-sm text-slate-300">
                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center">✓</span>
                            Profil favorable pour négocier avec plusieurs banques.
                          </li>
                          <li className="flex gap-3 text-sm text-slate-300">
                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center">✓</span>
                            Potentiel de marge de négociation à la baisse (-0.2% à -0.3%).
                          </li>
                        </>
                      )}
                      
                      {result.category === 'Moyen' && (
                         <li className="flex gap-3 text-sm text-slate-300">
                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center">i</span>
                            Améliorez la documentation du projet pour rassurer les banquiers.
                          </li>
                      )}
                    </ul>
                  </GlassCard>
                </div>
              </>
            )}

            {error && (
              <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 flex items-center gap-3 text-red-400">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                {error}
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
