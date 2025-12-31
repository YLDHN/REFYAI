'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

interface Procedure {
  id: string;
  name: string;
  description: string;
  typical_duration_days: number;
}

interface TimelinePhase {
  name: string;
  start_date: string;
  end_date: string;
  duration_days: number;
  procedures?: string[];
}

interface ProjectTimeline {
  phases: TimelinePhase[];
  total_duration_months: number;
  start_date: string;
  estimated_completion: string;
  critical_path: string[];
}

export default function TimelinePage() {
  const params = useParams();
  const projectId = params?.id as string;

  const [availableProcedures, setAvailableProcedures] = useState<Procedure[]>([]);
  const [selectedProcedures, setSelectedProcedures] = useState<string[]>([]);
  const [complexity, setComplexity] = useState(1.0);
  const [hasABF, setHasABF] = useState(false);
  const [constructionMonths, setConstructionMonths] = useState(12);
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [timeline, setTimeline] = useState<ProjectTimeline | null>(null);
  const [loading, setLoading] = useState(false);
  const [viewMode, setViewMode] = useState<'optimistic' | 'realistic' | 'pessimistic'>('realistic');

  useEffect(() => {
    loadProcedures();
  }, []);

  useEffect(() => {
    if (selectedProcedures.length > 0) {
      calculateTimeline();
    }
  }, [selectedProcedures, complexity, hasABF, constructionMonths, startDate, viewMode]);

  const loadProcedures = () => {
    // Mock data - à remplacer par GET /api/v1/admin-delays/available-procedures
    const mockProcedures: Procedure[] = [
      { id: 'PC', name: 'Permis de Construire', description: 'Instruction PC standard', typical_duration_days: 75 },
      { id: 'DP', name: 'Déclaration Préalable', description: 'DP pour travaux légers', typical_duration_days: 38 },
      { id: 'AT', name: 'Autorisation de Travaux', description: 'AT pour ERP', typical_duration_days: 60 },
      { id: 'PD', name: 'Permis de Démolir', description: 'Démolition totale/partielle', typical_duration_days: 60 },
      { id: 'CU', name: 'Certificat d\'Urbanisme', description: 'CU opérationnel', typical_duration_days: 60 },
      { id: 'DAACT', name: 'DAACT', description: 'Déclaration d\'Achèvement', typical_duration_days: 90 }
    ];

    setAvailableProcedures(mockProcedures);
    setSelectedProcedures(['PC']); // Default
  };

  const calculateTimeline = () => {
    setLoading(true);
    
    // Mock calculation
    const complexityMultiplier = viewMode === 'optimistic' ? 0.9 : viewMode === 'pessimistic' ? 1.2 : 1.0;
    const finalComplexity = complexity * complexityMultiplier;
    
    const etudesDurationMonths = Math.ceil((1 + (finalComplexity - 1) * 2) * 10) / 10;
    
    let adminDurationDays = 0;
    selectedProcedures.forEach(procId => {
      const proc = availableProcedures.find(p => p.id === procId);
      if (proc) {
        adminDurationDays += proc.typical_duration_days * finalComplexity;
      }
    });
    
    if (hasABF) {
      adminDurationDays += 45;
    }

    const daactDurationMonths = viewMode === 'optimistic' ? 2 : viewMode === 'pessimistic' ? 4 : 3;
    const constructionDuration = constructionMonths * complexityMultiplier;

    // Calculate dates
    const start = new Date(startDate);
    
    // Phase 1: Études
    const etudesEndDate = new Date(start);
    etudesEndDate.setMonth(etudesEndDate.getMonth() + etudesDurationMonths);
    
    // Phase 2: Admin
    const adminStartDate = new Date(etudesEndDate);
    const adminEndDate = new Date(adminStartDate);
    adminEndDate.setDate(adminEndDate.getDate() + adminDurationDays);
    
    // Phase 3: Travaux
    const travauxStartDate = new Date(adminEndDate);
    const travauxEndDate = new Date(travauxStartDate);
    travauxEndDate.setMonth(travauxEndDate.getMonth() + constructionDuration);
    
    // Phase 4: DAACT
    const daactStartDate = new Date(travauxEndDate);
    const daactEndDate = new Date(daactStartDate);
    daactEndDate.setMonth(daactEndDate.getMonth() + daactDurationMonths);

    const totalMonths = Math.ceil(
      (daactEndDate.getTime() - start.getTime()) / (1000 * 60 * 60 * 24 * 30)
    );

    const mockTimeline: ProjectTimeline = {
      phases: [
        {
          name: 'Études Préalables',
          start_date: start.toISOString().split('T')[0],
          end_date: etudesEndDate.toISOString().split('T')[0],
          duration_days: Math.ceil((etudesEndDate.getTime() - start.getTime()) / (1000 * 60 * 60 * 24))
        },
        {
          name: 'Procédures Administratives',
          start_date: adminStartDate.toISOString().split('T')[0],
          end_date: adminEndDate.toISOString().split('T')[0],
          duration_days: adminDurationDays,
          procedures: selectedProcedures
        },
        {
          name: 'Travaux',
          start_date: travauxStartDate.toISOString().split('T')[0],
          end_date: travauxEndDate.toISOString().split('T')[0],
          duration_days: Math.ceil((travauxEndDate.getTime() - travauxStartDate.getTime()) / (1000 * 60 * 60 * 24))
        },
        {
          name: 'DAACT & Réception',
          start_date: daactStartDate.toISOString().split('T')[0],
          end_date: daactEndDate.toISOString().split('T')[0],
          duration_days: daactDurationMonths * 30
        }
      ],
      total_duration_months: totalMonths,
      start_date: start.toISOString().split('T')[0],
      estimated_completion: daactEndDate.toISOString().split('T')[0],
      critical_path: ['Études', 'PC', 'ABF', 'Travaux', 'DAACT']
    };

    setTimeline(mockTimeline);
    setLoading(false);
  };

  const toggleProcedure = (procId: string) => {
    if (selectedProcedures.includes(procId)) {
      setSelectedProcedures(selectedProcedures.filter(p => p !== procId));
    } else {
      setSelectedProcedures([...selectedProcedures, procId]);
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };

  const getPhaseColor = (index: number) => {
    const colors = [
      'bg-purple-600',
      'bg-blue-600',
      'bg-orange-600',
      'bg-green-600'
    ];
    return colors[index] || 'bg-gray-600';
  };

  const getComplexityLabel = (value: number) => {
    if (value === 1.0) return 'Simple';
    if (value === 1.3) return 'Modérée';
    if (value === 1.6) return 'Complexe';
    if (value === 2.0) return 'Très Complexe';
    return `${value}`;
  };

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Header */}
      <div className="bg-gray-900 border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">Planning Projet</h1>
              <p className="text-gray-400 mt-1">Estimation des délais administratifs et travaux</p>
            </div>
            <Link
              href={`/projects/${projectId}`}
              className="px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition"
            >
              ← Retour
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Configuration */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Configuration</h3>

              <div className="space-y-4">
                {/* Start Date */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Date de Début
                  </label>
                  <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600"
                  />
                </div>

                {/* Procedures */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Procédures Administratives
                  </label>
                  <div className="space-y-2">
                    {availableProcedures.filter(p => p.id !== 'DAACT').map(proc => (
                      <label key={proc.id} className="flex items-center space-x-3 p-3 bg-gray-800 rounded-lg cursor-pointer hover:bg-gray-750 transition">
                        <input
                          type="checkbox"
                          checked={selectedProcedures.includes(proc.id)}
                          onChange={() => toggleProcedure(proc.id)}
                          className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-600"
                        />
                        <div className="flex-1">
                          <div className="text-white text-sm font-medium">{proc.name}</div>
                          <div className="text-gray-400 text-xs">{proc.description}</div>
                        </div>
                        <div className="text-gray-400 text-xs">
                          {proc.typical_duration_days}j
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                {/* ABF */}
                <label className="flex items-center space-x-3 p-3 bg-gray-800 rounded-lg cursor-pointer">
                  <input
                    type="checkbox"
                    checked={hasABF}
                    onChange={(e) => setHasABF(e.target.checked)}
                    className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-600"
                  />
                  <div className="flex-1">
                    <div className="text-white text-sm font-medium">Avis ABF Requis</div>
                    <div className="text-gray-400 text-xs">+45 jours supplémentaires</div>
                  </div>
                </label>

                {/* Complexity */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Complexité - {getComplexityLabel(complexity)}
                  </label>
                  <input
                    type="range"
                    min="1.0"
                    max="2.0"
                    step="0.3"
                    value={complexity}
                    onChange={(e) => setComplexity(Number(e.target.value))}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-600"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Simple</span>
                    <span>Très Complexe</span>
                  </div>
                </div>

                {/* Construction Duration */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Durée Travaux - {constructionMonths} mois
                  </label>
                  <input
                    type="range"
                    min="3"
                    max="36"
                    step="1"
                    value={constructionMonths}
                    onChange={(e) => setConstructionMonths(Number(e.target.value))}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-600"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>3 mois</span>
                    <span>36 mois</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Scenario */}
            <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
              <h3 className="text-lg font-semibold text-white mb-3">Scénario</h3>
              <div className="space-y-2">
                <button
                  onClick={() => setViewMode('optimistic')}
                  className={`w-full px-4 py-2 rounded-lg transition ${
                    viewMode === 'optimistic'
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
                  }`}
                >
                  🟢 Optimiste (-10%)
                </button>
                <button
                  onClick={() => setViewMode('realistic')}
                  className={`w-full px-4 py-2 rounded-lg transition ${
                    viewMode === 'realistic'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
                  }`}
                >
                  🔵 Réaliste
                </button>
                <button
                  onClick={() => setViewMode('pessimistic')}
                  className={`w-full px-4 py-2 rounded-lg transition ${
                    viewMode === 'pessimistic'
                      ? 'bg-orange-600 text-white'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
                  }`}
                >
                  🟠 Pessimiste (+20%)
                </button>
              </div>
            </div>
          </div>

          {/* Timeline Visualization */}
          {timeline && (
            <div className="lg:col-span-2 space-y-6">
              {/* Summary Card */}
              <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg border border-blue-500 p-6">
                <h3 className="text-xl font-semibold text-white mb-4">Durée Totale du Projet</h3>
                <div className="flex items-end space-x-8">
                  <div>
                    <div className="text-5xl font-bold text-white">{timeline.total_duration_months}</div>
                    <div className="text-blue-200 mt-1">mois</div>
                  </div>
                  <div className="flex-1 space-y-2 pb-2">
                    <div className="flex justify-between text-blue-100 text-sm">
                      <span>Début:</span>
                      <span className="font-semibold">{formatDate(timeline.start_date)}</span>
                    </div>
                    <div className="flex justify-between text-blue-100 text-sm">
                      <span>Fin estimée:</span>
                      <span className="font-semibold">{formatDate(timeline.estimated_completion)}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Gantt Chart */}
              <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
                <h3 className="text-lg font-semibold text-white mb-6">Planning Détaillé</h3>
                
                <div className="space-y-6">
                  {timeline.phases.map((phase, index) => (
                    <div key={index}>
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-3">
                          <div className={`w-3 h-3 rounded-full ${getPhaseColor(index)}`}></div>
                          <span className="text-white font-medium">{phase.name}</span>
                          {phase.procedures && phase.procedures.length > 0 && (
                            <span className="text-xs text-gray-400">
                              ({phase.procedures.join(', ')})
                            </span>
                          )}
                        </div>
                        <div className="text-gray-400 text-sm">
                          {Math.ceil(phase.duration_days / 30)} mois ({phase.duration_days}j)
                        </div>
                      </div>

                      {/* Progress bar */}
                      <div className="relative h-8 bg-gray-800 rounded-lg overflow-hidden">
                        <div
                          className={`h-full ${getPhaseColor(index)} flex items-center px-3`}
                          style={{
                            width: `${(phase.duration_days / (timeline.total_duration_months * 30)) * 100}%`
                          }}
                        >
                          <span className="text-white text-xs font-medium truncate">
                            {formatDate(phase.start_date)} → {formatDate(phase.end_date)}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Critical Path */}
              <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-yellow-400 mb-3">Chemin Critique</h3>
                <div className="flex flex-wrap gap-2">
                  {timeline.critical_path.map((step, index) => (
                    <div key={index} className="flex items-center">
                      <span className="px-3 py-1 bg-yellow-500/20 text-yellow-200 rounded-lg text-sm font-medium">
                        {step}
                      </span>
                      {index < timeline.critical_path.length - 1 && (
                        <svg className="w-5 h-5 text-yellow-400 mx-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      )}
                    </div>
                  ))}
                </div>
                <p className="text-yellow-200/80 text-sm mt-3">
                  ⚠️ Les étapes du chemin critique ne peuvent pas être parallélisées et déterminent la durée minimale du projet.
                </p>
              </div>

              {/* Phases Details Table */}
              <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
                <div className="p-4 bg-gray-800 border-b border-gray-700">
                  <h3 className="text-lg font-semibold text-white">Détails des Phases</h3>
                </div>
                <table className="w-full">
                  <thead className="bg-gray-800">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">Phase</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">Début</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">Fin</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase">Durée</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-800">
                    {timeline.phases.map((phase, index) => (
                      <tr key={index} className="hover:bg-gray-800/50">
                        <td className="px-4 py-3 text-sm text-white font-medium">{phase.name}</td>
                        <td className="px-4 py-3 text-sm text-gray-300">{formatDate(phase.start_date)}</td>
                        <td className="px-4 py-3 text-sm text-gray-300">{formatDate(phase.end_date)}</td>
                        <td className="px-4 py-3 text-sm text-gray-300 text-right">
                          {Math.ceil(phase.duration_days / 30)} mois
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
