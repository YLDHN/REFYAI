'use client';

import * as React from 'react';
import Link from 'next/link';
import { cn } from '@/lib/cn';
import { Badge } from '@/components/ui/Badge';

export interface Project {
  id: string;
  name: string;
  address: string;
  city: string;
  typologie: string;
  surface_totale: number;
  prix_acquisition: number;
  tri_avant_is?: number;
  score_bloquant?: number;
  score_technique?: number;
  status: 'En cours' | 'Terminé' | 'Bloqué';
  created_at: string;
}

interface Column<T> {
  key: keyof T | string;
  header: string;
  sortable?: boolean;
  render?: (value: any, row: T) => React.ReactNode;
}

interface DataGridProps<T> {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (row: T) => void;
  loading?: boolean;
  emptyMessage?: string;
}

export function DataGrid<T extends { id: string }>({
  data,
  columns,
  onRowClick,
  loading = false,
  emptyMessage = 'Aucune donnée disponible',
}: DataGridProps<T>) {
  const [sortConfig, setSortConfig] = React.useState<{
    key: keyof T | string;
    direction: 'asc' | 'desc';
  } | null>(null);

  const sortedData = React.useMemo(() => {
    if (!sortConfig) return data;

    return [...data].sort((a, b) => {
      const aValue = a[sortConfig.key as keyof T];
      const bValue = b[sortConfig.key as keyof T];

      if (aValue === bValue) return 0;
      if (aValue == null) return 1;
      if (bValue == null) return -1;

      const comparison = aValue < bValue ? -1 : 1;
      return sortConfig.direction === 'asc' ? comparison : -comparison;
    });
  }, [data, sortConfig]);

  const handleSort = (key: keyof T | string) => {
    setSortConfig((current) => {
      if (current?.key === key) {
        return current.direction === 'asc'
          ? { key, direction: 'desc' }
          : null;
      }
      return { key, direction: 'asc' };
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        <p>{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-800">
      <table className="w-full">
        <thead className="bg-gray-900/50">
          <tr>
            {columns.map((column) => (
              <th
                key={String(column.key)}
                className={cn(
                  'px-6 py-4 text-left text-sm font-semibold text-gray-300',
                  column.sortable && 'cursor-pointer hover:text-white'
                )}
                onClick={() => column.sortable && handleSort(column.key)}
              >
                <div className="flex items-center gap-2">
                  {column.header}
                  {column.sortable && sortConfig?.key === column.key && (
                    <span className="text-blue-400">
                      {sortConfig.direction === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800">
          {sortedData.map((row) => (
            <tr
              key={row.id}
              onClick={() => onRowClick?.(row)}
              className={cn(
                'hover:bg-gray-900/30 transition-colors',
                onRowClick && 'cursor-pointer'
              )}
            >
              {columns.map((column) => {
                const value = row[column.key as keyof T];
                return (
                  <td key={String(column.key)} className="px-6 py-4 text-sm text-gray-300">
                    {column.render ? column.render(value, row) : String(value ?? '-')}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Colonnes prédéfinies pour les projets
export const projectColumns: Column<Project>[] = [
  {
    key: 'name',
    header: 'Nom du Projet',
    sortable: true,
    render: (value, row) => (
      <Link href={`/projects/${row.id}`} className="font-medium text-blue-400 hover:underline">
        {value}
      </Link>
    ),
  },
  {
    key: 'address',
    header: 'Adresse',
    sortable: true,
  },
  {
    key: 'city',
    header: 'Ville',
    sortable: true,
  },
  {
    key: 'typologie',
    header: 'Type',
    sortable: true,
  },
  {
    key: 'surface_totale',
    header: 'Surface (m²)',
    sortable: true,
    render: (value) => value ? `${value.toLocaleString('fr-FR')} m²` : '-',
  },
  {
    key: 'prix_acquisition',
    header: 'Prix',
    sortable: true,
    render: (value) => value ? `${value.toLocaleString('fr-FR')} €` : '-',
  },
  {
    key: 'tri_avant_is',
    header: 'TRI',
    sortable: true,
    render: (value) => value ? `${(value * 100).toFixed(1)}%` : '-',
  },
  {
    key: 'score_technique',
    header: 'Score Technique',
    sortable: true,
    render: (value) => {
      if (value == null) return '-';
      const score = value * 100;
      return (
        <span className={cn(
          'font-medium',
          score >= 80 ? 'text-green-400' :
          score >= 60 ? 'text-yellow-400' :
          'text-red-400'
        )}>
          {score.toFixed(0)}/100
        </span>
      );
    },
  },
  {
    key: 'status',
    header: 'Statut',
    sortable: true,
    render: (value) => {
      const variant = 
        value === 'Terminé' ? 'success' :
        value === 'Bloqué' ? 'error' :
        'warning';
      return <Badge variant={variant}>{value}</Badge>;
    },
  },
];
