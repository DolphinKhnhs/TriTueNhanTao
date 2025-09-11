import tkinter as tk

N= 8
size = 50

class UI:
    def __init__(self, window, algorithm, target):
        window.title("8 Rooks")
        window_width = 1000
        window_height = 600
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        UI.drawtable(UI.canvas_left(window), [[0]*N for i in range(N)])
        UI.drawtable(UI.canvas_right(window), [[0]*N for i in range(N)])

        solve_btn = tk.Button(window, text="Solve with DFS", command=lambda: algorithm.dfs(target, window))
        solve_btn.config(font=('Lato', 12, 'bold'))
        solve_btn.place(x=675, y=525, width=150, height=50)



    @staticmethod
    def drawtable(canvas, rooks):
        canvas.delete("all")
        for i in range(N):
            for j in range(N):
                x1 = 25 + j * size
                y1 = 25 + i * size
                x2 = x1 + size
                y2 = y1 + size
                color = "#e6e1a5" if (i + j) % 2 == 0 else "#a86b21"
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                if rooks[i][j] == 1:
                    canvas.create_text(
                        x1 + size / 2,
                        y1 + size / 2,
                        text="♖", fill="red", font=('Lato', 24, 'bold')
                    )

        for i in range(N):
            name1 = str(i+1)
            name2 = str(i+1)
            x = size / 2 + i * size + size / 2
            y = size / 2 + i * size + size / 2
            canvas.create_text(10, y, text=name1, font=("Arial", 12, "bold"))
            #canvas.create_text(10 + N * size + 25, y, text=name1, font=("Arial", 12, "bold"))
            canvas.create_text(x, 10, text=name2, font=("Arial", 12, "bold"))
            #canvas.create_text(x, 10 + N * size + 25, text=name2, font=("Arial", 12, "bold"))

    @staticmethod
    def canvas_left(window):
        canvas = tk.Canvas(window, width=N * size + 50, height=N * size + 50, highlightthickness=0)
        canvas.place(x=50, y=50)
        return canvas

    @staticmethod
    def canvas_right(window):
        canvas = tk.Canvas(window, width=N * size + 50, height=N * size + 50, highlightthickness=0)
        canvas.place(x=500, y=50)
        return canvas



