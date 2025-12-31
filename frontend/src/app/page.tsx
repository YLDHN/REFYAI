import { Hero } from "@/components/landing/Hero";
import { GlassCard } from "@/components/ui/GlassCard";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />

      {/* Features Grid */}
      <section className="py-20 relative z-10">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-4">Fonctionnalités Puissantes</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Une suite complète d'outils pour sécuriser vos opérations immobilières
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <GlassCard className="hover:bg-white/10 transition-colors group cursor-pointer">
              <div className="w-12 h-12 rounded-lg bg-blue-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Analyse PLU</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Extraction automatique des règles d'urbanisme et contraintes légales depuis vos documents.
              </p>
            </GlassCard>

            <GlassCard className="hover:bg-white/10 transition-colors group cursor-pointer">
              <div className="w-12 h-12 rounded-lg bg-green-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Smart Finance</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Calcul instantané de rentabilité (TRI, VAN) et ratios bancaires (LTV, DSCR).
              </p>
            </GlassCard>

            <GlassCard className="hover:bg-white/10 transition-colors group cursor-pointer">
              <div className="w-12 h-12 rounded-lg bg-purple-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">IA Assistant</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Chattez avec vos documents et obtenez des réponses précises sur la faisabilité technique.
              </p>
            </GlassCard>

            <GlassCard className="hover:bg-white/10 transition-colors group cursor-pointer">
              <div className="w-12 h-12 rounded-lg bg-orange-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Business Plan</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Export automatique de dossiers financiers complets au format Excel et PDF.
              </p>
            </GlassCard>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 mt-20 bg-black/20 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-500 text-sm">© 2025 REFY AI. All rights reserved.</p>
            <div className="flex gap-6">
              <a href="#" className="text-gray-500 hover:text-white transition-colors text-sm">Terms</a>
              <a href="#" className="text-gray-500 hover:text-white transition-colors text-sm">Privacy</a>
              <a href="#" className="text-gray-500 hover:text-white transition-colors text-sm">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
}
