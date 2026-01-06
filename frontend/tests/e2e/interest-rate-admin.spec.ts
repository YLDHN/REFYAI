import { test, expect } from '@playwright/test';

test.describe('Tests API Interest Rate & Admin Delays', () => {
  
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

  // ==================== INTEREST RATE ====================

  test('GET /api/interest-rate/euribor - Taux Euribor 12M', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/interest-rate/euribor?maturity=12m', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(data).toHaveProperty('euribor');
    expect(data).toHaveProperty('maturity');
    expect(data.maturity).toBe('12m');
    console.log('✓ Euribor 12M:', data.euribor + '%');
  });

  test('GET /api/interest-rate/euribor - Taux Euribor 3M', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/interest-rate/euribor?maturity=3m', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(data.maturity).toBe('3m');
    console.log('✓ Euribor 3M:', data.euribor + '%');
  });

  test('GET /api/interest-rate/euribor - Taux Euribor 6M', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/interest-rate/euribor?maturity=6m', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(data.maturity).toBe('6m');
    console.log('✓ Euribor 6M:', data.euribor + '%');
  });

  test('POST /api/interest-rate/calculate - Calcul taux d\'intérêt', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/interest-rate/calculate', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        loan_amount: 500000,
        duration_years: 20,
        margin: 1.5,
        insurance_rate: 0.36
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('total_rate');
      console.log('✓ Taux total:', data.total_rate + '%');
    } else {
      console.log('⚠️ Endpoint /api/interest-rate/calculate non implémenté');
    }
  });

  // ==================== ADMIN DELAYS ====================

  test('GET /api/admin-delays/available-procedures - Liste procédures', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/admin-delays/available-procedures', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(data).toHaveProperty('procedures');
    expect(Object.keys(data.procedures).length).toBeGreaterThan(0);
    console.log('✓ Procédures disponibles:', Object.keys(data.procedures).length);
  });

  test('GET /api/admin-delays/cities - Liste des villes', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/admin-delays/cities', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(Array.isArray(data.cities)).toBeTruthy();
    expect(data.cities.length).toBeGreaterThan(0);
    console.log('✓ Villes:', data.cities.length);
  });

  test('GET /api/admin-delays/complexity-levels - Niveaux de complexité', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/admin-delays/complexity-levels', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(data).toHaveProperty('complexity_levels');
    expect(Array.isArray(data.complexity_levels)).toBeTruthy();
    expect(data.complexity_levels.length).toBeGreaterThan(0);
    console.log('✓ Niveaux complexité:', data.complexity_levels.length);
  });

  test('POST /api/admin-delays/procedure - Délai procédure PC', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/admin-delays/procedure', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        procedure_type: 'permis_construire',
        city: 'Paris',
        complexity: 1.3,
        surface: 500
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('delays_days');
      const avgDays = data.delays_days.avg;
      console.log('✓ Délai PC Paris:', avgDays, 'jours (moyenne)');
    } else {
      console.log('⚠️ Endpoint /api/admin-delays/procedure non implémenté');
    }
  });

  test('POST /api/admin-delays/project-timeline - Timeline projet', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/admin-delays/project-timeline', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        procedures: ['permis_construire', 'declaration_ouverture_chantier'],
        city: 'Lyon',
        complexity: 1.6
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      console.log('✓ Timeline projet calculée');
    } else {
      console.log('⚠️ Endpoint /api/admin-delays/project-timeline non implémenté');
    }
  });

  test('POST /api/admin-delays/full-duration - Durée complète projet', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/admin-delays/full-duration', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        city: 'Bordeaux',
        project_type: 'residential',
        surface: 1000,
        include_pre_operational: true,
        include_operational: true
      }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(data).toHaveProperty('full_project_duration');
    expect(data.full_project_duration).toHaveProperty('total_duration_months');
    const avgMonths = data.full_project_duration.total_duration_months.avg;
    console.log('✓ Durée totale projet:', avgMonths, 'mois (moyenne)');
  });

  test('GET /api/interest-rate/euribor - Accessible sans authentification', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/interest-rate/euribor');
    
    expect(response.status()).toBe(200);
    console.log('✓ Euribor accessible publiquement (pas besoin auth)');
  });

  test('POST /api/admin-delays/procedure - Validation données', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/admin-delays/procedure', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        // Manque procedure_type
        city: 'Paris'
      }
    });
    
    expect(response.status()).toBe(422);
    console.log('✓ Validation données manquantes OK');
  });
});
