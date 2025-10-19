/**
 * Map API Client
 * Funciones para comunicarse con el backend de mapas
 */

import axios from 'axios';

const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

/**
 * Sube un archivo de mapa al backend
 * @param {File} file - Archivo .txt con el mapa
 * @returns {Promise} Respuesta del servidor con el mapa cargado
 */
export const uploadMap = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(`${backendUrl}/api/map/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 'Error al cargar el mapa'
    );
  }
};

/**
 * Obtiene el mapa actual del backend
 * @returns {Promise} Mapa y metadatos
 */
export const getMap = async () => {
  try {
    const response = await axios.get(`${backendUrl}/api/map`);
    return response.data;
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error('No hay mapa cargado');
    }
    throw new Error(
      error.response?.data?.detail || 'Error al obtener el mapa'
    );
  }
};

/**
 * Reinicia el mapa actual
 * @returns {Promise} Confirmacion del reset
 */
export const resetMap = async () => {
  try {
    const response = await axios.post(`${backendUrl}/api/map/reset`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 'Error al reiniciar el mapa'
    );
  }
};

/**
 * Establece la posicion objetivo en el mapa
 * @param {number} row - Fila (0-9)
 * @param {number} col - Columna (0-9)
 * @returns {Promise} Confirmacion
 */
export const setGoal = async (row, col) => {
  try {
    const response = await axios.post(`${backendUrl}/api/map/goal`, {
      row,
      col,
    });
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 'Error al establecer objetivo'
    );
  }
};

/**
 * Obtiene el valor de una celda especifica
 * @param {number} row - Fila (0-9)
 * @param {number} col - Columna (0-9)
 * @returns {Promise} Valor de la celda
 */
export const getCell = async (row, col) => {
  try {
    const response = await axios.get(`${backendUrl}/api/map/cell/${row}/${col}`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 'Error al obtener celda'
    );
  }
};

/**
 * Obtiene solo los metadatos del mapa
 * @returns {Promise} Metadatos
 */
export const getMetadata = async () => {
  try {
    const response = await axios.get(`${backendUrl}/api/map/metadata`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 'Error al obtener metadatos'
    );
  }
};
