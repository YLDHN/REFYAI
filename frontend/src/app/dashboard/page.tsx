'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';
import { DataGrid, projectColumns, type Project } from '@/components/ui/data-grid';
import { GlassCard } from '@/components/ui/GlassCard';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Button } from '@/components/ui/Button';
import { Plus, TrendingUp, AlertTriangle, FileText, LogOut, User } from 'lucide-react';

interface DashboardStats {
  total_projects: number;
  active_projects: number;
  average_tri: number;
  total_investment: number;
}

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout, isAuthenticated } = useAuthStore();

  // Rediriger si non authentifié
  React.useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  // Charger les projets ET les stats BP
  const { data: projectsData, isLoading: projectsLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      try {
        const response = await apiClient.get('/projects');
        return response.data;
      } catch (error) {
        console.error('Erreur lors du chargement des projets:', error);
        return [];
      }
    },
  });

  // Charger stats BP depuis nouveau endpoint
  const { data: bpStats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats', user?.id],
    queryFn: async () => {
      if (!user?.id) return null;
      try {
        const response = await apiClient.get(`/dashboard/stats?user_id=${user.id}`);
        return response.data.stats;
      } catch (error) {
        console.error('Erreur stats BP:', error);
        return null;
      }
    },
    enabled: !!user?.id
  });

  const projects: Project[] = Array.isArray(projectsData) ? projectsData : [];

  // Calculer investissement total pour affichage
  const totalInvestment = projects.reduce((sum, p) => sum + ((p.purchase_price || p.acquisition_price) || 0), 0);

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
            <p className="text-slate-400">Vue d'ensemble de vos projets immobiliers</p>
          </div>
          <div className="flex items-center gap-3">
            {user && (
              <GlassCard className="flex items-center gap-2 px-4 py-2 border-white/10 bg-white/5">
                <User className="w-4 h-4 text-slate-400" />
                <span className="text-sm text-slate-300">{user.email}</span>
              </GlassCard>
            )}
            <Button
              onClick={handleLogout}
              variant="glass"
              className="text-slate-300 hover:text-red-400 hover:bg-red-500/10 border-white/10"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Déconnexion
            </Button>
            <Button
              onClick={() => router.push('/projects/new')}
              className="bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-500/20"
            >
              <Plus className="w-4 h-4 mr-2" />
              Nouveau Projet
            </Button>
          </div>
        </div>

        {/* Stats Cards - BP Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <GlassCard className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-400 mb-1">Projets Totaux</p>
                <p className="text-3xl font-bold text-white">{bpStats?.total_projects || 0}</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center border border-blue-500/10">
                <FileText className="w-6 h-6 text-blue-400" />
              </div>
            </div>
          </GlassCard>

          <GlassCard className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-400 mb-1">En Cours</p>
                <p className="text-3xl font-bold text-white">{bpStats?.active_projects || 0}</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center border border-amber-500/10">
                <AlertTriangle className="w-6 h-6 text-amber-400" />
              </div>
            </div>
          </GlassCard>

          <GlassCard className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-400 mb-1">Equity Disponible</p>
                <p className="text-2xl font-bold text-emerald-400">
                  {bpStats ? `${(bpStats.equity_available / 1000000).toFixed(1)}M€` : 'N/A'}
                </p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center border border-emerald-500/10">
                <TrendingUp className="w-6 h-6 text-emerald-400" />
              </div>
            </div>
          </GlassCard>

          <GlassCard className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-400 mb-1">Durée Moy. Restante</p>
                <p className="text-2xl font-bold text-white">
                  {bpStats ? `${bpStats.avg_duration_remaining_months.toFixed(0)} mois` : 'N/A'}
                </p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center border border-purple-500/10">
                <TrendingUp className="w-6 h-6 text-purple-400" />
              </div>
            </div>
          </GlassCard>

          {bpStats?.technical_score_avg && (
            <GlassCard className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-400 mb-1">Score Technique Moyen</p>
                  <p className="text-3xl font-bold text-sky-400">
                    {bpStats.technical_score_avg.toFixed(1)}/100
                  </p>
                </div>
                <div className="w-12 h-12 rounded-xl bg-sky-500/20 flex items-center justify-center border border-sky-500/10">
                  <TrendingUp className="w-6 h-6 text-sky-400" />
                </div>
              </div>
            </GlassCard>
          )}

          <GlassCard className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-400 mb-1">Investissement Total</p>
                <p className="text-2xl font-bold text-white">
                  {(totalInvestment / 1000000).toFixed(1)}M€
                </p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-indigo-500/20 flex items-center justify-center border border-indigo-500/10">
                <FileText className="w-6 h-6 text-indigo-400" />
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Projects Table */}
        <GlassCard className="p-0 overflow-hidden">
          <div className="p-6 border-b border-white/10">
            <h2 className="text-xl font-bold text-white">Tous les Projets</h2>
          </div>
          <div className="p-6">
            <DataGrid
              data={projects}
              columns={projectColumns}
              onRowClick={(project) => router.push(`/projects/${project.id}`)}
              loading={projectsLoading}
              emptyMessage="Aucun projet créé. Commencez par créer votre premier projet !"
            />
          </div>
        </GlassCard>
      </div>
    </DashboardLayout>
  );
}
