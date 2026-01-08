'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { GlassCard } from '@/components/ui/GlassCard';

export default function RegisterPage() {
  const router = useRouter();
  const { setAuth } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }

    if (formData.password.length < 6) {
      setError('Le mot de passe doit contenir au moins 6 caractères');
      return;
    }

    if (!formData.email.includes('@')) {
      setError('Email invalide');
      return;
    }

    setLoading(true);

    try {
      // Créer le compte
      await apiClient.post('/auth/register', {
        email: formData.email,
        password: formData.password,
        full_name: formData.full_name || formData.email.split('@')[0]
      });

      // Se connecter automatiquement après création
      const loginResponse = await apiClient.post('/auth/login', {
        username: formData.email,
        password: formData.password
      });

      const { access_token, user } = loginResponse.data;

      // Stocker le token et l'utilisateur
      setAuth(access_token, user);

      // Rediriger vers le dashboard
      router.push('/dashboard');
    } catch (err: any) {
      console.error('Erreur inscription:', err);
      setError(
        err.response?.data?.detail || 
        err.response?.data?.message ||
        'Une erreur est survenue lors de la création du compte'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-4">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Logo and Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-tr from-blue-500 to-purple-600 mb-4 shadow-lg shadow-blue-500/50">
            <span className="text-2xl font-bold text-white">R</span>
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">REFY AI</h1>
          <p className="text-slate-400">Analyse Immobilière Intelligente</p>
        </div>

        <GlassCard className="p-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-white mb-2">Créer un compte</h2>
            <p className="text-sm text-slate-400">
              Commencez votre analyse immobilière
            </p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
              <p className="text-sm text-red-400">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-4">
              <Input
                label="Nom complet (optionnel)"
                id="full_name"
                type="text"
                placeholder="Jean Dupont"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              />

              <Input
                label="Email"
                id="email"
                type="email"
                placeholder="vous@exemple.com"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
              />

              <Input
                label="Mot de passe"
                id="password"
                type="password"
                placeholder="Minimum 6 caractères"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
              />

              <Input
                label="Confirmer le mot de passe"
                id="confirmPassword"
                type="password"
                placeholder="Confirmer le mot de passe"
                value={formData.confirmPassword}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                required
              />
            </div>

            <Button
              type="submit"
              variant="primary"
              className="w-full py-3 text-lg font-semibold shadow-blue-500/20"
              isLoading={loading}
            >
              Créer mon compte
            </Button>

            <div className="text-center pt-4 border-t border-white/5">
              <p className="text-sm text-slate-400">
                Vous avez déjà un compte ?{' '}
                <Link href="/login" className="text-blue-400 hover:text-blue-300 font-medium transition-colors">
                  Se connecter
                </Link>
              </p>
            </div>
          </form>
        </GlassCard>
      </div>
    </div>
  );
}
