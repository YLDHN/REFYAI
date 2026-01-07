'use client';

import { useState, useEffect, useRef } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { GlassCard } from '@/components/ui/GlassCard';
import { documentsAPI } from '@/lib/api';

interface Document {
  id: number;
  name: string;
  type: 'PLU' | 'Diagnostic' | 'Cadastre' | 'Autre';
  size: string;
  uploadedAt: string;
  status: 'processed' | 'processing' | 'pending';
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await documentsAPI.getAll();
      const docs = Array.isArray(response.data) ? response.data : [];
      setDocuments(docs);
    } catch (err: any) {
      console.error('Erreur lors du chargement des documents:', err);
      // Fallback vers données mock en cas d'erreur
      setDocuments([
        { id: 1, name: 'PLU_Paris_16.pdf', type: 'PLU', size: '2.4 MB', uploadedAt: '2025-12-30', status: 'processed' },
        { id: 2, name: 'DPE_Rapport.pdf', type: 'Diagnostic', size: '856 KB', uploadedAt: '2025-12-28', status: 'processed' },
        { id: 3, name: 'Plan_Cadastral.pdf', type: 'Cadastre', size: '1.2 MB', uploadedAt: '2025-12-25', status: 'processing' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file: File) => {
    setUploading(true);
    setError(null);
    try {
      await documentsAPI.upload(file);
      await fetchDocuments();
      alert('✅ Document uploadé avec succès !');
    } catch (err: any) {
      console.error('Erreur upload:', err);
      setError(err.response?.data?.detail || 'Erreur lors de l\'upload');
      alert('❌ Erreur lors de l\'upload du document');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id: number, name: string) => {
    if (!confirm(`Supprimer "${name}" ?`)) return;
    
    try {
      await documentsAPI.delete(id);
      await fetchDocuments();
      alert('✅ Document supprimé');
    } catch (err: any) {
      console.error('Erreur suppression:', err);
      alert('❌ Erreur lors de la suppression');
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleUpload(file);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  const getTypeStyle = (type: string) => {
    switch (type) {
      case 'PLU': return 'bg-blue-500/20 text-blue-300 border-blue-500/20';
      case 'Diagnostic': return 'bg-green-500/20 text-green-300 border-green-500/20';
      case 'Cadastre': return 'bg-purple-500/20 text-purple-300 border-purple-500/20';
      default: return 'bg-slate-500/20 text-slate-300 border-slate-500/20';
    }
  };

  const getStatusStyle = (status: string) => {
    switch (status) {
      case 'processed': return 'bg-green-500/10 text-green-400 border border-green-500/20';
      case 'processing': return 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20';
      default: return 'bg-slate-500/10 text-slate-400 border border-slate-500/20';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'processed': return 'Traité';
      case 'processing': return 'En cours';
      default: return 'En attente';
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Documents</h1>
            <p className="text-slate-400">Gérez et analysez vos documents de projet</p>
          </div>
          <button 
            onClick={triggerFileInput}
            disabled={uploading}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40 hover:-translate-y-0.5 transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            {uploading ? 'Upload...' : 'Téléverser'}
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.png,.jpg,.jpeg,.doc,.docx"
            onChange={handleFileSelect}
            className="hidden"
          />
        </div>

        {/* Upload Zone */}
        <div 
          onClick={triggerFileInput}
          className="group relative overflow-hidden rounded-2xl border-2 border-dashed border-white/10 bg-white/5 hover:bg-white/10 hover:border-blue-500/50 hover:shadow-[0_0_20px_rgba(59,130,246,0.1)] transition-all duration-300 cursor-pointer p-12 text-center"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
          
          <div className="relative z-10">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-blue-500 to-purple-600 p-0.5 mx-auto mb-4 group-hover:scale-110 transition-transform duration-300 shadow-lg shadow-blue-500/20">
              <div className="w-full h-full rounded-[14px] bg-slate-900 flex items-center justify-center">
                <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
            </div>
            <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-blue-300 transition-colors">
              {uploading ? '⏳ Upload en cours...' : 'Glissez vos documents ici'}
            </h3>
            <p className="text-slate-400 mb-4 group-hover:text-slate-300">ou cliquez pour parcourir vos fichiers</p>
            <p className="text-xs text-slate-500 uppercase tracking-widest font-medium">PDG PNG JPG DOC jusqu'à 10MB</p>
          </div>
        </div>

        {/* Categories Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            { label: 'PLU', count: 1, icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z', color: 'blue' },
            { label: 'Diagnostics', count: 1, icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2', color: 'green' },
            { label: 'Cadastre', count: 1, icon: 'M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7', color: 'purple' },
            { label: 'Autres', count: 0, icon: 'M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z', color: 'slate' },
          ].map((stat, idx) => (
            <GlassCard key={idx} className="p-4 flex items-center justify-between group hover:-translate-y-1 transition-transform">
              <div>
                <p className="text-sm font-medium text-slate-400 mb-1">{stat.label}</p>
                <p className="text-2xl font-bold text-white">{stat.count}</p>
              </div>
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center bg-${stat.color}-500/10 text-${stat.color}-400 group-hover:bg-${stat.color}-500/20 transition-colors`}>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={stat.icon} />
                </svg>
              </div>
            </GlassCard>
          ))}
        </div>

        {/* Documents List */}
        <GlassCard className="overflow-hidden">
          <div className="p-6 border-b border-white/10 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Tous les Documents</h2>
            <div className="flex items-center gap-3">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Rechercher..."
                  className="bg-slate-900/50 border border-white/10 rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 w-64"
                />
                <svg className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/5 bg-white/5">
                  <th className="px-6 py-4 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Nom</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Type</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Taille</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Statut</th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-4 text-right text-xs font-semibold text-slate-400 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {documents.map((doc) => (
                  <tr key={doc.id} className="hover:bg-white/5 transition-colors group">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-10 h-10 rounded-lg bg-slate-800 border border-white/5 flex items-center justify-center mr-3 group-hover:border-blue-500/30 transition-colors">
                          <svg className="w-5 h-5 text-slate-400 group-hover:text-blue-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                        </div>
                        <span className="text-sm font-medium text-slate-200 group-hover:text-white transition-colors">{doc.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${getTypeStyle(doc.type)}`}>
                        {doc.type}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-400">
                      {doc.size}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${getStatusStyle(doc.status)}`}>
                        {getStatusLabel(doc.status)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-400">
                      {new Date(doc.uploadedAt).toLocaleDateString('fr-FR')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                      <div className="flex items-center justify-end gap-3 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button className="text-slate-400 hover:text-white transition-colors" title="Voir">
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                        </button>
                        <button className="text-blue-400 hover:text-blue-300 transition-colors" title="Télécharger">
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                          </svg>
                        </button>
                        <button 
                          onClick={() => handleDelete(doc.id, doc.name)}
                          className="text-red-400 hover:text-red-300 transition-colors"
                          title="Supprimer"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>

        {/* Info Box */}
        <GlassCard className="p-6 bg-gradient-to-br from-blue-900/20 to-purple-900/20 border-blue-500/20">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center flex-shrink-0 text-blue-400">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">📄 Analyse Automatique</h3>
              <p className="text-slate-300 mb-3 text-sm leading-relaxed">
                Nos algorithmes IA analysent automatiquement vos documents pour extraire les informations clés :
              </p>
              <ul className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <li className="flex items-center gap-2 text-slate-400">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                  <span className="text-slate-200 font-medium">PLU :</span> Zones, COS, Hauteurs
                </li>
                <li className="flex items-center gap-2 text-slate-400">
                  <span className="w-1.5 h-1.5 rounded-full bg-green-400"></span>
                  <span className="text-slate-200 font-medium">Diagnostics :</span> DPE, Amiante, Plomb
                </li>
                <li className="flex items-center gap-2 text-slate-400">
                  <span className="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
                  <span className="text-slate-200 font-medium">Cadastre :</span> Parcelles, Surfaces
                </li>
              </ul>
            </div>
          </div>
        </GlassCard>
      </div>
    </DashboardLayout>
  );
}
