"""
Depth-First Search (DFS) Algorithm
Búsqueda en profundidad evitando ciclos para recolectar las 3 muestras científicas
"""

def solve(params: dict):
    """
    Ejecuta el algoritmo DFS para encontrar un camino que recolecte las 3 muestras.
    Utiliza una pila (LIFO) para explorar en profundidad primero.
    
    Args:
        params: Diccionario con parámetros del problema
               - map: Matriz 10x10 con valores 0-6
               - start: Tupla (fila, columna) del inicio
               - goal: NO SE USA, el objetivo es recolectar las 3 muestras (valor 6)
    
    Returns:
        dict: Resultado con el camino encontrado y estadísticas
    """
    mapa = params.get("map", [])
    start = tuple(params.get("start", [0, 0]))
    
    # Validaciones básicas
    if not mapa or len(mapa) != 10 or len(mapa[0]) != 10:
        return {
            "path": [],
            "nodes_expanded": 0,
            "cost": 0,
            "max_depth": 0,
            "message": "Mapa inválido"
        }
    
    # Encontrar todas las muestras (valor 6)
    muestras = set()
    for i in range(10):
        for j in range(10):
            if mapa[i][j] == 6:
                muestras.add((i, j))
    
    if len(muestras) != 3:
        return {
            "path": [],
            "nodes_expanded": 0,
            "cost": 0,
            "max_depth": 0,
            "message": f"Error: Se esperan 3 muestras, se encontraron {len(muestras)}"
        }
    
    # Obtener orden de operadores desde parámetros (opcional)
    # Por defecto: ['arriba', 'abajo', 'izquierda', 'derecha']
    operator_order = params.get("operator_order", ['arriba', 'abajo', 'izquierda', 'derecha'])
    
    def get_neighbors(pos, mapa, order):
        """
        Obtiene los vecinos válidos de una posición.
        El orden se determina por el parámetro 'order'
        """
        fila, col = pos
        
        # Mapeo de nombres a movimientos
        movimientos = {
            'arriba': (-1, 0),
            'abajo': (1, 0),
            'izquierda': (0, -1),
            'derecha': (0, 1)
        }
        
        # Crear lista de direcciones según el orden especificado
        direcciones = [movimientos[op] for op in order if op in movimientos]
        
        vecinos = []
        for df, dc in direcciones:
            nueva_fila, nueva_col = fila + df, col + dc
            
            # Verificar límites del mapa
            if 0 <= nueva_fila < 10 and 0 <= nueva_col < 10:
                # Verificar que no sea obstáculo (valor 1)
                if mapa[nueva_fila][nueva_col] != 1:
                    vecinos.append((nueva_fila, nueva_col))
        
        return vecinos
    
    # Estado inicial: (posición, muestras_recolectadas, ha_tomado_nave)
    # ha_tomado_nave es booleano: True si ya tomó la nave, False si no
    estado_inicial = (start, frozenset(), False)
    
    # Pila para DFS: cada elemento es ((posición, muestras, ha_tomado_nave), camino, combustible)
    pila = [(estado_inicial, [start], 0)]
    
    # Conjunto de estados visitados para evitar ciclos
    # Estado = (posición, muestras, ha_tomado_nave)
    # ha_tomado_nave indica si YA tomó la nave anteriormente (solo puede tomarla una vez)
    # Esto permite: visitar una posición SIN haber tomado nave, luego CON nave tomada
    # Pero NO permite: tomar la nave múltiples veces
    visitados = {estado_inicial}
    
    nodos_expandidos = 0
    max_profundidad = 0
    
    # Algoritmo DFS con pila
    while pila:
        # Pop desde el final (LIFO - Last In First Out)
        (pos_actual, muestras_recolectadas, ha_tomado_nave), camino, combustible = pila.pop()
        nodos_expandidos += 1
        max_profundidad = max(max_profundidad, len(camino))
        
        # Verificar si estamos en una muestra y aún no la hemos recolectado
        if pos_actual in muestras and pos_actual not in muestras_recolectadas:
            muestras_recolectadas = frozenset(muestras_recolectadas | {pos_actual})
        
        # Verificar si recolectamos todas las muestras (META)
        if len(muestras_recolectadas) == 3:
            # Calcular costo del camino
            costo_total = 0
            combustible_actual = 0
            
            for i in range(len(camino) - 1):
                fila, col = camino[i + 1]
                celda = mapa[fila][col]
                
                # Si estamos en la nave, recargamos combustible
                if celda == 5:
                    combustible_actual = 20
                
                # Calcular costo del movimiento
                if combustible_actual > 0:
                    costo_total += 0.5
                    combustible_actual -= 1
                else:
                    # Costo según terreno
                    if celda == 0 or celda == 2 or celda == 6:
                        costo_total += 1
                    elif celda == 3:
                        costo_total += 3
                    elif celda == 4:
                        costo_total += 5
                    elif celda == 5:
                        costo_total += 1
            
            # Convertir camino a lista de listas para JSON
            camino_json = [list(pos) for pos in camino]
            
            return {
                "path": camino_json,
                "nodes_expanded": nodos_expandidos,
                "cost": costo_total,
                "max_depth": max_profundidad,
                "message": "Solución encontrada - 3 muestras recolectadas"
            }
        
        # Expandir vecinos y agregarlos a la pila
        vecinos = get_neighbors(pos_actual, mapa, operator_order)
        
        # Para DFS con pila (LIFO), agregamos en orden INVERSO
        # Así el primero en salir (pop) será el primero que pusimos (arriba)
        # Orden de push: derecha, izquierda, abajo, arriba
        # Orden de pop (expansión): arriba, abajo, izquierda, derecha
        for vecino in reversed(vecinos):
            # Calcular nuevo combustible y si toma la nave
            nuevo_combustible = combustible
            ha_tomado_nave_nuevo = ha_tomado_nave
            
            # Solo puede tomar la nave si está en la casilla 5 y NO la ha tomado antes
            if mapa[vecino[0]][vecino[1]] == 5 and not ha_tomado_nave:
                # Toma la nave por primera (y única) vez
                nuevo_combustible = 20
                ha_tomado_nave_nuevo = True
            elif nuevo_combustible > 0:
                # Consume combustible si lo tiene
                nuevo_combustible -= 1
            
            # El estado considera si YA ha tomado la nave (independiente del combustible actual)
            # Esto evita que pueda tomar la nave múltiples veces
            nuevo_estado = (vecino, muestras_recolectadas, ha_tomado_nave_nuevo)
            
            # EVITAR CICLOS MEJORADO:
            # - Puede visitar una posición sin haber tomado la nave
            # - Puede visitar la MISMA posición después de tomar la nave (solo UNA vez)
            # - Puede visitar con diferentes muestras recolectadas
            # - La nave solo se puede tomar UNA vez en todo el recorrido
            # - PERO NO puede visitar la misma (posición + ha_tomado_nave + muestras) dos veces
            if nuevo_estado not in visitados:
                visitados.add(nuevo_estado)
                pila.append((nuevo_estado, camino + [vecino], nuevo_combustible))
    
    # No se encontró solución
    return {
        "path": [],
        "nodes_expanded": nodos_expandidos,
        "cost": 0,
        "max_depth": max_profundidad,
        "message": "No se encontró solución para recolectar las 3 muestras"
    }
    