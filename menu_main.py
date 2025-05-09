import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from color_diff import ColorDiffGame
from puzzle import PuzzleApp
import os

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

    #依照遊戲類別更改難度和模式的選項    
    def change_option(self, *args):
        game = self.game_var.get()
        self.diff_combobox["values"] = {"色差遊戲": ["6x6", "7x7", "8x8", "9x9"],
                                        "漸層/拼圖遊戲": ["簡單", "中等", "困難",]}[game]
        self.diff_combobox.current(0)
        self.mode_combobox["values"] = {"色差遊戲": ["限時60秒", "完成30關", "無盡"],
                                        "漸層/拼圖遊戲": ["挑戰", "無盡"]}[game]
        self.mode_combobox.current(0)

    #呼叫對應遊戲，提供能返回主頁和遊戲設定資訊的必要參數
    def start_game(self):
        game = self.game_var.get()
        difficulty = self.diff_var.get()
        mode = self.mode_var.get()
        self.menu_frame.pack_forget()  # 隱藏選單畫面
        if game == "色差遊戲":
            ColorDiffGame(self.root, self.menu_frame, difficulty, mode)
        else:
            PuzzleApp(self.root, self.menu_frame, difficulty, mode)

    #控制顯示成績紀錄的排序
    def treeview_sortCols(self, col, head):

        lst = [st for st in self.tree.get_children("")]
        
        self.reverseFlag[col] = not self.reverseFlag[col] #改變正反序
        icon = "▲" if self.reverseFlag[col] else "▼"
        self.tree.heading(col, text = icon+head,
                            command=lambda c=col, h=head: self.treeview_sortCols(c,h))
        re = 1 if self.reverseFlag[col] else -1 #對時間、分/步數有用的正反序
        re_mode = 1 if self.reverseFlag["mode"] else -1 #對模式有用的正反序
        re_diff = 1 if self.reverseFlag["diff"] else -1 #對難度有用的正反序

        mode_priority = {"限時60秒": 0, "完成30關": 1, "挑戰": 2, "無盡": 3}
        diff_priority = {"簡單": 0, "中等": 1, "困難": 2, "6x6":3, "7x7":4, "8x8":5, "9x9":6}
        if col == "mode": #先排模式後排難度
            lst.sort(key=lambda item: (mode_priority.get(self.tree.set(item, "mode"), 999)*re_mode,
                                       diff_priority.get(self.tree.set(item, "diff"), 999)*re_diff))
            self.sortFlag = 1
        elif col == "diff": #先排難度後排模式
            lst.sort(key=lambda item: (diff_priority.get(self.tree.set(item, "diff"), 999)*re_diff,
                                       mode_priority.get(self.tree.set(item, "mode"), 999)*re_mode))
            self.sortFlag = 2
        elif col == "score_step": #步數
            self.tree.heading("sec", text = "遊玩時間", #時間有icon的話刪掉
                            command=lambda c="sec", h="遊玩時間": self.treeview_sortCols(c,h)) 
            if self.sortFlag == 0: #直接排
                lst.sort(key=lambda item: (int(self.tree.set(item, col))*re))
            elif self.sortFlag == 1: #先排模式後排難度再排
                lst.sort(key=lambda item: (mode_priority.get(self.tree.set(item, "mode"), 999)*re_mode,
                                           diff_priority.get(self.tree.set(item, "diff"), 999)*re_diff,
                                           int(self.tree.set(item, col))*re))
            else:                    #先排難度後排模式再排
                lst.sort(key=lambda item: (diff_priority.get(self.tree.set(item, "diff"), 999)*re_diff,
                                           mode_priority.get(self.tree.set(item, "mode"), 999)*re_mode,                                           
                                           int(self.tree.set(item, col))*re))
        else: #時間
            self.tree.heading(self.cols[3], text = self.head[3], #分/步數有icon的話刪掉
                            command=lambda c=self.cols[3], h=self.head[3]: self.treeview_sortCols(c,h)) 
            if self.sortFlag == 0: #直接排
                lst.sort(key=lambda item: (int(self.tree.item(item, "text"))*re))
            elif self.sortFlag == 1: #先排模式後排難度再排
                lst.sort(key=lambda item: (mode_priority.get(self.tree.set(item, "mode"), 999)*re_mode,
                                           diff_priority.get(self.tree.set(item, "diff"), 999)*re_diff,
                                           int(self.tree.item(item, "text"))*re))
            else:                    #先排難度後排模式再排
                lst.sort(key=lambda item: (diff_priority.get(self.tree.set(item, "diff"), 999)*re_diff,
                                           mode_priority.get(self.tree.set(item, "mode"), 999)*re_mode,                                           
                                           int(self.tree.item(item, "text"))*re))

        for index, item in enumerate(lst):
            self.tree.move(item, "", index)
            tag = "evenColor" if index % 2 == 1 else "oddColor"
            self.tree.item(item, tags=tag)

    #顯示成績紀錄
    def check_score(self):
        game = self.game_var.get()
        score_window = tk.Toplevel()
        score_window.title("成績紀錄")
        score_window.grab_set()    # 阻止使用者與其他視窗互動
        file_path = os.path.dirname(os.path.realpath(__file__))
        if game == "色差遊戲":
            head_last = "分數/破關數"
            file_path += "/colordiff_history.csv"
        else:
            head_last = "移動步數"
            file_path += "/puzzle_history.csv"
        self.cols = ("diff", "mode", "sec", "score_step")
        self.head = ["難度", "模式", "遊玩時間", head_last]
        self.tree = ttk.Treeview(score_window, columns=self.cols, show="headings")
        self.tree.pack()
        self.reverseFlag = {} #正反序
        self.sortFlag = 0 #排序右兩項會用到
        for i in range(4):
            self.tree.heading(self.cols[i], text = self.head[i],
                              command=lambda c=self.cols[i], h=self.head[i]: self.treeview_sortCols(c,h))
            self.tree.column(self.cols[i], anchor=tk.CENTER, width=120)
            self.reverseFlag[self.cols[i]] = False
        self.tree.tag_configure("evenColor", background="lightblue")
        self.tree.tag_configure("oddColor", background="white")
        bg = 1
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = []
                for line in file:
                    vals = line.split(",")
                    sec = int(vals[2])
                    if vals[1] == "限時60秒":
                        sec = 60
                    vals[2] = f"{sec//60:02}:{sec%60:02}"
                    data.append((sec, vals))
                data.reverse()
                for sec, vals in data:
                    if bg % 2 == 0:
                        self.tree.insert("", text = sec,index=tk.END, values=vals, tags=("evenColor"))
                    else:
                        self.tree.insert("", text = sec,index=tk.END, values=vals)
                    bg += 1
        except Exception:
            messagebox.showerror("讀檔錯誤", f"暫無資料或載入失敗")
            
    
    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    menu = MainMenu()
    menu.start()