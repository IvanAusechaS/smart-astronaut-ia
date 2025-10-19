/**
 * GridDisplay
 * Visualizacion de la cuadricula del mapa 10x10 con animacion del recorrido
 */

import './GridDisplay.css';

const cellColors = {
  0: '#ffffff',
  1: '#7a7a7a',
  2: '#007bff',
  3: '#8b4513',
  4: '#b22222',
  5: '#ffff00',
  6: '#00ff00',
};

const cellLabels = {
  0: 'Libre',
  1: 'Obstaculo',
  2: 'Astronauta',
  3: 'Rocoso (costo 3)',
  4: 'Volcanico (costo 5)',
  5: 'Nave (20 mov x 0.5)',
  6: 'Muestra Cientifica',
};

const GridDisplay = ({ grid, path = null }) => {
  if (!grid || !Array.isArray(grid) || grid.length !== 10) {
    return (
      <div className="grid-error">
        <p>Mapa invalido o no cargado</p>
      </div>
    );
  }

  const isInPath = (row, col) => {
    if (!path || !Array.isArray(path)) return false;
    return path.some(([r, c]) => r === row && c === col);
  };

  return (
    <div className="grid-container">
      <div className="grid">
        {grid.map((row, rowIndex) => (
          <div key={rowIndex} className="grid-row">
            {row.map((cell, colIndex) => {
              const inPath = isInPath(rowIndex, colIndex);
              return (
                <div
                  key={`${rowIndex}-${colIndex}`}
                  className={`grid-cell ${inPath ? 'in-path' : ''}`}
                  style={{ backgroundColor: inPath ? '#ff00ff' : (cellColors[cell] || '#ffffff') }}
                  title={`${cellLabels[cell] || 'Desconocido'}`}
                >
                  {inPath && '🛸'}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
};

export default GridDisplay;
