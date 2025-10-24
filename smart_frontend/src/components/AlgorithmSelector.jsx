/**
 * AlgorithmSelector Component
 * Selector de algoritmos con ejecución y resultados
 * Incluye selector de orden de operadores para DFS
 */

import { useState, useEffect } from 'react';
import { useMap } from '../context';
import { getAlgorithms, runAlgorithm } from '../api/algorithmApi';
import './AlgorithmSelector.css';

const AlgorithmSelector = ({ onResultsChange }) => {
  const { mapData, metadata } = useMap();
  const [algorithms, setAlgorithms] = useState([]);
  const [searchType, setSearchType] = useState(''); // 'uninformed' o 'informed'
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  
  // Estado para el orden de operadores del DFS
  const [operatorOrder, setOperatorOrder] = useState(['arriba', 'abajo', 'izquierda', 'derecha']);

  // Clasificación de algoritmos según el enunciado
  const uninformedAlgorithms = ['bfs', 'uniform_cost', 'dfs'];
  const informedAlgorithms = ['greedy', 'astar'];

  useEffect(() => {
    loadAlgorithms();
  }, []);

  useEffect(() => {
    if (onResultsChange) {
      console.log('Enviando resultados al padre:', results);
      onResultsChange(results);
    }
  }, [results, onResultsChange]);

  // Limpiar resultados cuando no hay mapa cargado
  useEffect(() => {
    if (!mapData) {
      setResults(null);
      setError(null);
      setSearchType('');
      setSelectedAlgorithm('');
    }
  }, [mapData]);

  const loadAlgorithms = async () => {
    try {
      const data = await getAlgorithms();
      setAlgorithms(data.algorithms || []);
    } catch (err) {
      console.error('Error loading algorithms:', err);
    }
  };

  // Filtrar algoritmos según el tipo de búsqueda seleccionado
  const getFilteredAlgorithms = () => {
    if (!searchType) return [];
    
    const filterList = searchType === 'uninformed' ? uninformedAlgorithms : informedAlgorithms;
    return algorithms.filter(algo => filterList.includes(algo.name));
  };

  // Resetear algoritmo seleccionado cuando cambia el tipo de búsqueda
  useEffect(() => {
    setSelectedAlgorithm('');
    setResults(null);
    setError(null);
    // Resetear orden de operadores al valor por defecto
    setOperatorOrder(['arriba', 'abajo', 'izquierda', 'derecha']);
  }, [searchType]);

  const handleExecute = async () => {
    if (!selectedAlgorithm) {
      setError('Selecciona un algoritmo');
      return;
    }
    
    // Validar operadores duplicados si es DFS
    if (selectedAlgorithm === 'dfs') {
      const uniqueOperators = new Set(operatorOrder);
      if (uniqueOperators.size !== operatorOrder.length) {
        setError('Error: Has seleccionado operadores duplicados. Cada dirección (Arriba, Abajo, Izquierda, Derecha) debe aparecer exactamente una vez. Por favor, asegúrate de que cada posición tenga un operador diferente.');
        return;
      }
    }

    if (!mapData) {
      setError('Debes cargar un mapa primero');
      return;
    }

    if (!metadata?.astronaut_position) {
      setError('El mapa no tiene posición de inicio del astronauta');
      return;
    }

    if (!metadata?.spacecraft_position) {
      setError('El mapa no tiene nave auxiliar definida');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const params = {
        map: mapData,
        start: metadata.astronaut_position,
        goal: metadata.spacecraft_position,
      };
      
      // Si el algoritmo es DFS, agregar el orden de operadores
      if (selectedAlgorithm === 'dfs') {
        params.operator_order = operatorOrder;
      }

      console.log('Ejecutando algoritmo:', selectedAlgorithm);
      console.log('Parámetros:', params);

      const response = await runAlgorithm(selectedAlgorithm, params);
      console.log('Respuesta del backend:', response);
      
      // El backend devuelve { algorithm, status, execution_time, result }
      // Combinamos execution_time con el result para el componente
      const result = {
        ...response.result,
        execution_time: response.execution_time,
        algorithm: response.algorithm
      };
      
      console.log('Resultado procesado:', result);
      setResults(result);
    } catch (err) {
      console.error('Error completo:', err);
      setError(err.message || 'Error al ejecutar búsqueda');
      console.error('Execution error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setResults(null);
    setError(null);
  };

  const filteredAlgorithms = getFilteredAlgorithms();

  return (
    <div className="algorithm-selector">
      <h3 className="selector-title">Búsqueda de Muestras</h3>

      <div className="selector-controls">
        {/* PASO 1: Seleccionar tipo de búsqueda */}
        <div className="select-wrapper">
          <label htmlFor="search-type-select" className="select-label">
            Tipo de Búsqueda
          </label>
          <select
            id="search-type-select"
            value={searchType}
            onChange={(e) => setSearchType(e.target.value)}
            disabled={loading || !mapData}
            className="algorithm-select"
          >
            <option value="">-- Selecciona tipo de búsqueda --</option>
            <option value="uninformed">No Informada</option>
            <option value="informed">Informada</option>
          </select>
        </div>

        {/* PASO 2: Seleccionar algoritmo específico */}
        {searchType && (
          <div className="select-wrapper">
            <label htmlFor="algorithm-select" className="select-label">
              {searchType === 'uninformed' 
                ? 'Algoritmo (Amplitud / Costo Uniforme / Profundidad)' 
                : 'Algoritmo (Avara / A*)'}
            </label>
            <select
              id="algorithm-select"
              value={selectedAlgorithm}
              onChange={(e) => setSelectedAlgorithm(e.target.value)}
              disabled={loading || !mapData || filteredAlgorithms.length === 0}
              className="algorithm-select"
            >
              <option value="">-- Selecciona un algoritmo --</option>
              {filteredAlgorithms.map((algo) => (
                <option key={algo.name} value={algo.name}>
                  {algo.display_name}
                </option>
              ))}
            </select>
          </div>
        )}
        
        {/* PASO 3: Configurar orden de operadores (solo para DFS) */}
        {selectedAlgorithm === 'dfs' && (
          <div className="operator-order-wrapper">
            <label className="select-label">Orden de Operadores</label>
            <div className="operator-order-grid">
              {[0, 1, 2, 3].map((index) => (
                <div key={index} className="operator-select-item">
                  <label className="operator-label">{index + 1}°:</label>
                  <select
                    value={operatorOrder[index]}
                    onChange={(e) => {
                      const newOrder = [...operatorOrder];
                      newOrder[index] = e.target.value;
                      setOperatorOrder(newOrder);
                    }}
                    className="operator-select"
                    disabled={loading}
                  >
                    <option value="arriba">⬆️ Arriba</option>
                    <option value="abajo">⬇️ Abajo</option>
                    <option value="izquierda">⬅️ Izquierda</option>
                    <option value="derecha">➡️ Derecha</option>
                  </select>
                </div>
              ))}
            </div>
            <p className="operator-order-hint">
              Define el orden en que DFS explorará los vecinos de cada posición
            </p>
          </div>
        )}

        <div className="action-buttons">
          <button
            onClick={handleExecute}
            disabled={loading || !mapData || !selectedAlgorithm}
            className="btn btn-execute"
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Buscando...
              </>
            ) : (
              <>
                <span></span>
                Ejecutar Búsqueda
              </>
            )}
          </button>

          {results && (
            <button onClick={handleClear} className="btn btn-clear">
              <span></span>
              Limpiar
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {results && (
        <div className="results-container">
          <div className="results-header">
            <h4>Reporte de Búsqueda</h4>
            <span className="algorithm-badge">{selectedAlgorithm.toUpperCase()}</span>
          </div>

          <div className="results-grid">
            <div className="result-item">
              <span className="result-label">Nodos Expandidos</span>
              <span className="result-value">{results.nodes_expanded || 0}</span>
            </div>

            <div className="result-item">
              <span className="result-label">Profundidad</span>
              <span className="result-value">
                {results.max_depth || 0}
              </span>
            </div>

            <div className="result-item">
              <span className="result-label">Tiempo de Cómputo</span>
              <span className="result-value">
                {results.execution_time ? `${results.execution_time.toFixed(3)}s` : 'N/A'}
              </span>
            </div>

            <div className="result-item">
              <span className="result-label">Costo Total</span>
              <span className="result-value">{results.cost || 0}</span>
            </div>
          </div>

          {results.message && (
            <div className="result-message">
              <p>{results.message}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AlgorithmSelector;
