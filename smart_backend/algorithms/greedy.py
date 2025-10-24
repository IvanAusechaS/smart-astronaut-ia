"""
Greedy Best-First Search Algorithm
Greedy search that uses heuristic to find solutions by always expanding the most promising node first
"""

import heapq

def solve(params: dict):
    """
    Executes the Greedy Best-First Search algorithm to find a path that collects all 3 samples.
    Uses a heuristic function to prioritize which nodes to expand first, always choosing
    the most promising node based on the heuristic value.
    
    Args:
        params: Dictionary with problem parameters
               - map: 10x10 matrix with values 0-6
               - start: Tuple (row, column) of starting position
               - goal: NOT USED, objective is to collect 3 samples (value 6)
    
    Returns:
        dict: Result with found path and statistics
    """
    mapa = params.get("map", [])
    start = tuple(params.get("start", [0, 0]))
    
    # Basic validations
    if not mapa or len(mapa) != 10 or len(mapa[0]) != 10:
        return {
            "path": [],
            "nodes_expanded": 0,
            "cost": 0,
            "max_depth": 0,
            "message": "Invalid map"
        }
    
    # Find all samples (value 6)
    samples = set()
    for i in range(10):
        for j in range(10):
            if mapa[i][j] == 6:
                samples.add((i, j))
    
    if len(samples) != 3:
        return {
            "path": [],
            "nodes_expanded": 0,
            "cost": 0,
            "max_depth": 0,
            "message": f"Error: Expected 3 samples, found {len(samples)}"
        }
    
    def get_neighbors(pos, mapa):
        """Get valid neighbors of a position"""
        row, col = pos
        neighbors = []
        # Movements: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check map boundaries
            if 0 <= new_row < 10 and 0 <= new_col < 10:
                # Check that it's not an obstacle (value 1)
                if mapa[new_row][new_col] != 1:
                    neighbors.append((new_row, new_col))
        
        return neighbors
    
    def heuristic(pos, collected_samples, all_samples):
        """
        Heuristic function: Manhattan distance to the closest uncollected sample divided by 2.
        Returns 0 if all samples are collected.
        """
        if len(collected_samples) == 3:
            return 0
        
        remaining_samples = all_samples - collected_samples
        min_distance = float('inf')
        
        for sample in remaining_samples:
            distance = abs(pos[0] - sample[0]) + abs(pos[1] - sample[1])
            min_distance = min(min_distance, distance)
        
        return min_distance / 2
    
    # Initial state: (position, collected_samples_frozenset, fuel, has_taken_ship)
    initial_state = (start, frozenset(), 0, False)

    
    # Priority queue for Greedy: (heuristic_value, state, path)
    # We use a min-heap, so lower heuristic values have higher priority
    priority_queue = [(heuristic(start, frozenset(), samples), initial_state, [start])]
    
    # Set of visited states to avoid cycles
    visited = {initial_state}
    nodes_expanded = 0
    max_depth = 0
    
    while priority_queue:
        # Pop the node with the lowest heuristic value (most promising)
        heuristic_val, (pos_actual, collected_samples, fuel, has_taken_ship), path = heapq.heappop(priority_queue)
        max_depth = max(max_depth, len(path))
        
        # Check if we're at a sample and haven't collected it yet
        if pos_actual in samples and pos_actual not in collected_samples:
            collected_samples = frozenset(collected_samples | {pos_actual})
        
        # Check if we collected all samples (GOAL)
        if len(collected_samples) == 3:
            # Calculate path cost
            total_cost = 0
            current_fuel = 0
            
            for i in range(len(path) - 1):
                row, col = path[i + 1]
                cell = mapa[row][col]
                
                # If we're at the ship, refuel
                if cell == 5:
                    current_fuel = 20
                
                # Calculate movement cost
                if current_fuel > 0:
                    total_cost += 0.5
                    current_fuel -= 1
                else:
                    # Cost based on terrain
                    if cell == 0 or cell == 2 or cell == 6:
                        total_cost += 1
                    elif cell == 3:
                        total_cost += 3
                    elif cell == 4:
                        total_cost += 5
                    elif cell == 5:
                        total_cost += 1
            
            # Convert path to list of lists for JSON
            path_json = [list(pos) for pos in path]
            
            return {
                "path": path_json,
                "nodes_expanded": nodes_expanded,
                "cost": total_cost,
                "max_depth": max_depth,
                "message": "Solution found - 3 samples collected"
            }
        
        # Expand neighbors - only count as expanded if we actually generate children
        neighbors_added = 0
        for neighbor in get_neighbors(pos_actual, mapa):
            # Calculate new fuel and ship status
            new_fuel = fuel
            has_taken_ship_new = has_taken_ship
            
            # Can only take the ship if at cell 5 and hasn't taken it before
            if mapa[neighbor[0]][neighbor[1]] == 5 and not has_taken_ship:
                new_fuel = 20
                has_taken_ship_new = True
            elif new_fuel > 0:
                new_fuel -= 1
            
            new_state = (neighbor, collected_samples, new_fuel, has_taken_ship_new)
            
            # Only visit if we haven't been in this exact state
            if new_state not in visited:
                visited.add(new_state)
                # Calculate heuristic for the new state
                h_val = heuristic(neighbor, collected_samples, samples)
                heapq.heappush(priority_queue, (h_val, new_state, path + [neighbor]))
                neighbors_added += 1
        
        # Only count as expanded if we actually added neighbors to the queue
        if neighbors_added > 0:
            nodes_expanded += 1
    
    # No solution found
    return {
        "path": [],
        "nodes_expanded": nodes_expanded,
        "cost": 0,
        "max_depth": max_depth,
        "message": "No solution found to collect the 3 samples"
    }
