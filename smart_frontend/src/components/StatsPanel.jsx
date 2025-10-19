/**
 * StatsPanel Component
 * Panel de estadisticas del mapa
 */

import { useMap } from '../context';
import './StatsPanel.css';

const StatsPanel = () => {
  const { metadata, mapData } = useMap();

  if (!mapData || !metadata) {
    return (
      <div className="stats-panel empty">
        <h3 className="stats-title">Estadísticas del Mapa</h3>
        <p className="empty-message">Carga un mapa para ver las estadísticas</p>
      </div>
    );
  }

  const stats = [
    {
      label: 'Dimensiones',
      value: `${metadata.rows || 10} × ${metadata.cols || 10}`,
      icon: '📏',
    },
    {
      label: 'Obstáculos',
      value: metadata.obstacles || 0,
      icon: '🚧',
      color: '#7a7a7a',
    },
    {
      label: 'Muestras Científicas',
      value: metadata.scientific_samples || 0,
      icon: '🔬',
      color: '#00ff00',
    },
    {
      label: 'Nave Auxiliar',
      value: metadata.spacecraft || 0,
      icon: '🛸',
      color: '#ffff00',
    },
    {
      label: 'Terreno Rocoso',
      value: metadata.rocky_terrain || 0,
      icon: '🪨',
      color: '#8b4513',
    },
    {
      label: 'Terreno Volcánico',
      value: metadata.volcanic_terrain || 0,
      icon: '🌋',
      color: '#b22222',
    },
  ];

  const positions = [
    {
      label: 'Posición Astronauta',
      value: metadata.astronaut_position
        ? `[${metadata.astronaut_position.join(', ')}]`
        : 'No definido',
      icon: '🧑‍🚀',
      color: '#007bff',
    },
    {
      label: 'Posición Nave',
      value: metadata.spacecraft_position
        ? `[${metadata.spacecraft_position.join(', ')}]`
        : 'No definido',
      icon: '�',
      color: '#ffff00',
    },
  ];

  return (
    <div className="stats-panel">
      <h3 className="stats-title">Estadísticas del Mapa</h3>

      <div className="stats-grid">
        {stats.map((stat, idx) => (
          <div key={idx} className="stat-card">
            <div className="stat-icon" style={{ color: stat.color }}>
              {stat.icon}
            </div>
            <div className="stat-content">
              <span className="stat-label">{stat.label}</span>
              <span className="stat-value">{stat.value}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="positions-section">
        <h4 className="section-subtitle">Posiciones</h4>
        <div className="positions-grid">
          {positions.map((pos, idx) => (
            <div key={idx} className="position-card">
              <span className="position-icon" style={{ color: pos.color }}>
                {pos.icon}
              </span>
              <div className="position-content">
                <span className="position-label">{pos.label}</span>
                <span className="position-value">{pos.value}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {metadata.valid !== undefined && (
        <div className={`validation-badge ${metadata.valid ? 'valid' : 'invalid'}`}>
          <span>{metadata.valid ? '✅' : '❌'}</span>
          <span>{metadata.valid ? 'Mapa Válido' : 'Mapa Inválido'}</span>
        </div>
      )}
    </div>
  );
};

export default StatsPanel;
