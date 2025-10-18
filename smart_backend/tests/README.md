# Test Suite - SmartAstronaut Backend

Suite completa de pruebas unitarias para el backend del proyecto SmartAstronaut.

## Estructura de Tests

```
tests/
├── __init__.py           # Inicializacion del paquete de tests
├── conftest.py           # Fixtures compartidas
├── test_map_loader.py    # Tests del cargador de mapas
├── test_algorithms_list_endpoint.py  # Tests del endpoint de listado
└── test_run_endpoint_stub.py        # Tests del endpoint de ejecucion
```

## Fixtures Disponibles

### `client`
Cliente de pruebas de FastAPI para hacer peticiones HTTP.

```python
def test_example(client):
    response = client.get("/api/algorithms")
    assert response.status_code == 200
```

### `valid_map_10x10`
Mapa valido de 10x10 para pruebas.

### `small_map_text`
Mapa pequeno valido para pruebas rapidas.

### `invalid_map_*`
Varios mapas invalidos para probar validacion.

## Ejecutar Tests

### Todos los tests
```bash
pytest
```

### Tests especificos
```bash
pytest tests/test_map_loader.py
pytest tests/test_algorithms_list_endpoint.py
pytest tests/test_run_endpoint_stub.py
```

### Con cobertura
```bash
pytest --cov=. --cov-report=html
```

### Tests por marcador
```bash
pytest -m unit
pytest -m api
```

### Modo verbose
```bash
pytest -v
```

### Ver prints
```bash
pytest -s
```

## En Docker

### Ejecutar tests en el contenedor
```bash
docker-compose exec smart_backend pytest
```

### Con cobertura
```bash
docker-compose exec smart_backend pytest --cov=. --cov-report=term-missing
```

### Ejecutar test especifico
```bash
docker-compose exec smart_backend pytest tests/test_map_loader.py -v
```

## Tests Implementados

### test_map_loader.py (16 tests)
- ✅ Carga de mapas validos desde string
- ✅ Carga desde StringIO
- ✅ Validacion de valores correctos
- ✅ Manejo de espacios extra
- ✅ Validacion de numero de filas
- ✅ Validacion de columnas inconsistentes
- ✅ Deteccion de caracteres no numericos
- ✅ Manejo de mapas vacios
- ✅ Validacion de estructura completa

### test_algorithms_list_endpoint.py (11 tests)
- ✅ Endpoint existe y responde
- ✅ Retorna JSON valido
- ✅ Contiene claves requeridas
- ✅ Lista algoritmos esperados (bfs, dfs, uniform_cost, greedy, astar)
- ✅ Retorna conteo correcto
- ✅ Incluye detalles de algoritmos
- ✅ Todos los algoritmos disponibles
- ✅ Excluye __init__.py
- ✅ Estructura de respuesta correcta
- ✅ Detalles de algoritmo especifico
- ✅ Manejo de algoritmo inexistente

### test_run_endpoint_stub.py (17 tests)
- ✅ Endpoint existe
- ✅ Error con algoritmo inexistente
- ✅ Error sin especificar algoritmo
- ✅ Ejecucion basica de BFS stub
- ✅ Estructura de respuesta
- ✅ Ejecucion con mapa pequeno
- ✅ Ejecucion de todos los algoritmos
- ✅ Campos esperados en resultado
- ✅ Path es una lista
- ✅ Incluye metricas de ejecucion
- ✅ Manejo de parametros vacios
- ✅ Manejo de JSON invalido
- ✅ Validacion de campo algorithm
- ✅ Manejo de valores None
- ✅ Manejo de strings vacios
- ✅ Parametros opcionales

## Cobertura Esperada

- `core/map_loader.py`: ~95%
- `app.py`: ~80%
- `core/executor.py`: ~75%
- `algorithms/*.py`: No se testea implementacion interna (stubs)

## Agregar Nuevos Tests

1. Crear archivo `test_*.py` en el directorio `tests/`
2. Importar fixtures desde `conftest.py`
3. Crear clases `Test*` con metodos `test_*`
4. Usar aserciones claras y mensajes descriptivos

Ejemplo:
```python
import pytest

class TestNewFeature:
    def test_feature_works(self, client):
        """Test: Nueva caracteristica funciona correctamente"""
        response = client.get("/new-endpoint")
        assert response.status_code == 200
```

## Notas

- Los tests usan stubs de algoritmos (no implementacion real)
- Se usa monkeypatch cuando es necesario mockear
- Todos los tests son independientes y pueden ejecutarse en paralelo
- Los mapas de prueba se crean en memoria (no archivos)

## Continua Integracion

Estos tests estan listos para integrarse en un pipeline de CI/CD:

```yaml
# Ejemplo para GitHub Actions
- name: Run tests
  run: |
    cd smart_backend
    pytest --cov=. --cov-report=xml
```

## Troubleshooting

### Imports no resueltos
Asegurarse de que pytest se ejecuta desde el directorio `smart_backend/`.

### Tests fallan en Docker
Verificar que el contenedor tiene pytest instalado:
```bash
docker-compose exec smart_backend pip install -r requirements.txt
```

### Cobertura baja
Agregar mas tests o marcar codigo como no testeable con `# pragma: no cover`.
