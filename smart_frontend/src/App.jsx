import { useState, useEffect } from 'react'
import axios from 'axios'
import { MapProvider, useMap } from './context'
import FileUploader from './components/FileUploader'
import GridDisplay from './components/GridDisplay'
import AlgorithmSelector from './components/AlgorithmSelector'
import StatsPanel from './components/StatsPanel'
import LegendCard from './components/LegendCard'
import './App.css'

function Dashboard() {
  const { mapData } = useMap();
  const [pathResults, setPathResults] = useState(null);
  const [backendStatus, setBackendStatus] = useState('Conectando...');
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

  useEffect(() => {
    const checkBackend = async () => {
      try {
        await axios.get(`${backendUrl}/`);
        setBackendStatus('Conectado');
      } catch (error) {
        setBackendStatus('Desconectado');
        console.error('Error conectando al backend:', error);
      }
    };

    checkBackend();
    const interval = setInterval(checkBackend, 30000);
    return () => clearInterval(interval);
  }, [backendUrl]);

  // Limpiar resultados cuando no hay mapa cargado
  useEffect(() => {
    if (!mapData) {
      setPathResults(null);
    }
  }, [mapData]);

  const handleResultsChange = (results) => {
    setPathResults(results);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <div className="header-left">
            <h1 className="app-title">🪐 Smart Astronaut</h1>
            <p className="app-subtitle">Explorador Marciano – Sistema de Búsqueda Inteligente</p>
          </div>
          <div className="header-right">
            <div className={`status-badge ${backendStatus === 'Conectado' ? 'online' : 'offline'}`}>
              <span className="status-dot"></span>
              <span className="status-text">{backendStatus}</span>
            </div>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="dashboard-grid">
          <div className="left-panel">
            <FileUploader />
            <AlgorithmSelector onResultsChange={handleResultsChange} />
          </div>

          <div className="center-panel">
            <div className="map-section">
              <div className="map-header">
                <h2 className="section-title">Mapa de Marte</h2>
              </div>

              {mapData ? (
                <GridDisplay
                  grid={mapData}
                  path={pathResults?.path}
                />
              ) : (
                <div className="map-placeholder">
                  <div className="placeholder-content">
                    <span className="placeholder-icon">🗺️</span>
                    <h3>No hay mapa cargado</h3>
                    <p>Carga un archivo .txt con el mapa marciano desde el panel izquierdo</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="right-panel">
            <LegendCard />
          </div>
        </div>

        <div className="bottom-panel">
          <StatsPanel />
        </div>
      </main>

      <footer className="app-footer">
        <p>🚀 Smart Astronaut – Explorador Marciano • Sistema de Búsqueda de Muestras Científicas</p>
        <p className="tech-stack">React + Vite • FastAPI + Python 3.11 • Docker</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <MapProvider>
      <Dashboard />
    </MapProvider>
  );
}

export default App
