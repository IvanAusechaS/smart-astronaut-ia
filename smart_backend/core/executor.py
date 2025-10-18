"""
Executor Module
Carga y ejecuta algoritmos de busqueda de forma dinamica
"""

import importlib
import time
from typing import Dict, Any


def run_algorithm(name: str, params: dict) -> Dict[str, Any]:
    """
    Ejecuta un algoritmo de busqueda de forma dinamica
    
    Args:
        name: Nombre del algoritmo a ejecutar (ej: 'bfs', 'astar')
        params: Parametros para el algoritmo
    
    Returns:
        Diccionario con el resultado de la ejecucion
    """
    try:
        # Importar el modulo del algoritmo dinamicamente
        module = importlib.import_module(f"algorithms.{name}")
        
        # Verificar que el modulo tiene la funcion solve
        if not hasattr(module, 'solve'):
            return {
                "error": f"El algoritmo '{name}' no tiene una funcion 'solve()'"
            }
        
        # Ejecutar el algoritmo y medir tiempo
        start_time = time.time()
        result = module.solve(params)
        execution_time = time.time() - start_time
        
        # Agregar metadata
        return {
            "algorithm": name,
            "status": "success",
            "execution_time": round(execution_time, 4),
            "result": result
        }
        
    except ModuleNotFoundError:
        return {
            "error": f"Algoritmo '{name}' no encontrado",
            "status": "error"
        }
    except Exception as e:
        return {
            "error": f"Error al ejecutar '{name}': {str(e)}",
            "status": "error"
        }


def get_algorithm_info(name: str) -> Dict[str, Any]:
    """
    Obtiene informacion sobre un algoritmo especifico
    
    Args:
        name: Nombre del algoritmo
    
    Returns:
        Diccionario con informacion del algoritmo
    """
    try:
        module = importlib.import_module(f"algorithms.{name}")
        return {
            "name": name,
            "docstring": module.__doc__.strip() if module.__doc__ else "Sin descripcion",
            "available": True
        }
    except ModuleNotFoundError:
        return {
            "name": name,
            "available": False
        }
