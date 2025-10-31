#!/usr/bin/env python3
"""
Script de Práctica para Sustentación BFS
Permite probar diferentes configuraciones del algoritmo
"""

import sys
import os
sys.path.append('smart_backend')

from algorithms.bfs import solve
import time

def cargar_mapa(archivo='mapa.txt'):
    """Carga el mapa desde archivo"""
    with open(archivo, 'r') as f:
        lines = f.readlines()
        mapa = []
        for line in lines:
            if line.strip():
                row = [int(x) for x in line.strip().split()]
                mapa.append(row)
    return mapa

def encontrar_posicion_inicial(mapa):
    """Encuentra la posición del astronauta (valor 2)"""
    for i in range(10):
        for j in range(10):
            if mapa[i][j] == 2:
                return [i, j]
    return None

def encontrar_muestras(mapa):
    """Encuentra todas las muestras (valor 6)"""
    muestras = []
    for i in range(10):
        for j in range(10):
            if mapa[i][j] == 6:
                muestras.append([i, j])
    return muestras

def ejecutar_bfs(mapa, start):
    """Ejecuta BFS y mide el tiempo"""
    params = {
        "map": mapa,
        "start": start
    }
    
    inicio = time.time()
    resultado = solve(params)
    fin = time.time()
    
    resultado['tiempo_real'] = fin - inicio
    return resultado

def mostrar_estadisticas(resultado):
    """Muestra las estadísticas del resultado"""
    print("\n" + "="*70)
    print("📊 ESTADÍSTICAS BFS")
    print("="*70)
    print(f"✅ Mensaje: {resultado['message']}")
    print(f"📍 Longitud del camino: {len(resultado['path'])} posiciones")
    print(f"🚶 Movimientos realizados: {len(resultado['path']) - 1}")
    print(f"🔍 Nodos expandidos: {resultado['nodes_expanded']}")
    print(f"📏 Profundidad máxima: {resultado['max_depth']}")
    print(f"💰 Costo total: {resultado['cost']}")
    print(f"⏱️  Tiempo de ejecución: {resultado['tiempo_real']*1000:.2f} ms")
    print("="*70)

def mostrar_camino_detallado(resultado, mapa):
    """Muestra el camino paso a paso"""
    print("\n🗺️  CAMINO DETALLADO:")
    print("-" * 70)
    
    path = resultado['path']
    for i, pos in enumerate(path):
        celda = mapa[pos[0]][pos[1]]
        emoji = ""
        descripcion = ""
        
        if i == 0:
            emoji = "🚀"
            descripcion = "INICIO"
        elif celda == 6:
            emoji = "📦"
            descripcion = "MUESTRA CIENTÍFICA"
        elif celda == 5:
            emoji = "🛸"
            descripcion = "NAVE (recarga combustible)"
        elif celda == 3:
            emoji = "🪨"
            descripcion = "Terreno rocoso (costo 3)"
        elif celda == 4:
            emoji = "🌋"
            descripcion = "Terreno volcánico (costo 5)"
        elif celda == 0:
            emoji = "⬜"
            descripcion = "Terreno libre"
        
        print(f"  Paso {i:2d}: {pos} {emoji} {descripcion}")
        
        # Mostrar separadores cada 5 pasos
        if (i + 1) % 5 == 0 and i < len(path) - 1:
            print("  " + "·" * 30)
    
    print("-" * 70)

def menu_principal():
    """Menú interactivo"""
    print("\n" + "="*70)
    print("🎓 PRÁCTICA DE SUSTENTACIÓN - ALGORITMO BFS")
    print("="*70)
    print("\nOpciones:")
    print("  1. Ejecutar BFS con configuración estándar")
    print("  2. Ver análisis detallado del camino")
    print("  3. Comparar con diferentes mapas")
    print("  4. Simular modificación: cambiar orden de operadores")
    print("  5. Simular modificación: limitar profundidad")
    print("  6. Ver información del mapa actual")
    print("  7. Explicación teórica de BFS")
    print("  8. Preguntas frecuentes")
    print("  0. Salir")
    print("="*70)
    
    return input("\n👉 Selecciona una opción: ").strip()

def explicacion_teorica():
    """Muestra explicación teórica de BFS"""
    print("\n" + "="*70)
    print("📚 EXPLICACIÓN TEÓRICA: BREADTH-FIRST SEARCH (BFS)")
    print("="*70)
    
    print("""
¿QUÉ ES BFS?
-----------
BFS (Búsqueda en Anchura) es un algoritmo de búsqueda NO INFORMADA que:
- Explora el grafo/árbol nivel por nivel
- Usa una estructura FIFO (cola) para gestionar nodos
- Garantiza encontrar la solución con MENOS PASOS

CARACTERÍSTICAS CLAVE:
---------------------
✅ Completitud: Siempre encuentra solución si existe
✅ Optimalidad: Encuentra el camino más corto en PASOS
⚠️  No óptimo: En COSTO si los arcos tienen diferentes pesos
❌ Memoria: Alta (O(b^d)) - guarda todos los nodos en frontera

PSEUDOCÓDIGO:
-------------
1. Crear cola FIFO vacía
2. Agregar estado inicial a la cola
3. Mientras la cola no esté vacía:
   a. Extraer primer elemento de la cola
   b. ¿Es objetivo? → Retornar solución
   c. Expandir vecinos
   d. Agregar vecinos no visitados a la cola
4. Si cola vacía → No hay solución

COMPLEJIDAD:
-----------
- Temporal: O(b^d) donde b=ramificación, d=profundidad
- Espacial: O(b^d) - todos los nodos en memoria

CUÁNDO USAR BFS:
---------------
✓ Quieres el camino con MENOS PASOS
✓ Los costos son uniformes o no importan
✓ Tienes suficiente memoria disponible
✓ El espacio de búsqueda no es muy grande

CUÁNDO NO USAR BFS:
------------------
✗ Necesitas el camino de MENOR COSTO → usar Costo Uniforme o A*
✗ Espacio de búsqueda muy grande → usar DFS o IDA*
✗ Tienes una heurística buena → usar A* o Greedy
    """)
    
    input("\nPresiona ENTER para continuar...")

def preguntas_frecuentes():
    """Muestra preguntas frecuentes"""
    print("\n" + "="*70)
    print("❓ PREGUNTAS FRECUENTES DEL PROFESOR")
    print("="*70)
    
    preguntas = [
        {
            "pregunta": "¿Por qué BFS encuentra 27 pasos y DFS 146?",
            "respuesta": """
BFS explora nivel por nivel, garantizando encontrar la solución más 
cercana primero. DFS va en profundidad y puede seguir caminos muy 
largos antes de encontrar la solución. BFS sacrifica memoria por 
optimalidad en pasos."""
        },
        {
            "pregunta": "¿Por qué usas frozenset para las muestras?",
            "respuesta": """
frozenset es inmutable y hashable, lo que permite:
1. Usarlo como parte de la clave en el conjunto 'visitados'
2. Evitar modificaciones accidentales
3. Representar conjuntos de forma eficiente
Las muestras recolectadas son parte del ESTADO, no solo del camino."""
        },
        {
            "pregunta": "¿Cómo evitas ciclos infinitos?",
            "respuesta": """
Mantengo un conjunto 'visitados' que almacena estados COMPLETOS:
    estado = (posición, muestras_recolectadas, combustible)
Solo expando estados que NO he visitado antes. Esto permite revisitar
posiciones pero con diferentes contextos (más muestras, distinto fuel)."""
        },
        {
            "pregunta": "¿Por qué 1,098 nodos expandidos?",
            "respuesta": """
BFS explora TODOS los estados alcanzables nivel por nivel hasta 
encontrar la solución. Cada posición puede visitarse con diferentes
combinaciones de:
- Muestras recolectadas (8 combinaciones: 2^3)
- Niveles de combustible (21 valores: 0-20)
Por eso el espacio de búsqueda es grande."""
        },
        {
            "pregunta": "¿BFS garantiza el camino de menor COSTO?",
            "respuesta": """
NO. BFS solo garantiza el camino con MENOS PASOS.
En nuestro caso:
- BFS: 27 pasos, costo 53
- A*:  27 pasos, costo 42 (mejor!)

Para minimizar costo, usar Búsqueda de Costo Uniforme o A*."""
        },
        {
            "pregunta": "¿Qué pasa si cambias el orden de los operadores?",
            "respuesta": """
Cambiar el orden (ej: derecha, arriba, abajo, izquierda) puede resultar
en un camino DIFERENTE pero con la misma LONGITUD (27 pasos).
BFS garantiza la longitud óptima, no un camino único. Múltiples caminos
pueden tener la misma longitud mínima."""
        }
    ]
    
    for i, qa in enumerate(preguntas, 1):
        print(f"\n{i}. {qa['pregunta']}")
        print("-" * 70)
        print(qa['respuesta'])
    
    input("\n\nPresiona ENTER para continuar...")

def info_mapa(mapa):
    """Muestra información del mapa"""
    print("\n" + "="*70)
    print("🗺️  INFORMACIÓN DEL MAPA")
    print("="*70)
    
    # Contar elementos
    libre = sum(row.count(0) for row in mapa)
    obstaculos = sum(row.count(1) for row in mapa)
    astronauta = sum(row.count(2) for row in mapa)
    rocoso = sum(row.count(3) for row in mapa)
    volcanico = sum(row.count(4) for row in mapa)
    nave = sum(row.count(5) for row in mapa)
    muestras = sum(row.count(6) for row in mapa)
    
    print(f"\n📊 Composición:")
    print(f"  ⬜ Terreno libre: {libre} celdas")
    print(f"  ⛰️  Obstáculos: {obstaculos} celdas")
    print(f"  🚶 Astronauta: {astronauta} celda")
    print(f"  🪨 Terreno rocoso: {rocoso} celdas (costo 3)")
    print(f"  🌋 Terreno volcánico: {volcanico} celdas (costo 5)")
    print(f"  🛸 Nave auxiliar: {nave} celda")
    print(f"  📦 Muestras científicas: {muestras} celdas")
    
    # Posiciones importantes
    print(f"\n📍 Posiciones clave:")
    for i in range(10):
        for j in range(10):
            if mapa[i][j] == 2:
                print(f"  🚶 Astronauta: [{i}, {j}]")
            elif mapa[i][j] == 5:
                print(f"  🛸 Nave: [{i}, {j}]")
            elif mapa[i][j] == 6:
                print(f"  📦 Muestra: [{i}, {j}]")
    
    # Visualización del mapa
    print(f"\n🎨 Visualización:")
    print("   " + " ".join([str(i) for i in range(10)]))
    print("  " + "-" * 21)
    
    emojis = {
        0: "⬜", 1: "⛰️ ", 2: "🚶", 3: "🪨",
        4: "🌋", 5: "🛸", 6: "📦"
    }
    
    for i, row in enumerate(mapa):
        print(f"{i} |", end="")
        for cell in row:
            print(emojis[cell], end="")
        print(f"| {i}")
    
    print("  " + "-" * 21)
    print("   " + " ".join([str(i) for i in range(10)]))
    
    input("\n\nPresiona ENTER para continuar...")

def main():
    """Función principal"""
    print("\n🚀 Cargando sistema...")
    
    # Cargar mapa
    try:
        mapa = cargar_mapa('mapa.txt')
        start = encontrar_posicion_inicial(mapa)
        muestras = encontrar_muestras(mapa)
        
        print(f"✅ Mapa cargado correctamente")
        print(f"📍 Posición inicial: {start}")
        print(f"📦 Muestras encontradas: {len(muestras)}")
    except Exception as e:
        print(f"❌ Error cargando mapa: {e}")
        return
    
    resultado_actual = None
    
    while True:
        opcion = menu_principal()
        
        if opcion == "1":
            print("\n⏳ Ejecutando BFS...")
            resultado_actual = ejecutar_bfs(mapa, start)
            mostrar_estadisticas(resultado_actual)
            
        elif opcion == "2":
            if resultado_actual:
                mostrar_camino_detallado(resultado_actual, mapa)
            else:
                print("\n⚠️  Primero ejecuta BFS (opción 1)")
            
        elif opcion == "3":
            print("\n📂 Mapas disponibles:")
            print("  1. mapa.txt (estándar)")
            print("  2. mapa2.txt (alternativo)")
            archivo = input("👉 Selecciona archivo (1 o 2): ").strip()
            
            try:
                nombre = "mapa.txt" if archivo == "1" else "mapa2.txt"
                mapa = cargar_mapa(nombre)
                start = encontrar_posicion_inicial(mapa)
                print(f"✅ Mapa '{nombre}' cargado correctamente")
                resultado_actual = None
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "4":
            print("\n🔧 SIMULACIÓN: Cambiar orden de operadores")
            print("-" * 70)
            print("En el archivo bfs.py, línea ~51:")
            print("\nORDEN ACTUAL:")
            print("  direcciones = [(-1,0), (1,0), (0,-1), (0,1)]")
            print("  Orden: Arriba → Abajo → Izquierda → Derecha")
            print("\nORDEN ALTERNATIVO 1:")
            print("  direcciones = [(0,1), (1,0), (0,-1), (-1,0)]")
            print("  Orden: Derecha → Abajo → Izquierda → Arriba")
            print("\nORDEN ALTERNATIVO 2:")
            print("  direcciones = [(-1,0), (0,1), (1,0), (0,-1)]")
            print("  Orden: Arriba → Derecha → Abajo → Izquierda")
            print("\n⚠️  NOTA: Cambiar el orden puede resultar en un camino")
            print("   diferente pero con la MISMA longitud (27 pasos).")
            
        elif opcion == "5":
            print("\n🔧 SIMULACIÓN: Limitar profundidad")
            print("-" * 70)
            print("Modificación en bfs.py dentro del while:")
            print("\n  # Limitar profundidad máxima")
            print("  MAX_DEPTH = 50  # Por ejemplo")
            print("  if len(camino) > MAX_DEPTH:")
            print("      continue  # No expandir este nodo")
            print("\n💡 Esto convierte BFS en 'BFS con límite de profundidad'")
            print("   Útil para evitar búsquedas muy costosas.")
            print("\nEFECTO:")
            print("  - Reduce nodos expandidos")
            print("  - Puede NO encontrar solución si límite < 27")
            print("  - Si límite >= 27, resultado igual")
            
        elif opcion == "6":
            info_mapa(mapa)
            
        elif opcion == "7":
            explicacion_teorica()
            
        elif opcion == "8":
            preguntas_frecuentes()
            
        elif opcion == "0":
            print("\n👋 ¡Buena suerte en tu sustentación!\n")
            break
        
        else:
            print("\n❌ Opción inválida. Intenta de nuevo.")
        
        input("\nPresiona ENTER para continuar...")

if __name__ == "__main__":
    main()
