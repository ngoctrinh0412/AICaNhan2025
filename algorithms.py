import heapq
import random
import math
import numpy as np
from utils import get_neighbors, manhattan_distance, find_zero, apply_action, update_belief_states, generate_partial_state, generate_full_belief_states, generate_initial_belief_states
from copy import deepcopy
from collections import defaultdict

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
def belief_state_search(start_state, goal_state, max_steps=1000):
    real_state = deepcopy(start_state)
    partial_state = generate_partial_state(start_state, num_unknown=2)
    real_path = [real_state]
    
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
        
        if all(state == goal_state for state in belief_states):
            print(f"Đạt goal_state sau {len(path)-1} bước.")
            return path
        
        for action in actions:
            new_real_state = apply_action(real_state, action)
            if new_real_state:
                new_belief_states = update_belief_states(belief_states, action, real_state=None, partial_state=partial_state)
                if not new_belief_states:
                    continue
                new_g_score = g_score + 1
                new_f_score = new_g_score + manhattan_distance(new_real_state, goal_state)
                new_path = path + [new_real_state]
                new_actions = action_sequence + [action]
                heapq.heappush(queue, (new_f_score, new_g_score, new_real_state, new_belief_states, new_path, new_actions))
    
    print(f"Không tìm thấy lời giải sau {step_count} bước.")
    return None

# Thuật toán Searching with Partial Observation
def searching_with_partial_observation(start_state, goal_state, max_steps=1000):
    real_state = deepcopy(start_state)
    real_path = [real_state]
    
    partial_state = generate_partial_state(start_state, num_unknown=2)
    print(f"Partial State (Có None): {partial_state}")
    known_positions = [partial_state[i][j] for i in range(3) for j in range(3) if partial_state[i][j] is not None]
    belief_states = generate_initial_belief_states(partial_state, known_positions, goal_state)
    
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
        
        # Kiểm tra nếu real_state đã đạt goal_state
        if real_state == goal_state:
            print(f"Đạt goal_state sau {len(path)-1} bước.")
            return path
        
        for action in actions:
            new_real_state = apply_action(real_state, action)
            if new_real_state:
                new_belief_states = update_belief_states(belief_states, action, new_real_state, partial_state=partial_state)
                if not new_belief_states:
                    print("Không còn belief states khả thi sau hành động:", action)
                    return None  # Không còn trạng thái khả thi, dừng thuật toán
                new_g_score = g_score + 1
                new_f_score = new_g_score + manhattan_distance(new_real_state, goal_state)
                new_path = path + [new_real_state]
                new_actions = action_sequence + [action]
                heapq.heappush(queue, (new_f_score, new_g_score, new_real_state, new_belief_states, new_path, new_actions))
    
    print(f"Không tìm thấy lời giải sau {step_count} bước.")
    return None

# Thuật toán Backtracking Search (dựa trên DFS)
def backtracking_search(start, goal, max_depth=100):
    def backtrack(state, path, visited, depth):
        # Kiểm tra trạng thái hiện tại có phải là đích không
        if np.array_equal(state, goal):
            return path + [state]
        
        # Kiểm tra độ sâu tối đa để tránh vòng lặp vô hạn
        if depth >= max_depth:
            return None
        
        # Thêm trạng thái hiện tại vào tập đã thăm
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited:
            return None
        visited.add(state_tuple)
        
        # Lấy các trạng thái lân cận (các di chuyển khả thi)
        neighbors = get_neighbors(state)
        for neighbor in neighbors:
            # Thử di chuyển này và quay lui nếu cần
            result = backtrack(neighbor, path + [state], visited, depth + 1)
            if result is not None:
                return result
        
        # Nếu không tìm thấy đường đi, quay lui
        return None

    visited = set()
    return backtrack(start, [], visited, 0)

# Thuật toán Backtracking with Forward Checking
def backtracking_with_forward_checking(start, goal, max_depth=100):
    def forward_check(state, domains):
        new_domains = domains  # Tránh deepcopy nếu không cần thiết
        zero_pos = find_zero(state)
        zero_row, zero_col = zero_pos

    # Chỉ kiểm tra các ô lân cận của ô trống
        neighbors_pos = []
        if zero_row > 0:
            neighbors_pos.append((zero_row - 1, zero_col))
        if zero_row < 2:
            neighbors_pos.append((zero_row + 1, zero_col))
        if zero_col > 0:
            neighbors_pos.append((zero_row, zero_col - 1))
        if zero_col < 2:
            neighbors_pos.append((zero_row, zero_col + 1))

    # Cập nhật miền giá trị của các ô lân cận
        for pos in neighbors_pos:
            i, j = pos
            val = state[i][j]
        # Loại bỏ giá trị này khỏi miền của các ô khác
            for other_pos in variables:
                if other_pos != pos and other_pos != (zero_row, zero_col) and val in new_domains[other_pos]:
                    new_domains[other_pos].remove(val)
                    if not new_domains[other_pos]:
                        return False, new_domains
        return True, new_domains

    def backtrack(state, path, visited, domains, depth):
        if np.array_equal(state, goal):
            return path + [state]
        if depth >= max_depth:
            return None
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited:
            return None
        visited.add(state_tuple)

    # Cập nhật miền giá trị dựa trên trạng thái hiện tại
        new_domains = {pos: domains[pos] for pos in domains}  # Sao chép nông
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                pos = (i, j)
                new_domains[pos] = [val]

        consistent, new_domains = forward_check(state, new_domains)
        if not consistent:
            return None

        neighbors = get_neighbors(state)
    # Sắp xếp neighbors theo Manhattan Distance
        neighbors.sort(key=lambda x: manhattan_distance(x, goal))
        for neighbor in neighbors:
            consistent, temp_domains = forward_check(neighbor, new_domains)
            if consistent:
                result = backtrack(neighbor, path + [state], visited, temp_domains, depth + 1)
                if result is not None:
                    return result
        return None

    # Khởi tạo miền giá trị
    variables = [(i, j) for i in range(3) for j in range(3)]
    domains = {pos: list(range(9)) for pos in variables}
    neighbors = {pos: [other_pos for other_pos in variables if other_pos != pos] for pos in variables}
    visited = set()
    return backtrack(start, [], visited, domains, 0)

def ac3(state, goal_state, constraints):
    """
    AC-3 algorithm for constraint propagation.
    - state: Current state of the puzzle (3x3 grid).
    - goal_state: Goal state (not used directly in AC-3 but included for consistency).
    - constraints: Function to check constraints between variables (e.g., uniqueness of values).
    Returns: True if arc-consistent, False if no solution.
    """
    # Convert state to a CSP representation
    variables = [(i, j) for i in range(3) for j in range(3)]  # Variables are positions (i, j)
    domains = {}
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                domains[(i, j)] = list(range(9))  # Empty cell can take any value
            else:
                domains[(i, j)] = [state[i][j]]  # Fixed value

    # Neighbors: Each position is constrained with all other positions (uniqueness constraint)
    neighbors = {var: [other_var for other_var in variables if other_var != var] for var in variables}

    # Initialize queue with all arcs
    queue = [(xi, xj) for xi in variables for xj in neighbors[xi]]

    while queue:
        (xi, xj) = queue.pop(0)
        if revise(domains, xi, xj, constraints):
            if len(domains[xi]) == 0:
                return False, domains
            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True, domains

def revise(domains, xi, xj, constraints):
    """
    Revise the domain of xi to satisfy the constraint between xi and xj.
    Returns True if the domain of xi is revised.
    """
    revised = False
    values_to_remove = []
    for x in domains[xi]:
        # Check if there exists a value y in xj's domain that satisfies the constraint
        if not any(constraints(xi, x, xj, y) for y in domains[xj]):
            values_to_remove.append(x)
            revised = True
    for x in values_to_remove:
        domains[xi].remove(x)
    return revised

def constraints(xi, x, xj, y):
    """
    Constraint: Two positions cannot have the same value unless they are both 0 (empty).
    Additionally, ensure the empty tile can only move to adjacent positions.
    """
    if x == 0 or y == 0:
        # If one is the empty tile, check adjacency constraint
        (i1, j1), (i2, j2) = xi, xj
        if x == 0 and y != 0:
            # xi is empty, check if xj is adjacent
            return (abs(i1 - i2) + abs(j1 - j2)) == 1
        if y == 0 and x != 0:
            # xj is empty, check if xi is adjacent
            return (abs(i1 - i2) + abs(j1 - j2)) == 1
        return True
    return x != y  # Uniqueness constraint

def is_goal(state, goal_state):
    """
    Kiểm tra xem trạng thái hiện tại có phải là trạng thái mục tiêu không.
    - state: Trạng thái hiện tại.
    - goal_state: Trạng thái mục tiêu.
    Trả về: True nếu trạng thái hiện tại là mục tiêu, False nếu không.
    """
    return state == goal_state

def maintaining_arc_consistency(state, goal_state):
    """
    Thuật toán Maintaining Arc-Consistency (MAC) cải tiến cho bài toán 8-Puzzle.
    Sử dụng tìm kiếm không gian trạng thái với heuristic (Manhattan distance) để dẫn dắt tìm kiếm.
    - state: Trạng thái ban đầu (lưới 3x3).
    - goal_state: Trạng thái mục tiêu (lưới 3x3).
    Trả về: Danh sách các bước từ trạng thái ban đầu đến trạng thái mục tiêu.
    """
    def backtrack(current_state, visited, depth_limit):
        """
        Tìm kiếm backtracking với giới hạn độ sâu để tìm đường đi từ trạng thái hiện tại đến trạng thái mục tiêu.
        - current_state: Trạng thái hiện tại.
        - visited: Tập hợp các trạng thái đã duyệt qua (dạng chuỗi).
        - depth_limit: Giới hạn độ sâu tìm kiếm.
        Trả về: Danh sách các trạng thái từ trạng thái hiện tại đến mục tiêu, hoặc None nếu không tìm thấy.
        """
        if is_goal(current_state, goal_state):
            return [current_state]

        state_str = str(current_state)
        if state_str in visited:
            return None
        visited.add(state_str)

        # Lấy các trạng thái kế tiếp
        neighbors = get_neighbors(current_state)
        # Sắp xếp các trạng thái kế tiếp theo khoảng cách Manhattan để ưu tiên trạng thái gần mục tiêu
        neighbors.sort(key=lambda s: manhattan_distance(s, goal_state))

        for next_state in neighbors:
            sub_path = backtrack(next_state, visited, depth_limit)
            if sub_path is not None:
                return [current_state] + sub_path

        return None

    # Bắt đầu tìm kiếm với độ sâu tăng dần (giống Iterative Deepening Search)
    visited = set()
    depth_limit = 0
    max_depth = 100  # Giới hạn độ sâu tối đa để tránh vòng lặp vô hạn

    while depth_limit <= max_depth:
        result = backtrack(state, visited.copy(), depth_limit)
        if result is not None:
            # Loại bỏ các trạng thái trùng lặp nhưng vẫn giữ nguyên thứ tự
            seen = set()
            unique_path = []
            for s in result:
                state_str = str(s)
                if state_str not in seen:
                    seen.add(state_str)
                    unique_path.append(s)
            return unique_path
        depth_limit += 1

    return []  # Không tìm thấy lời giải

def q_learning(state, goal_state, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
    """
    Thuật toán Q-Learning cho bài toán 8-Puzzle.
    - state: Trạng thái ban đầu (lưới 3x3).
    - goal_state: Trạng thái mục tiêu (lưới 3x3).
    - episodes: Số lần huấn luyện (mặc định: 1000).
    - alpha: Tốc độ học (learning rate, mặc định: 0.1).
    - gamma: Hệ số giảm giá (discount factor, mặc định: 0.9).
    - epsilon: Tỷ lệ khám phá (exploration rate, mặc định: 0.1).
    Trả về: Danh sách các bước từ trạng thái ban đầu đến trạng thái mục tiêu.
    """
    # Chuyển trạng thái thành dạng chuỗi để lưu trong Q-Table
    def state_to_str(state):
        return str([[state[i][j] for j in range(3)] for i in range(3)])

    # Khởi tạo Q-Table (lưu chỉ mục của action trong possible_actions)
    q_table = defaultdict(lambda: defaultdict(float))

    # Hàm chọn hành động dựa trên epsilon-greedy
    def choose_action(state_str, possible_actions):
        if random.uniform(0, 1) < epsilon:  # Khám phá (exploration)
            return random.choice(possible_actions)
        else:  # Khai thác (exploitation)
            q_values = q_table[state_str]
            if not q_values:  # Nếu chưa có giá trị Q nào, chọn ngẫu nhiên
                return random.choice(possible_actions)
            max_q = max(q_values.values(), default=0)
            # Lấy chỉ mục action có Q-value cao nhất
            best_indices = [idx for idx, q in q_values.items() if q == max_q]
            chosen_idx = random.choice(best_indices)
            return possible_actions[chosen_idx]

    # Huấn luyện Q-Learning
    for episode in range(episodes):
        current_state = [row[:] for row in state]  # Sao chép trạng thái ban đầu
        current_state_str = state_to_str(current_state)
        steps = 0
        max_steps = 1000  # Giới hạn số bước tối đa trong mỗi episode

        while steps < max_steps:
            # Lấy các hành động có thể (các trạng thái kế tiếp)
            possible_actions = get_neighbors(current_state)
            if not possible_actions:  # Nếu không có hành động nào, thoát
                break

            # Chọn hành động
            action = choose_action(current_state_str, possible_actions)
            action_idx = possible_actions.index(action)  # Lấy chỉ mục của action

            # Tính phần thưởng
            reward = -1  # Phạt cho mỗi bước di chuyển
            if is_goal(action, goal_state):
                reward = 100  # Thưởng lớn nếu đạt mục tiêu
                next_state = action
            else:
                next_state = action

            # Cập nhật Q-Table với chỉ mục
            next_state_str = state_to_str(next_state)
            old_q = q_table[current_state_str][action_idx]
            future_q = max(q_table[next_state_str].values()) if q_table[next_state_str] else 0
            new_q = old_q + alpha * (reward + gamma * future_q - old_q)
            q_table[current_state_str][action_idx] = new_q

            # Chuyển sang trạng thái mới
            current_state = [row[:] for row in next_state]  # Đảm bảo copy danh sách
            current_state_str = next_state_str
            steps += 1

            # Thoát nếu đạt mục tiêu
            if is_goal(current_state, goal_state):
                break

    # Sử dụng Q-Table đã huấn luyện để tìm đường đi
    path = [state]
    current_state = [row[:] for row in state]
    current_state_str = state_to_str(current_state)
    visited = set()
    visited.add(current_state_str)
    max_steps = 100  # Giới hạn số bước tối đa khi tìm đường

    for _ in range(max_steps):
        possible_actions = get_neighbors(current_state)
        if not possible_actions:
            break

        # Chọn hành động tốt nhất (khai thác)
        q_values = q_table[current_state_str]
        if not q_values:  # Nếu không có giá trị Q, thoát
            break

        max_q = max(q_values.values(), default=0)
        best_indices = [idx for idx, q in q_values.items() if q == max_q]
        if not best_indices:
            break

        chosen_idx = random.choice(best_indices)
        next_state = possible_actions[chosen_idx]

        next_state_str = state_to_str(next_state)

        path.append(next_state)
        current_state = [row[:] for row in next_state]
        current_state_str = next_state_str

        if is_goal(current_state, goal_state):
            break

        if next_state_str in visited:
            break
        visited.add(next_state_str)

    return path if path else None