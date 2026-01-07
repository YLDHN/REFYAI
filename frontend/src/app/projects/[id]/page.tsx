'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { GlassCard } from '@/components/ui/GlassCard';
import { Button } from '@/components/ui/Button';

export default function ProjectDetailPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params?.id as string;

  // Charger les données du projet depuis l'API
  const { data: project, isLoading, error } = useQuery({
    queryKey: ['project', projectId],
    queryFn: async () => {
      const response = await apiClient.get(`/projects/${projectId}`);
      return response.data;
    },
    enabled: !!projectId,
  });

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !project) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <p className="text-red-400 mb-4">Erreur lors du chargement du projet</p>
          <Button onClick={() => router.push('/dashboard')}>
            Retour au dashboard
          </Button>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link href="/projects">
                <Button variant="ghost" className="p-2 h-auto">
                    <svg className="w-6 h-6 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                </Button>
              </Link>
              <div>
                <h1 className="text-3xl font-bold text-white">{project.name}</h1>
                <p className="text-slate-400 mt-1">
                  {project.address && project.city ? `${project.address}, ${project.city}` : project.city || project.address || 'Adresse non renseignée'}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <span className={`px-4 py-2 rounded-full text-sm font-medium border ${
                project.status === 'completed' ? 'bg-green-500/10 text-green-400 border-green-500/20' :
                project.status === 'in_progress' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' :
                'bg-slate-500/10 text-slate-400 border-slate-500/20'
              }`}>
                {project.status === 'completed' ? 'Terminé' :
                 project.status === 'in_progress' ? 'En cours' : 'Brouillon'}
              </span>
            </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Stats */}
            <div className="grid grid-cols-3 gap-4">
              <GlassCard className="p-4 bg-slate-900/40 border-white/5">
                <div className="text-sm text-slate-400">LTV</div>
                <div className="text-2xl font-bold text-blue-400 mt-1">
                  {project.ltv ? `${project.ltv.toFixed(0)}%` : 'N/A'}
                </div>
              </GlassCard>
              <GlassCard className="p-4 bg-slate-900/40 border-white/5">
                <div className="text-sm text-slate-400">Prix d'achat</div>
                <div className="text-2xl font-bold text-white mt-1">
                  {project.purchase_price ? `${(project.purchase_price / 1000000).toFixed(1)}M€` : 'N/A'}
                </div>
              </GlassCard>
              <GlassCard className="p-4 bg-slate-900/40 border-white/5">
                <div className="text-sm text-slate-400">Surface</div>
                <div className="text-2xl font-bold text-white mt-1">
                  {project.surface ? `${project.surface.toLocaleString('fr-FR')}m²` : 'N/A'}
                </div>
              </GlassCard>
            </div>

            {/* Description */}
            {project.description && (
              <GlassCard className="p-6">
                <h2 className="text-xl font-bold text-white mb-4">Description du Projet</h2>
                <p className="text-slate-300 leading-relaxed">{project.description}</p>
              </GlassCard>
            )}

            {/* Données financières */}
            {(project.purchase_price || project.renovation_budget || project.estimated_value) && (
              <GlassCard className="p-6">
                <h2 className="text-xl font-bold text-white mb-4">Données Financières</h2>
                <div className="grid grid-cols-2 gap-4">
                  {project.purchase_price && (
                    <div>
                      <div className="text-sm text-slate-400">Prix d'acquisition</div>
                      <div className="text-lg font-semibold text-white mt-1">
                        {(project.purchase_price / 1000000).toFixed(2)}M€
                      </div>
                    </div>
                  )}
                  {project.renovation_budget && (
                    <div>
                      <div className="text-sm text-slate-400">Budget travaux</div>
                      <div className="text-lg font-semibold text-white mt-1">
                        {(project.renovation_budget / 1000).toFixed(0)}K€
                      </div>
                    </div>
                  )}
                  {project.estimated_value && (
                    <div>
                      <div className="text-sm text-slate-400">Valeur estimée</div>
                      <div className="text-lg font-semibold text-emerald-400 mt-1">
                        {(project.estimated_value / 1000000).toFixed(2)}M€
                      </div>
                    </div>
                  )}
                  {project.financing_amount && (
                    <div>
                      <div className="text-sm text-slate-400">Financement</div>
                      <div className="text-lg font-semibold text-white mt-1">
                        {(project.financing_amount / 1000000).toFixed(2)}M€
                      </div>
                    </div>
                  )}
                  {project.interest_rate && (
                    <div>
                      <div className="text-sm text-slate-400">Taux d'intérêt</div>
                      <div className="text-lg font-semibold text-white mt-1">
                        {project.interest_rate.toFixed(2)}%
                      </div>
                    </div>
                  )}
                  {project.loan_duration && (
                    <div>
                      <div className="text-sm text-slate-400">Durée du prêt</div>
                      <div className="text-lg font-semibold text-white mt-1">
                        {project.loan_duration} ans
                      </div>
                    </div>
                  )}
                </div>
              </GlassCard>
            )}

            {/* Données locatives */}
            {(project.current_rent || project.market_rent || project.occupancy_rate || project.walb || project.walt) && (
              <GlassCard className="p-6">
                <h2 className="text-xl font-bold text-white mb-4">Données Locatives</h2>
                <div className="grid grid-cols-2 gap-4">
                  {project.current_rent && (
                    <div>
                      <div className="text-sm text-slate-400">Loyer actuel (annuel)</div>
                      <div className="text-lg font-semibold text-white mt-1">
                        {(project.current_rent / 1000).toFixed(0)}K€
                      </div>
                    </div>
                  )}
                  {project.market_rent && (
                    <div>
                      <div className="text-sm text-slate-400">Loyer de marché (VLM)</div>
                      <div className="text-lg font-semibold text-emerald-400 mt-1">
                        {(project.market_rent / 1000).toFixed(0)}K€
                      </div>
                    </div>
                  )}
                  {project.occupancy_rate && (
                    <div>
                      <div className="text-sm text-slate-400">Taux d'occupation</div>
                      <div className="text-lg font-semibold text-white mt-1">
                        {project.occupancy_rate.toFixed(0)}%
                      </div>
                    </div>
                  )}
                  {project.walb && (
                    <div>
                      <div className="text-sm text-slate-400">WALB</div>
                      <div className="text-lg font-semibold text-white mt-1">
                        {project.walb.toFixed(1)} ans
                      </div>
                    </div>
                  )}
                  {project.walt && (
                    <div>
                      <div className="text-sm text-slate-400">WALT</div>
                      <div className="text-lg font-semibold text-white mt-1">
                        {project.walt.toFixed(1)} ans
                      </div>
                    </div>
                  )}
                </div>
              </GlassCard>
            )}

            {/* Actions Grid */}
            <GlassCard className="p-6">
              <h2 className="text-xl font-bold text-white mb-4">Analyses & Outils</h2>
              <div className="grid grid-cols-2 gap-4">
                <ProjectToolCard 
                    href="/questionnaire"
                    title="Questionnaire"
                    subtitle="Analyse complète"
                    color="blue"
                    icon={<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />}
                />
                
                <ProjectToolCard 
                    href="/showstoppers"
                    title="Showstoppers"
                    subtitle="Points bloquants"
                    color="red"
                    icon={<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />}
                />

                <ProjectToolCard 
                    href="/market"
                    title="Analyse de Marché"
                    subtitle="Comparables DVF"
                    color="green"
                    icon={<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />}
                />

                <ProjectToolCard 
                    href="/calculator"
                    title="Calculateur"
                    subtitle="Taux d'intérêt"
                    color="purple"
                    icon={<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />}
                />

                <ProjectToolCard 
                    href={`/projects/${projectId}/capex`}
                    title="CAPEX"
                    subtitle="Budget travaux"
                    color="orange"
                    icon={<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />}
                />

                <ProjectToolCard 
                    href={`/projects/${projectId}/timeline`}
                    title="Timeline"
                    subtitle="Planning projet"
                    color="indigo"
                    icon={<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />}
                />
              </div>
            </GlassCard>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Project Info */}
            <GlassCard className="p-6">
              <h3 className="font-semibold text-white mb-4">Informations</h3>
              <div className="space-y-3 text-sm">
                <InfoRow label="Type" value={project.type === 'rental' ? 'Locatif' : project.type === 'resale' ? 'Revente' : 'Mixte'} />
                <InfoRow label="Prix/m²" value={`${project.price_per_sqm}€`} />
                <InfoRow label="Budget CAPEX" value={`${(project.capex_budget / 1000).toFixed(0)}K€`} />
                <div className="h-px bg-white/10 my-3"></div>
                <InfoRow label="Créé le" value={new Date(project.createdAt).toLocaleDateString('fr-FR')} />
                <InfoRow label="Mis à jour" value={new Date(project.updatedAt).toLocaleDateString('fr-FR')} />
                <InfoRow label="Fin estimée" value={new Date(project.completion_date).toLocaleDateString('fr-FR')} />
              </div>
            </GlassCard>

            {/* Quick Actions */}
            <GlassCard className="p-6">
              <h3 className="font-semibold text-white mb-4">Actions Rapides</h3>
              <div className="space-y-3">
                <Button variant="primary" className="w-full">Modifier le projet</Button>
                <Button variant="outline" className="w-full border-white/10 text-slate-300 hover:bg-white/10 hover:text-white">Exporter en PDF</Button>
                <Button variant="outline" className="w-full border-white/10 text-slate-300 hover:bg-white/10 hover:text-white">Partager</Button>
                <Button variant="outline" className="w-full border-red-500/30 text-red-400 hover:bg-red-500/10 hover:text-red-300">Supprimer</Button>
              </div>
            </GlassCard>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

// Helpers

function InfoRow({ label, value }: { label: string, value: string }) {
    return (
        <div className="flex justify-between">
            <span className="text-slate-400">{label}</span>
            <span className="font-medium text-slate-200">{value}</span>
        </div>
    )
}

function ProjectToolCard({ href, title, subtitle, color, icon }: any) {
    const colorClasses: any = {
        blue: 'bg-blue-500/20 text-blue-400 group-hover:bg-blue-500/30',
        red: 'bg-red-500/20 text-red-400 group-hover:bg-red-500/30',
        green: 'bg-green-500/20 text-green-400 group-hover:bg-green-500/30',
        purple: 'bg-purple-500/20 text-purple-400 group-hover:bg-purple-500/30',
        orange: 'bg-orange-500/20 text-orange-400 group-hover:bg-orange-500/30',
        indigo: 'bg-indigo-500/20 text-indigo-400 group-hover:bg-indigo-500/30',
    };

    const borderClasses: any = {
        blue: 'hover:border-blue-500/50 hover:bg-blue-500/5',
        red: 'hover:border-red-500/50 hover:bg-red-500/5',
        green: 'hover:border-green-500/50 hover:bg-green-500/5',
        purple: 'hover:border-purple-500/50 hover:bg-purple-500/5',
        orange: 'hover:border-orange-500/50 hover:bg-orange-500/5',
        indigo: 'hover:border-indigo-500/50 hover:bg-indigo-500/5',
    }

    return (
        <Link
            href={href}
            className={`p-4 border border-white/10 rounded-xl transition-all duration-300 group ${borderClasses[color]}`}
        >
            <div className="flex items-center space-x-3">
            <div className={`w-12 h-12 rounded-lg flex items-center justify-center transition ${colorClasses[color]}`}>
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    {icon}
                </svg>
            </div>
            <div>
                <div className="font-semibold text-white">{title}</div>
                <div className="text-sm text-slate-400">{subtitle}</div>
            </div>
            </div>
        </Link>
    )
}
