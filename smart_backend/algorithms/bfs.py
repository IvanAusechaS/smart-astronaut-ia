from collections import deque

"""
Breadth-First Search (BFS) Algorithm
Búsqueda en anchura para recolectar las 3 muestras científicas
"""

def solve(params: dict):
    """
    Ejecuta el algoritmo BFS para encontrar un camino que recolecte las 3 muestras.
    
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
    
    def get_neighbors(pos, mapa):
        """Obtiene los vecinos válidos de una posición"""
        fila, col = pos
        vecinos = []
        # Movimientos: arriba, abajo, izquierda, derecha
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for df, dc in direcciones:
            nueva_fila, nueva_col = fila + df, col + dc
            
            # Verificar límites del mapa
            if 0 <= nueva_fila < 10 and 0 <= nueva_col < 10:
                # Verificar que no sea obstáculo (valor 1)
                if mapa[nueva_fila][nueva_col] != 1:
                    vecinos.append((nueva_fila, nueva_col))
        
        return vecinos
    
    # Estado: (posición, muestras_recolectadas_frozenset, combustible)
    estado_inicial = (start, frozenset(), 0)
    cola = deque([(estado_inicial, [start])])
    visitados = {estado_inicial}
    nodos_expandidos = 0
    max_profundidad = 0
    
    while cola:
        (pos_actual, muestras_recolectadas, combustible), camino = cola.popleft()
        nodos_expandidos += 1
        max_profundidad = max(max_profundidad, len(camino))
        
        # Verificar si estamos en una muestra y aún no la hemos recolectado
        if pos_actual in muestras and pos_actual not in muestras_recolectadas:
            muestras_recolectadas = frozenset(muestras_recolectadas | {pos_actual})
        
        # Verificar si recolectamos todas las muestras
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
        
        # Expandir vecinos
        for vecino in get_neighbors(pos_actual, mapa):
            # Calcular nuevo combustible
            nuevo_combustible = combustible
            if mapa[vecino[0]][vecino[1]] == 5:
                nuevo_combustible = 20
            elif nuevo_combustible > 0:
                nuevo_combustible -= 1
            
            nuevo_estado = (vecino, muestras_recolectadas, nuevo_combustible)
            
            # Solo visitamos si no hemos estado en este estado exacto
            # PERO permitimos revisitar posiciones con diferentes estados de muestras/combustible
            if nuevo_estado not in visitados:
                visitados.add(nuevo_estado)
                cola.append((nuevo_estado, camino + [vecino]))
    
    # No se encontró solución
    return {
        "path": [],
        "nodes_expanded": nodos_expandidos,
        "cost": 0,
        "max_depth": max_profundidad,
        "message": "No se encontró solución para recolectar las 3 muestras"
    }
