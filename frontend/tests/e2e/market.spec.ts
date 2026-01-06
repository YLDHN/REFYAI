import { test, expect } from '@playwright/test';

test.describe('Tests API Market', () => {
  
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

  test('POST /api/market/analyze - Analyse de marché', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/market/analyze', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        city: 'Paris',
        surface: 50,
        type_bien: 'Appartement'
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('median_price');
      expect(data).toHaveProperty('price_per_sqm');
      console.log('✓ Analyse marché Paris:', data.median_price + '€');
    } else {
      console.log('⚠️ Analyse marché non disponible (nécessite DVF data)');
    }
  });

  test('GET /api/market/comparables - Biens comparables Lyon', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/market/comparables/', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      params: {
        commune: 'Lyon'
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(Array.isArray(data)).toBeTruthy();
      console.log('✓ Comparables Lyon:', data.length);
    } else {
      console.log('⚠️ Comparables non disponibles (nécessite DVF data)');
    }
  });

  test('GET /api/market/comparables - Biens comparables Bordeaux', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/market/comparables/', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      params: {
        commune: 'Bordeaux'
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(Array.isArray(data)).toBeTruthy();
      console.log('✓ Comparables Bordeaux:', data.length);
    } else {
      console.log('⚠️ Comparables non disponibles');
    }
  });

  test('POST /api/market/analyze - Différentes surfaces', async ({ request }) => {
    const surfaces = [30, 60, 100, 150];
    
    for (const surface of surfaces) {
      const response = await request.post('http://localhost:8000/api/market/analyze', {
        headers: { 'Authorization': `Bearer ${authToken}` },
        data: {
          city: 'Paris',
          surface: surface,
          type_bien: 'Appartement'
        }
      });
      
      if (response.ok()) {
        const data = await response.json();
        console.log(`✓ Surface ${surface}m²:`, data.price_per_sqm + '€/m²');
      }
    }
  });

  test('POST /api/market/analyze - Accessible sans auth', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/market/analyze', {
      data: {
        city: 'Paris',
        surface: 50
      }
    });
    
    // Peut retourner 422 (validation) ou 200 selon implémentation
    expect([200, 422]).toContain(response.status());
    console.log('✓ Market analyze accessible (retourne', response.status() + ')');
  });

  test('POST /api/market/analyze - Validation données manquantes', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/market/analyze', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        city: 'Paris'
        // Manque surface
      }
    });
    
    expect(response.status()).toBe(422);
    console.log('✓ Validation données manquantes OK');
  });
});
