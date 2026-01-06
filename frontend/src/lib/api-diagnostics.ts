/**
 * Utilitaire de diagnostic de connexion API
 * 
 * Ajouter dans n'importe quelle page pour diagnostiquer les problèmes de connexion
 * Utilisation: import { diagnoseAPI } from '@/lib/api-diagnostics';
 *              await diagnoseAPI();
 */

import { apiClient } from './api';

export interface DiagnosticResult {
  endpoint: string;
  status: 'success' | 'error' | 'timeout';
  statusCode?: number;
  responseTime: number;
  error?: string;
  retries?: number;
}

export async function diagnoseAPI(): Promise<DiagnosticResult[]> {
  const results: DiagnosticResult[] = [];
  
  const endpoints = [
    { method: 'GET', url: '/health', name: 'Health Check' },
    { method: 'GET', url: '/interest-rate/euribor', name: 'Euribor' },
    { method: 'GET', url: '/capex/categories', name: 'CAPEX Categories' },
    { 
      method: 'POST', 
      url: '/interest-rate/calculate', 
      name: 'Interest Rate Calculation',
      data: {
        city: 'Paris',
        ltv: 70,
        tri: 12,
        showstoppers_count: 0,
        company_experience: 'intermediate',
        project_type: 'restructuration_lourde',
        complexity: 'moderate'
      }
    },
  ];

  console.group('🔍 Diagnostic API REFY AI');
  console.log('Base URL:', apiClient.defaults.baseURL);
  console.log('Timeout:', apiClient.defaults.timeout, 'ms');
  console.log('---');

  for (const endpoint of endpoints) {
    const startTime = performance.now();
    
    try {
      const config: any = {
        method: endpoint.method,
        url: endpoint.url,
      };
      
      if (endpoint.data) {
        config.data = endpoint.data;
      }

      const response = await apiClient.request(config);
      const responseTime = performance.now() - startTime;

      const result: DiagnosticResult = {
        endpoint: endpoint.name,
        status: 'success',
        statusCode: response.status,
        responseTime: Math.round(responseTime),
        retries: (response.config as any).retryCount || 0,
      };

      results.push(result);
      console.log(
        `✓ ${endpoint.name}:`,
        `${response.status}`,
        `(${Math.round(responseTime)}ms)`,
        result.retries ? `[${result.retries} retries]` : ''
      );
    } catch (error: any) {
      const responseTime = performance.now() - startTime;
      const isTimeout = error.code === 'ECONNABORTED' || responseTime >= 30000;

      const result: DiagnosticResult = {
        endpoint: endpoint.name,
        status: isTimeout ? 'timeout' : 'error',
        statusCode: error.response?.status,
        responseTime: Math.round(responseTime),
        error: error.userMessage || error.message,
        retries: (error.config as any)?.retryCount || 0,
      };

      results.push(result);
      console.error(
        `✗ ${endpoint.name}:`,
        result.status.toUpperCase(),
        result.statusCode ? `(${result.statusCode})` : '',
        `[${result.error}]`,
        result.retries ? `[${result.retries} retries]` : ''
      );
    }
  }

  // Résumé
  const successful = results.filter(r => r.status === 'success').length;
  const failed = results.filter(r => r.status === 'error').length;
  const timeouts = results.filter(r => r.status === 'timeout').length;
  const avgResponseTime = Math.round(
    results.reduce((sum, r) => sum + r.responseTime, 0) / results.length
  );

  console.log('---');
  console.log('📊 Résumé:');
  console.log(`  ✓ Success: ${successful}/${results.length}`);
  console.log(`  ✗ Errors: ${failed}/${results.length}`);
  console.log(`  ⏱ Timeouts: ${timeouts}/${results.length}`);
  console.log(`  ⚡ Avg Response: ${avgResponseTime}ms`);
  console.groupEnd();

  return results;
}

/**
 * Test de connectivité rapide
 */
export async function quickHealthCheck(): Promise<boolean> {
  try {
    const response = await apiClient.get('/health', { timeout: 5000 });
    return response.status === 200;
  } catch {
    return false;
  }
}

/**
 * Afficher les diagnostics dans la console
 */
export async function showDiagnostics() {
  const results = await diagnoseAPI();
  
  // Afficher dans un format tableau pour la console
  console.table(
    results.map(r => ({
      Endpoint: r.endpoint,
      Status: r.status,
      'HTTP Code': r.statusCode || '-',
      'Time (ms)': r.responseTime,
      Retries: r.retries || 0,
      Error: r.error || '-',
    }))
  );
  
  return results;
}

/**
 * Hook React pour diagnostics en temps réel
 */
export function useAPIDiagnostics() {
  const [results, setResults] = React.useState<DiagnosticResult[]>([]);
  const [loading, setLoading] = React.useState(false);

  const runDiagnostics = async () => {
    setLoading(true);
    const diagnosticResults = await diagnoseAPI();
    setResults(diagnosticResults);
    setLoading(false);
  };

  return { results, loading, runDiagnostics };
}

// Import React pour le hook
import React from 'react';
