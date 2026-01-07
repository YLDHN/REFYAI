'use client';

import Link from 'next/link';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { GlassCard } from '@/components/ui/GlassCard';

export default function AnalysesPage() {
  return (
    <DashboardLayout>
      <div className="flex flex-col gap-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Analyses</h1>
          <p className="text-slate-400">Outils d'analyse pour vos projets immobiliers</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Questionnaire */}
          <Link href="/questionnaire" className="group block">
            <GlassCard className="h-full p-6 transition-all duration-300 hover:bg-white/10 hover:border-blue-500/30 hover:scale-[1.02] cursor-pointer relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-opacity group-hover:opacity-75"></div>
              
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500/20 to-blue-600/20 text-blue-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 border border-blue-500/10">
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              
              <h3 className="text-xl font-bold text-white mb-3 group-hover:text-blue-300 transition-colors">Questionnaire</h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">Collectez toutes les informations nécessaires pour votre projet avec notre questionnaire intelligent.</p>
              
              <div className="flex items-center text-blue-400 text-sm font-medium group-hover:translate-x-2 transition-transform">
                Démarrer
                <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </GlassCard>
          </Link>

          {/* Showstoppers */}
          <Link href="/showstoppers" className="group block">
            <GlassCard className="h-full p-6 transition-all duration-300 hover:bg-white/10 hover:border-red-500/30 hover:scale-[1.02] cursor-pointer relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-opacity group-hover:opacity-75"></div>
              
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-red-500/20 to-red-600/20 text-red-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 border border-red-500/10">
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              
              <h3 className="text-xl font-bold text-white mb-3 group-hover:text-red-300 transition-colors">Points Bloquants</h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">Détectez automatiquement les showstoppers et obtenez un plan d'action priorisé.</p>
              
              <div className="flex items-center text-red-400 text-sm font-medium group-hover:translate-x-2 transition-transform">
                Analyser
                <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </GlassCard>
          </Link>

          {/* Market Analysis */}
          <Link href="/market" className="group block">
            <GlassCard className="h-full p-6 transition-all duration-300 hover:bg-white/10 hover:border-emerald-500/30 hover:scale-[1.02] cursor-pointer relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-opacity group-hover:opacity-75"></div>
              
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-emerald-600/20 text-emerald-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 border border-emerald-500/10">
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                </svg>
              </div>
              
              <h3 className="text-xl font-bold text-white mb-3 group-hover:text-emerald-300 transition-colors">Analyse de Marché</h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">Évaluez votre bien avec les données DVF et les comparables récents du marché.</p>
              
              <div className="flex items-center text-emerald-400 text-sm font-medium group-hover:translate-x-2 transition-transform">
                Explorer
                <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </GlassCard>
          </Link>

          {/* Interest Rate Calculator */}
          <Link href="/calculator" className="group block">
            <GlassCard className="h-full p-6 transition-all duration-300 hover:bg-white/10 hover:border-violet-500/30 hover:scale-[1.02] cursor-pointer relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-violet-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-opacity group-hover:opacity-75"></div>
              
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-violet-500/20 to-violet-600/20 text-violet-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 border border-violet-500/10">
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              
              <h3 className="text-xl font-bold text-white mb-3 group-hover:text-violet-300 transition-colors">Calculateur de Taux</h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">Simulez votre taux d'intérêt basé sur le profil de risque de votre projet.</p>
              
              <div className="flex items-center text-violet-400 text-sm font-medium group-hover:translate-x-2 transition-transform">
                Calculer
                <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </GlassCard>
          </Link>

          {/* CAPEX */}
          <div className="group block opacity-75 grayscale hover:grayscale-0 hover:opacity-100 transition-all duration-500">
            <GlassCard className="h-full p-6 relative overflow-hidden">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-amber-500/20 to-amber-600/20 text-amber-400 flex items-center justify-center mb-6 border border-amber-500/10">
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">CAPEX</h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">Estimez vos coûts de construction avec notre base de données de 60+ postes.</p>
              <div className="flex items-center text-slate-500 text-sm font-medium">
                Nécessite un projet
                <svg className="w-4 h-4 ml-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
            </GlassCard>
          </div>

          {/* Timeline */}
          <div className="group block opacity-75 grayscale hover:grayscale-0 hover:opacity-100 transition-all duration-500">
            <GlassCard className="h-full p-6 relative overflow-hidden">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-indigo-600/20 text-indigo-400 flex items-center justify-center mb-6 border border-indigo-500/10">
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Timeline</h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">Planifiez votre projet avec notre simulateur de délais administratifs et travaux.</p>
              <div className="flex items-center text-slate-500 text-sm font-medium">
                Nécessite un projet
                <svg className="w-4 h-4 ml-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
            </GlassCard>
          </div>
        </div>

        {/* Info Box */}
        <GlassCard className="p-6 bg-gradient-to-br from-blue-900/20 to-purple-900/20 border-blue-500/20">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center flex-shrink-0 text-blue-400">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-3">🚀 Workflow Recommandé</h3>
              <ol className="space-y-2.5 text-slate-300 text-sm">
                <li className="flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-slate-800 text-xs flex items-center justify-center text-slate-400 border border-white/10">1</span>
                  <span>Remplissez le <strong className="text-blue-300">Questionnaire</strong> pour collecter les informations</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-slate-800 text-xs flex items-center justify-center text-slate-400 border border-white/10">2</span>
                  <span>Vérifiez les <strong className="text-red-300">Points Bloquants</strong> potentiels</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-slate-800 text-xs flex items-center justify-center text-slate-400 border border-white/10">3</span>
                  <span>Effectuez une <strong className="text-emerald-300">Analyse de Marché</strong> pour la valorisation</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-slate-800 text-xs flex items-center justify-center text-slate-400 border border-white/10">4</span>
                  <span>Calculez votre <strong className="text-violet-300">Taux d'Intérêt</strong> selon le profil de risque</span>
                </li>
              </ol>
            </div>
          </div>
        </GlassCard>
      </div>
    </DashboardLayout>
  );
}
