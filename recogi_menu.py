import tkinter as tk
import random

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(pady=40)

        tk.Label(self.menu_frame, text="請選擇要開始的遊戲", font=("Arial", 16)).pack(pady=10)

        self.difficulty_var = tk.StringVar(value="6x6")
        difficulty_options = ["6x6", "7x7", "8x8", "9x9"]

        tk.Label(self.menu_frame, text="選擇難度：", font=("Arial", 12)).pack(pady=5)
        self.difficulty_menu = tk.OptionMenu(self.menu_frame, self.difficulty_var, *difficulty_options)
        self.difficulty_menu.pack(pady=5)

        tk.Button(self.menu_frame, text="開始 色差遊戲", font=("Arial", 14),
                  command=self.start_color_game).pack(pady=15)

        # 預留按鈕可以放漸層遊戲或其他遊戲
        tk.Button(self.menu_frame, text="（未來）開始 漸層遊戲", font=("Arial", 14),
                  state=tk.DISABLED).pack(pady=5)

    def start_color_game(self):
        difficulty = self.difficulty_var.get()
        self.menu_frame.destroy()  # 關閉選單畫面
        ColorDifferenceGame(self.root, difficulty)

class ColorDifferenceGame:
    def __init__(self, root, difficulty):
        self.root = root
        self.difficulty = difficulty
        self.max_size = int(difficulty[0])
        self.grid_size = 2
        self.grid_repeat_count = 0
        self.max_repeat = 3

        self.canvas_size = 400
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size + 40, bg="white")
        self.canvas.pack()

        self.time_left = 60
        self.score = 0
        self.info_label = tk.Label(root, text="", font=("Arial", 16))
        self.info_label.pack()

        self.update_timer()
        self.next_level()

    def update_timer(self):
        self.info_label.config(text=f"剩餘時間：{self.time_left} 秒 ｜ 第{self.score+1}關")
        if self.time_left > 0:
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.canvas.delete("all")
            self.canvas.create_text(self.canvas_size / 2, self.canvas_size / 2,
                                    text=f"遊戲結束！總分：{self.score}", font=("Arial", 24), fill="red")
            self.info_label.config(text=f"")

    def next_level(self):
        if self.time_left <= 0:
            return

        self.canvas.delete("all")
        base_color = [random.randint(50, 200) for _ in range(3)]
        diff_index = random.randint(0, self.grid_size ** 2 - 1)
        diff_color = base_color[:]
        diff_color[random.randint(0, 2)] += random.randint(10, 30)
        self.info_label.config(text=f"剩餘時間：{self.time_left} 秒 ｜ 第{self.score+1}關")
        #diff_color = [min(255, c) for c in diff_color]

        spacing = 10
        total_spacing = (self.grid_size + 1) * spacing
        box_size = (self.canvas_size - total_spacing) / self.grid_size
        radius = min(10, box_size / 5)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                idx = i * self.grid_size + j
                color = base_color if idx != diff_index else diff_color
                hex_color = "#%02x%02x%02x" % (color[0], color[1], color[2]) #f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
                x1 = spacing + j * (box_size + spacing)
                y1 = spacing + i * (box_size + spacing)
                x2 = x1 + box_size
                y2 = y1 + box_size
                if idx == diff_index:
                    self.correct_box = (x1, y1, x2, y2)
                rect = self.create_round_rect(x1, y1, x2, y2, radius, fill=hex_color, outline="")
                self.canvas.tag_bind(rect, '<Button-1>', self.check_answer)

        if self.grid_size < self.max_size:
            self.grid_repeat_count += 1
            if self.grid_repeat_count >= self.max_repeat:
                self.grid_size += 1
                self.grid_repeat_count = 0
        else:
            self.grid_repeat_count = 0

    def create_round_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def check_answer(self, event):
        x, y = event.x, event.y
        x1, y1, x2, y2 = self.correct_box
        if x1 <= x <= x2 and y1 <= y <= y2:
            self.score += 1
            self.next_level()

# 主程式入口
if __name__ == "__main__":
    root = tk.Tk()
    root.title("色彩遊戲選單")
    root.geometry("420x520")
    MainMenu(root)
    root.mainloop()