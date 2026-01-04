import { useState, useEffect } from 'react';
import { apiClient } from './api';

export function useAuth() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (token) {
        const response = await apiClient.get('/auth/me');
        setUser(response.data);
      }
    } catch (error) {
      localStorage.removeItem('auth_token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response = await apiClient.post('/auth/login', { email, password });
    localStorage.setItem('auth_token', response.data.access_token);
    await checkAuth();
    return response.data;
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setUser(null);
  };

  return { user, loading, login, logout, checkAuth };
}

export function useProjects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get('/projects');
      setProjects(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erreur lors du chargement');
    } finally {
      setLoading(false);
    }
  };

  const createProject = async (data: any) => {
    const response = await apiClient.post('/projects', data);
    await fetchProjects();
    return response.data;
  };

  const updateProject = async (id: number, data: any) => {
    const response = await apiClient.put(`/projects/${id}`, data);
    await fetchProjects();
    return response.data;
  };

  const deleteProject = async (id: number) => {
    await apiClient.delete(`/projects/${id}`);
    await fetchProjects();
  };

  return {
    projects,
    loading,
    error,
    fetchProjects,
    createProject,
    updateProject,
    deleteProject,
  };
}

export function useFinancial() {
  const calculateAnalysis = async (data: any) => {
    const response = await apiClient.post('/financial/analyze', data);
    return response.data;
  };

  const calculateTRI = async (initialInvestment: number, cashFlows: number[]) => {
    const response = await apiClient.post('/financial/tri', { 
      initial_investment: initialInvestment, 
      cash_flows: cashFlows 
    });
    return response.data;
  };

  const calculateLTV = async (loanAmount: number, propertyValue: number) => {
    const response = await apiClient.post('/financial/ltv', { 
      loan_amount: loanAmount, 
      property_value: propertyValue 
    });
    return response.data;
  };

  return {
    calculateAnalysis,
    calculateTRI,
    calculateLTV,
  };
}

export function useMarket() {
  const analyzeMarket = async (data: { city: string; surface: number; type_bien?: string }) => {
    const response = await apiClient.post('/market/analyze', data);
    return response.data;
  };

  const getComparables = async (commune: string) => {
    const response = await apiClient.get(`/market/comparables/${commune}`);
    return response.data;
  };

  return {
    analyzeMarket,
    getComparables,
  };
}

export function useShowstoppers() {
  const detectShowstoppers = async (data: any) => {
    const response = await apiClient.post('/showstoppers/detect', data);
    return response.data;
  };

  const getActionPlan = async (showstoppers: any[]) => {
    const response = await apiClient.post('/showstoppers/action-plan', { showstoppers });
    return response.data;
  };

  return {
    detectShowstoppers,
    getActionPlan,
  };
}
