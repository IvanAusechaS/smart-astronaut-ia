from collections import deque

"""
================================================================================
ALGORITMO: Breadth-First Search (BFS) - Búsqueda en Anchura
================================================================================
Autor: Ivan Ausecha
Fecha: Octubre 2025
Proyecto: Smart Astronaut - Sistema de Exploración Marciana

DESCRIPCIÓN:
    Implementación del algoritmo BFS para resolver el problema de recolección
    de muestras científicas en un mapa marciano de 10x10. El algoritmo debe
    encontrar un camino que permita recolectar las 3 muestras científicas
    presentes en el mapa.

CARACTERÍSTICAS:
    - Búsqueda en anchura (nivel por nivel)
    - Utiliza cola FIFO (First In, First Out)
    - Garantiza encontrar la solución óptima en grafos no ponderados
    - Gestión de combustible de nave auxiliar (20 movimientos a costo 0.5)
    - Manejo de costos variables según tipo de terreno
    
COMPLEJIDAD:
    - Tiempo: O(b^d) donde b=branching factor (máx 4 vecinos), d=profundidad
    - Espacio: O(b^d) para almacenar todos los nodos en la cola
================================================================================
"""

def solve(params: dict):
    """
    Función principal que ejecuta el algoritmo BFS.
    
    El algoritmo explora el espacio de estados nivel por nivel, garantizando
    encontrar la solución óptima en términos de número de movimientos.
    
    Args:
        params (dict): Diccionario con parámetros del problema:
            - map (list[list[int]]): Matriz 10x10 con valores 0-6 representando:
                * 0: Terreno libre (costo 1)
                * 1: Obstáculo (intransitable)
                * 2: Posición inicial del astronauta
                * 3: Terreno rocoso (costo 3)
                * 4: Terreno volcánico (costo 5)
                * 5: Nave auxiliar (recarga 20 combustible, movimientos costo 0.5)
                * 6: Muestra científica (objetivo)
            - start (list[int]): Lista [fila, columna] con posición inicial
            - goal: NO SE USA - el objetivo es recolectar las 3 muestras
    
    Returns:
        dict: Diccionario con los resultados de la búsqueda:
            - path (list[list[int]]): Camino solución como lista de posiciones
            - nodes_expanded (int): Cantidad de nodos expandidos durante búsqueda
            - cost (float): Costo total del camino encontrado
            - max_depth (int): Profundidad máxima alcanzada (número de movimientos)
            - message (str): Mensaje descriptivo del resultado
    
    Ejemplo:
        >>> params = {
        ...     "map": mapa_10x10,
        ...     "start": [2, 1]
        ... }
        >>> resultado = solve(params)
        >>> print(f"Camino: {len(resultado['path'])} posiciones")
        >>> print(f"Nodos expandidos: {resultado['nodes_expanded']}")
    """
    # =========================================================================
    # PASO 1: EXTRACCIÓN Y VALIDACIÓN DE PARÁMETROS
    # =========================================================================
    
    # Extraer mapa y posición inicial de los parámetros
    mapa = params.get("map", [])
    start = tuple(params.get("start", [0, 0]))
    
    # Validar dimensiones del mapa (debe ser exactamente 10x10)
    if not mapa or len(mapa) != 10 or len(mapa[0]) != 10:
        return {
            "path": [],
            "nodes_expanded": 0,
            "cost": 0,
            "max_depth": 0,
            "message": "Mapa inválido"
        }
    
    # =========================================================================
    # PASO 2: IDENTIFICAR MUESTRAS CIENTÍFICAS EN EL MAPA
    # =========================================================================
    
    # Buscar todas las celdas con valor 6 (muestras científicas)
    # Se usa set() para almacenamiento eficiente y búsquedas O(1)
    muestras = set()
    for i in range(10):
        for j in range(10):
            if mapa[i][j] == 6:
                muestras.add((i, j))
    
    # Validar que existan exactamente 3 muestras según especificación del problema
    if len(muestras) != 3:
        return {
            "path": [],
            "nodes_expanded": 0,
            "cost": 0,
            "max_depth": 0,
            "message": f"Error: Se esperan 3 muestras, se encontraron {len(muestras)}"
        }
    
    # =========================================================================
    # FUNCIÓN AUXILIAR: GENERADOR DE VECINOS
    # =========================================================================
    
    def get_neighbors(pos, mapa):
        """
        Genera todos los vecinos válidos de una posición dada.
        
        En BFS, el orden de exploración afecta qué solución se encuentra primero
        cuando hay múltiples soluciones con la misma profundidad. Este orden
        específico (arriba, abajo, izquierda, derecha) es estándar en problemas
        de búsqueda en grillas.
        
        Args:
            pos (tuple): Tupla (fila, columna) de la posición actual
            mapa (list[list[int]]): Matriz del mapa
        
        Returns:
            list[tuple]: Lista de tuplas (fila, columna) de vecinos válidos
        
        Nota:
            - Un vecino es válido si está dentro de los límites (0-9, 0-9)
            - Un vecino es válido si NO es obstáculo (valor != 1)
            - Se exploran en orden: arriba, abajo, izquierda, derecha
        """
        fila, col = pos
        vecinos = []
        
        # Direcciones en orden: arriba, abajo, izquierda, derecha
        # (-1,0): mover hacia arriba (decrementar fila)
        # (1,0): mover hacia abajo (incrementar fila)
        # (0,-1): mover hacia izquierda (decrementar columna)
        # (0,1): mover hacia derecha (incrementar columna)
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for df, dc in direcciones:
            nueva_fila, nueva_col = fila + df, col + dc
            
            # Verificar que la nueva posición esté dentro de los límites del mapa
            if 0 <= nueva_fila < 10 and 0 <= nueva_col < 10:
                # Verificar que no sea obstáculo (valor 1)
                # Todos los demás valores (0,2,3,4,5,6) son transitables
                if mapa[nueva_fila][nueva_col] != 1:
                    vecinos.append((nueva_fila, nueva_col))
        
        return vecinos
    
    # =========================================================================
    # PASO 3: INICIALIZACIÓN DE ESTRUCTURAS DE DATOS
    # =========================================================================
    
    # REPRESENTACIÓN DE ESTADO:
    # Un estado completo incluye: (posición, muestras_recolectadas, combustible)
    # - posición: tupla (fila, columna)
    # - muestras_recolectadas: frozenset de posiciones de muestras ya tomadas
    #   (frozenset es inmutable y hashable, necesario para usar en set visitados)
    # - combustible: cantidad de combustible restante de la nave (0-20)
    #
    # IMPORTANCIA: Dos estados son diferentes si alguno de estos tres componentes
    # es diferente, permitiendo revisitar posiciones bajo diferentes condiciones
    
    estado_inicial = (start, frozenset(), 0)
    
    # COLA (FIFO): Estructura fundamental de BFS
    # Usamos deque de collections para operaciones O(1) en ambos extremos
    # Cada elemento: (estado, camino_hasta_ese_estado)
    cola = deque([(estado_inicial, [start])])
    
    # VISITADOS: Set de estados ya explorados para evitar ciclos infinitos
    # Usamos set() para verificación de pertenencia en O(1)
    visitados = {estado_inicial}
    
    # MÉTRICAS DE RENDIMIENTO:
    nodos_expandidos = 0    # Contador de nodos que sacamos de la cola y exploramos
    max_profundidad = 0      # Profundidad máxima alcanzada (longitud del camino más largo explorado)
    
    # =========================================================================
    # PASO 4: BUCLE PRINCIPAL DE BFS
    # =========================================================================
    
    while cola:
        # EXTRACCIÓN DEL SIGUIENTE NODO (FIFO)
        # popleft() extrae del inicio de la cola (orden de llegada)
        # Esto garantiza exploración nivel por nivel (característica de BFS)
        (pos_actual, muestras_recolectadas, combustible), camino = cola.popleft()
        
        # ---------------------------------------------------------------------
        # VERIFICAR RECOLECCIÓN DE MUESTRA
        # ---------------------------------------------------------------------
        # Si estamos en una posición con muestra Y aún no la hemos recolectado
        if pos_actual in muestras and pos_actual not in muestras_recolectadas:
            # Agregar muestra al conjunto de recolectadas
            # Usamos | (union) para crear nuevo frozenset con la muestra agregada
            muestras_recolectadas = frozenset(muestras_recolectadas | {pos_actual})
        
        # ---------------------------------------------------------------------
        # TEST DE OBJETIVO: ¿Ya recolectamos las 3 muestras?
        # ---------------------------------------------------------------------
        if len(muestras_recolectadas) == 3:
            # ¡SOLUCIÓN ENCONTRADA! Calcular costo total del camino
            
            # Inicializar variables para cálculo de costo
            costo_total = 0
            combustible_actual = 0
            
            # Recorrer el camino movimiento por movimiento
            # range(len(camino) - 1) porque comparamos posición i con i+1
            for i in range(len(camino) - 1):
                fila, col = camino[i + 1]  # Posición destino del movimiento
                celda = mapa[fila][col]     # Tipo de terreno de la celda destino
                
                # RECARGA DE COMBUSTIBLE: Si llegamos a la nave (valor 5)
                if celda == 5:
                    combustible_actual = 20  # Recargar a máximo
                
                # CÁLCULO DE COSTO DEL MOVIMIENTO:
                # Regla: Si hay combustible, movimiento cuesta 0.5
                #        Si no hay combustible, costo depende del terreno
                if combustible_actual > 0:
                    costo_total += 0.5
                    combustible_actual -= 1  # Consumir 1 unidad de combustible
                else:
                    # Costo según tipo de terreno (sin combustible)
                    if celda == 0 or celda == 2 or celda == 6:  # Libre, Astronauta, Muestra
                        costo_total += 1
                    elif celda == 3:  # Rocoso
                        costo_total += 3
                    elif celda == 4:  # Volcánico
                        costo_total += 5
                    elif celda == 5:  # Nave
                        costo_total += 1
            
            # Convertir camino de tuplas a listas para serialización JSON
            camino_json = [list(pos) for pos in camino]
            
            # RETORNAR SOLUCIÓN ENCONTRADA
            return {
                "path": camino_json,
                "nodes_expanded": nodos_expandidos,
                "cost": costo_total,
                "max_depth": max_profundidad,
                "message": "Solución encontrada - 3 muestras recolectadas"
            }
        
        # ---------------------------------------------------------------------
        # ACTUALIZAR PROFUNDIDAD MÁXIMA
        # ---------------------------------------------------------------------
        # len(camino) - 1 porque contamos movimientos, no posiciones
        # Ejemplo: camino de 28 posiciones = 27 movimientos
        max_profundidad = max(max_profundidad, len(camino) - 1)
        
        # ---------------------------------------------------------------------
        # EXPANSIÓN DE NODO: Generar sucesores
        # ---------------------------------------------------------------------
        # Intentar expandir hacia todos los vecinos válidos
        vecinos_agregados = 0  # Contador de nuevos estados generados
        
        for vecino in get_neighbors(pos_actual, mapa):
            # CALCULAR NUEVO COMBUSTIBLE PARA EL ESTADO SUCESOR
            nuevo_combustible = combustible
            
            # Si el vecino es la nave (valor 5), recargamos combustible
            if mapa[vecino[0]][vecino[1]] == 5:
                nuevo_combustible = 20
            # Si tenemos combustible activo, se reduce en 1
            elif nuevo_combustible > 0:
                nuevo_combustible -= 1
            # Si no hay combustible, permanece en 0
            
            # CREAR NUEVO ESTADO
            # Importante: muestras_recolectadas se mantiene igual hasta que
            # el nuevo estado sea expandido y verifique si está en una muestra
            nuevo_estado = (vecino, muestras_recolectadas, nuevo_combustible)
            
            # VERIFICAR SI YA VISITAMOS ESTE ESTADO EXACTO
            # Esto previene ciclos y exploración redundante
            # Nota: Permitimos revisitar POSICIONES con diferentes estados
            # (ej: misma posición pero con diferente número de muestras)
            if nuevo_estado not in visitados:
                # Marcar estado como visitado
                visitados.add(nuevo_estado)
                
                # Agregar a la cola FIFO (al final)
                # Importante: camino + [vecino] crea NUEVO camino con vecino agregado
                cola.append((nuevo_estado, camino + [vecino]))
                
                # Contar vecino generado
                vecinos_agregados += 1
        
        # CONTAR NODO COMO EXPANDIDO
        # Solo si realmente generó al menos un hijo nuevo
        # (esto es más preciso que contar todos los nodos sacados de la cola)
        if vecinos_agregados > 0:
            nodos_expandidos += 1
    
    # =========================================================================
    # PASO 5: NO SE ENCONTRÓ SOLUCIÓN
    # =========================================================================
    # Si salimos del while sin retornar, significa que la cola se vació
    # sin encontrar un estado con las 3 muestras recolectadas
    return {
        "path": [],
        "nodes_expanded": nodos_expandidos,
        "cost": 0,
        "max_depth": max_profundidad,
        "message": "No se encontró solución para recolectar las 3 muestras"
    }

# =============================================================================
# NOTAS ADICIONALES SOBRE LA IMPLEMENTACIÓN
# =============================================================================
"""
VENTAJAS DE BFS EN ESTE PROBLEMA:
1. COMPLETITUD: Siempre encuentra solución si existe
2. OPTIMALIDAD: En grafos no ponderados, encuentra camino más corto
3. SISTEMATICIDAD: Explora nivel por nivel, sin sesgo direccional

DESVENTAJAS:
1. MEMORIA: Puede requerir mucha memoria (O(b^d)) para mapas grandes
2. TIEMPO: Explora muchos nodos antes de encontrar la solución
3. NO CONSIDERA COSTOS: En este problema hay costos variables, pero BFS
   los ignora durante la búsqueda (solo minimiza número de movimientos)

OPTIMIZACIONES IMPLEMENTADAS:
1. Uso de frozenset para muestras (inmutable y hashable)
2. Uso de deque para operaciones O(1) en cola
3. Set de visitados para verificación O(1)
4. Solo contar nodos realmente expandidos

CASOS DE USO IDEALES:
- Cuando el costo de todos los movimientos es uniforme
- Cuando se necesita el camino más corto en términos de pasos
- Cuando la solución está relativamente cerca del inicio
"""
