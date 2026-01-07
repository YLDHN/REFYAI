'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { apiClient } from '@/lib/api';
import { GlassCard } from '@/components/ui/GlassCard';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { AlertCircle } from 'lucide-react';
import Link from 'next/link';

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Appel à l'API de connexion
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await apiClient.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { access_token, user } = response.data;

      // Stocker le token et l'utilisateur
      setAuth(access_token, user);

      // Rediriger vers le dashboard
      router.push('/dashboard');
    } catch (err: any) {
      console.error('Erreur de connexion:', err);
      setError(
        err.response?.data?.detail || 
        'Email ou mot de passe incorrect'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative flex items-center justify-center p-6 overflow-hidden">
       {/* Background Decor */}
       <div className="fixed inset-0 z-0">
        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-slate-900 to-black"></div>
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-purple-600/20 rounded-full blur-[128px]"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-blue-600/10 rounded-full blur-[128px]"></div>
      </div>

      <div className="relative z-10 w-full max-w-md">
        <div className="text-center mb-8">
           <Link href="/" className="inline-flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
                <span className="text-white font-bold text-xl">R</span>
              </div>
              <span className="text-2xl font-bold text-white">REFY AI</span>
           </Link>
           <h2 className="text-xl text-slate-300">Bienvenue</h2>
        </div>

        <GlassCard className="backdrop-blur-xl border-white/10">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="text-center mb-6">
              <h1 className="text-2xl font-bold text-white">Connexion</h1>
              <p className="text-slate-400 text-sm mt-1">Accédez à votre espace d'analyse</p>
            </div>

            {error && (
              <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-400">{error}</p>
              </div>
            )}

            <div className="space-y-4">
              <Input
                label="Email"
                id="email"
                type="email"
                placeholder="email@exemple.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />

              <div className="space-y-1">
                <Input
                  label="Mot de passe"
                  id="password"
                  type="password"
                  placeholder="Mot de passe"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <div className="flex justify-end">
                   <a href="#" className="text-xs text-blue-400 hover:text-blue-300 transition-colors">Mot de passe oublié ?</a>
                </div>
              </div>
            </div>

            <Button
              type="submit"
              variant="primary"
              className="w-full py-3 text-lg font-semibold shadow-blue-500/20"
              isLoading={loading}
            >
              Se connecter
            </Button>

            <div className="text-center pt-4 border-t border-white/5">
              <p className="text-xs text-slate-500 mb-2">Compte de test :</p>
              <code className="px-2 py-1 rounded bg-slate-950/50 border border-white/5 text-xs text-slate-400 font-mono">
                demo@refyai.com / demo123
              </code>
            </div>
          </form>
        </GlassCard>
      </div>
    </div>
  );
}
