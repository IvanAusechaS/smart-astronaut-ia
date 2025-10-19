/**
 * Algorithm API Client
 * Funciones para obtener y ejecutar algoritmos
 */

import axios from 'axios';

const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

/**
 * Obtiene la lista de algoritmos disponibles
 * @returns {Promise} Lista de algoritmos con nombre y descripcion
 */
export const getAlgorithms = async () => {
  try {
    const response = await axios.get(`${backendUrl}/api/algorithms`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 'Error al obtener algoritmos'
    );
  }
};

/**
 * Ejecuta un algoritmo de busqueda
 * @param {string} algorithmName - Nombre del algoritmo (bfs, dfs, etc.)
 * @param {object} params - Parametros: map, start, goal
 * @returns {Promise} Resultado con path, cost, nodes_expanded, execution_time
 */
export const runAlgorithm = async (algorithmName, params) => {
  try {
    const response = await axios.post(`${backendUrl}/api/run`, {
      algorithm: algorithmName,
      params: params,
    });
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 'Error al ejecutar algoritmo'
    );
  }
};

/**
 * Obtiene informacion detallada de un algoritmo especifico
 * @param {string} algorithmName - Nombre del algoritmo
 * @returns {Promise} Informacion del algoritmo
 */
export const getAlgorithmInfo = async (algorithmName) => {
  try {
    const response = await axios.get(`${backendUrl}/api/algorithm/${algorithmName}`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 'Error al obtener informacion del algoritmo'
    );
  }
};
