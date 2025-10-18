import { useState, useEffect } from 'react'
import axios from 'axios'
import './Home.css'

function Home() {
  const [algorithms, setAlgorithms] = useState([])
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [algorithmDetails, setAlgorithmDetails] = useState([])
  
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

  // Cargar lista de algoritmos al montar el componente
  useEffect(() => {
    fetchAlgorithms()
  }, [])

  const fetchAlgorithms = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${backendUrl}/api/algorithms`)
      setAlgorithms(response.data.algorithms || [])
      setAlgorithmDetails(response.data.details || [])
      setError(null)
    } catch (err) {
      setError('Error al cargar algoritmos: ' + err.message)
      console.error('Error fetching algorithms:', err)
    } finally {
      setLoading(false)
    }
  }

  const executeAlgorithm = async () => {
    if (!selectedAlgorithm) {
      setError('Selecciona un algoritmo primero')
      return
    }

    try {
      setLoading(true)
      setError(null)
      setResult(null)

      const response = await axios.post(`${backendUrl}/api/run`, {
        algorithm: selectedAlgorithm,
        params: {
          // Aqui se pueden agregar parametros personalizados
          map: "default_map",
          start: [0, 0],
          goal: [9, 9]
        }
      })

      setResult(response.data)
    } catch (err) {
      setError('Error al ejecutar algoritmo: ' + err.message)
      console.error('Error executing algorithm:', err)
    } finally {
      setLoading(false)
    }
  }

  const getAlgorithmDescription = (name) => {
    const detail = algorithmDetails.find(d => d.name === name)
    return detail?.docstring || 'Sin descripcion'
  }

  return (
    <div className="home-container">
      <div className="algorithm-selector">
        <h2>Seleccionar Algoritmo</h2>
        
        {loading && algorithms.length === 0 && (
          <div className="status-message loading">
            Cargando algoritmos...
          </div>
        )}

        {error && !loading && (
          <div className="status-message error">
            {error}
          </div>
        )}

        {algorithms.length > 0 && (
          <div className="selector-group">
            <select 
              value={selectedAlgorithm}
              onChange={(e) => setSelectedAlgorithm(e.target.value)}
              className="algorithm-select"
              disabled={loading}
            >
              <option value="">-- Selecciona un algoritmo --</option>
              {algorithms.map((algo) => (
                <option key={algo} value={algo}>
                  {algo.toUpperCase().replace('_', ' ')}
                </option>
              ))}
            </select>

            {selectedAlgorithm && (
              <div className="algorithm-info">
                <strong>Descripcion:</strong>
                <p>{getAlgorithmDescription(selectedAlgorithm)}</p>
              </div>
            )}

            <button 
              onClick={executeAlgorithm}
              disabled={!selectedAlgorithm || loading}
              className="execute-button"
            >
              {loading ? 'Ejecutando...' : 'Ejecutar Algoritmo'}
            </button>
          </div>
        )}

        {algorithms.length === 0 && !loading && !error && (
          <div className="status-message">
            No hay algoritmos disponibles
          </div>
        )}
      </div>

      {result && (
        <div className="result-container">
          <h2>Resultado</h2>
          
          {result.status === 'success' && (
            <div className="success-badge">
              Ejecucion exitosa
            </div>
          )}

          {result.error && (
            <div className="error-badge">
              {result.error}
            </div>
          )}

          <div className="result-details">
            <div className="result-item">
              <strong>Algoritmo:</strong>
              <span>{result.algorithm}</span>
            </div>
            
            {result.execution_time && (
              <div className="result-item">
                <strong>Tiempo de ejecucion:</strong>
                <span>{result.execution_time}s</span>
              </div>
            )}

            {result.status === 'success' && result.result && (
              <div className="result-data">
                <strong>Datos del resultado:</strong>
                <pre>{JSON.stringify(result.result, null, 2)}</pre>
              </div>
            )}
          </div>

          <div className="result-json">
            <strong>Respuesta completa (JSON):</strong>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  )
}

export default Home
