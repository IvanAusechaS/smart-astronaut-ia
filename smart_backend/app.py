import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

from core.executor import run_algorithm, get_algorithm_info
from routes.map_routes import router as map_router

app = FastAPI(title="SmartAstronaut Backend", version="1.0.0")

# Configurar CORS - Leer origenes permitidos desde variable de entorno
cors_origins = os.getenv("CORS_ORIGINS", "*")
if cors_origins != "*":
    # Si se especifica, convertir a lista separada por comas
    origins_list = [origin.strip() for origin in cors_origins.split(",")]
else:
    origins_list = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelos Pydantic para validacion
class AlgorithmRequest(BaseModel):
    algorithm: str
    params: Optional[Dict[str, Any]] = {}


@app.get("/")
async def root():
    return {"message": "Backend conectado correctamente"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "smart_backend"}


@app.get("/api/algorithms")
async def list_algorithms():
    """
    Lista todos los algoritmos disponibles
    
    Returns:
        Lista de algoritmos con su informacion
    """
    try:
        algorithms_dir = "algorithms"
        
        # Obtener todos los archivos .py en el directorio algorithms
        if not os.path.exists(algorithms_dir):
            return {"algorithms": [], "error": "Directorio de algoritmos no encontrado"}
        
        files = [
            f[:-3] for f in os.listdir(algorithms_dir) 
            if f.endswith(".py") and f != "__init__.py"
        ]
        
        # Obtener informacion detallada de cada algoritmo
        algorithms_info = []
        for name in files:
            info = get_algorithm_info(name)
            algorithms_info.append(info)
        
        return {
            "algorithms": files,
            "count": len(files),
            "details": algorithms_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando algoritmos: {str(e)}")


@app.post("/api/run")
async def run_algorithm_endpoint(data: AlgorithmRequest):
    """
    Ejecuta un algoritmo especifico
    
    Args:
        data: Objeto con el nombre del algoritmo y sus parametros
    
    Returns:
        Resultado de la ejecucion del algoritmo
    """
    try:
        algorithm_name = data.algorithm
        params = data.params or {}
        
        if not algorithm_name:
            raise HTTPException(status_code=400, detail="Nombre de algoritmo requerido")
        
        # Ejecutar el algoritmo
        result = run_algorithm(algorithm_name, params)
        
        # Si hay error en la ejecucion
        if "error" in result:
            return result
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ejecutando algoritmo: {str(e)}")


@app.get("/api/algorithm/{name}")
async def get_algorithm_details(name: str):
    """
    Obtiene informacion detallada de un algoritmo especifico
    
    Args:
        name: Nombre del algoritmo
    
    Returns:
        Informacion del algoritmo
    """
    info = get_algorithm_info(name)
    if not info.get("available"):
        raise HTTPException(status_code=404, detail=f"Algoritmo '{name}' no encontrado")
    return info


# Incluir router de mapas
app.include_router(map_router, prefix="/api/map", tags=["maps"])
