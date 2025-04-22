import heapq
import random
import math
import numpy as np
from utils import get_neighbors, manhattan_distance, find_zero, apply_action, update_belief_states, generate_partial_state, generate_full_belief_states, generate_initial_belief_states
from copy import deepcopy

# Thuật toán BFS
def bfs(start, goal):
    queue = [(start, [])]
    visited = set()
    while queue:
        state, path = queue.pop(0)
        if state == goal:
            return path + [state]
        visited.add(tuple(map(tuple, state)))
        for neighbor in get_neighbors(state):
            if tuple(map(tuple, neighbor)) not in visited:
                queue.append((neighbor, path + [state]))
    return None

# Thuật toán DFS
def dfs(start, goal, max_depth=50):
    stack = [(start, [], 0)]
    visited = set()
    while stack:
        state, path, depth = stack.pop()
        if state == goal:
            return path + [state]
        if depth >= max_depth:
            continue
        visited.add(tuple(map(tuple, state)))
        for neighbor in get_neighbors(state):
            if tuple(map(tuple, neighbor)) not in visited:
                stack.append((neighbor, path + [state], depth + 1))
    return None

# Thuật toán IDS
def ids(start, goal):
    def dls(state, path, depth):
        if depth == 0:
            return None
        if state == goal:
            return path + [state]
        visited.add(tuple(map(tuple, state)))
        for neighbor in get_neighbors(state):
            if tuple(map(tuple, neighbor)) not in visited:
                result = dls(neighbor, path + [state], depth - 1)
                if result:
                    return result
        return None
    depth = 0
    while True:
        visited = set()
        result = dls(start, [], depth)
        if result:
            return result
        depth += 1

# Thuật toán UCS
def ucs(start, goal):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        cost, state, path = heapq.heappop(queue)
        if state == goal:
            return path + [state]
        visited.add(tuple(map(tuple, state)))
        for neighbor in get_neighbors(state):
            if tuple(map(tuple, neighbor)) not in visited:
                heapq.heappush(queue, (cost + 1, neighbor, path + [state]))
    return None

# Thuật toán Greedy
def greedy(start, goal):
    queue = [(manhattan_distance(start, goal), start, [])]
    visited = set()
    while queue:
        _, state, path = heapq.heappop(queue)
        if state == goal:
            return path + [state]
        state_tuple = tuple(map(tuple, state))
        if state_tuple not in visited:
            visited.add(state_tuple)
            for neighbor in get_neighbors(state):
                heapq.heappush(queue, (manhattan_distance(neighbor, goal), neighbor, path + [state]))
    return None

# Thuật toán A*
def astar(start, goal):
    queue = [(manhattan_distance(start, goal), 0, start, [])]
    visited = set()
    while queue:
        _, cost, state, path = heapq.heappop(queue)
        if state == goal:
            return path + [state]
        state_tuple = tuple(map(tuple, state))
        if state_tuple not in visited:
            visited.add(state_tuple)
            for neighbor in get_neighbors(state):
                new_cost = cost + 1
                priority = new_cost + manhattan_distance(neighbor, goal)
                heapq.heappush(queue, (priority, new_cost, neighbor, path + [state]))
    return None

# Thuật toán IDA*
def ida_star(start, goal):
    def search(path, g, threshold):
        state = path[-1]
        f = g + manhattan_distance(state, goal)
        if f > threshold:
            return f, None
        if state == goal:
            return f, path
        min_threshold = float('inf')
        for neighbor in get_neighbors(state):
            if neighbor not in path:
                path.append(neighbor)
                t, result = search(path, g + 1, threshold)
                if result:
                    return t, result
                min_threshold = min(min_threshold, t)
                path.pop()
        return min_threshold, None
    threshold = manhattan_distance(start, goal)
    path = [start]
    while True:
        t, result = search(path, 0, threshold)
        if result:
            return result
        if t == float('inf'):
            return None
        threshold = t

# Thuật toán Simple Hill Climbing
def simple_hill_climbing(start, goal):
    current = start
    path = [current]
    visited = set()
    while current != goal:
        visited.add(tuple(map(tuple, current)))
        neighbors = get_neighbors(current)
        next_state = min(neighbors, key=lambda x: manhattan_distance(x, goal), default=None)
        if not next_state or manhattan_distance(next_state, goal) >= manhattan_distance(current, goal):
            return None
        current = next_state
        path.append(current)
    return path

# Thuật toán Steepest-Ascent Hill Climbing
def steepest_ascent_hill_climbing(start, goal):
    current = start
    path = [current]
    visited = set()
    while current != goal:
        visited.add(tuple(map(tuple, current)))
        neighbors = [n for n in get_neighbors(current) if tuple(map(tuple, n)) not in visited]
        if not neighbors:
            return None
        next_state = min(neighbors, key=lambda x: manhattan_distance(x, goal))
        if manhattan_distance(next_state, goal) >= manhattan_distance(current, goal):
            return None
        current = next_state
        path.append(current)
    return path

# Thuật toán Stochastic Hill Climbing
def stochastic_hill_climbing(start, goal):
    current = start
    path = [current]
    visited = set()
    while current != goal:
        visited.add(tuple(map(tuple, current)))
        neighbors = get_neighbors(current)
        better_neighbors = [n for n in neighbors if manhattan_distance(n, goal) < manhattan_distance(current, goal)]
        if not better_neighbors:
            return None
        current = random.choice(better_neighbors)
        path.append(current)
    return path

# Thuật toán Simulated Annealing
def simulated_annealing(start, goal, T=100, cooling_rate=0.99, min_T=0.01, max_steps=10000):
    def optimize_path(path):
        if len(path) <= 1:
            return path
        optimized_path = [path[0]]
        moves = []
        for i in range(1, len(path)):
            prev_state = optimized_path[-1]
            curr_state = path[i]
            zero_row_prev, zero_col_prev = find_zero(prev_state)
            zero_row_curr, zero_col_curr = find_zero(curr_state)
            if zero_row_curr == zero_row_prev - 1:
                move = "up"
            elif zero_row_curr == zero_row_prev + 1:
                move = "down"
            elif zero_col_curr == zero_col_prev - 1:
                move = "left"
            elif zero_col_curr == zero_col_prev + 1:
                move = "right"
            else:
                continue
            if moves and ((move == "up" and moves[-1] == "down") or 
                          (move == "down" and moves[-1] == "up") or 
                          (move == "left" and moves[-1] == "right") or 
                          (move == "right" and moves[-1] == "left")):
                moves.pop()
                optimized_path.pop()
            else:
                moves.append(move)
                optimized_path.append(curr_state)
        return optimized_path

    current_state = [list(row) for row in start]
    current_cost = manhattan_distance(current_state, goal)
    path = [current_state]
    visited = {tuple(map(tuple, current_state))}
    step = 0
    while T > min_T and step < max_steps:
        step += 1
        neighbors = [n for n in get_neighbors(current_state) if tuple(map(tuple, n)) not in visited]
        if not neighbors:
            current_state = [list(row) for row in start]
            current_cost = manhattan_distance(current_state, goal)
            path = [current_state]
            visited = {tuple(map(tuple, current_state))}
            T *= 0.5
            continue
        neighbors_with_cost = [(n, manhattan_distance(n, goal)) for n in neighbors]
        neighbors_with_cost.sort(key=lambda x: x[1])
        if random.uniform(0, 1) < 0.7:
            next_state, next_cost = neighbors_with_cost[0]
        else:
            next_state, next_cost = random.choice(neighbors_with_cost)
        delta_cost = next_cost - current_cost
        if delta_cost < 0:
            current_state = [list(row) for row in next_state]
            current_cost = next_cost
            path.append(current_state)
            visited.add(tuple(map(tuple, current_state)))
        else:
            probability = math.exp(-delta_cost / T)
            if random.uniform(0, 1) < probability:
                current_state = [list(row) for row in next_state]
                current_cost = next_cost
                path.append(current_state)
                visited.add(tuple(map(tuple, current_state)))
        T *= cooling_rate
        if np.array_equal(current_state, goal):
            print("Reached goal state!")
            return optimize_path(path)
    print("Failed to reach goal state.")
    return None

# Thuật toán Beam Search
def beam_search(start, goal, beam_width=3):
    queue = [(manhattan_distance(start, goal), start, [start])]
    visited = set()
    visited.add(tuple(map(tuple, start)))
    while queue:
        queue = sorted(queue, key=lambda x: x[0])[:beam_width]
        next_queue = []
        for _, state, path in queue:
            if np.array_equal(state, goal):
                return path
            for neighbor in get_neighbors(state):
                state_tuple = tuple(map(tuple, neighbor))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    heuristic = manhattan_distance(neighbor, goal)
                    next_queue.append((heuristic, neighbor, path + [neighbor]))
        queue = next_queue
    return None

# Thuật toán Genetic Algorithm
def genetic_algorithm(start, goal, population_size=100, sequence_length=20, generations=100, mutation_rate=0.3):
    def apply_moves(state, moves):
        current_state = [list(row) for row in state]
        path = [current_state]
        visited = {tuple(map(tuple, current_state))}
        for move in moves:
            zero_row, zero_col = find_zero(current_state)
            new_state = [list(row) for row in current_state]
            if move == "up" and zero_row > 0:
                new_state[zero_row][zero_col], new_state[zero_row-1][zero_col] = new_state[zero_row-1][zero_col], new_state[zero_row][zero_col]
            elif move == "down" and zero_row < 2:
                new_state[zero_row][zero_col], new_state[zero_row+1][zero_col] = new_state[zero_row+1][zero_col], new_state[zero_row][zero_col]
            elif move == "left" and zero_col > 0:
                new_state[zero_row][zero_col], new_state[zero_row][zero_col-1] = new_state[zero_row][zero_col-1], new_state[zero_row][zero_col]
            elif move == "right" and zero_col < 2:
                new_state[zero_row][zero_col], new_state[zero_row][zero_col+1] = new_state[zero_row][zero_col+1], new_state[zero_row][zero_col]
            else:
                continue
            state_tuple = tuple(map(tuple, new_state))
            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            current_state = new_state
            path.append(current_state)
            if np.array_equal(current_state, goal):
                return path
        return path

    def optimize_path(path):
        if len(path) <= 1:
            return path
        optimized_path = [path[0]]
        moves = []
        for i in range(1, len(path)):
            prev_state = optimized_path[-1]
            curr_state = path[i]
            zero_row_prev, zero_col_prev = find_zero(prev_state)
            zero_row_curr, zero_col_curr = find_zero(curr_state)
            if zero_row_curr == zero_row_prev - 1:
                move = "up"
            elif zero_row_curr == zero_row_prev + 1:
                move = "down"
            elif zero_col_curr == zero_col_prev - 1:
                move = "left"
            elif zero_col_curr == zero_col_prev + 1:
                move = "right"
            else:
                continue
            if moves and ((move == "up" and moves[-1] == "down") or 
                          (move == "down" and moves[-1] == "up") or 
                          (move == "left" and moves[-1] == "right") or 
                          (move == "right" and moves[-1] == "left")):
                moves.pop()
                optimized_path.pop()
            else:
                moves.append(move)
                optimized_path.append(curr_state)
        return optimized_path

    moves = ["up", "down", "left", "right"]
    population = [[random.choice(moves) for _ in range(sequence_length)] for _ in range(population_size)]
    for generation in range(generations):
        fitness_scores = []
        for individual in population:
            path = apply_moves(start, individual)
            final_state = path[-1]
            if np.array_equal(final_state, goal):
                return optimize_path(path)
            fitness = manhattan_distance(final_state, goal) + len(path) * 0.5
            fitness_scores.append((fitness, individual, path))
        if not fitness_scores:
            return None
        fitness_scores.sort(key=lambda x: x[0])
        num_parents = population_size // 2
        parents = [individual for _, individual, _ in fitness_scores[:num_parents]]
        new_population = parents[:]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            cut_point = random.randint(1, sequence_length-1)
            child1 = parent1[:cut_point] + parent2[cut_point:]
            child2 = parent2[:cut_point] + parent1[cut_point:]
            for child in [child1, child2]:
                for i in range(sequence_length):
                    if random.random() < mutation_rate:
                        child[i] = random.choice(moves)
            new_population.extend([child1, child2])
        population = new_population[:population_size]
    return None

# Thuật toán AND-OR Search
def and_or_search(start, goal, max_depth=100):
    def solve(state, path, visited, depth):
        if state == goal:
            return path + [state]
        if depth >= max_depth:
            return None
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited:
            return None
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            result = solve(neighbor, path + [state], visited, depth + 1)
            if result is not None:
                return result
        return None
    visited = set()
    return solve(start, [], visited, 0)

# Thuật toán Belief State Search
def belief_state_search(start_state, goal_state, max_steps=1000, use_partial=True):
    real_state = deepcopy(start_state)
    real_path = [real_state]
    
    if use_partial:
        partial_state = generate_partial_state(start_state, num_unknown=1)
        print(f"Partial State (Có None): {partial_state}")
        known_positions = [partial_state[i][j] for i in range(3) for j in range(3) if partial_state[i][j] is not None]
        belief_states = generate_initial_belief_states(partial_state, known_positions, goal_state)
    else:
        partial_state = start_state
        print(f"Partial State (Không None): {partial_state}")
        belief_states = generate_full_belief_states(start_state, goal_state)
    
    if not belief_states:
        print("Không tạo được belief states khả thi.")
        return None
    
    print(f"Số belief states ban đầu: {len(belief_states)}")
    
    queue = [(manhattan_distance(real_state, goal_state), 0, real_state, belief_states, real_path, [])]
    visited = set()
    actions = ["up", "down", "left", "right"]
    step_count = 0
    
    while queue and step_count < max_steps:
        f_score, g_score, real_state, belief_states, path, action_sequence = heapq.heappop(queue)
        step_count += 1
        
        state_tuple = tuple(map(tuple, real_state))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        
        if real_state == goal_state:
            print(f"Đạt goal_state sau {len(path)-1} bước.")
            return path
        
        for action in actions:
            new_real_state = apply_action(real_state, action)
            if new_real_state:
                new_belief_states = update_belief_states(belief_states, action)
                if not new_belief_states:
                    continue
                new_g_score = g_score + 1
                new_f_score = new_g_score + manhattan_distance(new_real_state, goal_state)
                new_path = path + [new_real_state]
                new_actions = action_sequence + [action]
                heapq.heappush(queue, (new_f_score, new_g_score, new_real_state, new_belief_states, new_path, new_actions))
    
    print(f"Không tìm thấy lời giải sau {step_count} bước.")
    return None