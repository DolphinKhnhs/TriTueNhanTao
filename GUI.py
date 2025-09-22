import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Create_Target import Create
from BFS import run_bfs
from Hill_Climbing import run_hill_climbing
from Simulated_Annealing import run_simulated_annealing
from Local_Beam_Search import run_local_beam_search
from Genetic_Algorithm import  run_genetic_algorithm


N = 8
TILE_SIZE = 50
win_w = 1200
win_h = 550
ALGO = [
    "BFS",
    "DFS",
    "DLS",
    "IDS",
    "UCS",
    "A*",
    "Hill Climbing",
    "Genetic Algorithm",
    "Simulated annealing",
    "Local Beam Search"
]

def drawtable(canvas, rooks):
    canvas.delete("all")
    for i in range(N):
        for j in range(N):
            x1 = 25 + j * TILE_SIZE
            y1 = 25 + i * TILE_SIZE
            x2 = x1 + TILE_SIZE
            y2 = y1 + TILE_SIZE
            color = "#e6e1a5" if (i + j) % 2 == 0 else "#a86b21"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

            if rooks[i][j] == 1:
                canvas.create_text(
                    x1 + TILE_SIZE / 2,
                    y1 + TILE_SIZE / 2,
                    text="♖", fill="red", font=('Lato', 24, 'bold')
                )
def target():
    c = Create()
    return c.target()


class GUI:
    def __init__(self):
        self.selected_value = None
        self.combo = None
        self.WINDOW = tk.Tk()
        self.WINDOW.title("8 ROOKS")
        self.WINDOW.protocol("WM_DELETE_WINDOW", self.on_close)
        self.WINDOW.config(bg="#a19687")
        self.Target = target()
        self.canvasL = self.canvas_left()
        self.canvasR = self.canvas_right()
        # Gọi các hàm con
        self.center_window()
        self.create_label("8 ROOKS", 20, 275/2 - TILE_SIZE, 50)
        self.create_label("Thuật Toán:", 12, 10, TILE_SIZE*2)
        self.create_combobox(ALGO)
        self.create_button("START", TILE_SIZE*2+10, TILE_SIZE*3, self.click)

        #Hàm bên ngoài
        drawtable(self.canvasL, [[0] * N for _ in range(N)])
        drawtable(self.canvasR, self.Target)

#Căn cửa sổ ở giữa
    def center_window(self):
        screen_w = self.WINDOW.winfo_screenwidth()
        screen_h = self.WINDOW.winfo_screenheight()
        x = (screen_w // 2) - (win_w // 2)
        y = (screen_h // 2) - (win_h // 2)
        self.WINDOW.geometry(f"{win_w}x{win_h}+{x}+{y}")

# Tạo label
    def create_label(self, text, size,x,y):
        label = tk.Label(self.WINDOW,text=text,font=("Press Start 2P", size, "bold"),fg="black",bg="#a19687")
        label.place(x=x, y=y)

#Tắt cửa sổ không bị lỗi
    def on_close(self):
        if messagebox.askokcancel("Thoát", "Bạn có muốn thoát không?"):
            self.WINDOW.destroy()

#Canvas trái và canvas phải
    def canvas_left(self):
        canvas = tk.Canvas(self.WINDOW, width=N * TILE_SIZE + 50, height=N * TILE_SIZE + 50, highlightthickness=0)
        canvas.config(bg="#a19687")
        canvas.place(x=275, y=50)
        return canvas

    def canvas_right(self):
        canvas = tk.Canvas(self.WINDOW, width=N * TILE_SIZE + 50, height=N * TILE_SIZE + 50, highlightthickness=0)
        canvas.place(x=725, y=50)
        canvas.config(bg="#a19687")
        return canvas

#Tạo nút bấm
    def create_button(self, text, x, y, command):
        btn = tk.Button(self.WINDOW, text=text, command=command, font=("Press Start 2P", 12, "bold"))
        btn.place(x=x, y=y)
        return btn

#Tạo combobox
    def create_combobox(self, values):
        self.combo = ttk.Combobox(self.WINDOW, values=values, state="readonly")
        self.combo.current(0)
        self.combo.place(x=TILE_SIZE*2 + 15, y=TILE_SIZE*2 + 4)
        self.combo.bind("<<ComboboxSelected>>", self.on_select)

# Xử lý giá trị được chọn
    def on_select(self, event):
        selected = self.combo.get()
        self.selected_value = selected

#Xử lý sự kiện nhấn nút
    def click(self):
        selected = self.combo.get()
        if selected == "BFS":
            initial = [[0] * N for _ in range(N)]
            answer = run_bfs(initial, self.Target)
            if answer:
                print("Đã tìm thấy nghiệm! Số bước:", len(answer))
                for state in answer:
                    drawtable(self.canvasL, state)
                    self.WINDOW.update()
                    self.WINDOW.after(500)
            else:
                print("Không tìm thấy nghiệm.")
        # elif selected == "DFS":
        #     print("Đang chạy thuật toán DFS...")
        # elif selected == "DLS":
        #     print("Đang chạy thuật toán DLS...")
        # elif selected == "IDS":
        #     print("Đang chạy thuật toán IDS...")
        # elif selected == "UCS":
        #     print("Đang chạy thuật toán UCS...")
        # elif selected == "A*":
        #     print("Đang chạy thuật toán A*...")

        elif selected == "Hill Climbing":
            answer = run_hill_climbing(self.Target)
            if answer and answer[-1] == self.Target:
                print("✅ Đã tìm thấy nghiệm! Số bước:", len(answer) - 1)
            else:
                print("⚠️ Bị kẹt ở local optimum sau", len(answer) - 1, "bước")
            for state in answer:
                drawtable(self.canvasL, state)
                self.WINDOW.update()
                self.WINDOW.after(1000)
            else:
                print("Không tìm thấy nghiệm.")

        elif selected == "Simulated annealing":
            answer = run_simulated_annealing(self.Target)
            if answer and answer[-1] == self.Target:
                print("✅ Đã tìm thấy nghiệm! Số bước:", len(answer) - 1)
            else:
                print("⚠️ Bị kẹt ở local optimum sau", len(answer) - 1, "bước")
            for state in answer:
                drawtable(self.canvasL, state)
                self.WINDOW.update()
                self.WINDOW.after(100)
            else:
                print("Không tìm thấy nghiệm.")

        elif selected == "Local Beam Search":
            answer = run_local_beam_search(self.Target, 5)
            if answer and answer[-1] == self.Target:
                print("✅ Đã tìm thấy nghiệm! Số bước:", len(answer) - 1)
            else:
                print("⚠️ Bị kẹt ở local optimum sau", len(answer) - 1, "bước")
            for state in answer:
                drawtable(self.canvasL, state)
                self.WINDOW.update()
                self.WINDOW.after(100)
            else:
                print("Không tìm thấy nghiệm.")


        elif selected == "Genetic Algorithm":
            best, result = run_genetic_algorithm(self.Target)
            if result and result[-1] == self.Target:
                print("✅ Đã tìm thấy nghiệm!")
                for state in result:
                    print(state)
                    drawtable(self.canvasL, state)
                    self.WINDOW.update()
                    self.WINDOW.after(1000)
            else:
                print("⚠️ Không tìm thấy nghiệm chính xác, chỉ gần đúng.")
        #     print("Đang chạy thuật toán Hill Climbing...")
        # elif selected == "Genetic Algorithm":
        #     print("Đang chạy giải thuật di truyền...")
        # else:
        #     print("Chưa chọn thuật toán nào!")

    #Khởi chạy cửa sổ
    def run(self):
        self.WINDOW.mainloop()






