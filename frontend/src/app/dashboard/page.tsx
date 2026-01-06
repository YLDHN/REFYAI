'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';
import { DataGrid, projectColumns, type Project } from '@/components/ui/data-grid';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
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

  // Charger les projets
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

  const projects: Project[] = Array.isArray(projectsData) ? projectsData : [];

  // Calculer les stats
  const stats: DashboardStats = React.useMemo(() => {
    return {
      total_projects: projects.length,
      active_projects: projects.filter(p => p.status === 'En cours').length,
      average_tri: projects.length > 0
        ? projects.reduce((sum, p) => sum + (p.tri_avant_is || 0), 0) / projects.length
        : 0,
      total_investment: projects.reduce((sum, p) => sum + (p.prix_acquisition || 0), 0),
    };
  }, [projects]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-blue-950 to-purple-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
            <p className="text-gray-400">Vue d'ensemble de vos projets immobiliers</p>
          </div>
          <div className="flex items-center gap-3">
            {user && (
              <div className="flex items-center gap-2 px-4 py-2 bg-gray-800/50 rounded-lg border border-gray-700">
                <User className="w-4 h-4 text-gray-400" />
                <span className="text-sm text-gray-300">{user.email}</span>
              </div>
            )}
            <Button
              onClick={handleLogout}
              variant="outline"
              className="border-gray-700 text-gray-300 hover:bg-red-600 hover:border-red-600 hover:text-white"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Déconnexion
            </Button>
            <Button
              onClick={() => router.push('/projects/new')}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              <Plus className="w-4 h-4 mr-2" />
              Nouveau Projet
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="bg-gray-900/50 border-gray-800">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Projets Totaux</p>
                  <p className="text-3xl font-bold text-white">{stats.total_projects}</p>
                </div>
                <div className="w-12 h-12 rounded-lg bg-blue-500/20 flex items-center justify-center">
                  <FileText className="w-6 h-6 text-blue-400" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-900/50 border-gray-800">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">En Cours</p>
                  <p className="text-3xl font-bold text-white">{stats.active_projects}</p>
                </div>
                <div className="w-12 h-12 rounded-lg bg-yellow-500/20 flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-yellow-400" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-900/50 border-gray-800">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">TRI Moyen</p>
                  <p className="text-3xl font-bold text-white">
                    {(stats.average_tri * 100).toFixed(1)}%
                  </p>
                </div>
                <div className="w-12 h-12 rounded-lg bg-green-500/20 flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-green-400" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-900/50 border-gray-800">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Investissement Total</p>
                  <p className="text-2xl font-bold text-white">
                    {(stats.total_investment / 1000000).toFixed(1)}M€
                  </p>
                </div>
                <div className="w-12 h-12 rounded-lg bg-purple-500/20 flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-purple-400" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Projects Table */}
        <Card className="bg-gray-900/50 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Tous les Projets</CardTitle>
          </CardHeader>
          <CardContent>
            <DataGrid
              data={projects}
              columns={projectColumns}
              onRowClick={(project) => router.push(`/projects/${project.id}`)}
              loading={projectsLoading}
              emptyMessage="Aucun projet créé. Commencez par créer votre premier projet !"
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
