import React from 'react';
import { MetricsPreview } from './MetricsPreview';

export const Hero = () => {
  return (
    <section className="relative pt-32 pb-20 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-7xl pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-blue-600 rounded-full mix-blend-multiply filter blur-[100px] opacity-20 animate-blob" />
        <div className="absolute top-40 right-20 w-72 h-72 bg-purple-600 rounded-full mix-blend-multiply filter blur-[100px] opacity-20 animate-blob animation-delay-2000" />
        <div className="absolute -bottom-32 left-1/2 w-72 h-72 bg-indigo-600 rounded-full mix-blend-multiply filter blur-[100px] opacity-20 animate-blob animation-delay-4000" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="text-center lg:text-left">
            <div className="inline-flex items-center px-3 py-1 rounded-full border border-blue-500/30 bg-blue-500/10 text-blue-300 text-sm mb-6 backdrop-blur-sm">
              <span className="mr-2">✨</span> Nouvelle Version 2.0
            </div>
            
            <h1 className="text-5xl lg:text-7xl font-bold text-white mb-6 leading-tight">
              L'IA au service de votre <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
                Faisabilité Immo
              </span>
            </h1>
            
            <p className="text-xl text-gray-400 mb-8 max-w-xl mx-auto lg:mx-0">
              Analysez instantanément PLU, risques et rentabilité. Générez des Business Plans bancables en quelques secondes grâce à notre IA spécialisée.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <a href="/auth/register" className="glass-button px-8 py-4 rounded-xl text-white font-semibold flex items-center justify-center gap-2 group">
                Commencer un projet
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </a>
              <a href="/auth/login" className="px-8 py-4 rounded-xl text-gray-300 hover:text-white font-semibold flex items-center justify-center hover:bg-white/5 transition-colors">
                Voir la démo
              </a>
            </div>
          </div>

          <div className="relative">
            <MetricsPreview />
          </div>
        </div>
      </div>
    </section>
  );
};
