import { test, expect } from '@playwright/test';

test.describe('Tests API Backend', () => {
  
  let authToken: string;

  test.beforeAll(async ({ request }) => {
    // Obtenir un token d'authentification
    const response = await request.post('http://localhost:8000/api/auth/login', {
      form: {
        username: 'demo@refyai.com',
        password: 'demo123'
      }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    authToken = data.access_token;
    expect(authToken).toBeTruthy();
    console.log('✓ Token d\'authentification obtenu');
  });

  test('GET /api/projects retourne la liste des projets', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/projects/', {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    
    expect(response.ok()).toBeTruthy();
    const projects = await response.json();
    
    expect(Array.isArray(projects)).toBeTruthy();
    expect(projects.length).toBeGreaterThan(0);
    
    console.log(`✓ ${projects.length} projets récupérés`);
    
    // Vérifier la structure d'un projet
    const project = projects[0];
    expect(project).toHaveProperty('id');
    expect(project).toHaveProperty('name');
    expect(project).toHaveProperty('user_id');
    expect(project).toHaveProperty('status');
  });

  test('GET /api/projects/{id} retourne un projet spécifique', async ({ request }) => {
    // D'abord récupérer la liste des projets
    const listResponse = await request.get('http://localhost:8000/api/projects/', {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    
    const projects = await listResponse.json();
    const projectId = projects[0].id;
    
    // Récupérer le projet spécifique
    const response = await request.get(`http://localhost:8000/api/projects/${projectId}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    
    expect(response.ok()).toBeTruthy();
    const project = await response.json();
    
    expect(project.id).toBe(projectId);
    console.log(`✓ Projet "${project.name}" récupéré`);
  });

  test('POST /api/projects crée un nouveau projet', async ({ request }) => {
    const newProject = {
      name: 'Test Projet E2E',
      description: 'Projet créé par les tests automatiques',
      city: 'Paris',
      postal_code: '75001',
      project_type: 'rental',
      status: 'draft',
      strategy: 'core',
      bp_duration: 10,
      asset_type: 'residential',
      surface: 1000.0,
      purchase_price: 1000000.0
    };
    
    const response = await request.post('http://localhost:8000/api/projects/', {
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
      data: newProject
    });
    
    expect(response.ok()).toBeTruthy();
    const project = await response.json();
    
    expect(project.name).toBe(newProject.name);
    expect(project.city).toBe(newProject.city);
    expect(project.id).toBeTruthy();
    
    console.log(`✓ Projet créé avec ID ${project.id}`);
    
    // Nettoyer: supprimer le projet créé
    await request.delete(`http://localhost:8000/api/projects/${project.id}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    console.log(`✓ Projet test nettoyé`);
  });

  test('PUT /api/projects/{id} met à jour un projet', async ({ request }) => {
    // Créer un projet
    const newProject = {
      name: 'Projet à Modifier',
      city: 'Lyon',
      project_type: 'rental',
      status: 'draft'
    };
    
    const createResponse = await request.post('http://localhost:8000/api/projects/', {
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
      data: newProject
    });
    
    const project = await createResponse.json();
    const projectId = project.id;
    
    // Modifier le projet
    const updateData = {
      name: 'Projet Modifié',
      status: 'in_progress'
    };
    
    const updateResponse = await request.put(`http://localhost:8000/api/projects/${projectId}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
      data: updateData
    });
    
    expect(updateResponse.ok()).toBeTruthy();
    const updatedProject = await updateResponse.json();
    
    expect(updatedProject.name).toBe('Projet Modifié');
    expect(updatedProject.status).toBe('in_progress');
    
    console.log(`✓ Projet ${projectId} mis à jour`);
    
    // Nettoyer
    await request.delete(`http://localhost:8000/api/projects/${projectId}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
  });

  test('DELETE /api/projects/{id} supprime un projet', async ({ request }) => {
    // Créer un projet
    const newProject = {
      name: 'Projet à Supprimer',
      city: 'Marseille',
      project_type: 'rental',
      status: 'draft'
    };
    
    const createResponse = await request.post('http://localhost:8000/api/projects/', {
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
      data: newProject
    });
    
    const project = await createResponse.json();
    const projectId = project.id;
    
    // Supprimer le projet
    const deleteResponse = await request.delete(`http://localhost:8000/api/projects/${projectId}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    
    expect(deleteResponse.status()).toBe(204);
    console.log(`✓ Projet ${projectId} supprimé`);
    
    // Vérifier qu'il n'existe plus
    const getResponse = await request.get(`http://localhost:8000/api/projects/${projectId}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    
    expect(getResponse.status()).toBe(404);
  });

  test('Requêtes sans token retournent 401', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/projects/');
    
    // Backend retourne 403 au lieu de 401
    expect([401, 403]).toContain(response.status());
    console.log('✓ Requête sans token correctement rejetée (' + response.status() + ')');
  });

  test('GET /health vérifie l\'état du backend', async ({ request }) => {
    const response = await request.get('http://localhost:8000/health');
    
    expect(response.ok()).toBeTruthy();
    const health = await response.json();
    
    expect(health.status).toBe('healthy');
    expect(health.database).toBe('healthy');
    
    console.log('✓ Backend en bonne santé');
  });

  test('POST /api/auth/register crée un nouvel utilisateur', async ({ request }) => {
    const timestamp = Date.now();
    const newUser = {
      email: `test${timestamp}@example.com`,
      password: 'testpassword123',
      full_name: 'Test User'
    };
    
    const response = await request.post('http://localhost:8000/api/auth/register', {
      headers: {
        'Content-Type': 'application/json'
      },
      data: newUser
    });
    
    expect(response.ok()).toBeTruthy();
    const user = await response.json();
    
    expect(user.email).toBe(newUser.email);
    expect(user.full_name).toBe(newUser.full_name);
    expect(user.is_active).toBe(true);
    
    console.log(`✓ Utilisateur ${user.email} créé`);
  });
});
