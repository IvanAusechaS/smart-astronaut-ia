"""
Fixtures compartidas para los tests del proyecto SmartAstronaut
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


@pytest.fixture
def client():
    """
    Fixture que proporciona un TestClient de FastAPI
    para hacer peticiones HTTP a la aplicacion
    """
    return TestClient(app)


@pytest.fixture
def small_map_text():
    """
    Fixture que proporciona un mapa valido pequeno (10x10)
    para usar en las pruebas
    """
    return """0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0"""


@pytest.fixture
def valid_map_10x10():
    """
    Fixture que proporciona un mapa valido 10x10 completo
    Valores: 0=libre, 1=obstaculo, 2=rocoso, 3=volcanico
    """
    return """0 0 0 1 0 0 0 0 2 0
0 0 0 1 0 0 0 0 2 0
0 0 0 0 0 0 0 0 2 0
1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0"""


@pytest.fixture
def small_map_3x3():
    """
    Fixture que proporciona un mapa pequeno 3x3
    para pruebas rapidas (aunque no sea valido para el sistema real)
    """
    return """0 0 0
0 1 0
0 0 0"""


@pytest.fixture
def invalid_map_wrong_rows():
    """
    Fixture con un mapa invalido (menos de 10 filas)
    """
    return """0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0"""


@pytest.fixture
def invalid_map_wrong_cols():
    """
    Fixture con un mapa invalido (columnas inconsistentes)
    """
    return """0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0"""


@pytest.fixture
def invalid_map_non_numeric():
    """
    Fixture con un mapa invalido (caracteres no numericos)
    """
    return """0 0 0 0 0 0 0 0 0 0
0 X X 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0"""
