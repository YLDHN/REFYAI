'use client';

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Link from 'next/link';
import { useProjects } from '@/lib/hooks';
import { GlassCard } from '@/components/ui/GlassCard';
import { Button } from '@/components/ui/Button';

interface Project {
  id: number;
  name: string;
  address: string;
  type: 'rental' | 'resale' | 'mixed';
  status: 'analyzing' | 'negotiating' | 'offer_sent' | 'financing_search' | 'due_diligence' | 'under_contract' | 'acquired' | 'rejected' | 'draft' | 'in_progress' | 'completed';
  tri: number;
  investment: number;
  updatedAt: string;
  strategy?: 'core' | 'core_plus' | 'value_add';
  budget_total?: number;
  technical_score?: number;
}

export default function ProjectsPage() {
  const { projects, loading, error, fetchProjects, deleteProject } = useProjects();
  const [filter, setFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('date');

  useEffect(() => {
    fetchProjects();
  }, []);

  const projectsArray = (Array.isArray(projects) ? projects : []) as Project[];
  
  const filteredProjects = projectsArray.filter((project : Project) => {
    if (filter === 'all') return true;
    return project.status === filter;
  });

  const handleDelete = async (id: number) => {
    if (confirm('Voulez-vous vraiment supprimer ce projet ?')) {
      try {
        await deleteProject(id);
      } catch (err) {
        alert('Erreur lors de la suppression');
      }
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold text-white">Projets</h1>
            <p className="text-slate-400 mt-1">Gérez tous vos projets immobiliers</p>
          </div>
          <Link href="/projects/new">
            <Button variant="primary" className="shadow-lg shadow-blue-500/20">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Nouveau Projet
            </Button>
          </Link>
        </div>

        {/* Filters - 8 BP Statuses */}
        <GlassCard className="p-4 border-white/10">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex gap-2 w-full md:w-auto overflow-x-auto pb-2 md:pb-0">
              {[
                { value: 'all', label: `Tous (${projects.length})`, color: '' },
                { value: 'analyzing', label: 'Analyse', color: 'bg-sky-500/20 text-sky-400' },
                { value: 'negotiating', label: 'Négo', color: 'bg-orange-500/20 text-orange-400' },
                { value: 'offer_sent', label: 'Offre', color: 'bg-yellow-500/20 text-yellow-400' },
                { value: 'financing_search', label: 'Financement', color: 'bg-purple-500/20 text-purple-400' },
                { value: 'due_diligence', label: 'DD', color: 'bg-blue-500/20 text-blue-400' },
                { value: 'under_contract', label: 'Promesse', color: 'bg-indigo-500/20 text-indigo-400' },
                { value: 'acquired', label: 'Acquis', color: 'bg-emerald-500/20 text-emerald-400' },
                { value: 'rejected', label: 'Refusé', color: 'bg-red-500/20 text-red-400' }
              ].map((f) => (
                <button
                  key={f.value}
                  onClick={() => setFilter(f.value)}
                  className={`px-3 py-2 rounded-lg font-medium transition-all whitespace-nowrap text-sm ${
                    filter === f.value
                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20'
                      : `${f.color || 'bg-white/5 text-slate-400'} hover:bg-white/10 hover:text-white border border-white/5`
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-3 w-full md:w-auto">
              <span className="text-sm text-slate-400 whitespace-nowrap">Trier par:</span>
              <select 
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="bg-slate-900/50 text-white border border-white/10 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full md:w-auto"
              >
                <option value="date">Date de mise à jour</option>
                <option value="tri">TRI</option>
                <option value="investment">Investissement</option>
                <option value="name">Nom</option>
              </select>
            </div>
          </div>
        </GlassCard>

        {/* Projects Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects.map((project) => (
            <GlassCard key={project.id} className="group hover:-translate-y-1 transition-all duration-300 border-white/5 bg-slate-900/40" hoverEffect={true}>
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-white mb-1 group-hover:text-blue-400 transition-colors">{project.name}</h3>
                    <p className="text-sm text-slate-400">{project.address}</p>
                  </div>
                  <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${
                    project.status === 'acquired' || project.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                    project.status === 'under_contract' ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20' :
                    project.status === 'due_diligence' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' :
                    project.status === 'financing_search' ? 'bg-purple-500/10 text-purple-400 border-purple-500/20' :
                    project.status === 'offer_sent' ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' :
                    project.status === 'negotiating' || project.status === 'in_progress' ? 'bg-orange-500/10 text-orange-400 border-orange-500/20' :
                    project.status === 'analyzing' || project.status === 'draft' ? 'bg-sky-500/10 text-sky-400 border-sky-500/20' :
                    project.status === 'rejected' ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                    'bg-slate-500/10 text-slate-400 border-slate-500/20'
                  }`}>
                    {project.status === 'acquired' || project.status === 'completed' ? 'Acquis' :
                     project.status === 'under_contract' ? 'Promesse' :
                     project.status === 'due_diligence' ? 'Due Diligence' :
                     project.status === 'financing_search' ? 'Financement' :
                     project.status === 'offer_sent' ? 'Offre envoyée' :
                     project.status === 'negotiating' ? 'Négociation' :
                     project.status === 'analyzing' ? 'Analyse' :
                     project.status === 'rejected' ? 'Refusé' :
                     project.status === 'in_progress' ? 'En cours' :
                     project.status === 'draft' ? 'Brouillon' : project.status}
                  </span>
                </div>

                <div className="space-y-4 mb-6">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-500">Type</span>
                    <span className="px-2 py-1 bg-purple-500/10 text-purple-300 border border-purple-500/20 rounded text-xs font-medium">
                      {project.type === 'rental' ? 'Locatif' :
                       project.type === 'resale' ? 'Revente' : 'Mixte'}
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-500">TRI</span>
                    <span className={`text-lg font-bold ${
                      // TRI color coding by strategy (BP requirement)
                      (project as any).strategy === 'core' ? (
                        project.tri >= 4 && project.tri <= 6 ? 'text-emerald-400' : 'text-amber-400'
                      ) : (project as any).strategy === 'core_plus' ? (
                        project.tri >= 8 && project.tri <= 12 ? 'text-emerald-400' : 'text-amber-400'
                      ) : (project as any).strategy === 'value_add' ? (
                        project.tri >= 15 ? 'text-emerald-400' : 'text-amber-400'
                      ) : 'text-slate-400'
                    }`}>{project.tri}%</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-500">Investissement</span>
                    <span className="text-sm font-semibold text-white">
                      {(project.investment / 1000).toFixed(0)}K€
                    </span>
                  </div>

                  {(project as any).budget_total && (
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-500">Budget Total</span>
                      <span className="text-sm font-semibold text-blue-400">
                        {((project as any).budget_total / 1000).toFixed(0)}K€
                      </span>
                    </div>
                  )}

                  {(project as any).technical_score && (
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-500">Score Technique</span>
                      <div className="flex items-center gap-1">
                        {[...Array(5)].map((_, i) => (
                          <svg
                            key={i}
                            className={`w-3.5 h-3.5 ${
                              i < Math.round((project as any).technical_score / 20)
                                ? 'text-yellow-400 fill-current'
                                : 'text-slate-600'
                            }`}
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                            />
                          </svg>
                        ))}
                        <span className="text-xs text-slate-400 ml-1">
                          {(project as any).technical_score}/100
                        </span>
                      </div>
                    </div>
                  )}

                  <div className="flex items-center justify-between pt-4 border-t border-white/5">
                    <span className="text-xs text-slate-600">Mis à jour</span>
                    <span className="text-xs text-slate-400">{new Date(project.updatedAt).toLocaleDateString('fr-FR')}</span>
                  </div>
                </div>

                <div className="flex gap-2">
                  <Link 
                    href={`/projects/${project.id}`}
                    className="flex-1"
                  >
                    <Button variant="primary" className="w-full text-sm" size="sm">
                       Voir détails
                    </Button>
                  </Link>
                  <Button variant="glass" size="sm" className="px-3" onClick={() => handleDelete(project.id)}>
                    <svg className="w-4 h-4 text-slate-400 hover:text-red-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </Button>
                </div>
            </GlassCard>
          ))}
        </div>

        {filteredProjects.length === 0 && (
          <GlassCard className="p-12 text-center border-dashed border-2 border-white/10 bg-transparent">
            <div className="w-16 h-16 rounded-full bg-slate-800/50 flex items-center justify-center mx-auto mb-4">
               <svg className="w-8 h-8 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
               </svg>
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Aucun projet trouvé</h3>
            <p className="text-slate-400 mb-6">Créez votre premier projet pour commencer l'analyse</p>
            <Link href="/projects/new">
               <Button variant="primary">
                 Nouveau Projet
               </Button>
            </Link>
          </GlassCard>
        )}
      </div>
    </DashboardLayout>
  );
}
