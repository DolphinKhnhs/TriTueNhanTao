import tkinter as tk
from tkinter import ttk
from  tkinter import messagebox
import random
import Uninformed_search
import matplotlib.pyplot as plt
import Informed_search
import  Local_search

N = 8
CELL_SIZE = 30

class EightRooks_GUI:
    def __init__(self, window):
        self.window = window
        self.window.title("8 Rooks")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.resizable(True, True)
#Canh lề frame
        for i in range(4):
            self.window.grid_columnconfigure(i, weight=0)
        for i in range(4):
            self.window.grid_rowconfigure(i, weight=0)
########Variable#######
        self.target = self.create_target()
        self.algo_var = tk.StringVar()
        self.algo_var.set("BFS")
        self.algo_chart = tk.StringVar()
        self.algo_chart.set("Uninformed search")
        self.category = tk.StringVar()
        self.category.set(None)
        # Thông tin thuật toán
        self.nodes_expanded = 0
        self.max_frontier_size = 0
        self.solution_path = []
        self.time = 0.0
        self.heuristic_value = 0
        self.cost_value = 0
        self.total_cost_value = 0
        #Kiểm soát bước hiển thị
        self.current_step = 0
        self.total_steps = 0
        self.running = False
        self.run_delay_ms = 400
        #Bảng thông số
        self.stats_table = None

        #dict lưu dữ liệu vẽ biểu đồ
        self.algo_stats = {
            "Uninformed search": {
                "BFS": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                        "time": self.time},
                "DFS": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                        "time": self.time},
                "UCS": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                        "time": self.time},
                "DLS": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                        "time": self.time},
                "IDS": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                        "time": self.time}
            },
            "Informed search": {
                "A*": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                       "time": self.time},
                "Greedy": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                           "time": self.time}
            },
            "Local search": {
                "Hill Climbing": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                                  "time": self.time},
                "Simulated Annealing": {"nodes_expanded": self.nodes_expanded,
                                        "max_frontier_size": self.max_frontier_size, "time": self.time},
                "Genetic Algorithm": {"nodes_expanded": self.nodes_expanded,
                                      "max_frontier_size": self.max_frontier_size, "time": self.time},
                "Beam Search": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                                "time": self.time}
            },
            "CSP Algorithms": {
                "Backtracking": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                                 "time": self.time},
                "Forward Checking": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                                     "time": self.time},
                "AC-3": {"nodes_expanded": self.nodes_expanded, "max_frontier_size": self.max_frontier_size,
                         "time": self.time}
            },
            "Complex Environment": {
                "AND-OR Tree Search": {"nodes_expanded": self.nodes_expanded,
                                       "max_frontier_size": self.max_frontier_size, "time": self.time},
                "Partially Observable Search": {"nodes_expanded": self.nodes_expanded,
                                                "max_frontier_size": self.max_frontier_size, "time": self.time},
                "Belief State Search": {"nodes_expanded": self.nodes_expanded,
                                        "max_frontier_size": self.max_frontier_size, "time": self.time}
            }
        }

########Frame#########
#Bàn cờ và hiển thi các bước đặt quân cờ
        self.frame_target_state = tk.LabelFrame(window, text="Rooks board", font=("Arial", 8, "bold"))
        self.frame_target_state.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_step = tk.LabelFrame(window, text="Step Visualization", font=("Arial", 8, "bold"))
        self.frame_step.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_controls = tk.Frame(window)
        self.frame_controls.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

#Lựa chọn thuật toán và hiển thị kết quả
        self.frame_algo = tk.LabelFrame(window, text="Algorithm Selection", font=("Arial", 8, 'bold'))
        self.frame_algo.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.frame_result = tk.LabelFrame(window, text="Result (Stats)", font=("Arial", 8, 'bold'))
        self.frame_result.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.frame_button = tk.Frame(window)
        self.frame_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
#Frame vẽ biểu đồ thông số
        self.frame_chart = tk.LabelFrame(window, text="Chart", font=('Arial',8,'bold'))
        self.frame_chart.grid(row=0, column=2,rowspan=2, pady=5, padx=5, sticky="nsew")
########Label########
        self.label_target_state = tk.Label(self.frame_target_state, text="Target state", font=("Arial", 10, "bold"))
        self.label_target_state.pack(pady=(5, 0))
        self.label_pos_target_state = tk.Label(self.frame_target_state, text="Position: None", font=("Arial", 10, "bold"),
                                               justify='left', wraplength=200)
        self.label_pos_target_state.pack(pady=(0,5))
        self.label_pos_step = tk.Label(self.frame_step, text="Position: None",
                                       font=("Arial", 10, "bold"),
                                       justify='left', wraplength=200)
        self.label_pos_step.pack(pady=(0, 5))

########Cavas########

        self.canvas_target_state = tk.Canvas(self.frame_target_state, width=N*CELL_SIZE, height=N*CELL_SIZE)
        self.canvas_target_state.pack()

        self.canvas_step = tk.Canvas(self.frame_step, width=N*CELL_SIZE, height=N*CELL_SIZE)
        self.canvas_step.pack()

#######Gọi hàm#######
        self.draw_ui()

#Hàm trung gian gọi các hàm khác
#Vẽ giao diện
    def draw_ui(self):
        self.draw_chessboard(self.canvas_target_state)
        self.draw_rooks(self.canvas_target_state, self.target)
        self.draw_chessboard(self.canvas_step)
        self.create_button()
        self.create_algo_widgets()
        self.update_pos_info()
        self.create_result_frame()
        self.create_select_algo_chart()

    #Tạo nút
    def create_button(self):
        # Nhớ add chức năng button
        actions1 = [
            ("Shuffle", self.shuffle),
            ("Solve", self.solve),
            ("Run", self.run_solution),
            ("Stop", self.stop_solution),
            ("Reset", self.reset),
            ("Show All Steps", self.show_all_steps)
        ]
        for i, (txt,cmd) in enumerate(actions1):
            tk.Button(self.frame_button, text=txt, width=(12 if i == 5 else 8), font=("Arial", 12),
                      command=cmd).grid(row=0, column=i, padx=3, pady=3)

        actions2 = [
            ("<<", self.go_first_step),
            ("<", self.go_previous_step),
            ("Step: 0/0", None),
            (">", self.go_next_step),
            (">>", self.go_last_step)
        ]
        for i, (txt, cmd) in enumerate(actions2):
            if i == 2:
                self.label_step = tk.Label(self.frame_controls, text=txt, width=8, font=("Arial", 12))
                self.label_step.grid(row=0, column=i, padx=3, pady=3)
            else:
                tk.Button(self.frame_controls, text=txt, width=8, font=("Arial", 12), command=cmd).grid(row=0, column=i, padx=3, pady=3)

    def create_algo_widgets(self):
        # --- Hai khung trái/phải ---
        left = tk.Frame(self.frame_algo)
        left.pack(side="left", anchor="n", padx=5, pady=5)
        right = tk.Frame(self.frame_algo)
        right.pack(side="left", anchor="n", padx=5, pady=5)

        # --- Cấu trúc dữ liệu định nghĩa các nhóm thuật toán ---
        algo_groups = {
            left: {
                "Uninformed search": ["BFS", "DFS", "UCS", "DLS", "IDS"],
                "Informed search": ["A*", "Greedy"],
                "Local search": ["Hill Climbing", "Simulated Annealing", "Genetic Algorithm", "Beam Search"]
            },
            right: {
                "CSP Algorithms": ["Backtracking", "Forward Checking", "AC-3"],
                "Complex Environment": ["AND-OR Tree Search", "Partially Observable Search", "Belief State Search"]
            }
        }

        # --- Sinh giao diện tự động ---
        for side_frame, groups in algo_groups.items():
            for group_name, algos in groups.items():
                frame = tk.LabelFrame(side_frame, text=group_name, font=("Arial", 8, "bold"))
                frame.pack(anchor="w", padx=10, pady=5, fill="x")

                for algo in algos:
                    tk.Radiobutton(
                        frame,
                        text=algo,
                        variable=self.algo_var,
                        value=algo
                    ).pack(anchor="w")

    def create_select_algo_chart(self):
        frame_algo_select = tk.Frame(self.frame_chart)
        frame_algo_select.pack(side="left", anchor="n", padx=5, pady=5)
        algo_groups = ["Uninformed search", "Informed search", "Local search", "CSP Algorithms", "Complex Environment"]
        for algo in algo_groups:
            tk.Radiobutton(frame_algo_select,text=algo,variable=self.algo_chart,value=algo).pack(anchor="w")
        button_algo_selected = tk.Button(frame_algo_select, text="View chart", font=('Arial',8,'bold'), command=self.draw_chart)
        button_algo_selected.pack()

    def draw_chart(self):
        selected = self.algo_chart.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select an algorithm group first!")
            return

        algos = self.algo_stats[selected]
        names = list(algos.keys())
        nodes = [algos[a]["nodes_expanded"] for a in names]
        frontier = [algos[a]["max_frontier_size"] for a in names]
        times = [algos[a]["time"] for a in names]

        # --- Vẽ 3 biểu đồ ---
        fig, axes = plt.subplots(3, 1, figsize=(10, 12))
        fig.suptitle(f"Algorithm Performance - {selected}", fontsize=16, fontweight='bold')

        # Full màn hình (Windows)
        manager = plt.get_current_fig_manager()
        try:
            manager.window.state('zoomed')  # Windows
        except Exception:
            pass

        # Biểu đồ 1: Nodes Expanded
        bars1 = axes[0].bar(names, nodes, color='skyblue')
        axes[0].set_title("Nodes Expanded")
        axes[0].set_ylabel("Count")
        axes[0].grid(axis='y', linestyle='--', alpha=0.7)
        for bar in bars1:
            height = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width() / 2, height,
                         f'{height:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        # Biểu đồ 2: Max Frontier Size
        bars2 = axes[1].bar(names, frontier, color='lightgreen')
        axes[1].set_title("Max Frontier Size")
        axes[1].set_ylabel("Size")
        axes[1].grid(axis='y', linestyle='--', alpha=0.7)
        for bar in bars2:
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width() / 2, height,
                         f'{height:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        # Biểu đồ 3: Execution Time
        bars3 = axes[2].bar(names, times, color='salmon')
        axes[2].set_title("Execution Time (seconds)")
        axes[2].set_ylabel("Time (s)")
        axes[2].grid(axis='y', linestyle='--', alpha=0.7)
        for bar in bars3:
            height = bar.get_height()
            axes[2].text(bar.get_x() + bar.get_width() / 2, height,
                         f'{height:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        plt.tight_layout(rect=(0, 0, 1, 0.96))
        plt.show()

    def create_result_frame(self):
        columns = ("Parameter", "Value")
        self.stats_table = ttk.Treeview(self.frame_result, columns=columns, show="headings", height=6)
        self.stats_table.heading("Parameter", text="Parameter")
        self.stats_table.heading("Value", text="Value")
        self.stats_table.column("Parameter", width=150, anchor="w")
        self.stats_table.column("Value", width=120, anchor="center")

        # 6 rows with iids for easy update
        self.stats_table.insert("", "end", iid="nodes", values=("Nodes Expanded", "0"))
        self.stats_table.insert("", "end", iid="frontier", values=("Max Frontier Size", "0"))
        self.stats_table.insert("", "end", iid="time", values=("Time (seconds)", "0.0000"))
        self.stats_table.insert("", "end", iid="heuristic", values=("Heuristic h(x)", "0"))
        self.stats_table.insert("", "end", iid="cost", values=("Cost g(x)", "0"))
        self.stats_table.insert("", "end", iid="total_cost", values=("Total Cost f(x)", "0"))

        scrollbar = tk.Scrollbar(self.frame_result, orient="vertical", command=self.stats_table.yview)
        self.stats_table.configure(yscrollcommand=scrollbar.set)

        # grid layout inside table_frame
        self.frame_result.grid_rowconfigure(0, weight=1)
        self.frame_result.grid_columnconfigure(0, weight=1)
        self.stats_table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")


#Các hàm chức năng
#Vẽ bàn cờ
    def draw_chessboard(self, canvas):
        canvas.delete("board")
        for i in range(N):
            for j in range(N):
                color = "#cccbc8" if (i+j)%2==0 else "#a8a7a5"
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags="board")
#vẽ quân xe
    def draw_rooks(self, canvas, board):
        canvas.delete("rook")
        for i in range(N):
            for j in range(N):
                if board[i][j] == 1:
                    x = j * CELL_SIZE + CELL_SIZE // 2
                    y = i * CELL_SIZE + CELL_SIZE // 2
                    canvas.create_text(x, y, text="♖", font=("Arial", 20, "bold"), fill="red", tags="rook")

#Tạo trạng thái mục tiêu
    def create_target(self):
        matrix = [[0] * N for _ in range(N)]
        cols = list(range(N))
        random.shuffle(cols)
        for i, c in enumerate(cols):
            matrix[i][c] = 1
        return matrix

#Trộn vị trí quân xe
    def shuffle(self):
        self.target=self.create_target()
        self.draw_rooks(self.canvas_target_state, self.target)
        self.update_pos_info()

#Giải thuật toán
    def solve(self):
        selected = self.algo_var.get()
        if selected == "BFS":
            self.result = Uninformed_search.bfs_rooks(self.target)
            self.category.set("Uninformed search")
        if selected == "DFS":
            self.result = Uninformed_search.dfs_rooks(self.target)
            self.category.set("Uninformed search")
        if selected == "UCS":
            self.result = Uninformed_search.ucs_rooks(self.target)
            self.category.set("Uninformed search")
        if selected == "DLS":
            self.result = Uninformed_search.dls_rooks(self.target)
            self.category.set("Uninformed search")
        if selected == "IDS":
            self.result = Uninformed_search.ids_rooks(self.target)
            self.category.set("Uninformed search")
        if selected == "A*":
            self.result = Informed_search.a_star_rooks(self.target)
            self.category.set("Informed search")
        if selected == "Greedy":
            self.result = Informed_search.greedy_rooks(self.target)
            self.category.set("Informed search")
        if selected == "Hill Climbing":
            local_search = Local_search.LocalSearch(self.target)
            self.result = local_search.hill_climbing_rooks()
            self.category.set("Local search")
        if selected == "Simulated Annealing":
            local_search = Local_search.LocalSearch(self.target)
            self.result = local_search.simulated_annealing_rooks()
            self.category.set("Local search")
        if selected == "Genetic Algorithm":
            local_search = Local_search.LocalSearch(self.target)
            self.result = local_search.genetic_algorithm_rooks()
            self.category.set("Local search")
        if selected == "Beam Search":
            local_search = Local_search.LocalSearch(self.target)
            self.result = local_search.beam_search_rooks()
            self.category.set("Local search")


        self.update_stats(self.result)
        self.update_algo_stats_from_result(self.category.get(), selected, self.result)

    def update_stats(self, result):
        self.solution_path = result.get("path", [])
        self.nodes_expanded = result.get("nodes_expanded", 0)
        self.max_frontier_size = result.get("max_frontier_size", 0)
        self.time = result.get("time", 0.0)
        self.heuristic_value = result.get("heuristic", 0)
        self.cost_value = result.get("cost", 0)
        self.total_cost_value = result.get("total_cost", 0)
        self.total_steps = len(self.solution_path) - 1
        self.current_step = 0

        # Cập nhật bảng kết quả
        self.update_result_stats({
            "nodes_expanded": self.nodes_expanded,
            "max_frontier_size": self.max_frontier_size,
            "time": self.time,
            "heuristic": self.heuristic_value,
            "cost": self.cost_value,
            "total_cost": self.total_cost_value
        })

    def update_algo_stats_from_result(self, category, algorithm, result):
        if category not in self.algo_stats:
            print(f"[Warning] Category '{category}' not found in algo_stats.")
            return
        if algorithm not in self.algo_stats[category]:
            print(f"[Warning] Algorithm '{algorithm}' not found in category '{category}'.")
            return
        self.algo_stats[category][algorithm]["nodes_expanded"] = result.get("nodes_expanded", 0)
        self.algo_stats[category][algorithm]["max_frontier_size"] = result.get("max_frontier_size", 0)
        self.algo_stats[category][algorithm]["time"] = result.get("time", 0.0)

        print(f"[INFO] Updated stats for {algorithm} in {category}.")

    #Chạy kết quả hiển thị lên frame_step
    def run_solution(self):
        if not self.solution_path:
            messagebox.showwarning("No solution", "Please click 'Solve' before running.")
            return
        if self.running:
            return
        self.running = True
        self.run_()

    def run_(self):
        if not self.running:
            return
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.draw_step()
            self.window.after(self.run_delay_ms, self.run_)
        else:
            self.running = False
            self.draw_step()

    #Dừng in các thông tin trên frame_step
    def stop_solution(self):
        self.running = False
#Reset lại canvas_step
    def reset(self):
        # Reset logic variables
        self.solution_path = []
        self.current_step = 0
        self.total_steps = 0
        self.running = False

        # Xóa nội dung canvas và vẽ lại bàn cờ gốc
        self.canvas_target_state.delete("all")
        self.canvas_step.delete("all")
        self.draw_chessboard(self.canvas_target_state)
        self.draw_chessboard(self.canvas_step)

        # Vẽ lại quân cờ ban đầu
        self.draw_rooks(self.canvas_target_state, self.target)

        # Cập nhật label bước
        self.label_pos_step.config(text="Step: 0/0")
        self.label_step.config(text="Step: 0/0")

        # Reset bảng thống kê
        self.update_result_stats({
            "nodes_expanded": 0,
            "max_frontier_size": 0,
            "time": 0.0,
            "heuristic": 0,
            "cost": 0,
            "total_cost": 0
        })

        # Cập nhật thông tin khác nếu có
        self.update_pos_info()

    #Hiển thị toàn bộ bước đi
    def show_all_steps(self):
        pass

#điều khiển hiển thị thông tin step
    def go_first_step(self):
        if not self.solution_path:
            return
        self.current_step = 0
        self.draw_step()
    def go_previous_step(self):
        if not self.solution_path:
            return
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_step()
    def go_next_step(self):
        if not self.solution_path:
            return
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.draw_step()
    def go_last_step(self):
        if not self.solution_path:
            return
        self.current_step = len(self.solution_path) - 1
        self.draw_step()
#cập nhật thông tin vị trí
    def update_pos_info(self):
        self.label_pos_target_state.config(text=self.get_positions_text(self.target))
        # Current Step
        if self.solution_path and self.current_step < len(self.solution_path):
            current_board = self.solution_path[self.current_step]
            self.label_pos_step.config(text=self.get_positions_text(current_board))
        else:
            self.label_pos_step.config(text="Positions: None")
#cập nhật giá trị bước
    def update_step_label(self):
        self.label_step.config(text=f"Step: {self.current_step}/{self.total_steps}")
        self.label_step.config(text=f"Step: {self.current_step}/{self.total_steps}")
#vẽ bước sau khi chọn
    def draw_step(self):
        if not self.solution_path:
            return
        # clamp
        idx = max(0, min(self.current_step, len(self.solution_path) - 1))
        self.draw_rooks(self.canvas_step, self.solution_path[idx])
        self.update_step_label()
        self.update_pos_info()

#chuyển vị trí quân xe sang dạng text
    def get_positions_text(self, board):
        positions = []
        for i in range(N):
            for j in range(N):
                if board[i][j] == 1:
                    row = i + 1
                    col = chr(65 + j)  # A, B, C, ..., H
                    positions.append(f"{col}{row}")

        if positions:
            return "Positions: " + ", ".join(positions)
        else:
            return "Positions: None"
#Cập nhật thông tin stats
    def update_result_stats(self, stats_data):
        self.stats_table.item("nodes", values=("Nodes Expanded", stats_data["nodes_expanded"]))
        self.stats_table.item("frontier", values=("Max Frontier Size", stats_data["max_frontier_size"]))
        self.stats_table.item("time", values=("Time (seconds)", f"{stats_data['time']:.4f}"))
        self.stats_table.item("heuristic", values=("Heuristic h(x)", stats_data["heuristic"]))
        self.stats_table.item("cost", values=("Cost g(x)", stats_data["cost"]))
        self.stats_table.item("total_cost", values=("Total Cost f(x)", stats_data["total_cost"]))

if __name__ == "__main__":
    window = tk.Tk()
    app = EightRooks_GUI(window)
    window.mainloop()