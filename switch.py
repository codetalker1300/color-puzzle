import tkinter as tk
from tkinter import messagebox


class SquareSwapper:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=600, height=250, bg='white')
        self.canvas.pack()

        self.squares = []  # 儲存正方形 ID
        self.squares_coor = []
        self.colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow']  # 六種顏色

        # 建立 6 個正方形
        for i in range(6):
            x0 = 30 + i * 90  # 每個方塊間隔 90px
            y0 = 70
            rect = self.canvas.create_rectangle(
                x0, y0, x0 + 70, y0 + 70,
                fill=self.colors[i],
                width=2,
                outline=""  # 初始無邊框
            )
            self.squares_coor.append(self.canvas.coords(rect))
            self.squares.append(rect)

        self.canvas.bind("<Button-1>", self.on_click)
        self.selected = []

    def on_click(self, event):
        clicked_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)

        for item in clicked_items:
            if item in self.squares:
                self.toggle_selection(item)
                break  # 只處理第一個有效物件

    def toggle_selection(self, item):
        if item in self.selected:
            self.canvas.itemconfig(item, outline="")
            self.selected.remove(item)
        elif len(self.selected) < 2:
            self.canvas.itemconfig(item, outline="black")
            self.selected.append(item)

        if len(self.selected) == 2:
            # 交換顏色
            # color1 = self.canvas.itemcget(self.selected[0], 'fill')
            # color2 = self.canvas.itemcget(self.selected[1], 'fill')
            # self.canvas.itemconfig(self.selected[0], fill=color2, outline="")
            # self.canvas.itemconfig(self.selected[1], fill=color1, outline="")
            # self.selected.clear()
            position1 = self.canvas.coords(self.selected[0])
            position2 = self.canvas.coords(self.selected[1])
            self.canvas.coords(self.selected[0],position2)
            self.canvas.coords(self.selected[1],position1)
            self.canvas.itemconfig(self.selected[0],outline="")
            self.canvas.itemconfig(self.selected[1],outline="")
            self.selected.clear()
            for i in range (len(self.squares)):
                if self.canvas.coords(self.squares[i])!=self.squares_coor[i]:
                    break
                if i==(len(self.squares)-1) and self.canvas.coords(self.squares[i])==self.squares_coor[i]:
                    messagebox.showinfo('showwarning',"pass")
# 啟動程式
root = tk.Tk()
app = SquareSwapper(root)
root.mainloop()
