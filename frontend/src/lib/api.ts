import axios, { AxiosInstance, AxiosError, AxiosRequestConfig, InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Configuration des timeouts par type d'opération
const TIMEOUTS = {
  default: 30000,     // 30s pour opérations standard
  upload: 120000,     // 2min pour uploads
  download: 120000,   // 2min pour downloads
  quick: 10000,       // 10s pour opérations rapides (health, etc.)
};

// Configuration du retry
const RETRY_CONFIG = {
  maxRetries: 3,
  retryDelay: 1000,           // Délai initial: 1s
  retryableStatuses: [408, 429, 500, 502, 503, 504], // Statuses à retry
};

// Helper pour exponential backoff
const getRetryDelay = (retryCount: number): number => {
  return RETRY_CONFIG.retryDelay * Math.pow(2, retryCount); // 1s, 2s, 4s...
};

// Helper pour déterminer si on doit retry
const shouldRetry = (error: AxiosError, retryCount: number): boolean => {
  if (retryCount >= RETRY_CONFIG.maxRetries) return false;
  
  // Retry sur erreurs réseau
  if (!error.response) return true;
  
  // Retry sur statuses spécifiques
  const status = error.response.status;
  return RETRY_CONFIG.retryableStatuses.includes(status);
};

// Sleep helper pour retry
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: TIMEOUTS.default,
  headers: {
    'Content-Type': 'application/json',
  },
  // Permet d'annuler les requêtes en timeout
  validateStatus: (status) => status < 500, // Ne rejette que 500+
});

// Intercepteur pour ajouter le token d'authentification
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Token d'authentification depuis Zustand store
    if (typeof window !== 'undefined') {
      const authStore = localStorage.getItem('auth-storage');
      if (authStore) {
        const { state } = JSON.parse(authStore);
        if (state?.token) {
          config.headers.Authorization = `Bearer ${state.token}`;
        }
      }
    }
    
    // Ajuster timeout selon le type de requête
    if (config.url?.includes('/documents/upload')) {
      config.timeout = TIMEOUTS.upload;
    } else if (config.url?.includes('/health')) {
      config.timeout = TIMEOUTS.quick;
    }
    
    // Initialiser le compteur de retry
    (config as any).retryCount = (config as any).retryCount || 0;
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepteur pour gérer les erreurs avec retry logic
apiClient.interceptors.response.use(
  (response) => {
    // Log des succès en dev
    if (process.env.NODE_ENV === 'development') {
      console.log(`✓ ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`);
    }
    return response;
  },
  async (error: AxiosError) => {
    const config = error.config as InternalAxiosRequestConfig & { retryCount?: number };
    const retryCount = config?.retryCount || 0;
    
    // Log de l'erreur
    console.error(
      `✗ API Error [${error.response?.status || 'NETWORK'}]:`,
      error.config?.method?.toUpperCase(),
      error.config?.url,
      error.response?.data || error.message
    );
    
    // Gestion de l'authentification
    if (error.response?.status === 401) {
      // Déconnexion via Zustand
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth-storage');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
    
    // Retry logic
    if (config && shouldRetry(error, retryCount)) {
      config.retryCount = retryCount + 1;
      const delay = getRetryDelay(retryCount);
      
      console.warn(
        `⟳ Retry ${config.retryCount}/${RETRY_CONFIG.maxRetries} in ${delay}ms:`,
        config.method?.toUpperCase(),
        config.url
      );
      
      await sleep(delay);
      return apiClient(config);
    }
    
    // Enrichir l'erreur avec un message utilisateur
    const enhancedError: any = error;
    enhancedError.userMessage = getUserFriendlyErrorMessage(error);
    
    return Promise.reject(enhancedError);
  }
);

// Helper pour messages d'erreur utilisateur
function getUserFriendlyErrorMessage(error: AxiosError): string {
  if (!error.response) {
    return 'Impossible de contacter le serveur. Vérifiez votre connexion internet.';
  }
  
  const status = error.response.status;
  const data: any = error.response.data;
  
  switch (status) {
    case 400:
      return data?.detail || 'Données invalides. Vérifiez votre saisie.';
    case 403:
      return 'Accès refusé. Vous n\'avez pas les permissions nécessaires.';
    case 404:
      return 'Ressource introuvable.';
    case 408:
      return 'La requête a pris trop de temps. Réessayez.';
    case 429:
      return 'Trop de requêtes. Attendez quelques instants.';
    case 500:
    case 502:
    case 503:
    case 504:
      return 'Erreur serveur. Notre équipe a été notifiée.';
    default:
      return data?.detail || 'Une erreur est survenue. Réessayez.';
  }
}

// ==================== QUESTIONNAIRE ====================
export const questionnaireAPI = {
  getQuestions: () => 
    apiClient.get('/questionnaire/questions'),
  
  validateAnswers: (answers: Record<string, any>) =>
    apiClient.post('/questionnaire/validate', { answers }),
  
  extractFilters: (answers: Record<string, any>) =>
    apiClient.post('/questionnaire/extract-filters', { answers }),
};

// ==================== SHOWSTOPPERS ====================
export const showstoppersAPI = {
  detect: (data: any) =>
    apiClient.post('/showstoppers/detect', data),
  
  getActionPlan: (showstoppers: any[]) =>
    apiClient.post('/showstoppers/action-plan', { showstoppers }),
};

// ==================== MARKET ANALYSIS ====================
export const marketAPI = {
  analyze: (data: { city: string; surface: number; type_bien?: string }) =>
    apiClient.post('/market/analyze', data),
  
  getComparables: (params: any) =>
    apiClient.get('/market/comparables', { params }),
};

// ==================== INTEREST RATE ====================
export const interestRateAPI = {
  getEuribor: (maturity: '3m' | '6m' | '12m' = '12m') =>
    apiClient.get(`/interest-rate/euribor?maturity=${maturity}`),
  
  calculate: (data: any) =>
    apiClient.post('/interest-rate/calculate', data),
};

// ==================== CAPEX ====================
export const capexAPI = {
  getCategories: () =>
    apiClient.get('/capex/categories'),
  
  estimateItem: (data: any) =>
    apiClient.post('/capex/estimate', data),
  
  calculateProject: (data: any) =>
    apiClient.post('/capex/project', data),
  
  estimateRenovation: (data: any) =>
    apiClient.post('/capex/renovation-estimate', data),
  
  getCityTiers: () =>
    apiClient.get('/capex/city-tiers'),
};

// ==================== ADMINISTRATIVE DELAYS ====================
export const adminDelaysAPI = {
  getProcedures: () =>
    apiClient.get('/admin-delays/available-procedures'),
  
  getProcedureDelay: (data: any) =>
    apiClient.post('/admin-delays/procedure', data),
  
  calculateTimeline: (data: any) =>
    apiClient.post('/admin-delays/project-timeline', data),
  
  getFullDuration: (data: any) =>
    apiClient.post('/admin-delays/full-duration', data),
  
  getCities: () =>
    apiClient.get('/admin-delays/cities'),
  
  getComplexityLevels: () =>
    apiClient.get('/admin-delays/complexity-levels'),
};

// ==================== PROJECTS ====================
export const projectsAPI = {
  getAll: () =>
    apiClient.get('/projects'),
  
  getById: (id: number) =>
    apiClient.get(`/projects/${id}`),
  
  create: (data: any) =>
    apiClient.post('/projects', data),
  
  update: (id: number, data: any) =>
    apiClient.put(`/projects/${id}`, data),
  
  delete: (id: number) =>
    apiClient.delete(`/projects/${id}`),
};

// ==================== DOCUMENTS ====================
export const documentsAPI = {
  upload: (file: File, projectId?: number, documentType?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    if (projectId) formData.append('project_id', projectId.toString());
    if (documentType) formData.append('document_type', documentType);
    
    return apiClient.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  getAll: (projectId?: number) =>
    apiClient.get('/documents', { params: { project_id: projectId } }),
  
  getById: (id: number) =>
    apiClient.get(`/documents/${id}`),
  
  analyze: (documentId: number) =>
    apiClient.post(`/documents/${documentId}/analyze`),
  
  delete: (id: number) =>
    apiClient.delete(`/documents/${id}`),
};

// ==================== CHAT ====================
export const chatAPI = {
  sendMessage: (message: string, conversationId?: string) =>
    apiClient.post('/chat/message', { 
      message, 
      conversation_id: conversationId 
    }),
  
  getConversations: () =>
    apiClient.get('/chat/conversations'),
  
  getConversation: (id: string) =>
    apiClient.get(`/chat/conversations/${id}`),
};

export default apiClient;
