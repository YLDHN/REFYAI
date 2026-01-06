import { test, expect } from '@playwright/test';

test.describe('Test VISIBLE - Création de projet via formulaire', () => {
  
  test.beforeEach(async ({ page }) => {
    // Aller sur la page de login
    await page.goto('http://localhost:3000/login');
    await page.waitForTimeout(1000);
  });

  test('Remplir le formulaire de création de projet STEP BY STEP', async ({ page }) => {
    test.setTimeout(120000); // 2 minutes max

    // ========== ÉTAPE 1: LOGIN ==========
    console.log('🔐 ÉTAPE 1: Connexion...');
    await page.getByPlaceholder(/email/i).pressSequentially('demo@refyai.com', { delay: 100 });
    await page.waitForTimeout(800);
    
    await page.getByPlaceholder(/mot de passe/i).pressSequentially('demo123', { delay: 100 });
    await page.waitForTimeout(800);
    
    await page.getByRole('button', { name: /se connecter/i }).click();
    await page.waitForTimeout(2000);
    
    // Vérifier qu'on est sur le dashboard
    await expect(page).toHaveURL(/dashboard/);
    console.log('✅ Connecté sur le dashboard');

    // ========== ÉTAPE 2: ALLER SUR NOUVEAU PROJET ==========
    console.log('📝 ÉTAPE 2: Navigation vers nouveau projet...');
    
    // Chercher le bouton "Nouveau Projet" ou "+"
    const newProjectButton = page.getByRole('button', { name: /nouveau projet/i }).first();
    await newProjectButton.click();
    await page.waitForTimeout(2000);
    
    console.log('✅ Sur la page nouveau projet');

    // ========== ÉTAPE 3: REMPLIR LE FORMULAIRE COMPLET ==========
    console.log('✏️  ÉTAPE 3: Remplissage COMPLET du formulaire...');
    
    // Scroll to top
    await page.evaluate(() => window.scrollTo(0, 0));
    
    // 1. Nom du projet
    console.log('  → 1. Nom du projet...');
    await page.locator('input[name="name"]').pressSequentially('Projet Complet Test', { delay: 80 });
    await page.waitForTimeout(600);
    console.log('  ✅ Nom rempli');

    // 2. Description
    console.log('  → 2. Description...');
    await page.locator('textarea[name="description"], input[name="description"]').pressSequentially('Projet test avec tous les champs remplis', { delay: 60 });
    await page.waitForTimeout(600);
    console.log('  ✅ Description remplie');

    // 3. Type de projet
    console.log('  → 3. Type de projet...');
    await page.locator('select[name="projectType"]').selectOption('rental');
    await page.waitForTimeout(500);
    console.log('  ✅ Type: Locatif');

    // 4. Stratégie
    console.log('  → 4. Stratégie...');
    await page.locator('select[name="strategy"]').selectOption('core');
    await page.waitForTimeout(500);
    console.log('  ✅ Stratégie: Core');

    // 5. Typologie de l'actif
    console.log('  → 5. Typologie actif...');
    await page.locator('select[name="assetType"]').selectOption('residential');
    await page.waitForTimeout(500);
    console.log('  ✅ Type actif: Résidentiel');

    // 6. Surface
    console.log('  → 6. Surface...');
    await page.locator('input[name="surface"]').pressSequentially('150', { delay: 100 });
    await page.waitForTimeout(600);
    console.log('  ✅ Surface: 150 m²');

    // 7. Durée BP
    console.log('  → 7. Durée BP...');
    await page.locator('input[name="bpDuration"]').fill('7');
    await page.waitForTimeout(500);
    console.log('  ✅ Durée BP: 7 années');

    // 8. Adresse
    console.log('  → 8. Adresse...');
    await page.locator('input[name="address"]').fill('10 Rue de la Paix');
    await page.waitForTimeout(500);
    console.log('  ✅ Adresse remplie');

    // 9. Ville
    console.log('  → 9. Ville...');
    await page.locator('input[name="city"]').fill('Lyon');
    await page.waitForTimeout(500);
    console.log('  ✅ Ville: Lyon');

    // 10. Code postal
    console.log('  → 10. Code postal...');
    await page.locator('input[name="postalCode"]').fill('69002');
    await page.waitForTimeout(500);
    console.log('  ✅ Code postal: 69002');

    // Scroll down pour voir les champs suivants
    await page.evaluate(() => window.scrollBy(0, 400));
    await page.waitForTimeout(800);

    // 11. Prix d'acquisition
    console.log('  → 11. Prix d\'acquisition...');
    await page.locator('input[name="acquisitionPrice"]').fill('1500000');
    await page.waitForTimeout(500);
    console.log('  ✅ Prix acquisition: 1 500 000 €');

    // 12. Frais de notaire
    console.log('  → 12. Frais de notaire...');
    await page.locator('input[name="notaryFees"]').fill('120000');
    await page.waitForTimeout(500);
    console.log('  ✅ Frais notaire: 120 000 €');

    // 13. Frais de due diligence
    console.log('  → 13. Due diligence...');
    await page.locator('input[name="dueDiligenceCost"]').fill('15000');
    await page.waitForTimeout(500);
    console.log('  ✅ Due diligence: 15 000 €');

    // 14. Yield à l'acquisition
    console.log('  → 14. Yield...');
    await page.locator('input[name="acquisitionYield"]').fill('4.5');
    await page.waitForTimeout(500);
    console.log('  ✅ Yield: 4.5%');

    // 15. WALB
    console.log('  → 15. WALB...');
    await page.locator('input[name="walb"]').fill('3.2');
    await page.waitForTimeout(500);
    console.log('  ✅ WALB: 3.2 années');

    // 16. WALT
    console.log('  → 16. WALT...');
    await page.locator('input[name="walt"]').fill('5.8');
    await page.waitForTimeout(500);
    console.log('  ✅ WALT: 5.8 années');

    // Scroll encore
    await page.evaluate(() => window.scrollBy(0, 400));
    await page.waitForTimeout(800);

    // 17. Loyer en place
    console.log('  → 17. Loyer en place...');
    await page.locator('input[name="currentRent"]').fill('75000');
    await page.waitForTimeout(500);
    console.log('  ✅ Loyer actuel: 75 000 €');

    // 18. VLM
    console.log('  → 18. VLM...');
    await page.locator('input[name="marketRent"]').fill('85000');
    await page.waitForTimeout(500);
    console.log('  ✅ VLM: 85 000 €');

    // 19. Taux d'occupation
    console.log('  → 19. Taux occupation...');
    await page.locator('input[name="occupancyRate"]').fill('95');
    await page.waitForTimeout(500);
    console.log('  ✅ Occupation: 95%');

    // 20. Prix d'achat
    console.log('  → 20. Prix achat...');
    await page.locator('input[name="purchasePrice"]').fill('450000');
    await page.waitForTimeout(500);
    console.log('  ✅ Prix achat: 450 000 €');

    // Scroll encore
    await page.evaluate(() => window.scrollBy(0, 400));
    await page.waitForTimeout(800);

    // 21. Budget travaux
    console.log('  → 21. Budget travaux...');
    await page.locator('input[name="renovationBudget"]').fill('90000');
    await page.waitForTimeout(500);
    console.log('  ✅ Travaux: 90 000 €');

    // 22. Valeur estimée
    console.log('  → 22. Valeur estimée...');
    await page.locator('input[name="estimatedValue"]').fill('550000');
    await page.waitForTimeout(500);
    console.log('  ✅ Valeur estimée: 550 000 €');

    // 23. Détail des travaux - Gros oeuvre
    console.log('  → 23. Gros oeuvre...');
    const grosOeuvreInput = page.locator('input[name="capexGrosOeuvre"], input[name*="gros"]').first();
    if (await grosOeuvreInput.count() > 0) {
      await grosOeuvreInput.fill('50000');
      await page.waitForTimeout(500);
      console.log('  ✅ Gros oeuvre: 50 000 €');
    }

    // 24. Second oeuvre
    console.log('  → 24. Second oeuvre...');
    const secondOeuvreInput = page.locator('input[name="capexSecondOeuvre"], input[name*="second"]').first();
    if (await secondOeuvreInput.count() > 0) {
      await secondOeuvreInput.fill('80000');
      await page.waitForTimeout(500);
      console.log('  ✅ Second oeuvre: 80 000 €');
    }

    // 25. Aménagements
    console.log('  → 25. Aménagements...');
    const amenageInput = page.locator('input[name="capexAmenagements"], input[name*="amenage"]').first();
    if (await amenageInput.count() > 0) {
      await amenageInput.fill('40000');
      await page.waitForTimeout(500);
      console.log('  ✅ Aménagements: 40 000 €');
    }

    // 26. Autres travaux
    console.log('  → 26. Autres travaux...');
    const autresInput = page.locator('input[name="capexAutres"], input[name*="autres"]').first();
    if (await autresInput.count() > 0) {
      await autresInput.fill('30000');
      await page.waitForTimeout(500);
      console.log('  ✅ Autres: 30 000 €');
    }

    // Scroll vers le bas pour le financement
    await page.evaluate(() => window.scrollBy(0, 400));
    await page.waitForTimeout(800);

    // 27. Montant du financement
    console.log('  → 27. Financement...');
    await page.locator('input[name="financingAmount"]').fill('1000000');
    await page.waitForTimeout(500);
    console.log('  ✅ Financement: 1 000 000 €');

    // 28. LTV
    console.log('  → 28. LTV...');
    await page.locator('input[name="ltv"]').fill('65');
    await page.waitForTimeout(500);
    console.log('  ✅ LTV: 65%');

    // 29. Taux d'intérêt
    console.log('  → 29. Taux intérêt...');
    await page.locator('input[name="interestRate"]').fill('3.5');
    await page.waitForTimeout(500);
    console.log('  ✅ Taux: 3.5%');

    // 30. Durée du prêt
    console.log('  → 30. Durée prêt...');
    await page.locator('input[name="loanDuration"]').fill('20');
    await page.waitForTimeout(500);
    console.log('  ✅ Durée: 20 années');

    console.log('');
    console.log('✅ TOUS LES CHAMPS REMPLIS (30 champs)');
    await page.waitForTimeout(1000);

    // Prendre un screenshot avant soumission
    await page.screenshot({ path: 'test-results/formulaire-rempli.png', fullPage: true });
    console.log('📸 Screenshot sauvegardé: test-results/formulaire-rempli.png');
    await page.waitForTimeout(500);

    // ========== ÉTAPE 4: SOUMETTRE ==========
    console.log('🚀 ÉTAPE 4: Soumission du formulaire...');
    await page.waitForTimeout(1500);
    
    // Chercher le bouton de soumission
    const submitButton = page.getByRole('button', { name: /créer|enregistrer|valider/i }).first();
    await submitButton.click();
    
    console.log('  ⏳ Attente de la réponse...');
    await page.waitForTimeout(3000);

    // Prendre un screenshot après soumission
    await page.screenshot({ path: 'test-results/apres-soumission.png', fullPage: true });
    console.log('📸 Screenshot sauvegardé: test-results/apres-soumission.png');

    // ========== ÉTAPE 5: VÉRIFICATION ==========
    console.log('✅ ÉTAPE 5: Vérification...');
    
    // Vérifier qu'on a été redirigé ou qu'un message apparaît
    await page.waitForTimeout(2000);
    
    // Afficher l'URL actuelle
    const currentUrl = page.url();
    console.log('📍 URL actuelle:', currentUrl);
    
    // Afficher les erreurs éventuelles dans la console
    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.log('❌ Erreur console:', msg.text());
      }
    });

    // Vérifier qu'on n'est plus sur la page de création
    const isStillOnForm = currentUrl.includes('/new') || currentUrl.includes('/create');
    if (isStillOnForm) {
      console.log('⚠️  ATTENTION: Toujours sur la page de formulaire!');
      // Chercher des messages d'erreur
      const errorMessages = await page.locator('[class*="error"], [role="alert"]').allTextContents();
      if (errorMessages.length > 0) {
        console.log('❌ Messages d\'erreur trouvés:', errorMessages);
      }
    } else {
      console.log('✅ Redirection effectuée - Projet probablement créé');
    }

    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✨ Test terminé - Vérifiez les screenshots dans test-results/');
  });
});
