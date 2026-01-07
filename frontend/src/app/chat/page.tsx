'use client';

import { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { GlassCard } from '@/components/ui/GlassCard';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Bonjour ! Je suis votre assistant IA REFY. Comment puis-je vous aider avec vos projets immobiliers aujourd\'hui ?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const suggestions = [
    '💡 Quels sont les critères pour un bon TRI ?',
    '📊 Comment analyser un PLU ?',
    '⚠️ Qu\'est-ce qu\'un showstopper critique ?',
    '📈 Comment calculer la rentabilité locative ?',
  ];

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        role: 'assistant',
        content: 'Je suis actuellement en mode démo. Pour obtenir des réponses personnalisées basées sur vos projets, connectez-vous avec votre compte et synchronisez vos données.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
      setLoading(false);
    }, 1500);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col h-[calc(100vh-theme(spacing.24))]">
        {/* Header Content */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Chat IA</h1>
            <p className="text-slate-400">Votre assistant intelligent pour l'analyse immobilière</p>
          </div>
          <button className="px-4 py-2 rounded-lg bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-all text-sm font-medium">
            Nouvelle conversation
          </button>
        </div>

        {/* Chat Container */}
        <GlassCard className="flex-1 flex flex-col min-h-0 overflow-hidden relative">
          
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex items-start gap-4 max-w-3xl ${message.role === 'user' ? 'flex-row-reverse' : ''}`}>
                  {/* Avatar */}
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg ${
                    message.role === 'assistant' 
                      ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white' 
                      : 'bg-slate-700 text-slate-300'
                  }`}>
                    {message.role === 'assistant' ? (
                      <span className="text-lg">🤖</span>
                    ) : (
                      <span className="text-lg">👤</span>
                    )}
                  </div>

                  {/* Message Bubble */}
                  <div className={`rounded-2xl px-6 py-4 shadow-lg backdrop-blur-sm ${
                    message.role === 'assistant'
                      ? 'bg-white/5 border border-white/10 text-slate-200'
                      : 'bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-blue-500/20'
                  }`}>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">
                      {message.content}
                    </p>
                    <p className={`text-[10px] mt-2 font-medium ${message.role === 'assistant' ? 'text-slate-500' : 'text-blue-100/70'}`}>
                      {message.timestamp.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="flex items-start gap-4 max-w-3xl">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0 shadow-lg">
                    <span className="text-lg">🤖</span>
                  </div>
                  <div className="bg-white/5 border border-white/10 rounded-2xl px-6 py-4">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-75"></div>
                      <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-150"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {/* Empty State Suggestions */}
            {messages.length === 1 && !loading && (
              <div className="mt-12 mb-6">
                <p className="text-sm font-medium text-slate-400 mb-4 px-1">Suggestions de questions :</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => setInput(suggestion.replace(/^[^\s]+\s/, ''))}
                      className="text-left p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-blue-500/50 hover:shadow-lg hover:shadow-blue-500/10 transition-all group"
                    >
                      <span className="text-sm text-slate-300 group-hover:text-white transition-colors">
                        {suggestion}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-white/10 bg-black/20 backdrop-blur-md">
            <div className="relative flex items-end gap-2 bg-slate-900/50 border border-white/10 rounded-xl p-2 focus-within:border-blue-500/50 focus-within:ring-1 focus-within:ring-blue-500/50 transition-all">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Posez votre question à l'IA..."
                rows={1}
                className="flex-1 max-h-32 resize-none bg-transparent border-0 focus:ring-0 text-slate-200 placeholder-slate-500 text-sm py-3 px-2 scrollbar-thin"
                style={{ minHeight: '44px' }}
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || loading}
                className="p-2.5 rounded-lg bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40 disabled:opacity-50 disabled:cursor-not-allowed hover:-translate-y-0.5 transition-all flex-shrink-0"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
            <div className="flex items-center justify-between mt-3 text-xs text-slate-500 px-1">
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>L'IA utilise vos données projets pour contextaliser ses réponses.</span>
              </div>
              <span className={input.length > 1800 ? 'text-orange-400' : ''}>{input.length}/2000</span>
            </div>
          </div>
        </GlassCard>
      </div>
    </DashboardLayout>
  );
}
