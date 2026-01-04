import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercepteur pour gérer les erreurs
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Redirection vers login si non authentifié
      localStorage.removeItem('auth_token');
      window.location.href = '/auth/login';
    }
    console.error('API Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

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
