'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { GlassCard } from '@/components/ui/GlassCard';
import { Button, Input, Select } from '@/components/ui';
import { projectsAPI } from '@/lib/api';

export default function NewProjectPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    address: '',
    city: '',
    postalCode: '',
    projectType: 'rental',
    strategy: 'core',
    bpDuration: '',
    assetType: 'residential',
    surface: '',
    purchasePrice: '',
    renovationBudget: '',
    estimatedValue: '',
    // Données locatives
    currentRent: '',
    marketRent: '',
    occupancyRate: '',
    walb: '',
    walt: '',
    acquisitionYield: '',
    // Acquisition
    acquisitionPrice: '',
    notaryFees: '',
    dueDiligenceCost: '',
    // CAPEX détaillé
    capexGrosOeuvre: '',
    capexSecondOeuvre: '',
    capexAmenagements: '',
    capexAutres: '',
    // Financement
    financingAmount: '',
    ltv: '',
    interestRate: '',
    loanDuration: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      // Construire l'objet CAPEX détaillé
      const capexDetails: any = {};
      if (formData.capexGrosOeuvre) capexDetails.gros_oeuvre = parseFloat(formData.capexGrosOeuvre);
      if (formData.capexSecondOeuvre) capexDetails.second_oeuvre = parseFloat(formData.capexSecondOeuvre);
      if (formData.capexAmenagements) capexDetails.amenagements = parseFloat(formData.capexAmenagements);
      if (formData.capexAutres) capexDetails.autres = parseFloat(formData.capexAutres);

      const projectData = {
        name: formData.name,
        description: formData.description || null,
        address: formData.address || null,
        city: formData.city || null,
        postal_code: formData.postalCode || null,
        project_type: formData.projectType,
        strategy: formData.strategy || null,
        bp_duration: formData.bpDuration ? parseInt(formData.bpDuration) : null,
        asset_type: formData.assetType || null,
        surface: formData.surface ? parseFloat(formData.surface) : null,
        purchase_price: formData.purchasePrice ? parseFloat(formData.purchasePrice) : null,
        renovation_budget: formData.renovationBudget ? parseFloat(formData.renovationBudget) : null,
        estimated_value: formData.estimatedValue ? parseFloat(formData.estimatedValue) : null,
        // Locatif
        current_rent: formData.currentRent ? parseFloat(formData.currentRent) : null,
        market_rent: formData.marketRent ? parseFloat(formData.marketRent) : null,
        occupancy_rate: formData.occupancyRate ? parseFloat(formData.occupancyRate) : null,
        walb: formData.walb ? parseFloat(formData.walb) : null,
        walt: formData.walt ? parseFloat(formData.walt) : null,
        acquisition_yield: formData.acquisitionYield ? parseFloat(formData.acquisitionYield) : null,
        // Acquisition
        acquisition_price: formData.acquisitionPrice ? parseFloat(formData.acquisitionPrice) : null,
        notary_fees: formData.notaryFees ? parseFloat(formData.notaryFees) : null,
        due_diligence_cost: formData.dueDiligenceCost ? parseFloat(formData.dueDiligenceCost) : null,
        // CAPEX
        capex_details: Object.keys(capexDetails).length > 0 ? capexDetails : null,
        // Financement
        financing_amount: formData.financingAmount ? parseFloat(formData.financingAmount) : null,
        ltv: formData.ltv ? parseFloat(formData.ltv) : null,
        interest_rate: formData.interestRate ? parseFloat(formData.interestRate) : null,
        loan_duration: formData.loanDuration ? parseInt(formData.loanDuration) : null,
      };

      console.log('Création du projet:', projectData);
      
      await projectsAPI.create(projectData);
      
      router.push('/projects');
    } catch (error: any) {
      console.error('Erreur:', error);
      setError(error.response?.data?.detail || 'Erreur lors de la création du projet');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Nouveau Projet</h1>
          <p className="text-slate-400 mt-2">Créez un nouveau projet d'analyse immobilière</p>
        </div>

        {error && (
          <div className="mb-6 bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-xl flex items-center gap-2">
            <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Informations générales */}
          <GlassCard className="p-6">
            <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center text-sm">1</span>
              Informations générales
            </h2>
            <div className="space-y-4">
              <Input
                label="Nom du projet"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Ex: Immeuble Haussmannien Paris 16"
                required
              />

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">
                  Description
                </label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows={3}
                  className="w-full px-4 py-2.5 rounded-lg glass-input text-white placeholder-slate-500 transition-all duration-300"
                  placeholder="Description du projet..."
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Select
                  label="Type de projet"
                  name="projectType"
                  value={formData.projectType}
                  onChange={handleChange}
                  options={[
                    { value: 'rental', label: 'Locatif' },
                    { value: 'resale', label: 'Revente' },
                    { value: 'mixed', label: 'Mixte' },
                  ]}
                  required
                />

                <Select
                  label="Stratégie"
                  name="strategy"
                  value={formData.strategy}
                  onChange={handleChange}
                  options={[
                    { value: 'core', label: 'Core' },
                    { value: 'core_plus', label: 'Core+' },
                    { value: 'value_add', label: 'Value Add' },
                  ]}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Select
                  label="Typologie de l'actif"
                  name="assetType"
                  value={formData.assetType}
                  onChange={handleChange}
                  options={[
                    { value: 'residential', label: 'Résidentiel' },
                    { value: 'office', label: 'Bureau' },
                    { value: 'logistics', label: 'Logistique' },
                    { value: 'retail', label: 'Commerce' },
                    { value: 'mixed', label: 'Mixte' },
                  ]}
                />

                <div className="grid grid-cols-2 gap-4">
                  <Input
                    label="Surface (m²)"
                    name="surface"
                    type="number"
                    value={formData.surface}
                    onChange={handleChange}
                    placeholder="1500"
                  />
                  <Input
                    label="Durée BP (ans)"
                    name="bpDuration"
                    type="number"
                    value={formData.bpDuration}
                    onChange={handleChange}
                    placeholder="5"
                  />
                </div>
              </div>
            </div>
          </GlassCard>

          {/* Localisation */}
          <GlassCard className="p-6">
            <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-sm">2</span>
              Localisation
            </h2>
            <div className="space-y-4">
              <Input
                label="Adresse"
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="45 Avenue Foch"
                required
              />

              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="Ville"
                  name="city"
                  value={formData.city}
                  onChange={handleChange}
                  placeholder="Paris"
                  required
                />

                <Input
                  label="Code postal"
                  name="postalCode"
                  value={formData.postalCode}
                  onChange={handleChange}
                  placeholder="75016"
                  required
                />
              </div>
            </div>
          </GlassCard>

          {/* Acquisition */}
          <GlassCard className="p-6">
            <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-violet-500/20 text-violet-400 flex items-center justify-center text-sm">3</span>
              Acquisition
            </h2>
            <div className="space-y-4">
              <Input
                label="Prix d'acquisition (€)"
                name="acquisitionPrice"
                type="number"
                value={formData.acquisitionPrice}
                onChange={handleChange}
                placeholder="1500000"
              />

              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="Frais de notaire (€)"
                  name="notaryFees"
                  type="number"
                  value={formData.notaryFees}
                  onChange={handleChange}
                  placeholder="120000"
                />

                <Input
                  label="Due diligence (€)"
                  name="dueDiligenceCost"
                  type="number"
                  value={formData.dueDiligenceCost}
                  onChange={handleChange}
                  placeholder="15000"
                />
              </div>

              <Input
                label="Yield à l'acquisition (%)"
                name="acquisitionYield"
                type="number"
                step="0.01"
                value={formData.acquisitionYield}
                onChange={handleChange}
                placeholder="4.5"
              />
            </div>
          </GlassCard>

          {/* État locatif */}
          <GlassCard className="p-6">
            <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center text-sm">4</span>
              État locatif
            </h2>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="WALB (ans)"
                  name="walb"
                  type="number"
                  step="0.1"
                  value={formData.walb}
                  onChange={handleChange}
                  placeholder="3.2"
                />

                <Input
                  label="WALT (ans)"
                  name="walt"
                  type="number"
                  step="0.1"
                  value={formData.walt}
                  onChange={handleChange}
                  placeholder="5.8"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="Loyer actuel (€/an)"
                  name="currentRent"
                  type="number"
                  value={formData.currentRent}
                  onChange={handleChange}
                  placeholder="75000"
                />

                <Input
                  label="VLM (€/an)"
                  name="marketRent"
                  type="number"
                  value={formData.marketRent}
                  onChange={handleChange}
                  placeholder="80000"
                />
              </div>

              <Input
                label="Taux d'occupation (%)"
                name="occupancyRate"
                type="number"
                step="0.1"
                value={formData.occupancyRate}
                onChange={handleChange}
                placeholder="95"
              />
            </div>
          </GlassCard>

          {/* Données financières */}
          <GlassCard className="p-6">
            <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-pink-500/20 text-pink-400 flex items-center justify-center text-sm">5</span>
              Données financières
            </h2>
            <div className="space-y-4">
              <Input
                label="Budget travaux (€)"
                name="renovationBudget"
                type="number"
                value={formData.renovationBudget}
                onChange={handleChange}
                placeholder="50000"
              />

              <Input
                label="Valeur estimée (€)"
                name="estimatedValue"
                type="number"
                value={formData.estimatedValue}
                onChange={handleChange}
                placeholder="550000"
                helperText="Valeur après travaux"
              />
            </div>
          </GlassCard>

          {/* CAPEX & Travaux */}
          <GlassCard className="p-6">
            <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-orange-500/20 text-orange-400 flex items-center justify-center text-sm">6</span>
              Détail CAPEX
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Gros œuvre (€)"
                name="capexGrosOeuvre"
                type="number"
                value={formData.capexGrosOeuvre}
                onChange={handleChange}
                placeholder="50000"
              />

              <Input
                label="Second œuvre (€)"
                name="capexSecondOeuvre"
                type="number"
                value={formData.capexSecondOeuvre}
                onChange={handleChange}
                placeholder="80000"
              />

              <Input
                label="Aménagements (€)"
                name="capexAmenagements"
                type="number"
                value={formData.capexAmenagements}
                onChange={handleChange}
                placeholder="40000"
              />

              <Input
                label="Autres travaux (€)"
                name="capexAutres"
                type="number"
                value={formData.capexAutres}
                onChange={handleChange}
                placeholder="30000"
              />
            </div>
          </GlassCard>

          {/* Financement */}
          <GlassCard className="p-6">
            <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-sm">7</span>
              Financement
            </h2>
            <div className="space-y-4">
              <Input
                label="Montant financement (€)"
                name="financingAmount"
                type="number"
                value={formData.financingAmount}
                onChange={handleChange}
                placeholder="1000000"
              />

              <div className="grid grid-cols-3 gap-4">
                <Input
                  label="LTV (%)"
                  name="ltv"
                  type="number"
                  step="0.1"
                  value={formData.ltv}
                  onChange={handleChange}
                  placeholder="65"
                />

                <Input
                  label="Taux (%)"
                  name="interestRate"
                  type="number"
                  step="0.01"
                  value={formData.interestRate}
                  onChange={handleChange}
                  placeholder="3.5"
                />

                <Input
                  label="Durée (ans)"
                  name="loanDuration"
                  type="number"
                  value={formData.loanDuration}
                  onChange={handleChange}
                  placeholder="20"
                />
              </div>
            </div>
          </GlassCard>

          {/* Actions */}
          <div className="flex items-center gap-4 pt-4">
            <Button
              type="submit"
              size="lg"
              variant="primary"
              isLoading={isSubmitting}
              className="flex-1 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400"
            >
              Créer le projet
            </Button>
            <Button
              type="button"
              variant="outline"
              size="lg"
              onClick={() => router.back()}
              disabled={isSubmitting}
              className="px-8 border-white/10 text-slate-300 hover:bg-white/5 hover:text-white"
            >
              Annuler
            </Button>
          </div>
        </form>
      </div>
    </DashboardLayout>
  );
}
