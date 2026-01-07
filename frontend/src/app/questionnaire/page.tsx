'use client';

import { useState } from 'react';
import Link from 'next/link';
import { questionnaireAPI } from '@/lib/api';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { GlassCard } from '@/components/ui/GlassCard';

interface Question {
  id: string;
  question: string;
  type: string;
  required: boolean;
  options?: string[];
  help_text?: string;
}

export default function QuestionnairePage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const questions: Question[] = [
    {
      id: 'commune',
      question: 'Dans quelle commune se situe le bien ?',
      type: 'text',
      required: true,
      help_text: 'Exemple: Paris, Lyon, Marseille...'
    },
    {
      id: 'address',
      question: 'Quelle est l\'adresse du bien ?',
      type: 'text',
      required: true,
      help_text: 'Numéro et nom de rue'
    },
    {
      id: 'parcelle_cadastrale',
      question: 'Référence cadastrale (si connue)',
      type: 'text',
      required: false,
      help_text: 'Format: Section + Numéro (ex: AK 123)'
    },
    {
      id: 'zone_plu',
      question: 'Zone PLU (si connue)',
      type: 'select',
      required: false,
      options: ['UA', 'UB', 'UC', 'UD', 'UE', 'AU', 'A', 'N', 'Inconnue'],
      help_text: 'Zone d\'urbanisme du PLU'
    },
    {
      id: 'surface_terrain',
      question: 'Surface du terrain (m²)',
      type: 'number',
      required: true
    },
    {
      id: 'surface_construite',
      question: 'Surface construite actuelle (m²)',
      type: 'number',
      required: true
    },
    {
      id: 'monuments_historiques',
      question: 'Le bien est-il situé dans le périmètre des monuments historiques ?',
      type: 'boolean',
      required: true,
      options: ['Oui', 'Non', 'Ne sais pas']
    },
    {
      id: 'abf_required',
      question: 'Un avis ABF est-il requis ?',
      type: 'boolean',
      required: true,
      help_text: 'Architecte des Bâtiments de France',
      options: ['Oui', 'Non', 'Ne sais pas']
    },
    {
      id: 'destination_actuelle',
      question: 'Destination actuelle du bien',
      type: 'select',
      required: true,
      options: ['habitation', 'commerce', 'bureaux', 'hotel', 'industriel', 'mixte']
    },
    {
      id: 'destination_future',
      question: 'Destination future souhaitée',
      type: 'select',
      required: true,
      options: ['habitation', 'commerce', 'bureaux', 'hotel', 'industriel', 'mixte']
    },
    {
      id: 'type_travaux',
      question: 'Type de travaux envisagés',
      type: 'select',
      required: true,
      options: [
        'renovation_legere',
        'renovation_lourde',
        'extension',
        'surelevation',
        'changement_destination',
        'construction_neuve'
      ]
    },
    {
      id: 'surface_plancher',
      question: 'Surface de plancher projetée (m²)',
      type: 'number',
      required: true
    }
  ];

  const totalSteps = questions.length;
  const progress = ((currentStep + 1) / totalSteps) * 100;

  const handleAnswer = (questionId: string, value: any) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
    setErrors(prev => {
      const newErrors = { ...prev };
      delete newErrors[questionId];
      return newErrors;
    });
  };

  const validateCurrentStep = () => {
    const question = questions[currentStep];
    if (question.required && !answers[question.id]) {
      setErrors({ [question.id]: 'Ce champ est requis' });
      return false;
    }
    return true;
  };

  const handleNext = () => {
    if (validateCurrentStep()) {
      if (currentStep < totalSteps - 1) {
        setCurrentStep(prev => prev + 1);
      } else {
        handleSubmit();
      }
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      // Mock validation
      console.log('Soumission:', answers);
      setTimeout(() => {
        alert('✅ Questionnaire validé !');
        // TODO: Redirect
      }, 1000);
    } catch (error: any) {
      console.error('Erreur:', error);
      alert('Erreur lors de la soumission');
    } finally {
      setLoading(false);
    }
  };

  const currentQuestion = questions[currentStep];

  const renderInput = () => {
    switch (currentQuestion.type) {
      case 'text':
        return (
          <input
            type="text"
            value={answers[currentQuestion.id] || ''}
            onChange={(e) => handleAnswer(currentQuestion.id, e.target.value)}
            className="w-full px-4 py-3 text-lg rounded-xl glass-input text-white border border-white/10 focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all placeholder:text-slate-600"
            placeholder={currentQuestion.help_text || 'Votre réponse...'}
            autoFocus
          />
        );

      case 'number':
        return (
          <input
            type="number"
            value={answers[currentQuestion.id] || ''}
            onChange={(e) => handleAnswer(currentQuestion.id, parseFloat(e.target.value))}
            className="w-full px-4 py-3 text-lg rounded-xl glass-input text-white border border-white/10 focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all placeholder:text-slate-600"
            placeholder="Entrez un nombre"
            autoFocus
          />
        );

      case 'select':
        return (
          <div className="grid grid-cols-1 gap-3">
             <select
                value={answers[currentQuestion.id] || ''}
                onChange={(e) => handleAnswer(currentQuestion.id, e.target.value)}
                className="w-full px-4 py-3 rounded-xl glass-input text-white border border-white/10 p-2 appearance-none bg-[url('data:image/svg+xml;charset=us-ascii,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22white%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpolyline%20points%3D%226%209%2012%2015%2018%209%22%3E%3C%2Fpolyline%3E%3C%2Fsvg%3E')] bg-no-repeat bg-[right_1rem_center] bg-[length:1rem]"
             >
                <option value="" className="bg-slate-900 text-slate-400">Sélectionner une option...</option>
                {currentQuestion.options?.map(option => (
                  <option key={option} value={option} className="bg-slate-900 text-white">{option.replace(/_/g, ' ')}</option>
                ))}
            </select>
          </div>
        );

      case 'boolean':
        return (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {currentQuestion.options?.map(option => (
              <label 
                key={option} 
                className={`flex items-center justify-center p-4 rounded-xl border cursor-pointer transition-all duration-300 ${
                  answers[currentQuestion.id] === option 
                    ? 'bg-blue-600 text-white border-blue-500 shadow-[0_0_20px_rgba(37,99,235,0.3)]' 
                    : 'bg-white/5 border-white/10 text-slate-300 hover:bg-white/10 hover:border-white/20'
                }`}
              >
                <input
                  type="radio"
                  name={currentQuestion.id}
                  checked={answers[currentQuestion.id] === option}
                  onChange={() => handleAnswer(currentQuestion.id, option)}
                  className="hidden"
                />
                <span className="font-medium text-lg">{option}</span>
              </label>
            ))}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-theme(spacing.32))] py-8">
        <div className="w-full max-w-2xl space-y-8">
          
          {/* Header */}
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-white">Questionnaire</h1>
            <Link 
              href="/analyses"
              className="text-sm text-slate-400 hover:text-white transition-colors"
            >
              Annuler
            </Link>
          </div>

          {/* Progress Bar */}
          <div className="relative h-1.5 bg-slate-800 rounded-full overflow-hidden">
            <div 
              className="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-600 to-purple-600 transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            />
            <div 
              className="absolute top-0 right-0 h-full w-[2px] bg-white/50 blur-[2px]"
              style={{ left: `${progress}%`, transition: 'left 0.5s ease-out' }}
            />
          </div>

          {/* Card */}
          <GlassCard className="p-8 sm:p-10 relative overflow-hidden min-h-[400px] flex flex-col justify-center">
            {/* Background Decor */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/5 rounded-full blur-3xl -mr-32 -mt-32 pointer-events-none"></div>
            <div className="absolute bottom-0 left-0 w-64 h-64 bg-purple-500/5 rounded-full blur-3xl -ml-32 -mb-32 pointer-events-none"></div>

            <div className="relative z-10 space-y-8">
              {/* Question */}
              <div className="space-y-2">
                <span className="text-xs font-medium text-blue-400 uppercase tracking-widest">Question {currentStep + 1} / {totalSteps}</span>
                <h2 className="text-2xl sm:text-3xl font-bold text-white leading-tight">
                  {currentQuestion.question}
                </h2>
                {currentQuestion.help_text && (
                  <p className="text-slate-400 text-sm">{currentQuestion.help_text}</p>
                )}
              </div>

              {/* Input Area */}
              <div>
                {renderInput()}
                {errors[currentQuestion.id] && (
                  <p className="mt-2 text-red-400 text-sm flex items-center gap-1">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    {errors[currentQuestion.id]}
                  </p>
                )}
              </div>
            </div>

            {/* Navigation Buttons (Bottom of Card) */}
            <div className="mt-12 flex items-center justify-between pt-6 border-t border-white/5 relative z-10">
              <button
                onClick={handlePrevious}
                disabled={currentStep === 0}
                className={`text-slate-400 font-medium px-4 py-2 hover:text-white disabled:opacity-30 disabled:hover:text-slate-400 transition-colors ${currentStep === 0 ? 'invisible' : ''}`}
              >
                ← Précédent
              </button>

              <button
                onClick={handleNext}
                disabled={loading}
                className="group relative px-8 py-3 bg-white text-slate-900 rounded-xl font-bold hover:bg-slate-100 focus:ring-4 focus:ring-white/20 transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden"
              >
                <span className="relative z-10 flex items-center gap-2">
                  {loading ? 'Envoi...' : currentStep === totalSteps - 1 ? 'Terminer' : 'Suivant'}
                  {!loading && (
                    <svg className="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                  )}
                </span>
              </button>
            </div>
          </GlassCard>

          {/* Dots Indicator */}
          <div className="flex justify-center gap-2">
            {questions.map((_, index) => (
              <div
                key={index}
                className={`h-1.5 rounded-full transition-all duration-300 ${
                  index === currentStep ? 'w-8 bg-white' : 
                  index < currentStep ? 'w-1.5 bg-blue-500' : 
                  'w-1.5 bg-slate-800'
                }`}
              />
            ))}
          </div>

        </div>
      </div>
    </DashboardLayout>
  );
}
