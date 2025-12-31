'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, Button, Input, Select } from '@/components/ui';

export default function NewProjectPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    address: '',
    city: '',
    postalCode: '',
    projectType: 'rental',
    purchasePrice: '',
    renovationBudget: '',
    estimatedValue: '',
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

    try {
      // TODO: Appel API
      console.log('Création du projet:', formData);
      
      // Simulation
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      router.push('/projects');
    } catch (error) {
      console.error('Erreur:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="p-8 max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Nouveau Projet</h1>
          <p className="text-gray-600 mt-2">Créez un nouveau projet d'analyse immobilière</p>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Informations générales */}
          <Card title="Informations générales" className="mb-6">
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
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900 placeholder:text-gray-400"
                  placeholder="Description du projet..."
                />
              </div>

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
            </div>
          </Card>

          {/* Localisation */}
          <Card title="Localisation" className="mb-6">
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
          </Card>

          {/* Données financières */}
          <Card title="Données financières" className="mb-6">
            <div className="space-y-4">
              <Input
                label="Prix d'achat"
                name="purchasePrice"
                type="number"
                value={formData.purchasePrice}
                onChange={handleChange}
                placeholder="450000"
                helperText="Montant en euros"
              />

              <Input
                label="Budget travaux"
                name="renovationBudget"
                type="number"
                value={formData.renovationBudget}
                onChange={handleChange}
                placeholder="50000"
                helperText="Montant en euros"
              />

              <Input
                label="Valeur estimée"
                name="estimatedValue"
                type="number"
                value={formData.estimatedValue}
                onChange={handleChange}
                placeholder="550000"
                helperText="Valeur après travaux en euros"
              />
            </div>
          </Card>

          {/* Actions */}
          <div className="flex items-center gap-4">
            <Button
              type="submit"
              size="lg"
              isLoading={isSubmitting}
              className="flex-1"
            >
              Créer le projet
            </Button>
            <Button
              type="button"
              variant="outline"
              size="lg"
              onClick={() => router.back()}
              disabled={isSubmitting}
            >
              Annuler
            </Button>
          </div>
        </form>
      </div>
    </DashboardLayout>
  );
}
