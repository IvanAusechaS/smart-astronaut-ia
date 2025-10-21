/**
 * AlgorithmSelector Component
 * Selector de algoritmos con ejecución y resultados
 */

import { useState, useEffect } from 'react';
import { useMap } from '../context';
import { getAlgorithms, runAlgorithm } from '../api/algorithmApi';
import './AlgorithmSelector.css';

const AlgorithmSelector = ({ onResultsChange }) => {
  const { mapData, metadata } = useMap();
  const [algorithms, setAlgorithms] = useState([]);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAlgorithms();
  }, []);

  useEffect(() => {
    if (onResultsChange) {
      console.log('Enviando resultados al padre:', results);
      onResultsChange(results);
    }
  }, [results, onResultsChange]);

  const loadAlgorithms = async () => {
    try {
      const data = await getAlgorithms();
      setAlgorithms(data.algorithms || []);
      if (data.algorithms && data.algorithms.length > 0) {
        setSelectedAlgorithm(data.algorithms[0].name);
      }
    } catch (err) {
      console.error('Error loading algorithms:', err);
    }
  };

  const handleExecute = async () => {
    if (!selectedAlgorithm) {
      setError('Selecciona un algoritmo');
      return;
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

  return (
    <div className="algorithm-selector">
      <h3 className="selector-title">Búsqueda de Muestras</h3>

      <div className="selector-controls">
        <div className="select-wrapper">
          <label htmlFor="algorithm-select" className="select-label">
            Algoritmo de Búsqueda
          </label>
          <select
            id="algorithm-select"
            value={selectedAlgorithm}
            onChange={(e) => setSelectedAlgorithm(e.target.value)}
            disabled={loading || !mapData}
            className="algorithm-select"
          >
            {algorithms.map((algo) => (
              <option key={algo.name} value={algo.name}>
                {algo.display_name}
              </option>
            ))}
          </select>
        </div>

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
                {results.path ? results.path.length : 0}
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
