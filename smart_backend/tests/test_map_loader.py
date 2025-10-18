"""
Test suite para el modulo map_loader
Prueba la carga y validacion de mapas para el Smart Astronaut
"""

import pytest
import io
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.map_loader import load_map, validate_map


class TestLoadMap:
    """Tests para la funcion load_map"""
    
    def test_load_valid_map_from_string(self, valid_map_10x10):
        """
        Test: Cargar un mapa valido desde un string
        Verifica que se parsea correctamente y retorna una matriz 10x10
        """
        result = load_map(valid_map_10x10)
        
        assert isinstance(result, list), "El resultado debe ser una lista"
        assert len(result) == 10, f"El mapa debe tener 10 filas, tiene {len(result)}"
        
        for i, row in enumerate(result):
            assert isinstance(row, list), f"Fila {i} debe ser una lista"
            assert len(row) == 10, f"Fila {i} debe tener 10 columnas, tiene {len(row)}"
            assert all(isinstance(cell, int) for cell in row), f"Fila {i} debe contener solo enteros"
    
    def test_load_map_from_stringio(self, valid_map_10x10):
        """
        Test: Cargar un mapa desde un objeto StringIO
        Verifica que funciona con streams de texto en memoria
        """
        map_stream = io.StringIO(valid_map_10x10)
        result = load_map(map_stream)
        
        assert len(result) == 10
        assert all(len(row) == 10 for row in result)
    
    def test_load_map_correct_values(self):
        """
        Test: Verificar que los valores se parsean correctamente
        """
        simple_map = """0 1 2 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0"""
        
        result = load_map(simple_map)
        
        assert result[0][0] == 0
        assert result[0][1] == 1
        assert result[0][2] == 2
        assert result[0][3] == 3
    
    def test_load_map_with_extra_whitespace(self):
        """
        Test: Mapa con espacios extra debe procesarse correctamente
        """
        map_with_spaces = """0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0"""
        
        result = load_map(map_with_spaces)
        assert len(result) == 10
        assert all(len(row) == 10 for row in result)
    
    def test_load_map_wrong_number_of_rows(self, invalid_map_wrong_rows):
        """
        Test: Mapa con numero incorrecto de filas debe levantar ValueError
        """
        with pytest.raises(ValueError) as exc_info:
            load_map(invalid_map_wrong_rows)
        
        assert "debe tener exactamente 10 filas" in str(exc_info.value)
    
    def test_load_map_inconsistent_columns(self, invalid_map_wrong_cols):
        """
        Test: Mapa con filas de diferente longitud debe levantar ValueError
        """
        with pytest.raises(ValueError) as exc_info:
            load_map(invalid_map_wrong_cols)
        
        assert "debe tener exactamente 10 celdas" in str(exc_info.value)
    
    def test_load_map_non_numeric_characters(self, invalid_map_non_numeric):
        """
        Test: Mapa con caracteres no numericos debe levantar ValueError
        """
        with pytest.raises(ValueError) as exc_info:
            load_map(invalid_map_non_numeric)
        
        assert "caracteres no numericos" in str(exc_info.value).lower()
    
    def test_load_empty_map(self):
        """
        Test: Mapa vacio debe levantar ValueError
        """
        with pytest.raises(ValueError):
            load_map("")
    
    def test_load_map_too_many_rows(self):
        """
        Test: Mapa con mas de 10 filas debe levantar ValueError
        """
        map_11_rows = "\n".join(["0 0 0 0 0 0 0 0 0 0"] * 11)
        
        with pytest.raises(ValueError) as exc_info:
            load_map(map_11_rows)
        
        assert "10 filas" in str(exc_info.value)


class TestValidateMap:
    """Tests para la funcion validate_map"""
    
    def test_validate_correct_map(self, valid_map_10x10):
        """
        Test: Mapa valido debe pasar la validacion
        """
        grid = load_map(valid_map_10x10)
        assert validate_map(grid) is True
    
    def test_validate_empty_map(self):
        """
        Test: Mapa vacio debe fallar validacion
        """
        with pytest.raises(ValueError) as exc_info:
            validate_map([])
        
        assert "vacio" in str(exc_info.value).lower()
    
    def test_validate_wrong_rows(self):
        """
        Test: Mapa con numero incorrecto de filas debe fallar
        """
        invalid_grid = [[0] * 10 for _ in range(5)]
        
        with pytest.raises(ValueError) as exc_info:
            validate_map(invalid_grid)
        
        assert "10 filas" in str(exc_info.value)
    
    def test_validate_wrong_columns(self):
        """
        Test: Mapa con numero incorrecto de columnas debe fallar
        """
        invalid_grid = [[0] * 8 for _ in range(10)]
        
        with pytest.raises(ValueError) as exc_info:
            validate_map(invalid_grid)
        
        assert "10 celdas" in str(exc_info.value)
    
    def test_validate_non_integer_values(self):
        """
        Test: Mapa con valores no enteros debe fallar
        """
        invalid_grid = [["0"] * 10 for _ in range(10)]  # Strings en lugar de ints
        
        with pytest.raises(ValueError) as exc_info:
            validate_map(invalid_grid)
        
        assert "no enteros" in str(exc_info.value).lower()
