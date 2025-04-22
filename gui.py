import pygame
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import time
from constants import WIDTH, HEIGHT, COLORS
from utils import draw_board, update_canvas, display_state
from algorithms import bfs, dfs, ids, ucs, greedy, astar, ida_star, simple_hill_climbing, steepest_ascent_hill_climbing, stochastic_hill_climbing, simulated_annealing, beam_search, genetic_algorithm, and_or_search, belief_state_search

# Tkinter GUI
def start_gui():
    root = tk.Tk()
    root.title("8-Puzzle Solver")
    root.geometry("1200x900")
    root.configure(bg=COLORS["SECONDARY"]["hex"])
    
    # Header với gradient
    header_frame = tk.Frame(root, bg=COLORS["PRIMARY"]["hex"], height=60)
    header_frame.pack(fill=tk.X)
    header_label = tk.Label(header_frame, text="8-PUZZLE SOLVER", font=("Helvetica", 28, "bold"),
                            bg=COLORS["PRIMARY"]["hex"], fg=COLORS["WHITE"]["hex"], pady=10)
    header_label.pack()

    main_frame = tk.Frame(root, bg=COLORS["SECONDARY"]["hex"])
    main_frame.pack(pady=30, padx=20, fill=tk.BOTH, expand=True)

    # Frame bên trái (chọn thuật toán)
    frame_left = tk.Frame(main_frame, bg=COLORS["WHITE"]["hex"], relief="flat",
                          highlightthickness=2, highlightbackground=COLORS["SHADOW"]["hex"])
    frame_left.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

    # Khai báo các biến trước khi định nghĩa hàm con
    start_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    surface = pygame.Surface((WIDTH, HEIGHT))

    # Menu thả xuống để chọn thuật toán
    tk.Label(frame_left, text="Chọn thuật toán", font=("Helvetica", 16, "bold"),
             bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"]).pack(pady=(20, 10))
    algorithm_var = tk.StringVar(value="BFS")
    algorithms = ["BFS", "DFS", "IDS", "UCS", "Greedy", "A*", "IDA*", "Simple Hill Climbing",
                  "Steepest-Ascent Hill Climbing", "Stochastic Hill Climbing", "Simulated Annealing",
                  "Beam Search", "Genetic Algorithm", "AND-OR Search", "Belief State Search"]
    
    # Tùy chỉnh OptionMenu
    style = ttk.Style()
    style.configure("Custom.TMenubutton", font=("Helvetica", 12), background=COLORS["PRIMARY"]["hex"],
                    foreground=COLORS["WHITE"]["hex"])
    style.map("Custom.TMenubutton", background=[("active", COLORS["ACCENT"]["hex"])])
    algorithm_menu = ttk.OptionMenu(frame_left, algorithm_var, "BFS", *algorithms, style="Custom.TMenubutton")
    algorithm_menu.pack(pady=5, padx=20, fill=tk.X)

    # Menu thả xuống cho Belief State
    tk.Label(frame_left, text="Tùy chọn Belief State", font=("Helvetica", 14, "bold"),
             bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"]).pack(pady=(20, 10))
    belief_mode_var = tk.StringVar(value="Có None")
    belief_modes = ["Có None", "Không None"]
    belief_mode_menu = ttk.OptionMenu(frame_left, belief_mode_var, "Có None", *belief_modes, style="Custom.TMenubutton")
    belief_mode_menu.pack(pady=5, padx=20, fill=tk.X)

    # Frame giữa (trạng thái đầu và đích)
    frame_middle = tk.Frame(main_frame, bg=COLORS["WHITE"]["hex"], relief="flat",
                            highlightthickness=1, highlightbackground=COLORS["SHADOW"]["hex"])
    frame_middle.pack(side=tk.LEFT, padx=20, pady=20)

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
    frame_right.pack(side=tk.LEFT, padx=20, pady=20)
    tk.Label(frame_right, text="Tiến trình giải", font=("Helvetica", 16, "bold"),
             bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"]).pack(pady=(10, 5))

    canvas = tk.Canvas(frame_right, width=WIDTH, height=HEIGHT, bg=COLORS["WHITE"]["hex"], highlightthickness=0)
    canvas.pack(pady=10)

    draw_board(surface, start_state)
    update_canvas(canvas, surface)

    info_label = tk.Label(frame_right, text="Số bước: 0 | Thời gian: 0s", font=("Helvetica", 12),
                          bg=COLORS["WHITE"]["hex"], fg=COLORS["DARK_GRAY"]["hex"])
    info_label.pack(pady=10)

    # Frame hiển thị các bước
    frame_steps = tk.Frame(main_frame, bg=COLORS["WHITE"]["hex"], relief="flat",
                           highlightthickness=2, highlightbackground=COLORS["SHADOW"]["hex"])
    frame_steps.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)
    tk.Label(frame_steps, text="Các bước", font=("Helvetica", 16, "bold"),
             bg=COLORS["WHITE"]["hex"], fg=COLORS["BLACK"]["hex"]).pack(pady=(10, 5))

    # Tùy chỉnh Treeview
    style.configure("Custom.Treeview", font=("Helvetica", 11), rowheight=30)
    style.configure("Custom.Treeview.Heading", font=("Helvetica", 12, "bold"))
    step_list = ttk.Treeview(frame_steps, columns=("Step", "State"), show="headings", height=15, style="Custom.Treeview")
    step_list.heading("Step", text="Bước")
    step_list.heading("State", text="Trạng thái")
    step_list.column("Step", width=80, anchor="center")
    step_list.column("State", width=250)
    step_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(frame_steps, orient=tk.VERTICAL, command=step_list.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    step_list.configure(yscrollcommand=scrollbar.set)

    # Tùy chỉnh màu xen kẽ cho Treeview
    step_list.tag_configure("oddrow", background=COLORS["GRAY"]["hex"])
    step_list.tag_configure("evenrow", background=COLORS["WHITE"]["hex"])

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
                    start_state = [nums[i:i+3] for i in range(0, 9, 3)]
                    display_state(start_frame, start_state)
                    draw_board(surface, start_state)
                    update_canvas(canvas, surface)
                else:
                    messagebox.showerror("Lỗi", "Vui lòng nhập đúng 9 số từ 0-8!")
            except:
                messagebox.showerror("Lỗi", "Định dạng không hợp lệ!")

    def reset_state():
        nonlocal start_state
        start_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
        display_state(start_frame, start_state)
        draw_board(surface, start_state)
        update_canvas(canvas, surface)
        step_list.delete(*step_list.get_children())
        info_label.config(text="Số bước: 0 | Thời gian: 0s")

    def solve_puzzle():
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
            "Belief State Search": lambda start, goal: belief_state_search(start, goal, use_partial=(belief_mode_var.get() == "Có None"))
        }
        algo = algorithm_var.get()
        start_time = time.time()
        path = algorithms_dict[algo](start_state, goal_state)
        end_time = time.time()
        if path is None or not path:
            messagebox.showinfo("Kết quả", f"{algo}: Không tìm thấy lời giải!")
            return
        info_label.config(text=f"Số bước: {len(path)} | Thời gian: {end_time - start_time:.4f}s")
        step_list.delete(*step_list.get_children())
        for i, step in enumerate(path):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            step_list.insert("", "end", values=(i + 1, f"{step[0]} {step[1]} {step[2]}"), tags=(tag,))

        def animate(index=0):
            if index < len(path):
                draw_board(surface, path[index])
                update_canvas(canvas, surface)
                step_list.see(step_list.get_children()[index])
                canvas.after(300, animate, index + 1)

        animate()

    root.mainloop()

if __name__ == "__main__":
    start_gui()