'use client';

import Link from 'next/link';
import DashboardLayout from '@/components/layout/DashboardLayout';

export default function AnalysesPage() {
  return (
    <DashboardLayout>
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Analyses</h1>
          <p className="text-gray-600 mt-1">Outils d'analyse pour vos projets immobiliers</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Questionnaire */}
          <Link
            href="/questionnaire"
            className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg hover:border-blue-500 transition group"
          >
            <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-blue-200 transition">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Questionnaire</h3>
            <p className="text-gray-600 mb-4">Collectez toutes les informations nécessaires pour votre projet avec notre questionnaire intelligent.</p>
            <div className="flex items-center text-blue-600 font-medium group-hover:translate-x-2 transition">
              Démarrer →
            </div>
          </Link>

          {/* Showstoppers */}
          <Link
            href="/showstoppers"
            className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg hover:border-red-500 transition group"
          >
            <div className="w-16 h-16 bg-red-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-red-200 transition">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Points Bloquants</h3>
            <p className="text-gray-600 mb-4">Détectez automatiquement les showstoppers et obtenez un plan d'action priorisé.</p>
            <div className="flex items-center text-red-600 font-medium group-hover:translate-x-2 transition">
              Analyser →
            </div>
          </Link>

          {/* Market Analysis */}
          <Link
            href="/market"
            className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg hover:border-green-500 transition group"
          >
            <div className="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-green-200 transition">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Analyse de Marché</h3>
            <p className="text-gray-600 mb-4">Évaluez votre bien avec les données DVF et les comparables récents du marché.</p>
            <div className="flex items-center text-green-600 font-medium group-hover:translate-x-2 transition">
              Explorer →
            </div>
          </Link>

          {/* Interest Rate Calculator */}
          <Link
            href="/calculator"
            className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg hover:border-purple-500 transition group"
          >
            <div className="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-purple-200 transition">
              <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Calculateur de Taux</h3>
            <p className="text-gray-600 mb-4">Simulez votre taux d'intérêt basé sur le profil de risque de votre projet.</p>
            <div className="flex items-center text-purple-600 font-medium group-hover:translate-x-2 transition">
              Calculer →
            </div>
          </Link>

          {/* CAPEX */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="w-16 h-16 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">CAPEX</h3>
            <p className="text-gray-600 mb-4">Estimez vos coûts de construction avec notre base de données de 60+ postes.</p>
            <div className="flex items-center text-gray-400 font-medium">
              Nécessite un projet →
            </div>
          </div>

          {/* Timeline */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="w-16 h-16 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Timeline</h3>
            <p className="text-gray-600 mb-4">Planifiez votre projet avec notre simulateur de délais administratifs et travaux.</p>
            <div className="flex items-center text-gray-400 font-medium">
              Nécessite un projet →
            </div>
          </div>
        </div>

        {/* Info Box */}
        <div className="mt-8 bg-blue-50 rounded-lg border border-blue-200 p-6">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">🚀 Workflow Recommandé</h3>
              <ol className="text-gray-700 space-y-2 list-decimal list-inside">
                <li>Remplissez le <strong>Questionnaire</strong> pour collecter les informations</li>
                <li>Vérifiez les <strong>Points Bloquants</strong> potentiels</li>
                <li>Effectuez une <strong>Analyse de Marché</strong> pour la valorisation</li>
                <li>Calculez votre <strong>Taux d'Intérêt</strong> selon le profil de risque</li>
                <li>Estimez le <strong>CAPEX</strong> et la <strong>Timeline</strong> depuis votre projet</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
    </DashboardLayout>
  );
}
