import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState('Conectando...')
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

  useEffect(() => {
    // Intentar conectar con el backend
    const checkBackend = async () => {
      try {
        const response = await axios.get(`${backendUrl}/`)
        setBackendStatus(`Conectado: ${response.data.message}`)
      } catch (error) {
        setBackendStatus('Backend no disponible')
        console.error('Error conectando al backend:', error)
      }
    }

    checkBackend()
  }, [backendUrl])

  return (
    <div className="app-container">
      <div className="header">
        <h1>SmartAstronaut</h1>
        <h2>Frontend funcionando</h2>
      </div>
      
      <div className="content">
        <div className="status-card">
          <h3>Estado del Backend</h3>
          <p className="status-message">{backendStatus}</p>
          <p className="backend-url">URL: {backendUrl}</p>
        </div>

        <div className="info-card">
          <h3>Informacion del Proyecto</h3>
          <ul>
            <li>Frontend: React + Vite</li>
            <li>Backend: FastAPI + Python 3.11</li>
            <li>Puerto Frontend: 5173</li>
            <li>Puerto Backend: 8000</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default App
