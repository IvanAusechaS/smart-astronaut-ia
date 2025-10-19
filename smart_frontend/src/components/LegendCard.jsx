/**
 * LegendCard Component
 * Leyenda de colores del mapa
 */

import './LegendCard.css';

const LegendCard = () => {
  const legendItems = [
    { color: '#ffffff', label: 'Libre', value: 0, icon: '⬜' },
    { color: '#7a7a7a', label: 'Obstáculo', value: 1, icon: '🚧' },
    { color: '#007bff', label: 'Astronauta', value: 2, icon: '�‍🚀' },
    { color: '#8b4513', label: 'Rocoso (costo 3)', value: 3, icon: '🪨' },
    { color: '#b22222', label: 'Volcánico (costo 5)', value: 4, icon: '🌋' },
    { color: '#ffff00', label: 'Nave (combustible)', value: 5, icon: '�' },
    { color: '#00ff00', label: 'Muestra Científica', value: 6, icon: '�' },
  ];

  return (
    <div className="legend-card">
      <h3 className="legend-title">Leyenda del Terreno</h3>
      
      <div className="legend-grid">
        {legendItems.map((item) => (
          <div key={item.value} className="legend-item">
            <div className="legend-color-box" style={{ backgroundColor: item.color }}>
              <span className="legend-icon">{item.icon}</span>
            </div>
            <div className="legend-info">
              <span className="legend-label">{item.label}</span>
              <span className="legend-value">Valor: {item.value}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="legend-note">
        <span className="note-icon">💡</span>
        <p className="note-text">
          El astronauta debe recolectar todas las muestras científicas y regresar a la nave auxiliar. 
          La nave (celda 5) proporciona combustible interno para 20 movimientos con costo reducido (x0.5).
        </p>
      </div>
    </div>
  );
};

export default LegendCard;
