'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';

const menuItems = [
  { 
    name: 'Dashboard', 
    path: '/dashboard', 
    icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' 
  },
  { 
    name: 'Projets', 
    path: '/projects', 
    icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4' 
  },
  { 
    name: 'Analyses', 
    path: '/analyses', 
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' 
  },
  { 
    name: 'Documents', 
    path: '/documents', 
    icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' 
  },
  { 
    name: 'Chat IA', 
    path: '/chat', 
    icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z' 
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user } = useAuthStore();
  
  return (
    <aside className="w-72 h-screen fixed left-0 top-0 z-40">
      <div className="h-full flex flex-col glass-panel border-r border-white/10">
        {/* Logo Section */}
        <div className="p-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <span className="text-white font-bold text-xl">R</span>
            </div>
            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-blue-200">
              REFY AI
            </h1>
          </div>
          <p className="text-xs text-sky-200/60 font-medium tracking-wide uppercase ml-1">
            Analyse Immobilière Intelligente
          </p>
        </div>
        
        {/* Navigation */}
        <nav className="flex-1 px-4 space-y-2 mt-4 overflow-y-auto">
          {menuItems.map((item) => {
            const isActive = pathname.startsWith(item.path);
            return (
              <Link
                key={item.path}
                href={item.path}
                className={`
                  group relative flex items-center gap-3 px-4 py-3.5 rounded-xl transition-all duration-300
                  ${isActive 
                    ? 'bg-gradient-to-r from-blue-600/80 to-purple-600/80 text-white shadow-lg shadow-blue-900/20' 
                    : 'text-slate-400 hover:text-white hover:bg-white/5'
                  }
                `}
              >
                {isActive && (
                  <div className="absolute left-0 w-1 h-8 bg-white rounded-r-full shadow-[0_0_10px_rgba(255,255,255,0.5)]"></div>
                )}
                <svg 
                  className={`w-5 h-5 transition-transform duration-300 ${isActive ? 'scale-110' : 'group-hover:scale-110'}`} 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                </svg>
                <span className="font-medium tracking-wide text-sm">{item.name}</span>
              </Link>
            );
          })}
        </nav>
        
        {/* User Profile */}
        <div className="p-4 mx-4 mb-4 mt-auto">
          <Link href="/profile">
            <div className="p-4 rounded-xl bg-white/5 border border-white/5 flex items-center gap-3 hover:bg-white/10 transition-colors cursor-pointer group">
              <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-sky-400 to-blue-600 flex items-center justify-center text-white font-bold shadow-lg">
                {user?.email?.charAt(0).toUpperCase() || 'U'}
              </div>
              <div className="flex-1 overflow-hidden">
                <p className="text-sm font-semibold text-white truncate">
                  {user?.full_name || 'Utilisateur'}
                </p>
                <p className="text-xs text-slate-400 truncate group-hover:text-slate-300">
                  {user?.email || 'user@refy.ai'}
                </p>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </aside>
  );
}
