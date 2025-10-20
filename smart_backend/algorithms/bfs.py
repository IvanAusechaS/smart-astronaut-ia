from collections import deque

"""
Breadth-First Search (BFS) Algorithm
Búsqueda en anchura para encontrar el camino más corto en grafos no ponderados
"""

def solve(params: dict):
    """
    Ejecuta el algoritmo BFS para encontrar el camino más corto.
    
    Args:
        params: Diccionario con parámetros del problema
               - map: Matriz 10x10 con valores 0-6
               - start: Tupla (fila, columna) del inicio
               - goal: Tupla (fila, columna) del objetivo
    
    Returns:
        dict: Resultado con el camino encontrado y estadísticas
    """
    mapa = params.get("map", [])
    start = tuple(params.get("start", [0, 0]))
    goal = tuple(params.get("goal", [9, 9]))
    
    # Validaciones básicas
    if not mapa or len(mapa) != 10 or len(mapa[0]) != 10:
        return {
            "path": [],
            "nodes_expanded": 0,
            "cost": 0,
            "max_depth": 0,
            "message": "Mapa inválido"
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
    
    # Inicialización BFS
    cola = deque([start])
    visitados = {start}
    padres = {start: None}
    profundidades = {start: 0}
    
    nodes_expanded = 0
    max_depth = 0
    encontrado = False
    
    # BFS principal
    while cola:
        nodo_actual = cola.popleft()
        nodes_expanded += 1
        
        # Actualizar profundidad máxima
        profundidad_actual = profundidades[nodo_actual]
        max_depth = max(max_depth, profundidad_actual)
        
        # Verificar si llegamos al objetivo
        fila, col = nodo_actual
        if mapa[fila][col] == 6:  # Muestra científica (objetivo)
            encontrado = True
            goal = nodo_actual  # Actualizar goal al objetivo real encontrado
            break
        
        # Expandir vecinos
        for vecino in get_neighbors(nodo_actual, mapa):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = nodo_actual
                profundidades[vecino] = profundidad_actual + 1
                cola.append(vecino)
    
    # Reconstruir camino si se encontró solución
    if encontrado:
        path = []
        nodo = goal
        while nodo is not None:
            path.append(list(nodo))  # Convertir tupla a lista para JSON
            nodo = padres[nodo]
        path.reverse()
        
        return {
            "path": path,
            "nodes_expanded": nodes_expanded,
            "cost": len(path) - 1,  # Costo = número de pasos
            "max_depth": max_depth,
            "message": "Solución encontrada"
        }
    else:
        return {
            "path": [],
            "nodes_expanded": nodes_expanded,
            "cost": 0,
            "max_depth": max_depth,
            "message": "No se encontró camino"
        }

