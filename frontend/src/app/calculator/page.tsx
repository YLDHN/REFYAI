'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { interestRateAPI } from '@/lib/api';
import DashboardLayout from '@/components/layout/DashboardLayout';

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
    // Calculer automatiquement au chargement
    calculateInterestRate();
  }, []);

  const calculateInterestRate = async () => {
    setLoading(true);
    setError(null);
    try {
      // Appel API réel
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
      setError(err.response?.data?.detail || 'Erreur lors du calcul. Utilisation de données mockées.');
      
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
      case 'Excellent':
        return 'text-green-400';
      case 'Bon':
        return 'text-blue-400';
      case 'Moyen':
        return 'text-yellow-400';
      case 'Risqué':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  const getCategoryBg = (category: string) => {
    switch (category) {
      case 'Excellent':
        return 'bg-green-500/10 border-green-500/30';
      case 'Bon':
        return 'bg-blue-500/10 border-blue-500/30';
      case 'Moyen':
        return 'bg-yellow-500/10 border-yellow-500/30';
      case 'Risqué':
        return 'bg-red-500/10 border-red-500/30';
      default:
        return 'bg-gray-500/10 border-gray-500/30';
    }
  };

  return (
    <DashboardLayout>
      {/* Header */}
      <div className="bg-gray-900 border-b border-gray-800 -m-8 mb-8">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">Calculateur de Taux</h1>
              <p className="text-gray-400 mt-1">Simulation du taux d'intérêt basé sur le risque</p>
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

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form */}
          <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
            <h2 className="text-xl font-bold text-white mb-6">Paramètres du Projet</h2>

            <div className="space-y-6">
              {/* City */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Ville
                </label>
                <select
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                >
                  <option value="Paris">Paris</option>
                  <option value="Lyon">Lyon</option>
                  <option value="Marseille">Marseille</option>
                  <option value="Bordeaux">Bordeaux</option>
                  <option value="Toulouse">Toulouse</option>
                  <option value="Nice">Nice</option>
                </select>
              </div>

              {/* LTV */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  LTV (Loan-to-Value) - {ltv}%
                </label>
                <input
                  type="range"
                  min="40"
                  max="90"
                  step="5"
                  value={ltv}
                  onChange={(e) => setLtv(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-600"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>40%</span>
                  <span>90%</span>
                </div>
              </div>

              {/* TRI */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  TRI Cible - {tri}%
                </label>
                <input
                  type="range"
                  min="5"
                  max="20"
                  step="0.5"
                  value={tri}
                  onChange={(e) => setTri(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-600"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>5%</span>
                  <span>20%</span>
                </div>
              </div>

              {/* Showstoppers */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Nombre de Showstoppers Critiques
                </label>
                <input
                  type="number"
                  min="0"
                  max="10"
                  value={showstoppers}
                  onChange={(e) => setShowstoppers(Number(e.target.value))}
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                />
              </div>

              {/* Experience */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Expérience Promoteur
                </label>
                <select
                  value={experience}
                  onChange={(e) => setExperience(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                >
                  <option value="beginner">Débutant (&lt; 2 projets)</option>
                  <option value="intermediate">Intermédiaire (2-5 projets)</option>
                  <option value="expert">Expert (&gt; 5 projets)</option>
                </select>
              </div>

              {/* Project Type */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Type de Projet
                </label>
                <select
                  value={projectType}
                  onChange={(e) => setProjectType(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                >
                  <option value="rehabilitation_legere">Réhabilitation Légère</option>
                  <option value="restructuration_lourde">Restructuration Lourde</option>
                  <option value="construction_neuve">Construction Neuve</option>
                  <option value="marchand_de_biens">Marchand de Biens</option>
                </select>
              </div>

              {/* Complexity */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Complexité Administrative
                </label>
                <select
                  value={complexity}
                  onChange={(e) => setComplexity(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                >
                  <option value="simple">Simple (DP, pas d'ABF)</option>
                  <option value="moderate">Modérée (PC standard)</option>
                  <option value="complex">Complexe (PC + ABF)</option>
                  <option value="very_complex">Très Complexe (PC + ABF + Périmètre protégé)</option>
                </select>
              </div>

              <button
                onClick={calculateInterestRate}
                disabled={loading}
                className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {loading ? 'Calcul en cours...' : 'Calculer le Taux'}
              </button>
            </div>
          </div>

          {/* Results */}
          {result && (
            <div className="space-y-6">
              {/* Main Result Card */}
              <div className={`rounded-lg border p-6 ${getCategoryBg(result.category)}`}>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-white">Taux Final</h3>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getCategoryColor(result.category)}`}>
                    {result.category}
                  </span>
                </div>
                <div className="text-5xl font-bold text-white mb-2">
                  {result.final_rate.toFixed(2)}%
                </div>
                <div className="text-gray-400 text-sm">
                  Euribor {result.euribor_rate.toFixed(2)}% + Marge {result.margin.toFixed(2)}%
                </div>
              </div>

              {/* Risk Score */}
              <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Score de Risque</h3>
                
                {/* Gauge */}
                <div className="relative mb-6">
                  <div className="h-4 bg-gray-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full transition-all duration-500 ${
                        result.risk_score >= 80 ? 'bg-green-500' :
                        result.risk_score >= 60 ? 'bg-blue-500' :
                        result.risk_score >= 40 ? 'bg-yellow-500' :
                        'bg-red-500'
                      }`}
                      style={{ width: `${result.risk_score}%` }}
                    ></div>
                  </div>
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>0</span>
                    <span>100</span>
                  </div>
                  <div className="text-center mt-2">
                    <span className="text-3xl font-bold text-white">{result.risk_score}</span>
                    <span className="text-gray-400">/100</span>
                  </div>
                </div>

                {/* Factors Breakdown */}
                <div className="space-y-3">
                  <h4 className="text-sm font-medium text-gray-400 uppercase">Détail des Facteurs</h4>
                  {result.factors.map((factor, index) => (
                    <div key={index} className="bg-gray-800 rounded-lg p-3">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <span className="text-white font-medium">{factor.name}</span>
                          <span className="text-xs text-gray-500">×{factor.weight}%</span>
                        </div>
                        <span className={`text-sm font-bold ${
                          factor.score >= 80 ? 'text-green-400' :
                          factor.score >= 60 ? 'text-blue-400' :
                          factor.score >= 40 ? 'text-yellow-400' :
                          'text-red-400'
                        }`}>
                          {factor.score}
                        </span>
                      </div>
                      <div className="h-2 bg-gray-900 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${
                            factor.score >= 80 ? 'bg-green-500' :
                            factor.score >= 60 ? 'bg-blue-500' :
                            factor.score >= 40 ? 'bg-yellow-500' :
                            'bg-red-500'
                          }`}
                          style={{ width: `${factor.score}%` }}
                        ></div>
                      </div>
                      <p className="text-xs text-gray-400 mt-1">{factor.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
                <h3 className="text-lg font-semibold text-white mb-3">Recommandations</h3>
                <ul className="space-y-2 text-sm text-gray-300">
                  {result.category === 'Risqué' && (
                    <>
                      <li className="flex items-start">
                        <span className="text-red-400 mr-2">•</span>
                        Envisager de réduire le LTV pour améliorer le profil de risque
                      </li>
                      <li className="flex items-start">
                        <span className="text-red-400 mr-2">•</span>
                        Résoudre les showstoppers critiques avant financement
                      </li>
                    </>
                  )}
                  {result.category === 'Moyen' && (
                    <>
                      <li className="flex items-start">
                        <span className="text-yellow-400 mr-2">•</span>
                        Prévoir une marge de sécurité supplémentaire
                      </li>
                      <li className="flex items-start">
                        <span className="text-yellow-400 mr-2">•</span>
                        Documenter soigneusement le projet pour les banques
                      </li>
                    </>
                  )}
                  {(result.category === 'Bon' || result.category === 'Excellent') && (
                    <>
                      <li className="flex items-start">
                        <span className="text-green-400 mr-2">•</span>
                        Profil favorable pour négocier avec plusieurs banques
                      </li>
                      <li className="flex items-start">
                        <span className="text-green-400 mr-2">•</span>
                        Potentiel de marge de négociation à la baisse
                      </li>
                    </>
                  )}
                </ul>
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
              <p className="text-yellow-400 text-sm">⚠️ {error}</p>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
