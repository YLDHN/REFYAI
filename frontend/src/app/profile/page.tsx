'use client';

import React from 'react';
import Link from 'next/link';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/Button';
import { GlassCard } from '@/components/ui/GlassCard';

export default function ProfilePage() {
  const { user, logout } = useAuthStore();

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-white">Chargement...</p>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8 max-w-4xl">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Mon Profil</h1>
          <p className="text-slate-400 mt-1">Gérez vos informations personnelles</p>
        </div>
        <Link href="/dashboard">
          <Button variant="ghost" className="text-slate-300 hover:text-white">
            Retour au Dashboard
          </Button>
        </Link>
      </div>

      {/* Profile Card */}
      <GlassCard className="p-8">
        <div className="flex items-start gap-6">
          {/* Avatar */}
          <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-sky-400 to-blue-600 flex items-center justify-center text-white font-bold text-4xl shadow-lg">
            {user.email.charAt(0).toUpperCase()}
          </div>

          {/* User Info */}
          <div className="flex-1 space-y-6">
            {/* Full Name */}
            <div>
              <label className="text-sm text-slate-400 block mb-2">Nom complet</label>
              <div className="bg-slate-900/40 border border-white/5 rounded-lg px-4 py-3 text-white">
                {user.full_name || 'Non renseigné'}
              </div>
            </div>

            {/* Email */}
            <div>
              <label className="text-sm text-slate-400 block mb-2">Email</label>
              <div className="bg-slate-900/40 border border-white/5 rounded-lg px-4 py-3 text-white">
                {user.email}
              </div>
            </div>

            {/* Account Status */}
            <div className="flex items-center gap-4">
              <div>
                <label className="text-sm text-slate-400 block mb-2">Statut du compte</label>
                <div className="flex items-center gap-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    user.is_active 
                      ? 'bg-green-500/10 text-green-400 border border-green-500/20' 
                      : 'bg-red-500/10 text-red-400 border border-red-500/20'
                  }`}>
                    {user.is_active ? 'Actif' : 'Inactif'}
                  </span>
                </div>
              </div>

              {user.is_superuser && (
                <div>
                  <label className="text-sm text-slate-400 block mb-2">Rôle</label>
                  <div className="flex items-center gap-2">
                    <span className="px-3 py-1 rounded-full text-sm font-medium bg-purple-500/10 text-purple-400 border border-purple-500/20">
                      Administrateur
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </GlassCard>

      {/* Account Actions */}
      <GlassCard className="p-6">
        <h2 className="text-xl font-bold text-white mb-4">Actions du compte</h2>
        <div className="space-y-3">
          <Button
            onClick={() => {
              logout();
              window.location.href = '/login';
            }}
            className="w-full bg-red-600/20 hover:bg-red-600/30 text-red-400 border border-red-500/20"
          >
            Se déconnecter
          </Button>
        </div>
      </GlassCard>
    </div>
  );
}
