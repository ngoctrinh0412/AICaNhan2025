import pygame
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import time
from constants import WIDTH, HEIGHT, COLORS
from utils import draw_board, update_canvas, display_state
from algorithms import bfs, dfs, ids, ucs, greedy, astar, ida_star, simple_hill_climbing, steepest_ascent_hill_climbing, stochastic_hill_climbing, simulated_annealing, beam_search, genetic_algorithm, and_or_search, belief_state_search, searching_with_partial_observation, backtracking_search, backtracking_with_forward_checking,maintaining_arc_consistency, q_learning

# Tkinter GUI
def start_gui():
    root = tk.Tk()
    root.title("8-Puzzle Solver")
    root.geometry("1400x900")  # Tăng kích thước cửa sổ để giao diện thoáng hơn
    root.configure(bg=COLORS["SECONDARY"]["hex"])
    
    # Header với gradient
    header_frame = tk.Frame(root, bg=COLORS["PRIMARY"]["hex"], height=60)
    header_frame.pack(fill=tk.X)
    header_label = tk.Label(header_frame, text="8-PUZZLE SOLVER", font=("Helvetica", 28, "bold"),
                            bg=COLORS["PRIMARY"]["hex"], fg=COLORS["WHITE"]["hex"], pady=10)
    header_label.pack()

    main_frame = tk.Frame(root, bg=COLORS["SECONDARY"]["hex"])
    main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Frame bên trái (chọn thuật toán)
    frame_left = tk.Frame(main_frame, bg=COLORS["WHITE"]["hex"], relief="flat",
                          highlightthickness=2, highlightbackground=COLORS["SHADOW"]["hex"])
    frame_left.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

    # Khai báo các biến trước khi định nghĩa hàm con
    start_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    surface = pygame.Surface((WIDTH, HEIGHT))
    path = []  # Danh sách các bước
    current_page = tk.IntVar(value=1)  # Trang hiện tại
    steps_per_page = 6  # Số bước hiển thị trên mỗi trang (2x3 grid)

    # Menu thả xuống để chọn thuật toán
    tk.Label(frame_left, text="Chọn thuật toán", font=("Helvetica", 16, "bold"),
             bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"]).pack(pady=(20, 10))
    algorithm_var = tk.StringVar(value="BFS")
    algorithms = ["BFS", "DFS", "IDS", "UCS", "Greedy", "A*", "IDA*", "Simple Hill Climbing",
                  "Steepest-Ascent Hill Climbing", "Stochastic Hill Climbing", "Simulated Annealing",
                  "Beam Search", "Genetic Algorithm", "AND-OR Search", "Belief State Search" ,
                  "Searching with Partial Observation",
                  "Backtracking Search", "Backtracking with Forward Checking",
                  "Maintaining Arc-Consistency", "Q-Learning"]
    
    # Tùy chỉnh OptionMenu
    style = ttk.Style()
    style.configure("Custom.TMenubutton", font=("Helvetica", 12), background=COLORS["PRIMARY"]["hex"],
                    foreground=COLORS["WHITE"]["hex"])
    style.map("Custom.TMenubutton", background=[("active", COLORS["ACCENT"]["hex"])])
    algorithm_menu = ttk.OptionMenu(frame_left, algorithm_var, "BFS", *algorithms, style="Custom.TMenubutton")
    algorithm_menu.pack(pady=5, padx=20, fill=tk.X)

    # Frame giữa (trạng thái đầu và đích)
    frame_middle = tk.Frame(main_frame, bg=COLORS["WHITE"]["hex"], relief="flat",
                            highlightthickness=1, highlightbackground=COLORS["SHADOW"]["hex"])
    frame_middle.pack(side=tk.LEFT, padx=10, pady=10)

    tk.Label(frame_middle, text="Trạng thái đầu", font=("Helvetica", 16, "bold"),
             bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"]).pack(pady=(10, 5))
    start_frame = tk.Frame(frame_middle, bg=COLORS["WHITE"]["hex"])
    start_frame.pack(pady=10)
    display_state(start_frame, start_state)

    tk.Label(frame_middle, text="Trạng thái đích", font=("Helvetica", 16, "bold"),
             bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"]).pack(pady=(20, 5))
    goal_frame = tk.Frame(frame_middle, bg=COLORS["WHITE"]["hex"])
    goal_frame.pack(pady=10)
    display_state(goal_frame, goal_state)

    # Frame bên phải (tiến trình giải)
    frame_right = tk.Frame(main_frame, bg=COLORS["WHITE"]["hex"], relief="flat",
                           highlightthickness=2, highlightbackground=COLORS["SHADOW"]["hex"])
    frame_right.pack(side=tk.LEFT, padx=10, pady=10)
    tk.Label(frame_right, text="Tiến trình giải", font=("Helvetica", 16, "bold"),
             bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"]).pack(pady=(10, 5))

    canvas = tk.Canvas(frame_right, width=WIDTH, height=HEIGHT, bg=COLORS["WHITE"]["hex"], highlightthickness=0)
    canvas.pack(pady=10)

    draw_board(surface, start_state)
    update_canvas(canvas, surface)

    info_label = tk.Label(frame_right, text="Số bước: 0 | Thời gian: 0s", font=("Helvetica", 12),
                          bg=COLORS["WHITE"]["hex"], fg=COLORS["DARK_GRAY"]["hex"])
    info_label.pack(pady=10)

    # Frame hiển thị các bước (dạng lưới 2x4)
    frame_steps = tk.Frame(main_frame, bg=COLORS["WHITE"]["hex"], relief="flat",
                           highlightthickness=2, highlightbackground=COLORS["SHADOW"]["hex"])
    frame_steps.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
    tk.Label(frame_steps, text="Các bước", font=("Helvetica", 16, "bold"),
             bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"]).pack(pady=(10, 5))

    # Frame chứa các trạng thái (dạng lưới 2x4)
    steps_container = tk.Frame(frame_steps, bg=COLORS["WHITE"]["hex"])
    steps_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Frame phân trang
    pagination_frame = tk.Frame(frame_steps, bg=COLORS["WHITE"]["hex"])
    pagination_frame.pack(fill=tk.X, pady=5)

    page_label = tk.Label(pagination_frame, text="Trang 1", font=("Helvetica", 12),
                          bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"])
    page_label.pack(side=tk.LEFT, padx=10)

    def on_enter(e):
        e.widget['background'] = COLORS["ACCENT"]["hex"]

    def on_leave(e):
        e.widget['background'] = COLORS["PRIMARY"]["hex"]

    prev_button = tk.Button(pagination_frame, text="Trang trước", font=("Helvetica", 10, "bold"),
                            bg=COLORS["PRIMARY"]["hex"], fg=COLORS["WHITE"]["hex"],
                            relief="flat", padx=10, pady=5, borderwidth=0, highlightthickness=2,
                            highlightbackground=COLORS["SHADOW"]["hex"], state=tk.DISABLED)
    prev_button.pack(side=tk.LEFT, padx=5)
    prev_button.bind("<Enter>", on_enter)
    prev_button.bind("<Leave>", on_leave)

    next_button = tk.Button(pagination_frame, text="Trang sau", font=("Helvetica", 10, "bold"),
                            bg=COLORS["PRIMARY"]["hex"], fg=COLORS["WHITE"]["hex"],
                            relief="flat", padx=10, pady=5, borderwidth=0, highlightthickness=2,
                            highlightbackground=COLORS["SHADOW"]["hex"], state=tk.DISABLED)
    next_button.pack(side=tk.LEFT, padx=5)
    next_button.bind("<Enter>", on_enter)
    next_button.bind("<Leave>", on_leave)

    # Hàm hiển thị trạng thái dưới dạng lưới 3x3 với giao diện đẹp
    def display_state_custom(parent, state, step_num):
        step_frame = tk.Frame(parent, bg=COLORS["WHITE"]["hex"], bd=2, relief="groove")

        # Nhãn "Bước X"
        tk.Label(step_frame, text=f"Bước {step_num}", font=("Helvetica", 10, "bold"),
                 bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"]).grid(row=0, column=0, columnspan=3, pady=(5, 2))

        # Lưới 3x3
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                bg_color = COLORS["GRAY"]["hex"] if value == 0 else "#4A90E2"  # Màu xanh dịu hơn
                fg_color = COLORS["WHITE"]["hex"]
                btn = tk.Button(step_frame, text=str(value) if value != 0 else "",
                                font=("Helvetica", 16, "bold"),  # Font lớn hơn
                                width=2, height=1,  # Điều chỉnh để gần vuông hơn
                                bg=bg_color, fg=fg_color, relief="raised",
                                bd=3, highlightbackground=COLORS["SHADOW"]["hex"])
                btn.grid(row=i+1, column=j, padx=3, pady=3, ipadx=10, ipady=10, sticky="nsew")  # Áp dụng ipadx và ipady trong grid
                
        
        # Đảm bảo các ô trong step_frame căn chỉnh đều
        for i in range(4):  # 4 hàng: 1 cho nhãn, 3 cho lưới
            step_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):  # 3 cột
            step_frame.grid_columnconfigure(j, weight=1)

        return step_frame

    # Hàm hiển thị các bước trên trang hiện tại
    def display_steps():
        # Xóa các widget cũ trong steps_container
        for widget in steps_container.winfo_children():
            widget.destroy()

        # Tính toán các bước cần hiển thị trên trang hiện tại
        start_idx = (current_page.get() - 1) * steps_per_page
        end_idx = min(start_idx + steps_per_page, len(path))
        steps_to_display = path[start_idx:end_idx]

        # Hiển thị các bước dưới dạng lưới 2x4
        for idx, step in enumerate(steps_to_display):
            row = idx // 3  # 2 hàng
            col = idx % 3
            step_num = start_idx + idx + 1
            step_frame = display_state_custom(steps_container, step, step_num)
            steps_container.grid_rowconfigure(row, weight=1)
            steps_container.grid_columnconfigure(col, weight=1)
            step_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Cập nhật nút phân trang
        total_pages = (len(path) + steps_per_page - 1) // steps_per_page
        page_label.config(text=f"Trang {current_page.get()}/{total_pages}")
        prev_button.config(state=tk.NORMAL if current_page.get() > 1 else tk.DISABLED)
        next_button.config(state=tk.NORMAL if current_page.get() < total_pages else tk.DISABLED)

    # Hàm chuyển trang
    def prev_page():
        if current_page.get() > 1:
            current_page.set(current_page.get() - 1)
            display_steps()

    def next_page():
        total_pages = (len(path) + steps_per_page - 1) // steps_per_page
        if current_page.get() < total_pages:
            current_page.set(current_page.get() + 1)
            display_steps()

    prev_button.config(command=prev_page)
    next_button.config(command=next_page)

    # Các nút điều khiển
    button_frame = tk.Frame(frame_left, bg=COLORS["WHITE"]["hex"])
    button_frame.pack(pady=30)

    def on_enter(e):
        e.widget['background'] = COLORS["ACCENT"]["hex"]

    def on_leave(e):
        e.widget['background'] = COLORS["PRIMARY"]["hex"]

    btn_input = tk.Button(button_frame, text="Nhập trạng thái", command=lambda: input_start_state(),
                          font=("Helvetica", 12, "bold"), bg=COLORS["PRIMARY"]["hex"], fg=COLORS["WHITE"]["hex"],
                          relief="flat", padx=15, pady=8, borderwidth=0, highlightthickness=2,
                          highlightbackground=COLORS["SHADOW"]["hex"])
    btn_input.pack(pady=5, fill=tk.X, padx=20)
    btn_input.bind("<Enter>", on_enter)
    btn_input.bind("<Leave>", on_leave)

    btn_solve = tk.Button(button_frame, text="Giải", command=lambda: solve_puzzle(),
                          font=("Helvetica", 12, "bold"), bg=COLORS["PRIMARY"]["hex"], fg=COLORS["WHITE"]["hex"],
                          relief="flat", padx=15, pady=8, borderwidth=0, highlightthickness=2,
                          highlightbackground=COLORS["SHADOW"]["hex"])
    btn_solve.pack(pady=5, fill=tk.X, padx=20)
    btn_solve.bind("<Enter>", on_enter)
    btn_solve.bind("<Leave>", on_leave)

    btn_reset = tk.Button(button_frame, text="Reset", command=lambda: reset_state(),
                          font=("Helvetica", 12, "bold"), bg=COLORS["PRIMARY"]["hex"], fg=COLORS["WHITE"]["hex"],
                          relief="flat", padx=15, pady=8, borderwidth=0, highlightthickness=2,
                          highlightbackground=COLORS["SHADOW"]["hex"])
    btn_reset.pack(pady=5, fill=tk.X, padx=20)
    btn_reset.bind("<Enter>", on_enter)
    btn_reset.bind("<Leave>", on_leave)

    def input_start_state():
        nonlocal start_state
        input_str = simpledialog.askstring("Nhập trạng thái đầu", "Nhập 9 số (0-8, cách nhau bằng dấu cách):")
        if input_str:
            try:
                nums = list(map(int, input_str.split()))
                if len(nums) == 9 and sorted(nums) == list(range(9)):
                    if 0 not in nums:  # Kiểm tra xem có ô trống không
                        messagebox.showerror("Lỗi", "Trạng thái phải có một ô trống (giá trị 0)!")
                        return
                    start_state = [nums[i:i+3] for i in range(0, 9, 3)]
                    display_state(start_frame, start_state)
                    draw_board(surface, start_state)
                    update_canvas(canvas, surface)
                else:
                    messagebox.showerror("Lỗi", "Vui lòng nhập đúng 9 số từ 0-8!")
            except:
                messagebox.showerror("Lỗi", "Định dạng không hợp lệ!")

    def reset_state():
        nonlocal start_state, path
        start_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
        path = []
        display_state(start_frame, start_state)
        draw_board(surface

, start_state)
        update_canvas(canvas, surface)
        current_page.set(1)
        display_steps()
        info_label.config(text="Số bước: 0 | Thời gian: 0s")

    def solve_puzzle():
        nonlocal path
        algorithms_dict = {
            "BFS": bfs,
            "DFS": dfs,
            "IDS": ids,
            "UCS": ucs,
            "Greedy": greedy,
            "A*": astar,
            "IDA*": ida_star,
            "Simple Hill Climbing": simple_hill_climbing,
            "Steepest-Ascent Hill Climbing": steepest_ascent_hill_climbing,
            "Stochastic Hill Climbing": stochastic_hill_climbing,
            "Simulated Annealing": simulated_annealing,
            "Beam Search": beam_search,
            "Genetic Algorithm": genetic_algorithm,
            "AND-OR Search": and_or_search,
            "Belief State Search": belief_state_search,
            "Searching with Partial Observation": searching_with_partial_observation,
            "Backtracking Search": backtracking_search,
            "Backtracking with Forward Checking": backtracking_with_forward_checking,
    "Maintaining Arc-Consistency": maintaining_arc_consistency,
    "Q-Learning": q_learning  
        }
        algo = algorithm_var.get()
        start_time = time.time()
        path = algorithms_dict[algo](start_state, goal_state)
        end_time = time.time()
        if path is None or not path:
            messagebox.showinfo("Kết quả", f"{algo}: Không tìm thấy lời giải!")
            path = []
            return
        info_label.config(text=f"Số bước: {len(path)} | Thời gian: {end_time - start_time:.4f}s")
        current_page.set(1)
        display_steps()  # Chỉ gọi display_steps() một lần sau khi giải xong

        def animate(index=0):
            if index < len(path):
                draw_board(surface, path[index])
                update_canvas(canvas, surface)
                canvas.after(300, animate, index + 1)

        animate()

    root.mainloop()

if __name__ == "__main__":
    start_gui()