"""
Uniform Cost Search Algorithm
Busqueda de costo uniforme para encontrar el camino de menor costo
"""

def solve(params: dict):
    """
    Ejecuta el algoritmo de Costo Uniforme
    
    Args:
        params: Diccionario con parametros del problema
               - map: Mapa/grafo a resolver
               - start: Nodo inicial
               - goal: Nodo objetivo
    
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
    
    def calcular_costo_movimiento(pos, combustible_antes, mapa):
        """Calcula el costo de moverse a una posición"""
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
    
    estado_inicial = (start, frozenset(), 0)
    cola_prioridad = [(estado_inicial, [start], 0)]  # (estado, camino, costo)
    visitados = {estado_inicial}
    nodos_expandidos = 0
    max_profundidad = 0

    while cola_prioridad:
        # Extraer el nodo con el menor costo
        cola_prioridad.sort(key=lambda x: x[2])  # Ordenar por costo
        (pos_actual, muestras_recolectadas, combustible), camino, costo_acumulado = cola_prioridad.pop(0)
        max_profundidad = max(max_profundidad, len(camino))-1
        
        # Verificar si estamos en una muestra y aún no la hemos recolectado
        if pos_actual in muestras and pos_actual not in muestras_recolectadas:
            muestras_recolectadas = frozenset(muestras_recolectadas | {pos_actual})
            
        # Verificar si recolectamos todas las muestras
        if len(muestras_recolectadas) == 3:
            # Convertir camino a lista de listas para JSON
            camino_json = [list(pos) for pos in camino]
            
            return {
                "path": camino_json,
                "nodes_expanded": nodos_expandidos,
                "cost": costo_acumulado,  # Usar costo acumulado real
                "max_depth": max_profundidad,
                "message": "Solución encontrada - 3 muestras recolectadas"
            }
        
        
        # Expandir vecinos - solo contar como expandido si realmente generamos hijos nuevos
        vecinos_agregados = 0
        for vecino in get_neighbors(pos_actual, mapa, operator_order):  # Pasar operator_order
            # Calcular costo del movimiento ANTES de actualizar combustible
            costo_movimiento = calcular_costo_movimiento(vecino, combustible, mapa)
            nuevo_costo = costo_acumulado + costo_movimiento
            
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
                cola_prioridad.append((nuevo_estado, camino + [vecino], nuevo_costo))  # ✅ Agregar nuevo_costo
                vecinos_agregados += 1
        
        # Solo contar como expandido si realmente agregamos vecinos nuevos
        if vecinos_agregados > 0:
            nodos_expandidos += 1
                            
    # No se encontró solución
    return {
        "path": [],
        "nodes_expanded": nodos_expandidos,
        "cost": 0,
        "max_depth": max_profundidad,
        "message": "No se encontró solución para recolectar las 3 muestras"
    }
