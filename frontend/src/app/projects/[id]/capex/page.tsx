'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

interface CAPEXCategory {
  id: string;
  name: string;
  items: CAPEXItem[];
}

interface CAPEXItem {
  id: string;
  name: string;
  unit: string;
  min_price: number;
  avg_price: number;
  max_price: number;
  quantity?: number;
}

interface ProjectCAPEX {
  items: Array<{
    item: CAPEXItem;
    quantity: number;
    total_min: number;
    total_avg: number;
    total_max: number;
  }>;
  subtotal_min: number;
  subtotal_avg: number;
  subtotal_max: number;
  contingency: number;
  total_min: number;
  total_avg: number;
  total_max: number;
}

export default function CAPEXPage() {
  const params = useParams();
  const projectId = params?.id as string;

  const [categories, setCategories] = useState<CAPEXCategory[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedItem, setSelectedItem] = useState('');
  const [quantity, setQuantity] = useState(0);
  const [cityTier, setCityTier] = useState(1);
  const [contingency, setContingency] = useState(10);
  const [projectItems, setProjectItems] = useState<CAPEXItem[]>([]);
  const [capexResult, setCapexResult] = useState<ProjectCAPEX | null>(null);
  const [activeTab, setActiveTab] = useState<'detailed' | 'quick'>('detailed');

  // Quick estimate
  const [surface, setSurface] = useState(100);
  const [renovationLevel, setRenovationLevel] = useState('medium');

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    if (projectItems.length > 0) {
      calculateCAPEX();
    }
  }, [projectItems, contingency, cityTier]);

  const loadCategories = () => {
    // Mock data - à remplacer par appel API GET /api/v1/capex/categories
    const mockCategories: CAPEXCategory[] = [
      {
        id: 'structure',
        name: 'Structure',
        items: [
          { id: 'fondations', name: 'Fondations béton armé', unit: 'm³', min_price: 180, avg_price: 220, max_price: 280 },
          { id: 'plancher_beton', name: 'Plancher béton', unit: 'm²', min_price: 80, avg_price: 120, max_price: 180 },
          { id: 'murs_porteurs', name: 'Murs porteurs', unit: 'm²', min_price: 100, avg_price: 150, max_price: 220 }
        ]
      },
      {
        id: 'facade',
        name: 'Façade',
        items: [
          { id: 'enduit_exterieur', name: 'Enduit extérieur', unit: 'm²', min_price: 45, avg_price: 65, max_price: 90 },
          { id: 'bardage_bois', name: 'Bardage bois', unit: 'm²', min_price: 80, avg_price: 120, max_price: 180 },
          { id: 'ravalement', name: 'Ravalement complet', unit: 'm²', min_price: 60, avg_price: 90, max_price: 140 }
        ]
      },
      {
        id: 'toiture',
        name: 'Toiture',
        items: [
          { id: 'charpente_bois', name: 'Charpente bois', unit: 'm²', min_price: 80, avg_price: 120, max_price: 180 },
          { id: 'couverture_tuiles', name: 'Couverture tuiles', unit: 'm²', min_price: 60, avg_price: 85, max_price: 120 },
          { id: 'isolation_toiture', name: 'Isolation toiture', unit: 'm²', min_price: 35, avg_price: 55, max_price: 80 }
        ]
      },
      {
        id: 'menuiseries',
        name: 'Menuiseries',
        items: [
          { id: 'fenetres_pvc', name: 'Fenêtres PVC double vitrage', unit: 'unité', min_price: 400, avg_price: 600, max_price: 900 },
          { id: 'porte_entree', name: 'Porte d\'entrée', unit: 'unité', min_price: 800, avg_price: 1200, max_price: 2000 },
          { id: 'volets_roulants', name: 'Volets roulants', unit: 'unité', min_price: 300, avg_price: 450, max_price: 700 }
        ]
      },
      {
        id: 'electricite',
        name: 'Électricité',
        items: [
          { id: 'tableau_electrique', name: 'Tableau électrique', unit: 'unité', min_price: 800, avg_price: 1200, max_price: 1800 },
          { id: 'cablage_complet', name: 'Câblage complet', unit: 'm²', min_price: 40, avg_price: 60, max_price: 90 },
          { id: 'prises_interrupteurs', name: 'Prises et interrupteurs', unit: 'm²', min_price: 15, avg_price: 25, max_price: 40 }
        ]
      },
      {
        id: 'plomberie',
        name: 'Plomberie',
        items: [
          { id: 'reseau_eau', name: 'Réseau eau chaude/froide', unit: 'm²', min_price: 35, avg_price: 55, max_price: 80 },
          { id: 'sanitaires', name: 'Sanitaires complets', unit: 'unité', min_price: 800, avg_price: 1200, max_price: 2000 },
          { id: 'evacuation', name: 'Réseau évacuation', unit: 'm²', min_price: 25, avg_price: 40, max_price: 60 }
        ]
      }
    ];

    setCategories(mockCategories);
  };

  const calculateCAPEX = () => {
    const tierMultiplier = cityTier === 1 ? 1.0 : cityTier === 2 ? 0.85 : 0.70;
    
    const items = projectItems.map(item => {
      const qty = item.quantity || 0;
      return {
        item,
        quantity: qty,
        total_min: item.min_price * qty * tierMultiplier,
        total_avg: item.avg_price * qty * tierMultiplier,
        total_max: item.max_price * qty * tierMultiplier
      };
    });

    const subtotal_min = items.reduce((sum, i) => sum + i.total_min, 0);
    const subtotal_avg = items.reduce((sum, i) => sum + i.total_avg, 0);
    const subtotal_max = items.reduce((sum, i) => sum + i.total_max, 0);

    const contingencyAmount = (contingency / 100);

    setCapexResult({
      items,
      subtotal_min,
      subtotal_avg,
      subtotal_max,
      contingency,
      total_min: subtotal_min * (1 + contingencyAmount),
      total_avg: subtotal_avg * (1 + contingencyAmount),
      total_max: subtotal_max * (1 + contingencyAmount)
    });
  };

  const addItem = () => {
    if (!selectedCategory || !selectedItem || quantity <= 0) return;

    const category = categories.find(c => c.id === selectedCategory);
    const item = category?.items.find(i => i.id === selectedItem);

    if (item) {
      setProjectItems([...projectItems, { ...item, quantity }]);
      setSelectedItem('');
      setQuantity(0);
    }
  };

  const removeItem = (index: number) => {
    setProjectItems(projectItems.filter((_, i) => i !== index));
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0
    }).format(price);
  };

  const getQuickEstimate = () => {
    const ranges = {
      light: { min: 300, max: 600 },
      medium: { min: 600, max: 1200 },
      heavy: { min: 1200, max: 2000 },
      complete: { min: 2000, max: 3500 }
    };

    const range = ranges[renovationLevel as keyof typeof ranges];
    const tierMultiplier = cityTier === 1 ? 1.0 : cityTier === 2 ? 0.85 : 0.70;
    
    return {
      min: range.min * surface * tierMultiplier,
      max: range.max * surface * tierMultiplier,
      avg: ((range.min + range.max) / 2) * surface * tierMultiplier
    };
  };

  const quickEstimate = getQuickEstimate();

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Header */}
      <div className="bg-gray-900 border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">Estimation CAPEX</h1>
              <p className="text-gray-400 mt-1">Calcul détaillé des coûts de construction</p>
            </div>
            <Link
              href={`/projects/${projectId}`}
              className="px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition"
            >
              ← Retour
            </Link>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-6 pt-6">
        <div className="border-b border-gray-800">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('detailed')}
              className={`pb-3 px-1 border-b-2 transition ${
                activeTab === 'detailed'
                  ? 'border-blue-600 text-white'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              Calcul Détaillé
            </button>
            <button
              onClick={() => setActiveTab('quick')}
              className={`pb-3 px-1 border-b-2 transition ${
                activeTab === 'quick'
                  ? 'border-blue-600 text-white'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              Estimation Rapide
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-6">
        {activeTab === 'detailed' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Input Form */}
            <div className="lg:col-span-1 space-y-6">
              <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Ajouter un Poste</h3>

                <div className="space-y-4">
                  {/* City Tier */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Zone Géographique
                    </label>
                    <select
                      value={cityTier}
                      onChange={(e) => setCityTier(Number(e.target.value))}
                      className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600"
                    >
                      <option value={1}>Tier 1 (Paris, Lyon) - ×1.0</option>
                      <option value={2}>Tier 2 (Grandes villes) - ×0.85</option>
                      <option value={3}>Tier 3 (Province) - ×0.70</option>
                    </select>
                  </div>

                  {/* Category */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Catégorie
                    </label>
                    <select
                      value={selectedCategory}
                      onChange={(e) => {
                        setSelectedCategory(e.target.value);
                        setSelectedItem('');
                      }}
                      className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600"
                    >
                      <option value="">Sélectionner...</option>
                      {categories.map(cat => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                      ))}
                    </select>
                  </div>

                  {/* Item */}
                  {selectedCategory && (
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        Poste
                      </label>
                      <select
                        value={selectedItem}
                        onChange={(e) => setSelectedItem(e.target.value)}
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600"
                      >
                        <option value="">Sélectionner...</option>
                        {categories.find(c => c.id === selectedCategory)?.items.map(item => (
                          <option key={item.id} value={item.id}>
                            {item.name} ({formatPrice(item.avg_price)}/{item.unit})
                          </option>
                        ))}
                      </select>
                    </div>
                  )}

                  {/* Quantity */}
                  {selectedItem && (
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        Quantité ({categories.find(c => c.id === selectedCategory)?.items.find(i => i.id === selectedItem)?.unit})
                      </label>
                      <input
                        type="number"
                        min="0"
                        step="0.01"
                        value={quantity}
                        onChange={(e) => setQuantity(Number(e.target.value))}
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600"
                        placeholder="0"
                      />
                    </div>
                  )}

                  <button
                    onClick={addItem}
                    disabled={!selectedItem || quantity <= 0}
                    className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
                  >
                    Ajouter
                  </button>
                </div>
              </div>

              {/* Contingency */}
              <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
                <h3 className="text-lg font-semibold text-white mb-4">
                  Aléas - {contingency}%
                </h3>
                <input
                  type="range"
                  min="5"
                  max="20"
                  step="1"
                  value={contingency}
                  onChange={(e) => setContingency(Number(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-600"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>5%</span>
                  <span>20%</span>
                </div>
              </div>
            </div>

            {/* Items List & Results */}
            <div className="lg:col-span-2 space-y-6">
              {/* Items List */}
              {projectItems.length > 0 && (
                <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
                  <div className="p-4 bg-gray-800 border-b border-gray-700">
                    <h3 className="text-lg font-semibold text-white">Postes Ajoutés</h3>
                  </div>
                  <table className="w-full">
                    <thead className="bg-gray-800">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">Poste</th>
                        <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase">Quantité</th>
                        <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase">Prix Unit. Moy</th>
                        <th className="px-4 py-3 text-right text-xs font-medium text-gray-400 uppercase">Total</th>
                        <th className="px-4 py-3"></th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-800">
                      {capexResult?.items.map((item, index) => (
                        <tr key={index} className="hover:bg-gray-800/50">
                          <td className="px-4 py-3 text-sm text-white">{item.item.name}</td>
                          <td className="px-4 py-3 text-sm text-gray-300 text-right">
                            {item.quantity} {item.item.unit}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-300 text-right">
                            {formatPrice(item.item.avg_price)}
                          </td>
                          <td className="px-4 py-3 text-sm text-white text-right font-medium">
                            {formatPrice(item.total_avg)}
                          </td>
                          <td className="px-4 py-3 text-right">
                            <button
                              onClick={() => removeItem(index)}
                              className="text-red-400 hover:text-red-300 transition"
                            >
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {/* Total Result */}
              {capexResult && (
                <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg border border-blue-500 p-6">
                  <h3 className="text-xl font-semibold text-white mb-4">CAPEX Total (avec aléas {capexResult.contingency}%)</h3>
                  
                  <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="bg-blue-700/30 rounded-lg p-4">
                      <div className="text-blue-200 text-sm">Minimum</div>
                      <div className="text-2xl font-bold text-white mt-1">
                        {formatPrice(capexResult.total_min)}
                      </div>
                    </div>
                    <div className="bg-blue-700/50 rounded-lg p-4">
                      <div className="text-blue-200 text-sm">Moyen</div>
                      <div className="text-3xl font-bold text-white mt-1">
                        {formatPrice(capexResult.total_avg)}
                      </div>
                    </div>
                    <div className="bg-blue-700/30 rounded-lg p-4">
                      <div className="text-blue-200 text-sm">Maximum</div>
                      <div className="text-2xl font-bold text-white mt-1">
                        {formatPrice(capexResult.total_max)}
                      </div>
                    </div>
                  </div>

                  <div className="border-t border-blue-400/30 pt-4">
                    <div className="flex justify-between text-blue-100">
                      <span>Sous-total travaux</span>
                      <span className="font-semibold">{formatPrice(capexResult.subtotal_avg)}</span>
                    </div>
                    <div className="flex justify-between text-blue-100 mt-2">
                      <span>Aléas ({capexResult.contingency}%)</span>
                      <span className="font-semibold">
                        {formatPrice(capexResult.total_avg - capexResult.subtotal_avg)}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'quick' && (
          <div className="max-w-3xl mx-auto">
            <div className="bg-gray-900 rounded-lg border border-gray-800 p-6">
              <h3 className="text-xl font-semibold text-white mb-6">Estimation Rapide au m²</h3>

              <div className="space-y-6">
                {/* Surface */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Surface Habitable (m²)
                  </label>
                  <input
                    type="number"
                    min="10"
                    max="1000"
                    value={surface}
                    onChange={(e) => setSurface(Number(e.target.value))}
                    className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600"
                  />
                </div>

                {/* Renovation Level */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Niveau de Rénovation
                  </label>
                  <select
                    value={renovationLevel}
                    onChange={(e) => setRenovationLevel(e.target.value)}
                    className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600"
                  >
                    <option value="light">Légère (€300-600/m²) - Rafraîchissement</option>
                    <option value="medium">Moyenne (€600-1200/m²) - Rénovation standard</option>
                    <option value="heavy">Lourde (€1200-2000/m²) - Restructuration</option>
                    <option value="complete">Complète (€2000-3500/m²) - Rénovation totale</option>
                  </select>
                </div>

                {/* City Tier */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Zone Géographique
                  </label>
                  <select
                    value={cityTier}
                    onChange={(e) => setCityTier(Number(e.target.value))}
                    className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-600"
                  >
                    <option value={1}>Tier 1 (Paris, Lyon) - ×1.0</option>
                    <option value={2}>Tier 2 (Grandes villes) - ×0.85</option>
                    <option value={3}>Tier 3 (Province) - ×0.70</option>
                  </select>
                </div>
              </div>

              {/* Result */}
              <div className="mt-8 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg p-6">
                <h4 className="text-lg font-semibold text-white mb-4">Estimation Budget Travaux</h4>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <div className="text-blue-200 text-sm">Minimum</div>
                    <div className="text-2xl font-bold text-white mt-1">
                      {formatPrice(quickEstimate.min)}
                    </div>
                  </div>
                  <div>
                    <div className="text-blue-200 text-sm">Moyen</div>
                    <div className="text-3xl font-bold text-white mt-1">
                      {formatPrice(quickEstimate.avg)}
                    </div>
                  </div>
                  <div>
                    <div className="text-blue-200 text-sm">Maximum</div>
                    <div className="text-2xl font-bold text-white mt-1">
                      {formatPrice(quickEstimate.max)}
                    </div>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-blue-400/30 text-blue-100 text-sm">
                  💡 Cette estimation inclut les travaux de base. Prévoir des aléas de 10-20% supplémentaires.
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
