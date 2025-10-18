"""
Map Loader Module
Carga y valida mapas para el Smart Astronaut
"""

from typing import List
import io


def load_map(map_text: str) -> List[List[int]]:
    """
    Carga y parsea un mapa desde un string de texto
    
    Args:
        map_text: String con el mapa. Cada fila separada por salto de linea,
                  cada celda separada por espacios
    
    Returns:
        Matriz 10x10 de enteros representando el mapa
        
    Raises:
        ValueError: Si el mapa no tiene el formato correcto
    """
    if isinstance(map_text, io.StringIO):
        map_text = map_text.read()
    
    lines = map_text.strip().split('\n')
    
    # Filtrar lineas vacias
    lines = [line.strip() for line in lines if line.strip()]
    
    if len(lines) != 10:
        raise ValueError(f"El mapa debe tener exactamente 10 filas, se encontraron {len(lines)}")
    
    grid = []
    for i, line in enumerate(lines):
        try:
            row = [int(cell) for cell in line.split()]
        except ValueError as e:
            raise ValueError(f"Fila {i+1} contiene caracteres no numericos: {str(e)}")
        
        if len(row) != 10:
            raise ValueError(f"Fila {i+1} debe tener exactamente 10 celdas, tiene {len(row)}")
        
        grid.append(row)
    
    return grid


def validate_map(grid: List[List[int]]) -> bool:
    """
    Valida que un mapa tenga estructura correcta
    
    Args:
        grid: Matriz representando el mapa
        
    Returns:
        True si el mapa es valido
        
    Raises:
        ValueError: Si el mapa no es valido
    """
    if not grid:
        raise ValueError("El mapa esta vacio")
    
    if len(grid) != 10:
        raise ValueError(f"El mapa debe tener 10 filas, tiene {len(grid)}")
    
    for i, row in enumerate(grid):
        if len(row) != 10:
            raise ValueError(f"Fila {i+1} debe tener 10 celdas, tiene {len(row)}")
        
        if not all(isinstance(cell, int) for cell in row):
            raise ValueError(f"Fila {i+1} contiene valores no enteros")
    
    return True
