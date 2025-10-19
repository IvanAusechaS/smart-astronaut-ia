/**
 * useMap Hook
 * Hook personalizado para acceder al contexto del mapa
 */

import { useContext } from 'react';
import { MapContext } from './mapContextInstance';

export const useMap = () => {
  const context = useContext(MapContext);
  if (!context) {
    throw new Error('useMap debe usarse dentro de MapProvider');
  }
  return context;
};
