import { test, expect } from '@playwright/test';

/**
 * Tests visuels de démonstration
 * Ces tests s'exécutent dans un navigateur visible pour montrer
 * le fonctionnement de l'application
 */

test.describe('Démonstration visuelle du flux complet', () => {
  
  test.beforeEach(async ({ page }) => {
    // Nettoyer avant chaque test
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
  });

  test('🎬 Démonstration complète: Connexion → Dashboard → Déconnexion', async ({ page }) => {
    test.slow(); // Ce test prend plus de temps car il montre tout
    
    console.log('🎬 DÉBUT DE LA DÉMONSTRATION');
    
    // Étape 1: Page de connexion
    console.log('📍 Étape 1/5: Accès à la page de connexion');
    await page.goto('/login');
    await page.waitForTimeout(2000); // Pause pour voir
    
    await expect(page.getByRole('heading', { name: /connexion/i })).toBeVisible();
    console.log('✓ Page de connexion affichée');
    
    // Étape 2: Remplir le formulaire
    console.log('📍 Étape 2/5: Remplissage du formulaire');
    await page.getByPlaceholder(/email/i).click();
    await page.waitForTimeout(500);
    await page.getByPlaceholder(/email/i).pressSequentially('demo@refyai.com', { delay: 150 });
    await page.waitForTimeout(1500);
    
    await page.getByPlaceholder(/mot de passe/i).click();
    await page.waitForTimeout(500);
    await page.getByPlaceholder(/mot de passe/i).pressSequentially('demo123', { delay: 150 });
    await page.waitForTimeout(1500);
    console.log('✓ Formulaire rempli');
    
    // Étape 3: Connexion
    console.log('📍 Étape 3/5: Clic sur le bouton de connexion');
    await page.getByRole('button', { name: /se connecter/i }).click();
    await page.waitForTimeout(500);
    
    // Attendre la redirection
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    console.log('✓ Redirection vers le dashboard réussie');
    await page.waitForTimeout(2000);
    
    // Étape 4: Explorer le dashboard
    console.log('📍 Étape 4/5: Exploration du dashboard');
    
    // Vérifier l'en-tête
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();
    console.log('✓ Titre du dashboard visible');
    await page.waitForTimeout(1000);
    
    // Vérifier l'email utilisateur
    await expect(page.getByText(/demo@refyai\.com/i)).toBeVisible();
    console.log('✓ Email utilisateur affiché');
    await page.waitForTimeout(1500);
    
    // Vérifier les KPI
    const kpiTexts = ['Projets Totaux', 'En Cours', 'TRI Moyen', 'Investissement Total'];
    for (const text of kpiTexts) {
      await expect(page.getByText(text, { exact: false })).toBeVisible();
      console.log(`✓ KPI "${text}" visible`);
      await page.waitForTimeout(500);
    }
    await page.waitForTimeout(2000);
    
    // Vérifier les projets
    console.log('📍 Vérification des projets...');
    const projectNames = [
      'Tour de Bureaux - La Défense',
      'Résidence Étudiante Lyon',
      'Centre Commercial Bordeaux'
    ];
    
    for (const name of projectNames) {
      const projectVisible = await page.getByText(name).isVisible().catch(() => false);
      if (projectVisible) {
        console.log(`✓ Projet "${name}" visible`);
        await page.waitForTimeout(800);
      }
    }
    await page.waitForTimeout(2500);
    
    // Étape 5: Déconnexion
    console.log('📍 Étape 5/5: Déconnexion');
    await page.getByRole('button', { name: /déconnexion/i }).click();
    await page.waitForTimeout(500);
    
    await expect(page).toHaveURL('/login', { timeout: 5000 });
    console.log('✓ Redirection vers login après déconnexion');
    await page.waitForTimeout(2000);
    
    console.log('');
    console.log('✨ DÉMONSTRATION TERMINÉE AVEC SUCCÈS!');
    console.log('');
  });

  test('🔍 Vérification des appels API avec le token', async ({ page }) => {
    console.log('🔍 TEST: Vérification des appels API authentifiés');
    
    // Compteur pour les appels API
    let apiCalls: { url: string, hasToken: boolean }[] = [];
    
    // Intercepter toutes les requêtes
    page.on('request', request => {
      if (request.url().includes('/api/')) {
        const hasToken = request.headers()['authorization']?.startsWith('Bearer ');
        apiCalls.push({
          url: request.url(),
          hasToken: hasToken || false
        });
        
        const status = hasToken ? '✓ Avec token' : '✗ Sans token';
        console.log(`  ${status}: ${request.method()} ${request.url()}`);
      }
    });
    
    // Se connecter
    await page.goto('/login');
    await page.waitForTimeout(1000);
    await page.getByPlaceholder(/email/i).pressSequentially('demo@refyai.com', { delay: 100 });
    await page.waitForTimeout(500);
    await page.getByPlaceholder(/mot de passe/i).pressSequentially('demo123', { delay: 100 });
    await page.waitForTimeout(500);
    
    // Surveiller la requête de login
    const loginPromise = page.waitForResponse(response => 
      response.url().includes('/api/auth/login') && response.status() === 200
    );
    
    await page.getByRole('button', { name: /se connecter/i }).click();
    const loginResponse = await loginPromise;
    
    console.log('✓ Connexion réussie');
    
    // Attendre le dashboard et le chargement des projets
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    
    // Attendre que les projets se chargent
    await page.waitForResponse(response => 
      response.url().includes('/api/projects'), 
      { timeout: 10000 }
    );
    
    await page.waitForTimeout(3000);
    
    // Analyser les résultats
    console.log('');
    console.log('📊 RÉSULTATS:');
    console.log(`Total d'appels API: ${apiCalls.length}`);
    
    const withToken = apiCalls.filter(call => call.hasToken).length;
    const withoutToken = apiCalls.filter(call => !call.hasToken).length;
    
    console.log(`✓ Avec token JWT: ${withToken}`);
    console.log(`✗ Sans token: ${withoutToken}`);
    
    // Vérifier que les appels POST-login ont un token
    const projectsCalls = apiCalls.filter(call => call.url.includes('/projects'));
    const projectsWithToken = projectsCalls.filter(call => call.hasToken).length;
    
    expect(projectsWithToken).toBeGreaterThan(0);
    console.log(`✓ ${projectsWithToken} appels /api/projects avec authentification`);
    console.log('');
  });

  test('📱 Test de navigation complète', async ({ page }) => {
    console.log('📱 TEST: Navigation entre les pages');
    
    // Se connecter
    await page.goto('/login');
    await page.waitForTimeout(1000);
    await page.getByPlaceholder(/email/i).pressSequentially('demo@refyai.com', { delay: 100 });
    await page.waitForTimeout(500);
    await page.getByPlaceholder(/mot de passe/i).pressSequentially('demo123', { delay: 100 });
    await page.waitForTimeout(500);
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    await expect(page).toHaveURL('/dashboard');
    console.log('✓ Page 1/3: Dashboard');
    await page.waitForTimeout(2000);
    
    // Essayer d'aller sur la page d'accueil (devrait rester sur dashboard)
    await page.goto('/');
    await page.waitForTimeout(500);
    await expect(page).toHaveURL('/dashboard');
    console.log('✓ Page 2/3: Redirection automatique vers dashboard');
    await page.waitForTimeout(1500);
    
    // Cliquer sur "Nouveau Projet" (si disponible)
    const newProjectButton = page.getByRole('button', { name: /nouveau projet/i });
    if (await newProjectButton.isVisible()) {
      await newProjectButton.click();
      await page.waitForTimeout(1000);
      console.log('✓ Page 3/3: Formulaire nouveau projet');
      await page.waitForTimeout(2000);
      
      // Revenir au dashboard
      await page.goto('/dashboard');
      await page.waitForTimeout(500);
      console.log('✓ Retour au dashboard');
    }
    
    await page.waitForTimeout(1500);
    console.log('');
  });

  test('⚡ Test de performance: Temps de chargement', async ({ page }) => {
    console.log('⚡ TEST: Performance et temps de chargement');
    
    // Mesurer le temps de connexion
    const loginStart = Date.now();
    await page.goto('/login');
    await page.waitForTimeout(1000);
    await page.getByPlaceholder(/email/i).pressSequentially('demo@refyai.com', { delay: 100 });
    await page.waitForTimeout(500);
    await page.getByPlaceholder(/mot de passe/i).pressSequentially('demo123', { delay: 100 });
    await page.waitForTimeout(500);
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    const loginTime = Date.now() - loginStart;
    console.log(`⏱️  Temps de connexion: ${loginTime}ms`);
    
    // Mesurer le temps de chargement des projets
    const projectsStart = Date.now();
    await expect(page.getByText(/Tour de Bureaux/i)).toBeVisible({ timeout: 10000 });
    const projectsTime = Date.now() - projectsStart;
    console.log(`⏱️  Temps de chargement des projets: ${projectsTime}ms`);
    await page.waitForTimeout(2000);
    
    // Vérifications de performance
    expect(loginTime).toBeLessThan(8000); // Moins de 8 secondes (augmenté pour tenir compte des délais visuels)
    expect(projectsTime).toBeLessThan(5000); // Moins de 5 secondes (augmenté pour tenir compte des délais visuels)
    
    console.log('✓ Performance acceptable');
    console.log('');
  });
});
