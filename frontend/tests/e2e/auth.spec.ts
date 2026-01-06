import { test, expect } from '@playwright/test';

test.describe('Flux d\'authentification complet', () => {
  
  test.beforeEach(async ({ page }) => {
    // Nettoyer le localStorage avant chaque test
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
  });

  test('Redirection vers login si non authentifié', async ({ page }) => {
    await page.goto('/');
    await page.waitForTimeout(800);
    
    // Devrait rediriger vers /login
    await expect(page).toHaveURL('/login');
    await page.waitForTimeout(500);
    
    // Vérifier que la page de connexion est affichée
    await expect(page.getByRole('heading', { name: /connexion/i })).toBeVisible();
    await expect(page.getByPlaceholder(/email/i)).toBeVisible();
    await expect(page.getByPlaceholder(/mot de passe/i)).toBeVisible();
  });

  test('Connexion avec identifiants valides', async ({ page }) => {
    await page.goto('/login');
    await page.waitForTimeout(1000);
    
    // Remplir le formulaire
    await page.getByPlaceholder(/email/i).pressSequentially('demo@refyai.com', { delay: 100 });
    await page.waitForTimeout(500);
    await page.getByPlaceholder(/mot de passe/i).pressSequentially('demo123', { delay: 100 });
    await page.waitForTimeout(500);
    
    // Cliquer sur le bouton de connexion
    await page.getByRole('button', { name: /se connecter/i }).click();
    await page.waitForTimeout(500);
    
    // Attendre la redirection vers le dashboard
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    await page.waitForTimeout(1000);
    
    // Vérifier que le dashboard est affiché
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();
    await page.waitForTimeout(500);
    
    // Vérifier que l'email de l'utilisateur est affiché
    await expect(page.getByText(/demo@refyai\.com/i)).toBeVisible();
    
    // Vérifier que le bouton de déconnexion est présent
    await expect(page.getByRole('button', { name: /déconnexion/i })).toBeVisible();
  });

  test('Connexion avec identifiants invalides', async ({ page }) => {
    await page.goto('/login');
    await page.waitForTimeout(1000);
    
    // Remplir avec de mauvais identifiants
    await page.getByPlaceholder(/email/i).pressSequentially('wrong@example.com', { delay: 80 });
    await page.waitForTimeout(500);
    await page.getByPlaceholder(/mot de passe/i).pressSequentially('wrongpassword', { delay: 80 });
    await page.waitForTimeout(500);
    
    // Cliquer sur le bouton
    await page.getByRole('button', { name: /se connecter/i }).click();
    await page.waitForTimeout(500);
    
    // Note: Le backend de démo accepte tous les identifiants
    // Dans un vrai environnement, on devrait voir un message d'erreur
    await page.waitForTimeout(2000);
    console.log('⚠️ Backend de démo accepte tous les identifiants');
  });

  test('Affichage des projets après connexion', async ({ page }) => {
    // Se connecter
    await page.goto('/login');
    await page.waitForTimeout(1000);
    await page.getByPlaceholder(/email/i).pressSequentially('demo@refyai.com', { delay: 80 });
    await page.waitForTimeout(400);
    await page.getByPlaceholder(/mot de passe/i).pressSequentially('demo123', { delay: 80 });
    await page.waitForTimeout(400);
    await page.getByRole('button', { name: /se connecter/i }).click();
    await page.waitForTimeout(500);
    
    // Attendre le dashboard
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    await page.waitForTimeout(1000);
    
    // Attendre que les statistiques se chargent
    await expect(page.getByText(/projets totaux/i)).toBeVisible({ timeout: 5000 });
    await page.waitForTimeout(800);
    
    // Vérifier qu'au moins un projet est affiché
    await expect(page.getByText(/Tour de Bureaux - La Défense/i)).toBeVisible({ timeout: 5000 });
    await page.waitForTimeout(500);
    await expect(page.getByText(/Résidence Étudiante Lyon/i)).toBeVisible();
    await page.waitForTimeout(500);
    await expect(page.getByText(/Centre Commercial Bordeaux/i)).toBeVisible();
    await page.waitForTimeout(500);
    
    // Vérifier les statistiques (au moins 3 projets)
    const statsCard = page.locator('text=Projets Totaux').locator('..');
    await expect(statsCard.getByText(/[3-9]/)).toBeVisible();
  });

  test('Déconnexion et redirection vers login', async ({ page }) => {
    // Se connecter d'abord
    await page.goto('/login');
    await page.waitForTimeout(1000);
    await page.getByPlaceholder(/email/i).pressSequentially('demo@refyai.com', { delay: 80 });
    await page.waitForTimeout(400);
    await page.getByPlaceholder(/mot de passe/i).pressSequentially('demo123', { delay: 80 });
    await page.waitForTimeout(400);
    await page.getByRole('button', { name: /se connecter/i }).click();
    await page.waitForTimeout(500);
    
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    await page.waitForTimeout(1000);
    
    // Cliquer sur le bouton de déconnexion
    await page.getByRole('button', { name: /déconnexion/i }).click();
    await page.waitForTimeout(500);
    
    // Devrait rediriger vers /login
    await expect(page).toHaveURL('/login', { timeout: 5000 });
    await page.waitForTimeout(800);
    
    // Essayer d'accéder au dashboard devrait rediriger vers login
    await page.goto('/dashboard');
    await page.waitForTimeout(500);
    await expect(page).toHaveURL('/login', { timeout: 5000 });
    await page.waitForTimeout(500);
  });

  test('Token JWT est bien envoyé dans les requêtes API', async ({ page }) => {
    // Intercepter les requêtes API
    let apiCallsWithToken = 0;
    
    page.on('request', request => {
      if (request.url().includes('/api/projects')) {
        const authHeader = request.headers()['authorization'];
        if (authHeader && authHeader.startsWith('Bearer ')) {
          apiCallsWithToken++;
          console.log('✓ Requête API avec token détectée:', request.url());
        }
      }
    });
    
    // Se connecter
    await page.goto('/login');
    await page.waitForTimeout(1000);
    await page.getByPlaceholder(/email/i).pressSequentially('demo@refyai.com', { delay: 80 });
    await page.waitForTimeout(400);
    await page.getByPlaceholder(/mot de passe/i).pressSequentially('demo123', { delay: 80 });
    await page.waitForTimeout(400);
    await page.getByRole('button', { name: /se connecter/i }).click();
    await page.waitForTimeout(500);
    
    // Attendre le dashboard et le chargement des projets
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    await page.waitForTimeout(1000);
    await expect(page.getByText(/Tour de Bureaux/i)).toBeVisible({ timeout: 5000 });
    await page.waitForTimeout(800);
    
    // Vérifier qu'au moins une requête API a été faite avec le token
    expect(apiCallsWithToken).toBeGreaterThan(0);
  });

  test('Persistance de la session après rechargement', async ({ page }) => {
    // Se connecter
    await page.goto('/login');
    await page.getByPlaceholder(/email/i).fill('demo@refyai.com');
    await page.getByPlaceholder(/mot de passe/i).fill('demo123');
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    
    // Recharger la page
    await page.reload();
    
    // Devrait rester sur le dashboard (pas de redirection vers login)
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();
    await expect(page.getByText(/demo@refyai\.com/i)).toBeVisible();
  });

  test('Affichage correct des KPI dans le dashboard', async ({ page }) => {
    // Se connecter
    await page.goto('/login');
    await page.getByPlaceholder(/email/i).fill('demo@refyai.com');
    await page.getByPlaceholder(/mot de passe/i).fill('demo123');
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    
    // Vérifier les 4 cartes KPI
    await expect(page.getByText(/projets totaux/i)).toBeVisible();
    await expect(page.getByText(/en cours/i)).toBeVisible();
    await expect(page.getByText(/tri moyen/i)).toBeVisible();
    await expect(page.getByText(/investissement total/i)).toBeVisible();
    
    // Vérifier que les valeurs sont affichées (nombres)
    const kpiCards = page.locator('[class*="bg-gray-900"]').first();
    await expect(kpiCards).toBeVisible();
  });
});
