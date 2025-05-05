import tkinter as tk
from tkinter import PhotoImage, messagebox
import random

PIXEL_SIZE = 2
WIDTH, HEIGHT = 512, 512
GRID_SIZE = 8
SQUARE_SIZE = WIDTH // GRID_SIZE

class Cube:
    def __init__(self, img, ans_coord, now_coord, canvas):
        self.image = img
        self.ans_coordinate = ans_coord
        self.now_coordinate = now_coord
        self.block = canvas.create_image(*now_coord, image=img, anchor="nw")

    def move_to(self, canvas, new_coord):
        canvas.coords(self.block, *new_coord)
        self.now_coordinate = new_coord

    def is_correct(self):
        return self.now_coordinate == self.ans_coordinate

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("分割並打亂正方形")

        self.counter_frame =tk.Frame(root)
        self.counter_frame.pack()
        # Frame + Canvas
        self.canva_frame = tk.Frame(root)
        self.canva_frame.pack()
        self.canvas = tk.Canvas(self.canva_frame, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.blocks = []
        self.cubes = []
        self.selected = []
        self.outlines = {}

        self.correct_coords = []
        self.fix_coords = []

        self.gradient_image = self.generate_fixed_axis_gradient()
        self.prepare_blocks()
        self.bind_events()

    def generate_fixed_axis_gradient(self):
        axes = ['R', 'G', 'B']
        fixed_axis = random.choice(axes)
        fixed_value = random.randint(0, 255)
        print(f"固定軸：{fixed_axis}, 固定值：{fixed_value}")

        img = PhotoImage(width=WIDTH, height=HEIGHT)
        for y in range(256):
            for x in range(256):
                if fixed_axis == 'R':
                    r, g, b = fixed_value, y, x
                elif fixed_axis == 'G':
                    r, g, b = x, fixed_value, y
                else:
                    r, g, b = y, x, fixed_value
                color = f'#{r:02x}{g:02x}{b:02x}'
                for dx in range(PIXEL_SIZE):
                    for dy in range(PIXEL_SIZE):
                        img.put(color, (x * PIXEL_SIZE + dx, y * PIXEL_SIZE + dy))
        return img

    def get_block_image(self, img, block_x, block_y):
        block_image = PhotoImage(width=SQUARE_SIZE, height=SQUARE_SIZE)
        for y in range(SQUARE_SIZE):
            for x in range(SQUARE_SIZE):
                r, g, b = img.get(block_x * SQUARE_SIZE + x, block_y * SQUARE_SIZE + y)
                color = f'#{r:02x}{g:02x}{b:02x}'
                block_image.put(color, (x, y))
        return block_image

    def prepare_blocks(self):
        edge_coords = []
        for by in range(GRID_SIZE):
            for bx in range(GRID_SIZE):
                block = self.get_block_image(self.gradient_image, bx, by)
                self.blocks.append(block)
                coord = [bx * SQUARE_SIZE, by * SQUARE_SIZE]
                self.correct_coords.append(coord)
                if bx == 0 or by == 0 or bx == 7 or by == 7:
                    edge_coords.append(coord)

        shuffled_coords = self.correct_coords[:]
        random.shuffle(shuffled_coords)

        # 固定邊緣 10 塊
        self.fix_coords = random.sample(edge_coords, 4)
        for fixed in self.fix_coords:
            correct_idx = self.correct_coords.index(fixed)
            now_idx = shuffled_coords.index(fixed)
            shuffled_coords[correct_idx], shuffled_coords[now_idx] = shuffled_coords[now_idx], shuffled_coords[correct_idx]

        # 建立方塊
        for i in range(len(self.blocks)):
            cube = Cube(self.blocks[i], self.correct_coords[i], shuffled_coords[i], self.canvas)
            self.cubes.append(cube)

        # 顯示固定標記
        for coord in self.fix_coords:
            x, y = coord
            self.canvas.create_oval(x+25, y+25, x+37, y+37, fill='black')

        # 防止圖片被回收
        self.canvas.images = self.blocks

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        overlapping = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item_id in overlapping:
            for cube in self.cubes:
                if cube.block == item_id:
                    if cube in self.selected:
                        self.canvas.delete(self.outlines[cube])
                        self.selected.remove(cube)
                        del self.outlines[cube]
                    else:
                        if cube.now_coordinate in self.fix_coords:
                            break
                        if len(self.selected) < 2:
                            x, y = cube.now_coordinate
                            rect = self.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, outline="black", width=2)
                            self.outlines[cube] = rect
                            self.selected.append(cube)

                        if len(self.selected) == 2:
                            c1, c2 = self.selected
                            coord1, coord2 = c1.now_coordinate, c2.now_coordinate
                            c1.move_to(self.canvas, coord2)
                            c2.move_to(self.canvas, coord1)

                            self.canvas.delete(self.outlines[c1])
                            self.canvas.delete(self.outlines[c2])
                            self.outlines.clear()
                            self.selected.clear()

                            if all(c.is_correct() for c in self.cubes):
                                messagebox.showinfo("完成！", "你已成功復原所有方塊！")
                    break
            break

# 主程式
if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()
