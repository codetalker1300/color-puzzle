import tkinter as tk
import random
from tkinter import messagebox
import os

class ColorDiffGame:
    def __init__(self, root, menu_frame, difficulty, mode):
        self.root = root
        self.menu_frame = menu_frame
        self.color_game = tk.Frame(self.root)
        self.color_game.pack()
        self.root.title("色差遊戲")
        self.root.geometry("420x520")
        self.difficulty = difficulty
        self.max_size = int(difficulty[0])
        self.mode = mode
        self.max_repeat = 3
        self.after_id = None

        self.timer_label = tk.Label(self.color_game, text="", font=("Arial", 16))
        self.timer_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.level_label = tk.Label(self.color_game, text="", font=("Arial", 16))
        self.level_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5)

        self.canvas_size = 400
        self.canvas = tk.Canvas(self.color_game, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        self.reload = tk.Button(self.color_game, text="重新開始",
                                      font=("Arial", 12), command=self.start_game)
        self.reload.grid(row=2, column=0, padx=5, pady=5)

        self.skip = tk.Button(self.color_game, text="跳過此關",
                                      font=("Arial", 12), command=self.next_level)
        self.skip.grid(row=2, column=1, padx=5, pady=5)

        self.endbtn = tk.Button(self.color_game, text="結算",
                                      font=("Arial", 12), command=self.end_game)
        self.endbtn.grid(row=2, column=2, padx=5, pady=5)
        self.endbtn.grid_remove()

        self.back = tk.Button(self.color_game, text="回menu",
                                      font=("Arial", 12), command=self.back_menu)
        self.back.grid(row=2, column=3, padx=5, pady=5)

        self.start_game()  

    def start_game(self):
        if self.after_id:
            self.color_game.after_cancel(self.after_id)
        self.grid_size = 2
        self.grid_repeat_count = 0
        self.level = 0
        self.score = 0
        self.skip.config(state="normal")
        self.max_score = 30
        if self.mode == "限時60秒":
            self.time = 60
            self.update_timer_limit()
        elif self.mode == "完成30關":
            self.time = 0
            self.update_timer_level()
        else:
            self.endbtn.grid()
            self.endbtn.config(state="normal")
            self.time = 0
            self.update_timer_level()
        self.next_level()

    def update_timer_limit(self):
        self.timer_label.config(text=f"剩餘時間：{self.time} 秒")
        if self.time > 0:
            self.time -= 1
            self.after_id = self.color_game.after(1000, self.update_timer_limit)
        else:
            self.end_game()

    def update_timer_level(self):
        if self.mode == "完成30關" and self.score >= self.max_score:
            return
        m = self.time // 60
        s = self.time % 60
        self.timer_label.config(text=f"時間 ： {m:02}:{s:02}")
        self.time += 1
        self.after_id = self.color_game.after(1000, self.update_timer_level)

    def end_game(self):
        self.canvas.delete("all")
        if self.mode == "限時60秒":
            self.canvas.create_text(self.canvas_size / 2, self.canvas_size / 2,
                                    text=f"遊戲結束！\n總分：{self.score}", font=("Arial", 24), fill="red")
        elif self.mode == "完成30關":
            self.canvas.create_text(self.canvas_size / 2, self.canvas_size / 2,
                                    text=f"遊戲結束！\n用時：{self.time // 60:02}:{self.time % 60:02}",
                                    font=("Arial", 24), fill="red")
        else:
            self.canvas.create_text(self.canvas_size / 2, self.canvas_size / 2,
                                    text=f"遊戲結束！\n總分：{self.score}\n用時：{self.time // 60:02}:{self.time % 60:02}",
                                    font=("Arial", 24), fill="red")
            self.endbtn.config(state="disabled")
            self.color_game.after_cancel(self.after_id)
        self.skip.config(state="disabled")

        file_path = os.path.dirname(os.path.realpath(__file__))+ "/colordiff_history.csv"
        try:
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f"{self.difficulty},{self.mode},{self.time},{self.score}\n")
        except Exception:
            messagebox.showerror("存檔錯誤", "儲存成績失敗")

    def next_level(self):
        self.canvas.delete("all")

        if self.mode == "完成30關" and self.score >= self.max_score:
            self.end_game()
            return
        
        #生出統一顏色跟加上一點差距的
        self.level += 1
        base_color = [random.randint(50, 200) for _ in range(3)]
        diff_index = random.randint(0, self.grid_size ** 2 - 1)
        diff_color = base_color[:]
        if self.level<=20:
            diff_color[random.randint(0, 2)] += random.randint(15, 30)
        else:
            diff_color[random.randint(0, 2)] += random.randint(5, 20)
        self.level_label.config(text=f"第{self.level}關")
        diff_color = [min(255, c) for c in diff_color]

        #計算版面配置
        spacing = 10
        total_spacing = (self.grid_size + 1) * spacing
        box_size = (self.canvas_size - total_spacing) / self.grid_size
        radius = min(10, box_size / 5)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                idx = i * self.grid_size + j
                color = base_color if idx != diff_index else diff_color
                hex_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
                x1 = spacing + j * (box_size + spacing)
                y1 = spacing + i * (box_size + spacing)
                x2 = x1 + box_size
                y2 = y1 + box_size
                if idx == diff_index: #紀錄正確答案座標
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

    #畫圓角正方形
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

    def back_menu(self):
        self.root.title("色彩遊戲選單")
        self.root.geometry("420x320")
        self.color_game.destroy()
        self.menu_frame.pack(pady=40)