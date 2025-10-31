# 🔧 Guía Rápida de Modificaciones - BFS

## Archivo: `smart_backend/algorithms/bfs.py`

---

## 1️⃣ CAMBIAR ORDEN DE EXPANSIÓN DE VECINOS

### Ubicación: Línea ~51
```python
direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
```

### Opciones de Cambio:

**Opción A: Derecha → Abajo → Izquierda → Arriba**
```python
direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
```

**Opción B: Arriba → Derecha → Abajo → Izquierda (horario)**
```python
direcciones = [(-1, 0), (0, 1), (1, 0), (0, -1)]
```

**Opción C: Izquierda → Arriba → Derecha → Abajo**
```python
direcciones = [(0, -1), (-1, 0), (0, 1), (1, 0)]
```

### ⚠️ Efecto:
- Puede generar un camino DIFERENTE
- MISMA longitud (27 pasos)
- MISMO costo o muy similar

---

## 2️⃣ AGREGAR MOVIMIENTOS DIAGONALES

### Ubicación: Línea ~51
```python
# REEMPLAZAR:
direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# POR:
direcciones = [
    (-1, 0), (1, 0), (0, -1), (0, 1),  # Cardinales
    (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonales
]
```

### ⚠️ Efecto:
- Caminos más cortos posibles
- Mayor factor de ramificación (b=8 en lugar de 4)
- Más nodos expandidos
- Diferentes resultados

---

## 3️⃣ LIMITAR PROFUNDIDAD MÁXIMA

### Ubicación: Dentro del while, línea ~77
```python
while cola:
    (pos_actual, muestras_recolectadas, combustible), camino = cola.popleft()
    
    # AGREGAR ESTAS LÍNEAS:
    MAX_DEPTH = 50  # Ajustar según necesidad
    if len(camino) > MAX_DEPTH:
        continue  # No expandir este nodo
    
    # Verificar si estamos en una muestra...
```

### ⚠️ Efecto:
- Reduce nodos expandidos
- Puede NO encontrar solución si MAX_DEPTH < 27
- BFS se convierte en "BFS con límite de profundidad"

---

## 4️⃣ REQUERIR RETORNO A LA NAVE

### Ubicación: Condición de victoria, línea ~84
```python
# REEMPLAZAR:
if len(muestras_recolectadas) == 3:
    # Calcular costo del camino...

# POR:
# Primero, definir posición de la nave al inicio
nave_pos = None
for i in range(10):
    for j in range(10):
        if mapa[i][j] == 5:
            nave_pos = (i, j)
            break

# Luego, cambiar la condición:
if len(muestras_recolectadas) == 3 and pos_actual == nave_pos:
    # Calcular costo del camino...
```

### ⚠️ Efecto:
- Camino más largo
- Más nodos expandidos
- Solución más compleja

---

## 5️⃣ CAMBIAR CÁLCULO DE COSTO A UNIFORME

### Ubicación: Líneas ~100-110
```python
# REEMPLAZAR:
if combustible_actual > 0:
    costo_total += 0.5
    combustible_actual -= 1
else:
    if celda == 0 or celda == 2 or celda == 6:
        costo_total += 1
    elif celda == 3:
        costo_total += 3
    elif celda == 4:
        costo_total += 5
    elif celda == 5:
        costo_total += 1

# POR (costo uniforme = 1):
costo_total += 1
if celda == 5:
    combustible_actual = 20
elif combustible_actual > 0:
    combustible_actual -= 1
```

### ⚠️ Efecto:
- Costo total = número de movimientos (27)
- Más fácil de entender
- No refleja realidad del problema

---

## 6️⃣ PROHIBIR MOVIMIENTO SIN COMBUSTIBLE EN TERRENO PELIGROSO

### Ubicación: Al expandir vecinos, línea ~125
```python
# Expandir vecinos
for vecino in get_neighbors(pos_actual, mapa):
    # AGREGAR ESTA VALIDACIÓN:
    celda_vecino = mapa[vecino[0]][vecino[1]]
    if combustible == 0 and celda_vecino in [3, 4]:  # Rocoso o volcánico
        continue  # Saltar este vecino (no se puede sin fuel)
    
    # Calcular nuevo combustible...
```

### ⚠️ Efecto:
- Hace obligatorio pasar por la nave
- Camino más largo
- Más realista según algunas interpretaciones

---

## 7️⃣ AGREGAR CONTADOR DE ITERACIONES

### Ubicación: Al inicio del while, línea ~76
```python
# AGREGAR AL INICIO:
iteraciones = 0
MAX_ITERACIONES = 10000

while cola:
    iteraciones += 1
    
    # AGREGAR VERIFICACIÓN:
    if iteraciones > MAX_ITERACIONES:
        return {
            "path": [],
            "nodes_expanded": nodos_expandidos,
            "cost": 0,
            "max_depth": max_profundidad,
            "message": f"Límite de iteraciones alcanzado ({MAX_ITERACIONES})"
        }
    
    (pos_actual, muestras_recolectadas, combustible), camino = cola.popleft()
```

### ⚠️ Efecto:
- Evita bucles infinitos en casos extremos
- Proporciona control sobre tiempo de ejecución

---

## 8️⃣ REGISTRAR ESTADÍSTICAS ADICIONALES

### Ubicación: Variables de seguimiento, línea ~73
```python
# AGREGAR:
nodos_expandidos = 0
max_profundidad = 0
nodos_generados = 0  # NUEVO
max_frontera = 0      # NUEVO

while cola:
    max_frontera = max(max_frontera, len(cola))  # NUEVO
    
    # ... código existente ...
    
    # Al agregar a la cola:
    cola.append((nuevo_estado, camino + [vecino]))
    nodos_generados += 1  # NUEVO

# Al retornar:
return {
    "path": camino_json,
    "nodes_expanded": nodos_expandidos,
    "nodes_generated": nodos_generados,  # NUEVO
    "max_frontier": max_frontera,         # NUEVO
    "cost": costo_total,
    "max_depth": max_profundidad,
    "message": "Solución encontrada - 3 muestras recolectadas"
}
```

### ⚠️ Efecto:
- Más información para análisis
- Útil para comparaciones
- No cambia el resultado

---

## 9️⃣ PRIORIZAR MUESTRAS CERCANAS (Heurística Simple)

### ⚠️ IMPORTANTE: Esto convierte BFS en "Best-First Search"

### Ubicación: Modificar cola a priority queue
```python
# AL INICIO DEL ARCHIVO:
from collections import deque
import heapq  # AGREGAR

# REEMPLAZAR cola deque por priority queue:
# cola = deque([(estado_inicial, [start])])
cola = []
heapq.heappush(cola, (0, estado_inicial, [start]))

# EN EL WHILE:
while cola:
    prioridad, (pos_actual, muestras_recolectadas, combustible), camino = heapq.heappop(cola)
    
    # ... código existente ...
    
    # AL AGREGAR A LA COLA:
    # Calcular distancia Manhattan a muestra más cercana no recolectada
    distancia_min = 999
    for muestra in muestras:
        if muestra not in muestras_recolectadas:
            dist = abs(vecino[0] - muestra[0]) + abs(vecino[1] - muestra[1])
            distancia_min = min(distancia_min, dist)
    
    heapq.heappush(cola, (distancia_min, nuevo_estado, camino + [vecino]))
```

### ⚠️ Efecto:
- Ya NO es BFS puro
- Explora primero nodos cercanos a muestras
- Menos nodos expandidos
- **PUEDE perder optimalidad**

---

## 🔟 MODO DEBUG: Imprimir Exploración

### Ubicación: Dentro del while
```python
while cola:
    (pos_actual, muestras_recolectadas, combustible), camino = cola.popleft()
    
    # AGREGAR PARA DEBUG:
    if nodos_expandidos % 100 == 0:  # Cada 100 nodos
        print(f"[DEBUG] Nodos expandidos: {nodos_expandidos}")
        print(f"        Posición actual: {pos_actual}")
        print(f"        Muestras: {len(muestras_recolectadas)}/3")
        print(f"        Combustible: {combustible}/20")
        print(f"        Frontera: {len(cola)} estados")
        print(f"        Profundidad: {len(camino)}")
    
    # ... resto del código ...
```

### ⚠️ Efecto:
- Permite ver progreso en tiempo real
- Útil para explicar el algoritmo
- Ralentiza ejecución

---

## 📋 CHECKLIST DE CAMBIOS RÁPIDOS

Antes de modificar, pregunta al profesor:

- [ ] ¿Qué aspecto debo cambiar exactamente?
- [ ] ¿Cambio afecta orden de expansión?
- [ ] ¿Cambio afecta condición de parada?
- [ ] ¿Cambio afecta cálculo de costo?
- [ ] ¿Debo mostrar más/menos información?

## 🎯 DESPUÉS DE MODIFICAR

1. **Guardar archivo**: Ctrl+S
2. **Reconstruir Docker**:
   ```bash
   docker-compose up -d --build smart_backend
   ```
3. **Probar**:
   ```bash
   python test_bfs.py
   ```
4. **Ver resultados en frontend**: http://localhost:5173

---

## 💡 TIPS PARA LA SUSTENTACIÓN

1. **Conoce cada línea**: Debes poder explicar cualquier parte
2. **Ten backup**: Guarda una copia del código original
3. **Practica modificaciones**: Usa `practica_sustentacion.py`
4. **Entiende el "por qué"**: No solo el "cómo"
5. **Prepara justificaciones**: Para cada decisión de diseño

---

## 🚨 ERRORES COMUNES A EVITAR

1. ❌ Modificar y no guardar
2. ❌ No reconstruir Docker después de cambios
3. ❌ Confundir índices (fila, columna) vs (x, y)
4. ❌ Romper la lógica de visitados
5. ❌ Olvidar actualizar combustible
6. ❌ No validar límites del mapa (0-9)

---

## 📞 CONTACTO DE EMERGENCIA

Si algo falla durante la sustentación:

1. **Reiniciar sistema**:
   ```bash
   docker-compose restart
   ```

2. **Ver logs**:
   ```bash
   docker-compose logs smart_backend
   ```

3. **Volver a código original**:
   ```bash
   git checkout smart_backend/algorithms/bfs.py
   docker-compose up -d --build smart_backend
   ```

---

**¡Éxito en tu sustentación! 🚀**
