"""
World State Module
Gestiona el estado del mundo marciano (mapa) para el Smart Astronaut
"""

from typing import List, Dict, Tuple, Optional
from core.map_loader import load_map, validate_map


class MarsWorld:
    """
    Representa el estado del mundo marciano
    
    Atributos:
        grid: Matriz 10x10 con el mapa actual
        rows: Numero de filas (siempre 10)
        cols: Numero de columnas (siempre 10)
        metadata: Informacion adicional del mapa
    """
    
    def __init__(self):
        """Inicializa un mundo vacio"""
        self.grid: Optional[List[List[int]]] = None
        self.rows: int = 10
        self.cols: int = 10
        self.metadata: Dict = {
            'valid': False,
            'start': None,
            'goal': None,
            'samples': 0,
            'obstacles': 0,
            'rocky_terrain': 0,
            'volcanic_terrain': 0,
            'spacecraft_fuel': 0
        }
    
    def load_from_text(self, text: str) -> Dict:
        """
        Carga un mapa desde texto
        
        Args:
            text: String con el contenido del mapa
            
        Returns:
            Diccionario con el resultado de la operacion
            
        Raises:
            ValueError: Si el mapa no es valido
        """
        try:
            # Cargar y validar el mapa
            grid = load_map(text)
            validate_map(grid)
            
            # Almacenar el mapa
            self.grid = grid
            
            # Analizar el mapa y actualizar metadata
            self._analyze_map()
            
            return {
                'status': 'ok',
                'message': 'Mapa cargado exitosamente',
                'metadata': self.metadata
            }
            
        except ValueError as e:
            self.reset()
            raise ValueError(f"Error al cargar el mapa: {str(e)}")
    
    def _analyze_map(self):
        """
        Analiza el mapa y actualiza los metadatos
        Valores según especificación oficial:
        0 = casilla libre
        1 = obstaculo
        2 = astronauta (posicion inicial)
        3 = terreno rocoso (costo 3)
        4 = terreno volcanico (costo 5)
        5 = nave auxiliar (con combustible interno)
        6 = muestra cientifica
        """
        if not self.grid:
            return
        
        # Resetear contadores
        self.metadata['obstacles'] = 0
        self.metadata['rocky_terrain'] = 0
        self.metadata['volcanic_terrain'] = 0
        self.metadata['spacecraft'] = 0
        self.metadata['scientific_samples'] = 0
        self.metadata['astronaut_position'] = None
        self.metadata['spacecraft_position'] = None
        
        # Contar elementos
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    self.metadata['obstacles'] += 1
                elif cell == 2:
                    # Astronauta - posicion inicial
                    if self.metadata['astronaut_position'] is None:
                        self.metadata['astronaut_position'] = [i, j]
                elif cell == 3:
                    self.metadata['rocky_terrain'] += 1
                elif cell == 4:
                    self.metadata['volcanic_terrain'] += 1
                elif cell == 5:
                    # Nave auxiliar
                    self.metadata['spacecraft'] += 1
                    if self.metadata['spacecraft_position'] is None:
                        self.metadata['spacecraft_position'] = [i, j]
                elif cell == 6:
                    # Muestra cientifica
                    self.metadata['scientific_samples'] += 1
        
        # Marcar como valido
        self.metadata['valid'] = True
    
    def reset(self):
        """Limpia el estado del mundo"""
        self.grid = None
        self.metadata = {
            'valid': False,
            'astronaut_position': None,
            'spacecraft_position': None,
            'scientific_samples': 0,
            'obstacles': 0,
            'rocky_terrain': 0,
            'volcanic_terrain': 0,
            'spacecraft': 0
        }
    
    def to_dict(self) -> Dict:
        """
        Convierte el mundo a un diccionario serializable
        
        Returns:
            Diccionario con el estado completo del mundo
        """
        return {
            'grid': self.grid,
            'rows': self.rows,
            'cols': self.cols,
            'metadata': self.metadata,
            'loaded': self.is_loaded()
        }
    
    def is_loaded(self) -> bool:
        """
        Verifica si hay un mapa cargado y valido
        
        Returns:
            True si el mapa esta cargado y es valido
        """
        return self.grid is not None and self.metadata['valid']
    
    def get_cell(self, row: int, col: int) -> Optional[int]:
        """
        Obtiene el valor de una celda especifica
        
        Args:
            row: Fila (0-9)
            col: Columna (0-9)
            
        Returns:
            Valor de la celda o None si no esta cargado
        """
        if not self.is_loaded():
            return None
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        
        return None
    
    def set_goal(self, row: int, col: int) -> bool:
        """
        Establece la posicion objetivo (meta)
        
        Args:
            row: Fila (0-9)
            col: Columna (0-9)
            
        Returns:
            True si se establecio correctamente
        """
        if not self.is_loaded():
            return False
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.metadata['goal'] = (row, col)
            return True
        
        return False


# Instancia global del mundo
mars_world = MarsWorld()
