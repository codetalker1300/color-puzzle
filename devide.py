import tkinter as tk
from tkinter import PhotoImage
import random

PIXEL_SIZE = 2  # 每個顏色畫成 2x2 像素
WIDTH, HEIGHT = 512, 512
GRID_SIZE = 8  # 8x8 正方形
square_size = WIDTH // GRID_SIZE  # 每個正方形是 64x64 像素

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

            # 將 RGB 值轉換為十六進制顏色格式
            color = f'#{r:02x}{g:02x}{b:02x}'
            img.put(color, (x*PIXEL_SIZE, y*PIXEL_SIZE))
            img.put(color,(x*PIXEL_SIZE+1,y*PIXEL_SIZE))
            img.put(color, (x*PIXEL_SIZE, y*PIXEL_SIZE+1))
            img.put(color,(x*PIXEL_SIZE+1,y*PIXEL_SIZE+1))

    return img

def get_block_image(img, block_x, block_y):
    # 提取 (block_x, block_y) 的 32x32 正方形區塊
    block_image = PhotoImage(width=square_size, height=square_size)
    
    for y in range(square_size):
        for x in range(square_size):
            # 計算在原圖中的位置
            original_x = block_x * square_size + x
            original_y = block_y * square_size + y
            
            # 取得顏色 (這將會是一個 tuple，如 (r, g, b))
            color_tuple = img.get(original_x, original_y)
            
            # 把 tuple 轉換為十六進制顏色碼
            r, g, b = color_tuple
            color = f'#{r:02x}{g:02x}{b:02x}'  # 轉換為十六進制顏色碼

            # 放入 block_image
            block_image.put(color, (x, y))
    
    return block_image

def on_click(event):
    # 找出目前滑鼠點擊位置的項目
    overlapping = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    
    for item in overlapping:
        if item in shuffle_block:
            if item in selected:
                # 第二次點選：取消選取，刪除框線
                canvas.delete(outlines[item])
                selected.remove(item)
                del outlines[item]
            else:
                # 選取圖片（最多兩個）
                if len(selected) < 2:
                    x, y = canvas.coords(item)
                    bbox = (x, y, x + square_size, y + square_size)
                    rect = canvas.create_rectangle(*bbox, outline="black", width=2)
                    outlines[item] = rect
                    selected.append(item)

                # 如果選滿兩個，互換位置並清除框線
                if len(selected) == 2:
                    item1, item2 = selected
                    x1, y1 = canvas.coords(item1)
                    x2, y2 = canvas.coords(item2)
                    canvas.coords(item1, x2, y2)
                    canvas.coords(item2, x1, y1)
                    canvas.delete(outlines[item1])
                    canvas.delete(outlines[item2])
                    outlines.clear()
                    selected.clear()
            break


# 建立 tkinter 介面
root = tk.Tk()
root.title("分割並打亂正方形")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# 生成漸層圖片
gradient_image = generate_fixed_axis_gradient()
#canvas.create_image(100,100, image=gradient_image)
# 儲存所有的 64 個區塊圖像
stander_blocks = []
shuffle_block=[]
block_coord=[]
for block_y in range(GRID_SIZE):
    for block_x in range(GRID_SIZE):
        block_image = get_block_image(gradient_image, block_x, block_y)
        stander_blocks.append(block_image)
        shuffle_block.append(block_image)

# 打亂區塊的順序
random.shuffle(shuffle_block)

# 顯示打亂後的區塊
for i, block_image in enumerate(shuffle_block):
    # 計算每個區塊在畫布上的位置
    row = i // GRID_SIZE
    col = i % GRID_SIZE
    x_pos = col * square_size
    y_pos = row * square_size
    block_coord.append([x_pos,y_pos])
    
    
    # 在畫布上顯示打亂的區塊
    canvas.create_image(x_pos, y_pos, image=block_image, anchor="nw")

# 防止圖片被垃圾回收
canvas.image = shuffle_block[0]  # 保存其中一個圖像引用以防止被回收
selected = []
outlines = {}

# 綁定滑鼠事件
canvas.bind("<Button-1>", on_click)
root.mainloop()
