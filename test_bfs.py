#!/usr/bin/env python3
"""
Script de prueba para verificar el algoritmo BFS
"""

import sys
sys.path.append('smart_backend')

from algorithms.bfs import solve

# Leer mapa del archivo
with open('mapa.txt', 'r') as f:
    lines = f.readlines()
    mapa = []
    for line in lines:
        if line.strip():  # Ignorar líneas vacías
            row = [int(x) for x in line.strip().split()]
            mapa.append(row)

# Encontrar posición inicial (valor 2)
start = None
for i in range(10):
    for j in range(10):
        if mapa[i][j] == 2:
            start = [i, j]
            break
    if start:
        break

print(f"Mapa cargado: 10x10")
print(f"Posición inicial del astronauta: {start}")

# Encontrar muestras
muestras = []
for i in range(10):
    for j in range(10):
        if mapa[i][j] == 6:
            muestras.append([i, j])

print(f"Muestras encontradas: {muestras}")

# Ejecutar BFS
params = {
    "map": mapa,
    "start": start
}

print("\n" + "="*60)
print("EJECUTANDO BFS...")
print("="*60)

resultado = solve(params)

print(f"\nResultado:")
print(f"  - Camino encontrado: {len(resultado['path'])} posiciones")
print(f"  - Nodos expandidos: {resultado['nodes_expanded']}")
print(f"  - Costo total: {resultado['cost']}")
print(f"  - Profundidad máxima: {resultado['max_depth']}")
print(f"  - Mensaje: {resultado['message']}")

print(f"\nCamino completo:")
for i, pos in enumerate(resultado['path']):
    print(f"  Paso {i}: {pos}", end="")
    if i < len(resultado['path']):
        cell_value = mapa[pos[0]][pos[1]]
        if cell_value == 2:
            print(" (INICIO - Astronauta)")
        elif cell_value == 5:
            print(" (NAVE - Recarga combustible)")
        elif cell_value == 6:
            print(" (MUESTRA CIENTÍFICA)")
        elif cell_value == 0:
            print(" (Libre)")
        elif cell_value == 3:
            print(" (Rocoso)")
        elif cell_value == 4:
            print(" (Volcánico)")
        else:
            print()

print(f"\n{'='*60}")
print(f"ANÁLISIS:")
print(f"  - Posiciones en el camino: {len(resultado['path'])}")
print(f"  - Movimientos realizados: {len(resultado['path']) - 1}")
print(f"  - Nodos expandidos durante la búsqueda: {resultado['nodes_expanded']}")
print(f"{'='*60}")
