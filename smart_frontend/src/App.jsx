import { useState, useEffect } from 'react'
import axios from 'axios'
import Home from './pages/Home'
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
        <h1>Smart Astronaut Solver</h1>
        <p className="subtitle">Sistema de algoritmos de busqueda inteligente</p>
      </div>
      
      <div className="status-bar">
        <div className="status-indicator">
          <span className={`status-dot ${backendStatus.includes('Conectado') ? 'connected' : 'disconnected'}`}></span>
          <span className="status-text">{backendStatus}</span>
        </div>
        <div className="backend-info">
          <span className="backend-url">{backendUrl}</span>
        </div>
      </div>

      <Home />

      <footer className="app-footer">
        <p>SmartAstronaut - Proyecto de Inteligencia Artificial</p>
        <p className="tech-stack">React + Vite | FastAPI + Python 3.11 | Docker</p>
      </footer>
    </div>
  )
}

export default App
