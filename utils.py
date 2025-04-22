import pygame
import tkinter as tk
from PIL import Image, ImageTk
from constants import WIDTH, HEIGHT, TILE_SIZE, COLORS
import random
from copy import deepcopy

# Hàm vẽ trạng thái lên Pygame Surface
def draw_board(surface, state):
    surface.fill(COLORS["WHITE"]["rgb"])
    font = pygame.font.Font(None, 70)  # Tăng kích thước font
    for row in range(3):
        for col in range(3):
            num = state[row][col]
            rect = (col * TILE_SIZE + 5, row * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10)
            
            if num != 0:
                # Thêm bóng đổ
                pygame.draw.rect(surface, COLORS["SHADOW"]["rgb"], (rect[0] + 3, rect[1] + 3, rect[2], rect[3]), border_radius=15)
                pygame.draw.rect(surface, COLORS["PRIMARY"]["rgb"], rect, border_radius=15)
                text = font.render(str(num), True, COLORS["BLACK"]["rgb"])
                text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                surface.blit(text, text_rect)
            else:
                pygame.draw.rect(surface, COLORS["GRAY"]["rgb"], (col * TILE_SIZE + 2, row * TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4), border_radius=12)

# Hàm cập nhật hình ảnh lên Tkinter Canvas
def update_canvas(canvas, surface):
    image_data = pygame.image.tostring(surface, "RGB")
    image = Image.frombytes("RGB", (WIDTH, HEIGHT), image_data)
    photo = ImageTk.PhotoImage(image)
    canvas.photo = photo
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Hàm hiển thị trạng thái
def display_state(frame, state):
    for widget in frame.winfo_children():
        widget.destroy()
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            label = tk.Label(frame, text=str(value) if value != 0 else "", 
            width=4, height=2, font=("Helvetica", 20, "bold"), 
            bg=COLORS["PRIMARY"]["hex"] if value != 0 else COLORS["GRAY"]["hex"],
            fg=COLORS["BLACK"]["hex"], relief="flat",
            borderwidth=0, highlightthickness=2, highlightbackground=COLORS["SHADOW"]["hex"])
            label.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

# Hàm tìm vị trí ô trống
def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

# Hàm tạo trạng thái lân cận
# Hàm tạo trạng thái lân cận
def get_neighbors(state):
    neighbors = []
    zero_pos = find_zero(state)
    if zero_pos is None:
        return neighbors
    zero_row, zero_col = zero_pos
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, Xuống, Trái, Phải
    for dr, dc in moves:
        new_row, new_col = zero_row + dr, zero_col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [list(row) for row in state]
            new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[zero_row][zero_col]
            neighbors.append(new_state)
    return neighbors
# Hàm heuristic (Manhattan Distance)
def manhattan_distance(state, goal):
    total_distance = 0
    goal_positions = {goal[i][j]: (i, j) for i in range(3) for j in range(3)}
    for i in range(3):
        for j in range(3):
            num = state[i][j]
            if num != 0:
                goal_x, goal_y = goal_positions[num]
                total_distance += abs(i - goal_x) + abs(j - goal_y)
    return total_distance

# Hàm kiểm tra tính khả thi
def is_solvable(state, goal):
    def count_inversions(state):
        flat = [num for row in state for num in row if num != 0]
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        return inversions
    state_inv = count_inversions(state)
    goal_inv = count_inversions(goal)
    return (state_inv % 2) == (goal_inv % 2)

# Hàm tạo partial_state
def generate_partial_state(full_state, num_unknown=1):
    partial = [row[:] for row in full_state]
    positions = [(i, j) for i in range(3) for j in range(3) if (i, j) != find_zero(full_state)]
    unknown_positions = random.sample(positions, min(num_unknown, len(positions)))
    for i, j in unknown_positions:
        partial[i][j] = None
    return partial

# Hàm tạo belief states cho trạng thái đầy đủ
def generate_full_belief_states(full_state, goal_state, max_states=5):
    belief_states = [full_state]
    neighbors = get_neighbors(full_state)
    for neighbor in neighbors:
        if is_solvable(neighbor, goal_state):
            belief_states.append(neighbor)
            if len(belief_states) >= max_states:
                break
    return belief_states

# Hàm tạo belief states cho trạng thái có None
def generate_initial_belief_states(partial_state, known_positions, goal_state):
    from itertools import permutations
    all_numbers = set(range(9))
    used_numbers = set(known_positions)
    available_numbers = list(all_numbers - used_numbers)
    belief_states = []
    for perm in permutations(available_numbers):
        state = [row[:] for row in partial_state]
        perm_idx = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] is None:
                    state[i][j] = perm[perm_idx]
                    perm_idx += 1
        if is_solvable(state, goal_state):
            belief_states.append(state)
    return belief_states[:5]

# Hàm áp dụng hành động
def apply_action(state, action):
    zero_row, zero_col = find_zero(state)
    moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
    dr, dc = moves.get(action, (0, 0))
    new_row, new_col = zero_row + dr, zero_col + dc
    if 0 <= new_row < 3 and 0 <= new_col < 3:
        new_state = [row[:] for row in state]
        new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[zero_row][zero_col]
        return new_state
    return None

# Hàm cập nhật belief states dựa trên hành động thực tế
def update_belief_states(belief_states, real_action):
    new_belief_states = []
    for state in belief_states:
        new_state = apply_action(state, real_action)
        if new_state:
            new_belief_states.append(new_state)
    return new_belief_states