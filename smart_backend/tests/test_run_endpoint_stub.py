"""
Test suite para el endpoint de ejecucion de algoritmos
Prueba el endpoint POST /api/run con algoritmos stub
"""

import pytest
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestRunEndpointStub:
    """Tests para el endpoint POST /api/run"""
    
    def test_run_endpoint_exists(self, client):
        """
        Test: El endpoint /api/run debe existir
        """
        response = client.post("/api/run", json={
            "algorithm": "bfs",
            "params": {}
        })
        # Puede ser 200 (exito) o 400 (error), pero no 404
        assert response.status_code != 404, "El endpoint debe existir"
    
    def test_run_nonexistent_algorithm(self, client):
        """
        Test: Intentar ejecutar un algoritmo inexistente debe retornar error
        """
        response = client.post("/api/run", json={
            "algorithm": "nonexistent_algorithm_xyz",
            "params": {}
        })
        
        data = response.json()
        
        # Puede ser status code 400 o retornar error en JSON
        assert response.status_code == 200 or response.status_code == 400
        
        if response.status_code == 200:
            # Si retorna 200, debe tener un campo de error en el JSON
            assert "error" in data or data.get("status") == "error", \
                "Debe indicar que hay un error"
    
    def test_run_algorithm_without_name(self, client):
        """
        Test: Intentar ejecutar sin especificar algoritmo debe fallar
        """
        response = client.post("/api/run", json={
            "params": {}
        })
        
        # Debe retornar error (400 o similar)
        assert response.status_code >= 400
    
    def test_run_bfs_stub_basic(self, client):
        """
        Test: Ejecutar algoritmo BFS stub con parametros basicos
        """
        response = client.post("/api/run", json={
            "algorithm": "bfs",
            "params": {
                "map": "test_map",
                "start": [0, 0],
                "goal": [9, 9]
            }
        })
        
        assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"
        
        data = response.json()
        
        # Verificar estructura basica de respuesta
        assert "algorithm" in data, "La respuesta debe contener 'algorithm'"
        assert data["algorithm"] == "bfs", "El algoritmo debe ser 'bfs'"
        assert "status" in data, "La respuesta debe contener 'status'"
    
    def test_run_algorithm_response_structure(self, client):
        """
        Test: Verificar la estructura completa de la respuesta
        """
        response = client.post("/api/run", json={
            "algorithm": "bfs",
            "params": {}
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Campos obligatorios
        assert "algorithm" in data
        assert "status" in data
        
        # Si es exitoso, debe tener resultado
        if data["status"] == "success":
            assert "result" in data, "Respuesta exitosa debe contener 'result'"
            assert "execution_time" in data, "Debe incluir tiempo de ejecucion"
    
    def test_run_algorithm_with_small_map(self, client):
        """
        Test: Ejecutar algoritmo con un mapa pequeno en JSON
        """
        small_map = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        
        response = client.post("/api/run", json={
            "algorithm": "bfs",
            "params": {
                "map": small_map,
                "start": [0, 0],
                "goal": [2, 2]
            }
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success" or "result" in data
    
    def test_run_all_algorithms_stub(self, client):
        """
        Test: Ejecutar todos los algoritmos disponibles como stub
        """
        algorithms = ["bfs", "dfs", "uniform_cost", "greedy", "astar"]
        
        for algo in algorithms:
            response = client.post("/api/run", json={
                "algorithm": algo,
                "params": {
                    "map": "test",
                    "start": [0, 0],
                    "goal": [5, 5]
                }
            })
            
            assert response.status_code == 200, f"Algoritmo {algo} debe ejecutarse"
            data = response.json()
            
            assert data["algorithm"] == algo
            assert "status" in data
    
    def test_run_algorithm_result_has_expected_fields(self, client):
        """
        Test: El resultado debe contener los campos esperados
        """
        response = client.post("/api/run", json={
            "algorithm": "bfs",
            "params": {}
        })
        
        data = response.json()
        
        if data.get("status") == "success" and "result" in data:
            result = data["result"]
            
            # Campos comunes en resultados de algoritmos
            expected_fields = ["path", "nodes_expanded", "cost"]
            
            for field in expected_fields:
                assert field in result, f"El resultado debe contener '{field}'"
    
    def test_run_algorithm_path_is_list(self, client):
        """
        Test: El campo 'path' debe ser una lista
        """
        response = client.post("/api/run", json={
            "algorithm": "bfs",
            "params": {}
        })
        
        data = response.json()
        
        if data.get("status") == "success" and "result" in data:
            result = data["result"]
            
            if "path" in result:
                assert isinstance(result["path"], list), "El path debe ser una lista"
    
    def test_run_algorithm_metrics(self, client):
        """
        Test: Verificar que se incluyen metricas de ejecucion
        """
        response = client.post("/api/run", json={
            "algorithm": "astar",
            "params": {
                "map": "test",
                "start": [0, 0],
                "goal": [9, 9]
            }
        })
        
        data = response.json()
        
        if data.get("status") == "success":
            # Debe tener tiempo de ejecucion
            assert "execution_time" in data
            assert isinstance(data["execution_time"], (int, float))
            assert data["execution_time"] >= 0
    
    def test_run_with_empty_params(self, client):
        """
        Test: Ejecutar con parametros vacios debe funcionar (usar defaults)
        """
        response = client.post("/api/run", json={
            "algorithm": "bfs",
            "params": {}
        })
        
        # Debe responder, aunque sea con stub
        assert response.status_code == 200
        data = response.json()
        assert "algorithm" in data
    
    def test_run_invalid_json(self, client):
        """
        Test: Enviar JSON invalido debe retornar error
        """
        response = client.post("/api/run", 
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        # Debe ser error 4xx
        assert response.status_code >= 400


class TestRunEndpointValidation:
    """Tests para validacion de entrada del endpoint /api/run"""
    
    def test_run_missing_algorithm_field(self, client):
        """
        Test: Request sin campo 'algorithm' debe fallar
        """
        response = client.post("/api/run", json={
            "params": {"map": "test"}
        })
        
        assert response.status_code >= 400
    
    def test_run_algorithm_none(self, client):
        """
        Test: Campo 'algorithm' con valor None debe fallar
        """
        response = client.post("/api/run", json={
            "algorithm": None,
            "params": {}
        })
        
        assert response.status_code >= 400 or response.json().get("error")
    
    def test_run_algorithm_empty_string(self, client):
        """
        Test: Campo 'algorithm' vacio debe fallar
        """
        response = client.post("/api/run", json={
            "algorithm": "",
            "params": {}
        })
        
        data = response.json()
        assert response.status_code >= 400 or "error" in data
    
    def test_run_params_optional(self, client):
        """
        Test: El campo 'params' debe ser opcional
        """
        response = client.post("/api/run", json={
            "algorithm": "bfs"
        })
        
        # Debe funcionar sin params
        assert response.status_code == 200
        data = response.json()
        assert "algorithm" in data
