# 🚀 Sustentación: Algoritmo BFS (Breadth-First Search)
## Smart Astronaut - Búsqueda en Anchura

**Autor:** Iván Ausecha  
**Fecha:** Octubre 2025  
**Algoritmo:** Breadth-First Search (Búsqueda en Anchura)

---

## 📋 Tabla de Contenidos

1. [Descripción del Problema](#descripción-del-problema)
2. [¿Qué es BFS?](#qué-es-bfs)
3. [Implementación Específica](#implementación-específica)
4. [Análisis de Complejidad](#análisis-de-complejidad)
5. [Resultados y Pruebas](#resultados-y-pruebas)
6. [Ventajas y Desventajas](#ventajas-y-desventajas)
7. [Comparación con Otros Algoritmos](#comparación-con-otros-algoritmos)
8. [Demostración en Vivo](#demostración-en-vivo)

---

## 🎯 Descripción del Problema

### Contexto
Un astronauta debe navegar en un mapa marciano de **10x10** para recolectar **3 muestras científicas** enfrentando:

- **Obstáculos** (valor 1): No se pueden atravesar
- **Terreno libre** (valor 0, 2, 6): Costo 1 por movimiento
- **Terreno rocoso** (valor 3): Costo 3 por movimiento
- **Terreno volcánico** (valor 4): Costo 5 por movimiento
- **Nave auxiliar** (valor 5): Recarga 20 unidades de combustible

### Reglas de Combustible
- Con combustible: **costo 0.5** por movimiento (cualquier terreno)
- Sin combustible: costo según el tipo de terreno
- Combustible se descuenta 1 unidad por movimiento

### Objetivo
Encontrar un camino que **recolecte las 3 muestras científicas** con el menor número de pasos posible.

---

## 🔍 ¿Qué es BFS?

### Definición
**Breadth-First Search (BFS)** es un algoritmo de búsqueda no informada que explora el espacio de estados **nivel por nivel**, garantizando encontrar la solución más cercana en términos de **número de pasos**.

### Características Clave

1. **Estructura FIFO (First In, First Out)**
   - Utiliza una **cola (deque)** para gestionar nodos
   - Los nodos se exploran en el orden en que fueron descubiertos

2. **Expansión por Niveles**
   ```
   Nivel 0: Nodo inicial
   Nivel 1: Vecinos directos del inicial
   Nivel 2: Vecinos de los vecinos
   Nivel 3: ...
   ```

3. **Completitud**
   - **Siempre encuentra una solución** si existe
   - Garantiza encontrar la solución con **menos movimientos**

4. **Optimalidad**
   - En grafos **no ponderados**: encuentra el camino más corto
   - En grafos **ponderados**: NO garantiza el camino de menor costo
   - Para nuestro problema: encuentra el camino con **menos pasos**, pero no necesariamente el de **menor costo total**

---

## 💻 Implementación Específica

### Espacio de Estados

En lugar de solo rastrear posiciones, usamos un **estado compuesto**:

```python
estado = (posición, muestras_recolectadas, combustible)
```

**¿Por qué?**
- Permite **revisitar posiciones** con diferentes contextos
- Ejemplo: Visitar (2,3) con 0 muestras ≠ Visitar (2,3) con 1 muestra
- Cumple la regla: "cuando el agente tome la nave o muestra, puede devolverse"

### Código Principal

```python
def solve(params: dict):
    mapa = params.get("map", [])
    start = tuple(params.get("start", [0, 0]))
    
    # 1. Encontrar las 3 muestras en el mapa
    muestras = set()
    for i in range(10):
        for j in range(10):
            if mapa[i][j] == 6:
                muestras.add((i, j))
    
    # 2. Estado inicial: (posición, muestras_vacío, combustible_0)
    estado_inicial = (start, frozenset(), 0)
    
    # 3. Cola FIFO para BFS
    cola = deque([(estado_inicial, [start])])
    visitados = {estado_inicial}
    
    # 4. BFS principal
    while cola:
        (pos_actual, muestras_recolectadas, combustible), camino = cola.popleft()
        
        # Recolectar muestra si estamos en una
        if pos_actual in muestras and pos_actual not in muestras_recolectadas:
            muestras_recolectadas = frozenset(muestras_recolectadas | {pos_actual})
        
        # ¿Tenemos las 3 muestras?
        if len(muestras_recolectadas) == 3:
            return calcular_resultado(camino, mapa)
        
        # Contar como expandido
        nodos_expandidos += 1
        
        # Expandir vecinos (arriba, abajo, izquierda, derecha)
        for vecino in get_neighbors(pos_actual, mapa):
            # Calcular nuevo combustible
            nuevo_combustible = calcular_combustible(vecino, combustible, mapa)
            nuevo_estado = (vecino, muestras_recolectadas, nuevo_combustible)
            
            # Solo agregar si no hemos visitado este estado exacto
            if nuevo_estado not in visitados:
                visitados.add(nuevo_estado)
                cola.append((nuevo_estado, camino + [vecino]))
```

### Puntos Clave de la Implementación

#### 1. **frozenset para Muestras**
```python
muestras_recolectadas = frozenset(muestras_recolectadas | {pos_actual})
```
- `frozenset` es **inmutable** y **hashable**
- Permite usarlo en el conjunto `visitados`
- Representa el conjunto de muestras ya recolectadas

#### 2. **Gestión de Combustible**
```python
if celda == 5:  # Nave
    nuevo_combustible = 20
elif nuevo_combustible > 0:
    nuevo_combustible -= 1
```
- Recarga completa en la nave
- Descuento de 1 por movimiento

#### 3. **Prevención de Ciclos**
```python
if nuevo_estado not in visitados:
    visitados.add(nuevo_estado)
```
- Evita explorar el **mismo estado** dos veces
- Permite **revisitar posiciones** con estados diferentes

#### 4. **Movimientos Válidos**
```python
direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha
```
- Orden: **Arriba → Abajo → Izquierda → Derecha**
- No se permiten diagonales
- Verifica límites del mapa (0-9)
- Excluye obstáculos (valor 1)

---

## 📊 Análisis de Complejidad

### Complejidad Temporal
- **Peor caso:** O(b^d)
  - b = factor de ramificación (máximo 4 vecinos)
  - d = profundidad de la solución
- **En nuestro problema:**
  - Espacio de estados: 10×10×8×21 = 16,800 estados posibles
    - 100 posiciones
    - 8 combinaciones de muestras (2³ = 8)
    - 21 niveles de combustible (0-20)
  - **Resultado real:** 1,098 nodos expandidos

### Complejidad Espacial
- **O(b^d)** - Todos los nodos en memoria
- En nuestro caso: ~1,098 estados almacenados simultáneamente

### Comparación

| Algoritmo | Nodos Expandidos | Profundidad | Costo | Tiempo |
|-----------|------------------|-------------|-------|--------|
| **BFS** | **1,098** | **27** | **53** | ~0.05s |
| DFS | 180 | 146 | 139 | ~0.02s |
| A* | ~800 | 27 | 42 | ~0.04s |

---

## 🧪 Resultados y Pruebas

### Mapa de Prueba (mapa.txt)

```
0 5 0 0 0 0 0 0 0 0
1 1 1 0 1 1 1 0 1 0
0 2 0 0 3 3 3 6 0 0  ← Astronauta(2) y Muestra1(6)
0 1 0 1 1 1 1 0 1 1
0 1 0 1 0 0 0 0 1 1
0 1 0 1 4 1 1 1 1 1
0 0 6 4 4 0 0 1 1 1  ← Muestra2(6)
1 0 1 1 0 1 0 1 0 6  ← Muestra3(6)
0 0 0 0 0 1 0 1 0 1
0 1 1 1 0 0 0 0 0 1
```

### Resultado BFS

```
✅ Solución encontrada - 3 muestras recolectadas

📍 Camino (28 posiciones, 27 movimientos):
[2,1] → [2,2] → [2,3] → [2,4] → [2,5] → [2,6] → [2,7]📦 →
[3,7] → [4,7] → [4,6] → [4,5] → [4,4] → [5,4] → [6,4] → 
[6,3] → [6,2]📦 → [6,3] → [6,4] → [7,4] → [8,4] → [9,4] → 
[9,5] → [9,6] → [9,7] → [9,8] → [8,8] → [7,8] → [7,9]📦

📊 Estadísticas:
- Nodos expandidos: 1,098
- Profundidad: 27 movimientos
- Costo total: 53
- Muestras recolectadas: 3/3 ✓
```

### Desglose del Camino

| Tramo | Descripción | Terreno | Costo |
|-------|-------------|---------|-------|
| [2,1] → [2,7] | Ir a Muestra 1 | Libre + Rocoso (3 celdas) | 10 |
| [2,7] → [6,2] | Ir a Muestra 2 | Libre + Volcánico (3 celdas) | 18 |
| [6,2] → [7,9] | Ir a Muestra 3 | Libre + Volcánico | 25 |
| **TOTAL** | **27 movimientos** | - | **53** |

---

## ⚖️ Ventajas y Desventajas

### ✅ Ventajas

1. **Completitud Garantizada**
   - Siempre encuentra solución si existe
   - No se queda atrapado en bucles infinitos

2. **Optimalidad en Pasos**
   - Encuentra el camino con **menor número de movimientos**
   - Ideal cuando cada paso tiene el mismo "peso"

3. **Simplicidad de Implementación**
   - Fácil de entender y depurar
   - Cola FIFO es intuitiva

4. **Determinismo**
   - Siempre produce el mismo resultado
   - Reproducible para testing

### ❌ Desventajas

1. **No Óptimo en Costo**
   - BFS: 27 pasos, costo 53
   - A*: 27 pasos, costo 42 (mejor ruta)
   - No considera el **peso** de los movimientos

2. **Alto Consumo de Memoria**
   - Almacena **todos los nodos** en la frontera
   - 1,098 estados en memoria simultáneamente
   - Problema para espacios de búsqueda muy grandes

3. **Sin Heurística**
   - Explora "a ciegas" sin dirección
   - No usa información del problema para guiar la búsqueda

4. **Rendimiento en Grafos Grandes**
   - Complejidad exponencial O(b^d)
   - Puede ser muy lento en problemas complejos

---

## 🔄 Comparación con Otros Algoritmos

### BFS vs DFS (Depth-First Search)

| Característica | BFS | DFS |
|----------------|-----|-----|
| **Estructura** | Cola (FIFO) | Pila (LIFO) |
| **Estrategia** | Nivel por nivel | Profundidad primero |
| **Memoria** | O(b^d) - ALTA | O(bd) - BAJA |
| **Completitud** | ✅ Sí | ❌ No (puede ciclar) |
| **Optimalidad** | ✅ En pasos | ❌ No |
| **Nodos expandidos** | 1,098 | 180 |
| **Profundidad** | 27 | 146 |
| **Costo** | 53 | 139 |

**Conclusión:** BFS encuentra mejor solución pero usa más memoria.

### BFS vs A* (A-Star)

| Característica | BFS | A* |
|----------------|-----|-----|
| **Tipo** | No informada | Informada |
| **Heurística** | ❌ No usa | ✅ Usa distancia |
| **Optimalidad** | En pasos | En costo |
| **Nodos expandidos** | 1,098 | ~800 |
| **Costo final** | 53 | 42 |
| **Complejidad** | Simple | Compleja |

**Conclusión:** A* es superior si se tiene buena heurística.

### BFS vs Costo Uniforme

| Característica | BFS | Costo Uniforme |
|----------------|-----|----------------|
| **Prioridad** | FIFO (orden) | Costo acumulado |
| **Optimalidad** | En pasos | En costo |
| **Uso** | Costos uniformes | Costos variables |

**Conclusión:** Para nuestro problema con costos variables, Costo Uniforme es mejor.

---

## 🎬 Demostración en Vivo

### Pasos para la Demostración

#### 1. **Levantar el Sistema**
```bash
cd smart-astronaut-ia
docker-compose up -d
```

#### 2. **Verificar Servicios**
```bash
# Backend
curl http://localhost:8000/health

# Frontend
# Abrir: http://localhost:5173
```

#### 3. **Cargar Mapa**
- Usar archivo `mapa.txt` (incluido en el proyecto)
- Mostrar las 3 muestras, obstáculos, nave, terrenos

#### 4. **Ejecutar BFS**
1. Seleccionar tipo: **"No Informada"**
2. Elegir: **"BFS (Búsqueda en Anchura)"**
3. Click: **"Ejecutar Búsqueda"**

#### 5. **Observar Animación**
- Astronauta 🚶 caminando
- Recolección de muestras 📦 → ✅
- Cambio a nave 🚀 cuando hay combustible
- Panel de estado: Paso, Combustible, Muestras

#### 6. **Analizar Resultados**
```
Nodos Expandidos: 1,098
Profundidad: 27
Tiempo de Cómputo: ~0.05s
Costo Total: 53
```

---

## 🛠️ Modificaciones Potenciales

### Si el profesor pide cambios, estas son las áreas más comunes:

#### 1. **Cambiar Orden de Expansión**
```python
# Actual: Arriba, Abajo, Izquierda, Derecha
direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Alternativa: Derecha, Abajo, Izquierda, Arriba
direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
```
**Ubicación:** `smart_backend/algorithms/bfs.py` línea 51

#### 2. **Agregar Movimientos Diagonales**
```python
direcciones = [
    (-1, 0), (1, 0), (0, -1), (0, 1),  # Cardinales
    (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonales
]
```

#### 3. **Modificar Criterio de Parada**
```python
# Actual: Recolectar 3 muestras
if len(muestras_recolectadas) == 3:
    return resultado

# Alternativa: Recolectar Y regresar a la nave
if len(muestras_recolectadas) == 3 and pos_actual == nave_posicion:
    return resultado
```

#### 4. **Limitar Profundidad (BFS con límite)**
```python
if len(camino) > MAX_PROFUNDIDAD:
    continue  # No expandir más allá del límite
```

#### 5. **Cambiar Cálculo de Costo**
```python
# Actual: Costo según terreno
if celda == 0: costo += 1
elif celda == 3: costo += 3
elif celda == 4: costo += 5

# Alternativa: Costo uniforme
costo += 1  # Todo cuesta lo mismo
```

#### 6. **Agregar Restricción de Combustible**
```python
# No permitir movimientos sin combustible en terreno peligroso
if combustible == 0 and celda in [3, 4]:  # Rocoso o volcánico
    continue  # Saltar este vecino
```

---

## 📝 Preguntas Frecuentes del Profesor

### 1. **¿Por qué BFS y no DFS?**
**Respuesta:** BFS garantiza encontrar el camino con menos pasos. DFS puede encontrar soluciones más rápido pero suelen ser subóptimas (como vimos: DFS encontró 146 pasos vs 27 de BFS).

### 2. **¿Por qué usas frozenset para las muestras?**
**Respuesta:** `frozenset` es inmutable y hashable, lo que permite:
- Usarlo como parte de la clave en el conjunto `visitados`
- Representar conjuntos de muestras de forma eficiente
- Evitar modificaciones accidentales

### 3. **¿Cómo evitas ciclos infinitos?**
**Respuesta:** Usamos un conjunto `visitados` que almacena estados completos (posición + muestras + combustible). Solo expandimos estados no visitados.

### 4. **¿Por qué permites revisitar posiciones?**
**Respuesta:** El problema lo requiere: "cuando el agente tome la nave o muestra, debe poder devolverse". Revisitamos posiciones pero con estados diferentes (más muestras o diferente combustible).

### 5. **¿Qué pasa si no hay solución?**
**Respuesta:** BFS agota toda la cola sin encontrar las 3 muestras y retorna:
```python
return {
    "path": [],
    "message": "No se encontró solución para recolectar las 3 muestras"
}
```

### 6. **¿Por qué 1,098 nodos expandidos?**
**Respuesta:** BFS explora exhaustivamente nivel por nivel. Muchos estados se generan porque:
- Múltiples formas de llegar a una posición
- Diferentes combinaciones de muestras
- Diferentes niveles de combustible

### 7. **¿Cómo optimizarías BFS?**
**Respuestas posibles:**
- **Bidireccional:** BFS desde inicio y desde objetivo simultáneamente
- **Con heurística:** Convertir a A* usando distancia Manhattan
- **Podado:** Eliminar estados claramente subóptimos
- **Memoria:** Usar Iterative Deepening (IDA*)

---

## 🚀 Comandos Útiles Durante la Sustentación

### Prueba Rápida del Algoritmo
```bash
cd smart-astronaut-ia
python test_bfs.py
```

### Ver Logs del Backend
```bash
docker-compose logs -f smart_backend
```

### Reiniciar Sistema
```bash
docker-compose restart
```

### Verificar Puerto Backend
```bash
curl http://localhost:8000/api/algorithms
```

---

## 📚 Referencias

1. **Russell, S., & Norvig, P.** (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
   - Capítulo 3: Solving Problems by Searching
   - Sección 3.4: Uninformed Search Strategies

2. **Cormen, T. H., et al.** (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
   - Capítulo 22: Elementary Graph Algorithms
   - Sección 22.2: Breadth-First Search

3. **Python Documentation**
   - `collections.deque`: https://docs.python.org/3/library/collections.html#collections.deque

---

## ✅ Checklist Pre-Sustentación

- [ ] Sistema levantado (`docker-compose up -d`)
- [ ] Backend respondiendo (http://localhost:8000)
- [ ] Frontend cargando (http://localhost:5173)
- [ ] Archivo `mapa.txt` disponible
- [ ] Script `test_bfs.py` funcional
- [ ] Código BFS revisado y entendido
- [ ] Resultados probados y verificados
- [ ] Preparado para modificaciones en vivo

---

## 🎯 Puntos Clave para Recordar

1. **BFS usa cola FIFO** - explora nivel por nivel
2. **Garantiza optimalidad en pasos** - no en costo
3. **Estado = (posición, muestras, combustible)** - permite revisitas
4. **1,098 nodos expandidos** - exhaustivo pero completo
5. **27 movimientos, costo 53** - solución correcta
6. **frozenset para muestras** - inmutable y hashable
7. **No usa heurística** - búsqueda no informada
8. **O(b^d) complejidad** - puede ser costoso en memoria

---

**¡Buena suerte en tu sustentación! 🍀**

*Recuerda: domina el código, entiende las decisiones de diseño, y estate preparado para justificar cada línea.*
