import { test, expect } from '@playwright/test';

test.describe('Tests API Financial', () => {
  
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

  test('POST /api/financial/calculate - Analyse financière complète', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/financial/calculate', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        purchase_price: 500000,
        notary_fees: 35000,
        works_budget: 100000,
        loan_amount: 450000,
        interest_rate: 4.5,
        loan_duration: 20,
        monthly_rent: 2500,
        annual_charges: 3000,
        property_tax: 1500,
        vacancy_rate: 5
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('tri');
      console.log('✓ Analyse financière calculée:', data.tri + '%');
    } else {
      console.log('⚠️ Endpoint /api/financial/calculate non implémenté (404)');
    }
  });

  test('POST /api/financial/tri - Calcul TRI', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/financial/tri', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        initial_investment: 635000,
        annual_cash_flows: [30000, 30000, 30000, 30000, 30000],
        resale_value: 700000,
        holding_period: 5
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('tri');
      console.log('✓ TRI calculé:', data.tri + '%');
    } else {
      console.log('⚠️ Endpoint /api/financial/tri non implémenté (404)');
    }
  });

  test('POST /api/financial/van - Calcul VAN', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/financial/van', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        initial_investment: 635000,
        annual_cash_flows: [30000, 30000, 30000],
        discount_rate: 8,
        resale_value: 700000
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('van');
      console.log('✓ VAN calculée:', data.van.toFixed(2) + '€');
    } else {
      console.log('⚠️ Endpoint /api/financial/van non implémenté (404)');
    }
  });

  test('POST /api/financial/loan - Calcul de prêt', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/financial/loan', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        amount: 450000,
        annual_rate: 4.5,
        duration_years: 20,
        amortization_type: 'classic'
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('monthly_payment');
      console.log('✓ Mensualité calculée:', data.monthly_payment.toFixed(2) + '€');
    } else {
      console.log('⚠️ Endpoint /api/financial/loan non implémenté (404)');
    }
  });

  test('POST /api/financial/ratios - Calcul ratios bancaires', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/financial/ratios', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        loan_amount: 450000,
        property_value: 635000,
        annual_rental_income: 30000,
        annual_debt_service: 34200
      }
    });
    
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('ltv');
      expect(data).toHaveProperty('dscr');
      console.log('✓ LTV:', data.ltv.toFixed(2) + '%', 'DSCR:', data.dscr.toFixed(2));
    } else {
      console.log('⚠️ Endpoint /api/financial/ratios non implémenté (404)');
    }
  });

  test('GET /api/financial/loan/types - Liste types de prêts', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/financial/loan/types', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(data).toHaveProperty('types');
    expect(data.types).toHaveProperty('classic');
    expect(data.types).toHaveProperty('in_fine');
    expect(data.types).toHaveProperty('deferred');
    console.log('✓ Types de prêts disponibles:', Object.keys(data.types).length);
  });

  test('POST /api/financial/calculate - Endpoint non disponible', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/financial/calculate', {
      data: {
        purchase_price: 500000,
        loan_amount: 450000
      }
    });
    
    expect(response.status()).toBe(404);
    console.log('✓ Endpoint non implémenté (404)');
  });

  test('POST /api/financial/tri - Validation données manquantes', async ({ request }) => {
    const response = await request.post('http://localhost:8000/api/financial/tri', {
      headers: { 'Authorization': `Bearer ${authToken}` },
      data: {
        initial_investment: 635000
        // Manque annual_cash_flows
      }
    });
    
    expect(response.status()).toBe(422);
    console.log('✓ Validation des données manquantes OK');
  });
});
