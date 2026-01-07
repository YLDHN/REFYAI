'use client';

import React from 'react';
import Link from 'next/link';
import { GlassCard } from '@/components/ui/GlassCard';
import { Button } from '@/components/ui/Button';

export default function Home() {
  return (
    <div className="min-h-screen relative overflow-hidden text-white selection:bg-sky-500/30">
      
      {/* Background Decor */}
      <div className="fixed inset-0 z-0">
        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-slate-900 to-black"></div>
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-purple-500/30 rounded-full blur-[128px]"></div>
        <div className="absolute top-40 -left-20 w-72 h-72 bg-blue-500/20 rounded-full blur-[100px]"></div>
        <div className="absolute bottom-0 right-1/2 translate-x-1/2 w-[800px] h-[400px] bg-indigo-500/10 rounded-full blur-[120px]"></div>
      </div>

      {/* Navbar */}
      <nav className="relative z-50 p-6 flex items-center justify-between max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
           <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <span className="text-white font-bold text-lg">R</span>
            </div>
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-blue-200">
              REFY AI
            </span>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/login">
            <Button variant="glass" size="sm">Se Connecter</Button>
          </Link>
          <Link href="/signup">
            <Button variant="primary" size="sm" className="shadow-blue-500/25 shadow-lg">Commencer</Button>
          </Link>
        </div>
      </nav>

      <main className="relative z-10 max-w-7xl mx-auto px-6 py-20">
        
        {/* Hero Section */}
        <div className="text-center max-w-4xl mx-auto mb-32">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 mb-8 backdrop-blur-sm animate-float">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            <span className="text-sm text-slate-300">Nouvelle version disponible</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-8 leading-tight tracking-tight">
            L'Intelligence Artificielle au service de <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400">
              l'Analyse Immobilière
            </span>
          </h1>
          
          <p className="text-xl text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed">
            Automatisez vos études de faisabilité, générez des rapports financiers précis et débloquez le potentiel de vos investissements en quelques secondes.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
             <Link href="/login">
              <Button variant="primary" size="lg" className="w-full sm:w-auto text-lg px-8 py-4 shadow-xl shadow-blue-600/20 hover:shadow-blue-600/40">
                Lancer une Analyse
              </Button>
             </Link>
             <Link href="#features">
              <Button variant="glass" size="lg" className="w-full sm:w-auto text-lg px-8 py-4">
                Découvrir les fonctionnalités
              </Button>
             </Link>
          </div>
        </div>

        {/* Floating Cards / Preview */}
        <div className="relative mb-32 group perspective-1000">
          <div className="absolute inset-0 bg-blue-500/20 blur-[100px] -z-10 group-hover:bg-blue-500/30 transition-all duration-1000"></div>
          <GlassCard className="border-white/10 bg-slate-900/60 backdrop-blur-xl p-0 overflow-hidden shadow-2xl transform rotate-x-12 transition-transform duration-700 group-hover:rotate-0">
             <div className="grid grid-cols-12 gap-0">
                {/* Mock Sidebar */}
                <div className="hidden md:block col-span-2 border-r border-white/5 bg-white/5 p-4 space-y-4">
                  <div className="h-2 w-8 bg-white/20 rounded mb-6"></div>
                  <div className="h-8 w-full bg-blue-500/20 rounded border border-blue-500/30"></div>
                  <div className="h-8 w-3/4 bg-white/5 rounded"></div>
                  <div className="h-8 w-4/5 bg-white/5 rounded"></div>
                </div>
                {/* Mock Content */}
                <div className="col-span-12 md:col-span-10 p-8">
                  <div className="flex justify-between items-center mb-8">
                    <div>
                      <div className="h-8 w-64 bg-white/20 rounded mb-2"></div>
                      <div className="h-4 w-32 bg-white/10 rounded"></div>
                    </div>
                    <div className="flex gap-2">
                       <div className="h-10 w-24 bg-blue-500 rounded"></div>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-4 mb-8">
                    <div className="h-32 bg-white/5 rounded border border-white/5"></div>
                    <div className="h-32 bg-white/5 rounded border border-white/5"></div>
                    <div className="h-32 bg-white/5 rounded border border-white/5"></div>
                  </div>
                  <div className="h-64 bg-white/5 rounded border border-white/5"></div>
                </div>
             </div>
          </GlassCard>
        </div>

        {/* Features Grid */}
        <div id="features" className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-32">
          <FeatureCard 
            title="Analyses Automatisées"
            description="Laissez nos algorithmes traiter des documents complexes (PLU, bilans) pour en extraire les données clés instantanément."
            icon={<DocumentIcon />}
            delay="0"
          />
          <FeatureCard 
            title="Modélisation Financière"
            description="Générez des prévisionnels financiers détaillés (Cashflow, ROI, TRI) basés sur des données de marché en temps réel."
            icon={<ChartIcon />}
            delay="100"
          />
          <FeatureCard 
            title="Assistant IA Dédié"
            description="Dialoguez avec votre projet. Posez des questions sur la réglementation ou la rentabilité et obtenez des réponses précises."
            icon={<ChatIcon />}
            delay="200"
          />
        </div>
        
      </main>

      {/* Footer */}
      <footer className="border-t border-white/5 bg-black/40 backdrop-blur-xl py-12">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
          <p className="text-slate-500 text-sm">© 2026 REFY AI - Tous droits réservés.</p>
          <div className="flex gap-6 text-slate-400">
            <span className="hover:text-white cursor-pointer transition-colors">Mentions Légales</span>
            <span className="hover:text-white cursor-pointer transition-colors">Confidentialité</span>
            <span className="hover:text-white cursor-pointer transition-colors">Contact</span>
          </div>
        </div>
      </footer>

    </div>
  );
}

// Icons & Sub-components

function FeatureCard({ title, description, icon, delay }: { title: string, description: string, icon: React.ReactNode, delay: string }) {
  return (
    <GlassCard className="p-8 hover:bg-white/5 transition-all duration-300 hover:-translate-y-2 group" hoverEffect={true}>
      <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-400 mb-6 group-hover:scale-110 transition-transform duration-300 group-hover:bg-blue-500/20">
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3 text-white">{title}</h3>
      <p className="text-slate-400 leading-relaxed">
        {description}
      </p>
    </GlassCard>
  )
}

function DocumentIcon() {
  return (
    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  )
}

function ChartIcon() {
  return (
    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
    </svg>
  )
}

function ChatIcon() {
  return (
    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
    </svg>
  )
}
