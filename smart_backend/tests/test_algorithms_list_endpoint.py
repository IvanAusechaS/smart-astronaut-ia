"""
Test suite para el endpoint de listado de algoritmos
Prueba el endpoint GET /api/algorithms
"""

import pytest
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestAlgorithmsListEndpoint:
    """Tests para el endpoint GET /api/algorithms"""
    
    def test_algorithms_endpoint_exists(self, client):
        """
        Test: El endpoint /api/algorithms debe existir y responder
        """
        response = client.get("/api/algorithms")
        assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"
    
    def test_algorithms_returns_json(self, client):
        """
        Test: El endpoint debe retornar JSON valido
        """
        response = client.get("/api/algorithms")
        assert response.headers["content-type"] == "application/json"
        
        data = response.json()
        assert isinstance(data, dict), "La respuesta debe ser un diccionario"
    
    def test_algorithms_has_required_keys(self, client):
        """
        Test: La respuesta debe contener las claves esperadas
        """
        response = client.get("/api/algorithms")
        data = response.json()
        
        assert "algorithms" in data, "La respuesta debe contener la clave 'algorithms'"
        assert isinstance(data["algorithms"], list), "'algorithms' debe ser una lista"
    
    def test_algorithms_contains_expected_algorithms(self, client):
        """
        Test: La lista debe contener los algoritmos esperados
        """
        response = client.get("/api/algorithms")
        data = response.json()
        
        algorithms = data["algorithms"]
        algorithm_names = [algo["name"] for algo in algorithms]
        expected_algorithms = ["bfs", "dfs", "uniform_cost", "greedy", "astar"]
        
        for algo in expected_algorithms:
            assert algo in algorithm_names, f"Se esperaba encontrar el algoritmo '{algo}'"
    
    def test_algorithms_count(self, client):
        """
        Test: Verificar que se retorna el conteo de algoritmos
        """
        response = client.get("/api/algorithms")
        data = response.json()
        
        if "count" in data:
            assert isinstance(data["count"], int), "El conteo debe ser un entero"
            assert data["count"] == len(data["algorithms"]), "El conteo debe coincidir con la cantidad de algoritmos"
    
    def test_algorithms_details(self, client):
        """
        Test: Verificar que se retornan detalles de los algoritmos
        """
        response = client.get("/api/algorithms")
        data = response.json()
        
        if "details" in data:
            details = data["details"]
            assert isinstance(details, list), "Los detalles deben ser una lista"
            
            for detail in details:
                assert "name" in detail, "Cada detalle debe tener 'name'"
                assert "available" in detail, "Cada detalle debe tener 'available'"
                
                if "docstring" in detail:
                    assert isinstance(detail["docstring"], str), "docstring debe ser un string"
    
    def test_algorithms_all_available(self, client):
        """
        Test: Todos los algoritmos listados deben estar disponibles
        """
        response = client.get("/api/algorithms")
        data = response.json()
        
        if "details" in data:
            for detail in data["details"]:
                assert detail["available"] is True, f"Algoritmo {detail['name']} debe estar disponible"
    
    def test_algorithms_no_init_file(self, client):
        """
        Test: __init__.py no debe aparecer en la lista de algoritmos
        """
        response = client.get("/api/algorithms")
        data = response.json()
        
        algorithms = data["algorithms"]
        assert "__init__" not in algorithms, "__init__ no debe aparecer en la lista"
    
    def test_algorithms_response_structure(self, client):
        """
        Test: Verificar la estructura completa de la respuesta
        """
        response = client.get("/api/algorithms")
        data = response.json()
        
        # Estructura minima esperada
        assert "algorithms" in data
        assert isinstance(data["algorithms"], list)
        assert len(data["algorithms"]) > 0, "Debe haber al menos un algoritmo"
        
        # Cada algoritmo debe ser un dict con name, display_name, description, available
        for algo in data["algorithms"]:
            assert isinstance(algo, dict), f"Algoritmo debe ser dict, se obtuvo {type(algo)}"
            assert "name" in algo, "Algoritmo debe tener campo 'name'"
            assert "display_name" in algo, "Algoritmo debe tener campo 'display_name'"
            assert "description" in algo, "Algoritmo debe tener campo 'description'"
            assert "available" in algo, "Algoritmo debe tener campo 'available'"
            assert isinstance(algo["name"], str), "Campo 'name' debe ser string"
            assert len(algo["name"]) > 0, "Nombre de algoritmo no puede estar vacio"

class TestAlgorithmDetailsEndpoint:
    """Tests para el endpoint GET /api/algorithm/{name}"""
    
    def test_get_algorithm_details_bfs(self, client):
        """
        Test: Obtener detalles de un algoritmo especifico (BFS)
        """
        response = client.get("/api/algorithm/bfs")
        
        if response.status_code == 200:
            data = response.json()
            assert "name" in data
            assert data["name"] == "bfs"
            assert "available" in data
    
    def test_get_nonexistent_algorithm(self, client):
        """
        Test: Intentar obtener un algoritmo inexistente debe retornar 404
        """
        response = client.get("/api/algorithm/nonexistent_algo")
        assert response.status_code == 404
    
    def test_get_algorithm_details_all_available(self, client):
        """
        Test: Verificar detalles de todos los algoritmos disponibles
        """
        # Primero obtener la lista
        list_response = client.get("/api/algorithms")
        algorithms = list_response.json()["algorithms"]
        
        # Verificar cada uno
        for algo in algorithms:
            algo_name = algo["name"] if isinstance(algo, dict) else algo
            response = client.get(f"/api/algorithm/{algo_name}")
            assert response.status_code == 200, f"Algoritmo {algo_name} debe estar disponible"
            
            data = response.json()
            assert data["name"] == algo_name
            assert data["available"] is True
