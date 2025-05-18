import pygame
import tkinter as tk
from constants import WIDTH, HEIGHT, TILE_SIZE, COLORS
import random

# Hàm vẽ trạng thái lên Pygame Surface
def draw_board(surface, state):
    surface.fill(COLORS["WHITE"]["hex"])
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value == 0:
                color = COLORS["GRAY"]["hex"]
            else:
                color = "#4A90E2"
            pygame.draw.rect(surface, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - 5, TILE_SIZE - 5), border_radius=10)
            if value != 0:
                font = pygame.font.SysFont("Helvetica", 40, bold=True)
                text = font.render(str(value), True, COLORS["WHITE"]["hex"])
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))
                surface.blit(text, text_rect)

# Hàm cập nhật hình ảnh lên Tkinter Canvas
def update_canvas(canvas, surface):
    pygame.image.save(surface, "temp.png")
    img = tk.PhotoImage(file="temp.png")
    canvas.create_image(WIDTH // 2, HEIGHT // 2, image=img)
    canvas.image = img

# Hàm hiển thị trạng thái
def display_state(parent, state):
    for widget in parent.winfo_children():
        widget.destroy()
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            bg_color = COLORS["GRAY"]["hex"] if value == 0 else "#4A90E2"
            fg_color = COLORS["WHITE"]["hex"]
            btn = tk.Button(parent, text=str(value) if value != 0 else "", font=("Helvetica", 16, "bold"),
                            width=2, height=1, bg=bg_color, fg=fg_color, relief="raised", bd=3,
                            highlightbackground=COLORS["SHADOW"]["hex"])
            btn.grid(row=i, column=j, padx=3, pady=3, ipadx=10, ipady=10)
    for i in range(3):
        parent.grid_rowconfigure(i, weight=1)
        parent.grid_columnconfigure(i, weight=1)

# Hàm tìm vị trí ô trống
def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

# Hàm tạo trạng thái lân cận
def get_neighbors(state):
    def swap(state, i1, j1, i2, j2):
        new_state = [row[:] for row in state]
        new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
        return new_state
    neighbors = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                if i > 0:
                    neighbors.append(swap(state, i, j, i-1, j))
                if i < 2:
                    neighbors.append(swap(state, i, j, i+1, j))
                if j > 0:
                    neighbors.append(swap(state, i, j, i, j-1))
                if j < 2:
                    neighbors.append(swap(state, i, j, i, j+1))
                break
    return neighbors

# Hàm heuristic (Manhattan Distance)
def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                for m in range(3):
                    for n in range(3):
                        if goal[m][n] == value:
                            distance += abs(i - m) + abs(j - n)
                            break
    return distance

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
    # Kiểm tra tính hợp lệ của full_state: không có số trùng lặp (trừ 0)
    flat_state = [num for row in full_state for num in row]
    non_zero_nums = [num for num in flat_state if num != 0]
    if len(non_zero_nums) != len(set(non_zero_nums)):
        raise ValueError("full_state chứa các số trùng lặp, không hợp lệ cho 8-puzzle!")
    
    partial_state = [row[:] for row in full_state]
    positions = [(i, j) for i in range(3) for j in range(3) if full_state[i][j] != 0]
    if len(positions) < num_unknown:
        return partial_state
    unknown_positions = random.sample(positions, min(num_unknown, len(positions)))
    for i, j in unknown_positions:
        partial_state[i][j] = None
    return partial_state

# Hàm tạo belief states cho trạng thái đầy đủ
def generate_full_belief_states(start_state, goal_state):
    partial_state = generate_partial_state(start_state, num_unknown=1)  # Giả định 1 ô không xác định
    known_positions = [partial_state[i][j] for i in range(3) for j in range(3) if partial_state[i][j] is not None]
    belief_states = generate_initial_belief_states(partial_state, known_positions, goal_state)
    return belief_states

# Hàm tạo belief states cho trạng thái có None
def generate_initial_belief_states(partial_state, known_positions, goal_state):
    belief_states = []
    # Loại bỏ trùng lặp trong known_positions (trừ số 0)
    seen = set()
    unique_known = []
    for num in known_positions:
        if num == 0:
            unique_known.append(num)
        elif num not in seen:
            seen.add(num)
            unique_known.append(num)
    known_positions = unique_known

    # Tạo danh sách các số khả thi
    available_numbers = [i for i in range(9) if i not in known_positions or i == 0]
    # Đảm bảo available_numbers không chứa trùng lặp
    available_numbers = list(set(available_numbers))
    
    def is_valid_state(state):
        flat = [num for row in state for num in row]
        # Đảm bảo không có số trùng lặp và có ô trống (0)
        return len(set(flat)) == len(flat) and 0 in flat
    
    def generate_states(state, pos_idx, available_nums):
        if pos_idx >= 9:
            if is_valid_state(state):
                belief_states.append(state)
            return
        i, j = divmod(pos_idx, 3)
        if partial_state[i][j] is not None:
            generate_states(state, pos_idx + 1, available_nums)
            return
        
        # Thử tất cả các số khả thi tại vị trí (i, j)
        for num in available_nums:
            if num in available_nums:  # Kiểm tra để chắc chắn num tồn tại
                new_state = [row[:] for row in state]
                new_state[i][j] = num
                # Cập nhật danh sách số còn lại
                new_available = available_nums.copy()
                new_available.remove(num)  # Xóa num khỏi new_available
                generate_states(new_state, pos_idx + 1, new_available)
    
    # Khởi tạo trạng thái ban đầu
    initial_state = [[partial_state[i][j] if partial_state[i][j] is not None else 0 for j in range(3)] for i in range(3)]
    generate_states(initial_state, 0, available_numbers)
    return belief_states

# Hàm áp dụng hành động
def apply_action(state, action):
    zero_row, zero_col = find_zero(state)
    if not zero_row:
        return None
    new_state = [row[:] for row in state]
    if action == "up" and zero_row > 0:
        new_state[zero_row][zero_col], new_state[zero_row-1][zero_col] = new_state[zero_row-1][zero_col], new_state[zero_row][zero_col]
        return new_state
    elif action == "down" and zero_row < 2:
        new_state[zero_row][zero_col], new_state[zero_row+1][zero_col] = new_state[zero_row+1][zero_col], new_state[zero_row][zero_col]
        return new_state
    elif action == "left" and zero_col > 0:
        new_state[zero_row][zero_col], new_state[zero_row][zero_col-1] = new_state[zero_row][zero_col-1], new_state[zero_row][zero_col]
        return new_state
    elif action == "right" and zero_col < 2:
        new_state[zero_row][zero_col], new_state[zero_row][zero_col+1] = new_state[zero_row][zero_col+1], new_state[zero_row][zero_col]
        return new_state
    return None

# Hàm cập nhật belief states dựa trên hành động thực tế
def update_belief_states(belief_states, real_action, real_state=None, partial_state=None):
    new_belief_states = []
    for state in belief_states:
        new_state = apply_action(state, real_action)
        if new_state:
            new_belief_states.append(new_state)
    
    # Nếu có real_state và partial_state, thu hẹp belief states bằng cách cập nhật tất cả ô None
    if real_state and partial_state:
        updated = False
        for i in range(3):
            for j in range(3):
                if partial_state[i][j] is None:  # Ô chưa biết
                    real_value = real_state[i][j]  # Giá trị thực
                    new_belief_states = [state for state in new_belief_states if state[i][j] == real_value]
                    partial_state[i][j] = real_value  # Cập nhật partial_state
                    updated = True
        if not updated:  # Nếu không còn ô None nào để cập nhật, đảm bảo belief_states phản ánh real_state
            new_belief_states = [state for state in new_belief_states if state == real_state]
    
    return new_belief_states