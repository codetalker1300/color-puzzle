import tkinter as tk
from tkinter import ttk
from color_diff import ColorDiffGame
from puzzle import PuzzleApp

class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("色彩遊戲選單")
        self.root.geometry("420x320")
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=40)

        tk.Label(self.menu_frame, text="請選擇要開始的遊戲", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(self.menu_frame, text="選擇遊戲：", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        games = ["色差遊戲", "漸層/拼圖遊戲"]
        self.game_var = tk.StringVar()       
        self.game_combobox = ttk.Combobox(self.menu_frame, textvariable=self.game_var, values=games, state="readonly")
        self.game_combobox.current(0)
        self.game_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.game_var.trace_add("write", self.change_option)

        tk.Label(self.menu_frame, text="選擇難度：", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
        self.diff_opt = ["6x6", "7x7", "8x8", "9x9"]
        self.diff_var = tk.StringVar()
        self.diff_combobox = ttk.Combobox(self.menu_frame, textvariable=self.diff_var, values=self.diff_opt, state="readonly")
        self.diff_combobox.current(0)
        self.diff_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.menu_frame, text="選擇模式：", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
        self.mode_opt = ["限時60秒", "完成30關", "無盡"]
        self.mode_var = tk.StringVar()
        self.mode_combobox = ttk.Combobox(self.menu_frame, textvariable=self.mode_var, values=self.mode_opt, state="readonly")
        self.mode_combobox.current(0)
        self.mode_combobox.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.menu_frame, text="成績紀錄：", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(self.menu_frame, text="檢視", font=("Arial", 12),
                  command=self.check_score).grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        tk.Button(self.menu_frame, text="開始", font=("Arial", 14),
                  command=self.start_game).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
    def change_option(self, *args):
        game = self.game_var.get()
        self.diff_combobox["values"] = {"色差遊戲": ["6x6", "7x7", "8x8", "9x9"],
                                        "漸層/拼圖遊戲": ["簡單", "中等", "困難",]}[game]
        self.diff_combobox.current(0)
        self.mode_combobox["values"] = {"色差遊戲": ["限時60秒", "完成30關", "無盡"],
                                        "漸層/拼圖遊戲": ["限制步數", "無盡"]}[game]
        self.mode_combobox.current(0)

    def start_game(self):
        game = self.game_var.get()
        difficulty = self.diff_var.get()
        mode = self.mode_var.get()
        self.menu_frame.pack_forget()  # 隱藏選單畫面
        if game == "色差遊戲":
            ColorDiffGame(self.root, self.menu_frame, difficulty, mode)
        else:
            PuzzleApp(self.root, self.menu_frame, difficulty, mode)

    def check_score(self):
        return

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    menu = MainMenu()
    menu.start()