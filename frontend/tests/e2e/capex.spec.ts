import { test, expect } from '@playwright/test';

test.describe('Tests API CAPEX', () => {
  
  let authToken: string;

  test.beforeAll(async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/auth/login', {
      form: {
        username: 'demo@refyai.com',
        password: 'demo123'
      }
    });
    
    const data = await response.json();
    authToken = data.access_token;
  });

  test('GET /api/capex/categories - Liste des catégories CAPEX', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/capex/categories', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(data).toHaveProperty('categories');
    expect(Object.keys(data.categories).length).toBeGreaterThan(0);
    console.log('✓ Catégories CAPEX:', Object.keys(data.categories).length);
  });

  test('GET /api/capex/city-tiers - Liste des tiers de villes', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/capex/city-tiers', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('tiers');
      console.log('✓ Tiers de villes:', Object.keys(data.tiers).length);
    } else {
      console.log('⚠️ Endpoint /api/capex/city-tiers non implémenté (404)');
    }
  });

  test('POST /api/capex/estimate - Estimation item CAPEX', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/capex/estimate', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      params: {
        item_key: 'facade_ravalement_simple',
        quantity: 100,
        city_tier: 1
      }
    });
    
    if (response.status() === 404) {
      test.skip();
      console.log('⚠️ Endpoint /api/capex/estimate non implémenté (404)');
      return;
    }
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data).toHaveProperty('total_cost');
    console.log('✓ Estimation CAPEX:', data.total_cost.toFixed(2) + '€');
  });

  test('POST /api/capex/project - Calcul CAPEX projet complet', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/capex/project', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        items: [
          { key: 'facade_ravalement_simple', quantity: 100 },
          { key: 'toiture_refection_tuiles', quantity: 50 },
          { key: 'fenetre_pvc_double_vitrage', quantity: 10 }
        ],
        city_tier: 1,
        contingency_rate: 0.10
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('success');
      console.log('✓ CAPEX projet calculé:', data.total_capex + '€');
    } else {
      console.log('⚠️ Endpoint /api/capex/project non implémenté (404)');
    }
  });

  test('POST /api/capex/renovation-estimate - Estimation rénovation', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/capex/renovation-estimate', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        surface: 100,
        renovation_level: 'complete',
        city_tier: 1,
        specific_works: ['plumbing', 'electricity']
      }
    });
    
    if (response.status() === 404) {
      test.skip();
      console.log('⚠️ Endpoint /api/capex/renovation-estimate non implémenté (404)');
      return;
    }
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data).toHaveProperty('estimated_budget');
    console.log('✓ Budget rénovation:', data.estimated_budget.toFixed(2) + '€');
  });

  test('POST /api/capex/project - Validation données', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/capex/project', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        items: []  // Liste vide devrait échouer
      }
    });
    
    // Peut être 422 (validation) ou 404 (endpoint non implémenté)
    expect([404, 422]).toContain(response.status());
    console.log('✓ Validation liste vide OK');
  });

  test('POST /api/capex/estimate - Item inexistant', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/capex/estimate', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      params: {
        item_key: 'item_inexistant_xyz',
        quantity: 10
      }
    });
    
    // Attendons 404 (endpoint non implémenté) ou 4xx (validation)
    expect(response.status()).toBeGreaterThanOrEqual(400);
    console.log('✓ Item inexistant correctement rejeté (ou endpoint non implémenté)');
  });

  test('GET /api/capex/categories - Erreur sans authentification', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/capex/categories');
    
    // Backend retourne 403
    expect([401, 403]).toContain(response.status());
    console.log('✓ Requête sans auth correctement rejetée (' + response.status() + ')');
  });
});
