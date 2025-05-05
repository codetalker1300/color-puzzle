import tkinter as tk
from tkinter import PhotoImage
import random
from tkinter import messagebox


PIXEL_SIZE = 2
WIDTH, HEIGHT = 512, 512
GRID_SIZE = 8
square_size = WIDTH // GRID_SIZE

class Cube:
    def __init__(self, img, ans_coord, now_coord, canvas):
        self.image = img
        self.ans_coordinate = ans_coord  # 正確位置
        self.now_coordinate = now_coord  # 當前位置
        self.block = canvas.create_image(now_coord[0], now_coord[1], image=img, anchor="nw")

    def move_to(self, canvas, new_coord):
        """ 移動到新座標，更新畫面與座標屬性 """
        canvas.coords(self.block, new_coord[0], new_coord[1])
        self.now_coordinate = new_coord

    def is_correct(self):
        """ 判斷是否回到正確位置 """
        return self.now_coordinate == self.ans_coordinate

def generate_fixed_axis_gradient():
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
                    img.put(color, (x*PIXEL_SIZE + dx, y*PIXEL_SIZE + dy))
    return img

def get_block_image(img, block_x, block_y):
    block_image = PhotoImage(width=square_size, height=square_size)
    for y in range(square_size):
        for x in range(square_size):
            original_x = block_x * square_size + x
            original_y = block_y * square_size + y
            r, g, b = img.get(original_x, original_y)
            color = f'#{r:02x}{g:02x}{b:02x}'
            block_image.put(color, (x, y))
    return block_image

def on_click(event):
    overlapping = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    for item_id in overlapping:
        for cube in cubes:
            if cube.block == item_id:
                if cube in selected:
                    canvas.delete(outlines[cube])
                    selected.remove(cube)
                    del outlines[cube]
                else:
                    if cube.now_coordinate in fix_coords:
                        break
                    if len(selected) < 2:
                        x, y = cube.now_coordinate
                        rect = canvas.create_rectangle(x, y, x + square_size, y + square_size, outline="black", width=2)
                        outlines[cube] = rect
                        selected.append(cube)

                    if len(selected) == 2:
                        cube1, cube2 = selected
                        # 互換座標
                        coord1, coord2 = cube1.now_coordinate, cube2.now_coordinate
                        cube1.move_to(canvas, coord2)
                        cube2.move_to(canvas, coord1)

                        # 清除框線與選取
                        canvas.delete(outlines[cube1])
                        canvas.delete(outlines[cube2])
                        outlines.clear()
                        selected.clear()

                        # 檢查是否全部復原
                        if all(c.is_correct() for c in cubes):
                            messagebox.showinfo("完成！", "你已成功復原所有方塊！")

                break
        break


# 建立 tkinter 介面
root = tk.Tk()
root.title("分割並打亂正方形")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# 產生漸層圖
gradient_image = generate_fixed_axis_gradient()

# 建立區塊圖像
blocks = []
correct_coords = []
edge_coords = []
for by in range(GRID_SIZE):
    for bx in range(GRID_SIZE):
        block = get_block_image(gradient_image, bx, by)
        blocks.append(block)
        correct_coords.append([bx * square_size, by * square_size])
        if bx==0 or by==0 or bx==7 or by==7:
            edge_coords.append([bx * square_size, by * square_size])

# 洗牌
shuffled_coords = correct_coords[:]
random.shuffle(shuffled_coords)

fix_coords=random.sample(edge_coords, 10)
for i in fix_coords:
    correct_index=correct_coords.index(i)
    now_index=shuffled_coords.index(i)
    shuffled_coords[correct_index],shuffled_coords[now_index]=shuffled_coords[now_index],shuffled_coords[correct_index]
    

# 建立 Cube 實例並記錄
cubes = []
for i in range(len(blocks)):
    cube = Cube(blocks[i], correct_coords[i], shuffled_coords[i], canvas)
    cubes.append(cube)

for i in fix_coords:
    canvas.create_oval(i[0]+25,i[1]+25,i[0]+37,i[1]+37)

# 防止圖片回收
canvas.images = blocks

# 資料結構
selected = []
outlines = {}

# 綁定滑鼠事件
canvas.bind("<Button-1>", on_click)
root.mainloop()
