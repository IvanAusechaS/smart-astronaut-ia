"""
Map Routes
Endpoints para gestion de mapas del Smart Astronaut
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from core.world_state import mars_world


router = APIRouter(tags=["maps"])


class GoalRequest(BaseModel):
    """Modelo para establecer objetivo"""
    row: int
    col: int


@router.post("/upload")
async def upload_map(file: UploadFile = File(...)):
    """
    Carga un mapa desde un archivo .txt
    
    Args:
        file: Archivo de texto con el mapa 10x10
        
    Returns:
        Estado de la operacion y metadatos del mapa
    """
    try:
        # Validar que sea un archivo .txt
        if not file.filename.endswith('.txt'):
            raise HTTPException(
                status_code=400,
                detail="Solo se permiten archivos .txt"
            )
        
        # Leer el contenido del archivo
        content = await file.read()
        text = content.decode('utf-8')
        
        # Cargar el mapa en el mundo
        result = mars_world.load_from_text(text)
        
        return {
            "status": "ok",
            "message": "Mapa cargado exitosamente",
            "metadata": mars_world.metadata,
            "map": mars_world.grid
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo: {str(e)}"
        )


@router.get("")
async def get_map():
    """
    Obtiene el mapa actual si esta cargado
    
    Returns:
        Mapa y metadatos o error 404
    """
    if not mars_world.is_loaded():
        raise HTTPException(
            status_code=404,
            detail="No map loaded"
        )
    
    return mars_world.to_dict()


@router.post("/reset")
async def reset_map():
    """
    Limpia el mapa actual
    
    Returns:
        Confirmacion del reset
    """
    mars_world.reset()
    
    return {
        "status": "reset",
        "message": "Mapa reiniciado exitosamente"
    }


@router.post("/goal")
async def set_goal(goal: GoalRequest):
    """
    Establece la posicion objetivo en el mapa
    
    Args:
        goal: Posicion objetivo (fila, columna)
        
    Returns:
        Confirmacion o error
    """
    if not mars_world.is_loaded():
        raise HTTPException(
            status_code=404,
            detail="No map loaded. Please upload a map first."
        )
    
    if not (0 <= goal.row < 10 and 0 <= goal.col < 10):
        raise HTTPException(
            status_code=400,
            detail="Goal position must be within 0-9 range"
        )
    
    success = mars_world.set_goal(goal.row, goal.col)
    
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to set goal"
        )
    
    return {
        "status": "ok",
        "message": "Goal set successfully",
        "goal": (goal.row, goal.col),
        "metadata": mars_world.metadata
    }


@router.get("/cell/{row}/{col}")
async def get_cell(row: int, col: int):
    """
    Obtiene el valor de una celda especifica
    
    Args:
        row: Fila (0-9)
        col: Columna (0-9)
        
    Returns:
        Valor de la celda
    """
    if not mars_world.is_loaded():
        raise HTTPException(
            status_code=404,
            detail="No map loaded"
        )
    
    if not (0 <= row < 10 and 0 <= col < 10):
        raise HTTPException(
            status_code=400,
            detail="Position must be within 0-9 range"
        )
    
    cell_value = mars_world.get_cell(row, col)
    
    return {
        "row": row,
        "col": col,
        "value": cell_value
    }


@router.get("/metadata")
async def get_metadata():
    """
    Obtiene solo los metadatos del mapa sin el grid completo
    
    Returns:
        Metadatos del mapa
    """
    if not mars_world.is_loaded():
        raise HTTPException(
            status_code=404,
            detail="No map loaded"
        )
    
    return {
        "metadata": mars_world.metadata,
        "loaded": True
    }
