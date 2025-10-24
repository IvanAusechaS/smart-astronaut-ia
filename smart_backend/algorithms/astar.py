"""
A* Search Algorithm
Algoritmo A* que combina costo real (g) y heuristica (h) para busqueda optima
Utiliza f(n) = g(n) + h(n) donde:
- g(n) = costo real desde el inicio hasta n (como Uniform Cost)
- h(n) = estimacion heuristica desde n hasta el objetivo (como Greedy)
"""

import heapq

def solve(params: dict):
    """
    Ejecuta el algoritmo A* para encontrar el camino optimo que recolecte las 3 muestras.
    Combina el costo real acumulado (g) con la heuristica (h) para garantizar
    optimalidad si la heuristica es admisible.
    
    Args:
        params: Diccionario con parametros del problema
               - map: Matriz 10x10 con valores 0-6
               - start: Tupla (fila, columna) de la posicion inicial
               - goal: NO SE USA, el objetivo es recolectar 3 muestras (valor 6)
    
    Returns:
        dict: Resultado con el camino encontrado y estadisticas
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
    operator_order = params.get("operator_order", ['arriba', 'abajo', 'izquierda', 'derecha'])
    
    def get_neighbors(pos, mapa, order):
        """Obtiene los vecinos válidos de una posición"""
        fila, col = pos
        
        movimientos = {
            'arriba': (-1, 0),
            'abajo': (1, 0),
            'izquierda': (0, -1),
            'derecha': (0, 1)
        }
        
        direcciones = [movimientos[op] for op in order if op in movimientos]
        vecinos = []
        
        for df, dc in direcciones:
            nueva_fila, nueva_col = fila + df, col + dc
            
            if 0 <= nueva_fila < 10 and 0 <= nueva_col < 10:
                if mapa[nueva_fila][nueva_col] != 1:
                    vecinos.append((nueva_fila, nueva_col))
        
        return vecinos
    
    def calcular_costo_movimiento(pos, combustible_antes, mapa):
        """
        Calcula g(n): el costo real de moverse a una posición
        (Componente de Uniform Cost)
        """
        fila, col = pos
        celda = mapa[fila][col]
        
        # Si tenía combustible antes del movimiento, cuesta 0.5
        if combustible_antes > 0:
            return 0.5
        
        # Sin combustible, depende del terreno
        if celda in [0, 2, 5, 6]:
            return 1
        elif celda == 3:
            return 3
        elif celda == 4:
            return 5
        
        return 1
    
    def heuristic(pos, muestras_recolectadas, todas_muestras):
        """
        Calcula h(n): estimacion heuristica del costo restante
        (Componente de Greedy)
        
        Heuristica: Distancia Manhattan a la muestra no recolectada más cercana.
        Esta heuristica es ADMISIBLE (nunca sobreestima) porque:
        - La distancia Manhattan es el mínimo número de movimientos
        - El costo real siempre será >= número de movimientos (cada movimiento cuesta al menos 0.5)
        """
        if len(muestras_recolectadas) == 3:
            return 0
        
        muestras_restantes = todas_muestras - muestras_recolectadas
        min_distancia = float('inf')
        
        for muestra in muestras_restantes:
            distancia = abs(pos[0] - muestra[0]) + abs(pos[1] - muestra[1])
            min_distancia = min(min_distancia, distancia)
        
        # Multiplicamos por 0.5 (costo mínimo por movimiento) para mejor estimación
        return min_distancia * 0.5
    
    # Estado: (posición, muestras_recolectadas, ha_tomado_nave)
    estado_inicial = (start, frozenset(), False)
    
    # Cola de prioridad para A*: (f, g, contador, estado, camino, combustible)
    # f = g + h (costo total estimado)
    # g = costo real acumulado
    # contador para desempatar nodos con mismo f
    contador = 0
    h_inicial = heuristic(start, frozenset(), muestras)
    cola_prioridad = [(h_inicial, 0, contador, estado_inicial, [start], 0)]
    
    # Diccionario para guardar el mejor costo g por estado
    visitados = {}
    nodos_expandidos = 0
    max_profundidad = 0

    while cola_prioridad:
        # Extraer el nodo con el menor f (g + h)
        f_actual, g_actual, _, (pos_actual, muestras_recolectadas, ha_tomado_nave), camino, combustible = heapq.heappop(cola_prioridad)
        
        estado_key = (pos_actual, muestras_recolectadas, ha_tomado_nave)
        
        # Si ya visitamos este estado con menor o igual costo g, skip
        if estado_key in visitados and visitados[estado_key] <= g_actual:
            continue
            
        visitados[estado_key] = g_actual
        nodos_expandidos += 1
        max_profundidad = max(max_profundidad, len(camino))-1
        
        # Verificar si estamos en una muestra y aún no la hemos recolectado
        if pos_actual in muestras and pos_actual not in muestras_recolectadas:
            muestras_recolectadas = frozenset(muestras_recolectadas | {pos_actual})
        
        # Verificar si recolectamos todas las muestras (OBJETIVO)
        if len(muestras_recolectadas) == 3:
            camino_json = [list(pos) for pos in camino]
            
            return {
                "path": camino_json,
                "nodes_expanded": nodos_expandidos,
                "cost": g_actual,  # Retornar el costo real g(n)
                "max_depth": max_profundidad,
                "message": "Solución óptima encontrada - 3 muestras recolectadas"
            }
        
        # Expandir vecinos
        for vecino in get_neighbors(pos_actual, mapa, operator_order):
            # Calcular g(vecino): costo real acumulado
            costo_movimiento = calcular_costo_movimiento(vecino, combustible, mapa)
            nuevo_g = g_actual + costo_movimiento
            
            # Actualizar combustible y estado de nave
            nuevo_combustible = combustible
            ha_tomado_nave_nuevo = ha_tomado_nave
            
            if mapa[vecino[0]][vecino[1]] == 5 and not ha_tomado_nave:
                nuevo_combustible = 20
                ha_tomado_nave_nuevo = True
            elif nuevo_combustible > 0:
                nuevo_combustible -= 1
            
            nuevo_estado = (vecino, muestras_recolectadas, ha_tomado_nave_nuevo)
            nuevo_estado_key = nuevo_estado
            
            # Solo agregar si no hemos visitado o encontramos un camino más barato
            if nuevo_estado_key not in visitados or visitados[nuevo_estado_key] > nuevo_g:
                # Calcular h(vecino): estimación heurística
                nuevo_h = heuristic(vecino, muestras_recolectadas, muestras)
                
                # Calcular f(vecino) = g(vecino) + h(vecino)
                nuevo_f = nuevo_g + nuevo_h
                
                contador += 1
                heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, contador, nuevo_estado, camino + [vecino], nuevo_combustible))
    
    # No se encontró solución
    return {
        "path": [],
        "nodes_expanded": nodos_expandidos,
        "cost": 0,
        "max_depth": max_profundidad,
        "message": "No se encontró solución para recolectar las 3 muestras"
    }
