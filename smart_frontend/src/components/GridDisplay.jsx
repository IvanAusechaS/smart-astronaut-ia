/**
 * GridDisplay
 * Visualizacion de la cuadricula del mapa 10x10 con animacion del recorrido paso a paso
 */

import { useState, useEffect } from 'react';
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
  const [currentStep, setCurrentStep] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const [combustible, setCombustible] = useState(0);
  const [muestrasRecolectadas, setMuestrasRecolectadas] = useState(new Set());
  const [visitedCells, setVisitedCells] = useState(new Set());

  useEffect(() => {
    if (path && path.length > 0) {
      setCurrentStep(0);
      setIsAnimating(true);
      setCombustible(0);
      setMuestrasRecolectadas(new Set());
      setVisitedCells(new Set());
    } else {
      setIsAnimating(false);
      setCurrentStep(0);
      setCombustible(0);
      setMuestrasRecolectadas(new Set());
      setVisitedCells(new Set());
    }
  }, [path]);

  useEffect(() => {
    if (!isAnimating || !path || !Array.isArray(path) || path.length === 0 || currentStep >= path.length - 1) {
      if (path && path.length > 0 && currentStep >= path.length - 1) {
        setIsAnimating(false);
      }
      return;
    }

    const timer = setTimeout(() => {
      const [row, col] = path[currentStep + 1];
      const cell = grid[row][col];

      // Actualizar combustible
      let newCombustible = combustible;
      if (cell === 5) {
        newCombustible = 20; // Recargar en la nave
      } else if (newCombustible > 0) {
        newCombustible -= 1;
      }
      setCombustible(newCombustible);

      // Recolectar muestras
      if (cell === 6) {
        setMuestrasRecolectadas(prev => new Set([...prev, `${row}-${col}`]));
      }

      // Marcar celda como visitada
      setVisitedCells(prev => new Set([...prev, `${row}-${col}`]));

      setCurrentStep(currentStep + 1);
    }, 300); // 300ms por paso

    return () => clearTimeout(timer);
  }, [currentStep, isAnimating, path, grid, combustible]);

  if (!grid || !Array.isArray(grid) || grid.length !== 10) {
    return (
      <div className="grid-error">
        <p>Mapa invalido o no cargado</p>
      </div>
    );
  }

  const getCurrentPosition = () => {
    if (!path || !isAnimating || currentStep >= path.length) return null;
    return path[currentStep];
  };

  const isVisited = (row, col) => {
    return visitedCells.has(`${row}-${col}`);
  };

  const isMuestraRecolectada = (row, col) => {
    return muestrasRecolectadas.has(`${row}-${col}`);
  };

  const currentPos = getCurrentPosition();
  const enNave = combustible > 0;

  return (
    <div className="grid-container">
      {isAnimating && (
        <div className="animation-status">
          <div className="status-item">
            <span className="status-label">Paso:</span>
            <span className="status-value">{currentStep + 1}/{path?.length || 0}</span>
          </div>
          <div className="status-item">
            <span className="status-label">Combustible:</span>
            <span className="status-value">{combustible}/20</span>
          </div>
          <div className="status-item">
            <span className="status-label">Muestras:</span>
            <span className="status-value">{muestrasRecolectadas.size}/3</span>
          </div>
          <div className="status-item">
            <span className="status-label">Estado:</span>
            <span className="status-value">{enNave ? '🚀 Volando' : '🚶 Caminando'}</span>
          </div>
        </div>
      )}
      
      <div className="grid">
        {grid.map((row, rowIndex) => (
          <div key={rowIndex} className="grid-row">
            {row.map((cell, colIndex) => {
              const isCurrentPos = currentPos && currentPos[0] === rowIndex && currentPos[1] === colIndex;
              const visited = isVisited(rowIndex, colIndex);
              const muestraRecogida = isMuestraRecolectada(rowIndex, colIndex);
              
              let cellClass = 'grid-cell';
              if (isCurrentPos) cellClass += ' current-position';
              if (visited && !isCurrentPos) cellClass += ' visited';
              
              // Color de fondo
              let bgColor = cellColors[cell] || '#ffffff';
              if (visited && !isCurrentPos) {
                bgColor = '#e0e0ff'; // Color para celdas visitadas
              }
              if (isCurrentPos) {
                bgColor = enNave ? '#ffd700' : '#00bfff'; // Dorado si está en nave, azul si camina
              }

              // Determinar emoji a mostrar
              let emoji = '';
              if (isCurrentPos) {
                if (enNave) {
                  emoji = '🚀'; // Nave volando
                } else {
                  emoji = '🚶'; // Astronauta caminando
                }
              } else if (cell === 6 && !muestraRecogida) {
                emoji = '🧪'; // Muestra no recogida
              } else if (cell === 6 && muestraRecogida) {
                emoji = '✅'; // Muestra recogida
              } else if (cell === 5) {
                emoji = '🚀'; // Nave auxiliar (base)
              } else if (cell === 4) {
                emoji = '🌋'; // Terreno volcánico
              } else if (cell === 3) {
                emoji = '🪨'; // Terreno rocoso
              } else if (cell === 1) {
                emoji = '⛰️'; // Obstáculo (montaña/roca grande)
              }

              return (
                <div
                  key={`${rowIndex}-${colIndex}`}
                  className={cellClass}
                  style={{ backgroundColor: bgColor }}
                  title={`${cellLabels[cell] || 'Desconocido'} (${rowIndex},${colIndex})`}
                >
                  <span className="cell-emoji">{emoji}</span>
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
