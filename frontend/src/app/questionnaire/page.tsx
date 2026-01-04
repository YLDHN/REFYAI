'use client';

import { useState } from 'react';
import Link from 'next/link';
import { questionnaireAPI } from '@/lib/api';

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
      // Validation avec API backend
      const validateResponse = await questionnaireAPI.validateAnswers(answers);
      const data = validateResponse.data;
      
      if (data.valid) {
        // Extraire filtres PLU
        const filtersResponse = await questionnaireAPI.extractFilters(answers);
        const filters = filtersResponse.data;
        
        // Rediriger vers résultats
        alert('✅ Questionnaire validé ! Filtres PLU extraits.');
        console.log('Filtres PLU:', filters);
        // TODO: Rediriger vers page de résultats avec les filtres
      } else {
        setErrors(data.errors || {});
      }
    } catch (error: any) {
      console.error('Erreur:', error);
      alert(error.response?.data?.detail || 'Erreur lors de la soumission');
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
            className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder={currentQuestion.help_text}
          />
        );

      case 'number':
        return (
          <input
            type="number"
            value={answers[currentQuestion.id] || ''}
            onChange={(e) => handleAnswer(currentQuestion.id, parseFloat(e.target.value))}
            className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Entrez un nombre"
          />
        );

      case 'select':
        return (
          <select
            value={answers[currentQuestion.id] || ''}
            onChange={(e) => handleAnswer(currentQuestion.id, e.target.value)}
            className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Sélectionner...</option>
            {currentQuestion.options?.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        );

      case 'boolean':
        return (
          <div className="space-y-3">
            {currentQuestion.options?.map(option => (
              <label key={option} className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="radio"
                  name={currentQuestion.id}
                  checked={answers[currentQuestion.id] === option}
                  onChange={() => handleAnswer(currentQuestion.id, option)}
                  className="w-5 h-5 text-blue-600"
                />
                <span className="text-gray-300">{option}</span>
              </label>
            ))}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Header */}
      <div className="bg-gray-900 border-b border-gray-800">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">Questionnaire de Localisation</h1>
              <p className="text-gray-400 mt-1">Étape {currentStep + 1} sur {totalSteps}</p>
            </div>
            <Link
              href="/projects"
              className="px-4 py-2 text-gray-400 hover:text-white transition"
            >
              Annuler
            </Link>
          </div>

          {/* Progress bar */}
          <div className="mt-4 w-full bg-gray-800 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        <div className="bg-gray-900 rounded-xl border border-gray-800 p-8">
          {/* Question */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-2">
              {currentQuestion.question}
              {currentQuestion.required && <span className="text-red-500 ml-1">*</span>}
            </h2>
            {currentQuestion.help_text && (
              <p className="text-gray-400 text-sm">{currentQuestion.help_text}</p>
            )}
          </div>

          {/* Input */}
          <div className="mb-6">
            {renderInput()}
            {errors[currentQuestion.id] && (
              <p className="text-red-500 text-sm mt-2">{errors[currentQuestion.id]}</p>
            )}
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-between pt-6 border-t border-gray-800">
            <button
              onClick={handlePrevious}
              disabled={currentStep === 0}
              className="px-6 py-2 text-gray-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              ← Précédent
            </button>

            <button
              onClick={handleNext}
              disabled={loading}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {loading ? 'Envoi...' : currentStep === totalSteps - 1 ? 'Terminer' : 'Suivant →'}
            </button>
          </div>
        </div>

        {/* Steps indicator */}
        <div className="mt-8 flex justify-center space-x-2">
          {questions.map((_, index) => (
            <div
              key={index}
              className={`w-2 h-2 rounded-full transition ${
                index === currentStep
                  ? 'bg-blue-600 w-8'
                  : index < currentStep
                  ? 'bg-blue-600/50'
                  : 'bg-gray-700'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
