/**
 * MapProvider
 * Proveedor de estado global para el mapa de Marte
 */

import { useState } from 'react';
import { MapContext } from './mapContextInstance';
import * as mapApi from '../api/mapApi';

export const MapProvider = ({ children }) => {
  const [mapData, setMapData] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Carga un mapa desde archivo
   */
  const uploadMap = async (file) => {
    setLoading(true);
    setError(null);
    try {
      const result = await mapApi.uploadMap(file);
      setMapData(result.map);
      setMetadata(result.metadata);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Obtiene el mapa actual
   */
  const loadMap = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await mapApi.getMap();
      setMapData(result.map);
      setMetadata(result.metadata);
      return result;
    } catch (err) {
      setError(err.message);
      setMapData(null);
      setMetadata(null);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Reinicia el mapa
   */
  const resetMap = async () => {
    setLoading(true);
    setError(null);
    try {
      await mapApi.resetMap();
      setMapData(null);
      setMetadata(null);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Limpia mensajes de error
   */
  const clearError = () => {
    setError(null);
  };

  const value = {
    mapData,
    metadata,
    loading,
    error,
    uploadMap,
    loadMap,
    resetMap,
    clearError,
  };

  return <MapContext.Provider value={value}>{children}</MapContext.Provider>;
};
