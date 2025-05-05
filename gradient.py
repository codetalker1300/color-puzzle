import tkinter as tk
import random

PIXEL_SIZE = 2  # 每個顏色畫成 2x2 像素
WIDTH, HEIGHT = 256, 256
DISPLAY_WIDTH = WIDTH * PIXEL_SIZE
DISPLAY_HEIGHT = HEIGHT * PIXEL_SIZE

def generate_fixed_axis_gradient(canvas):
    axes = ['R', 'G', 'B']
    fixed_axis = random.choice(axes)
    fixed_value = random.randint(0, 255)
    print(f"固定軸：{fixed_axis}, 固定值：{fixed_value}")

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if fixed_axis == 'R':
                r, g, b = fixed_value, y, x
            elif fixed_axis == 'G':
                r, g, b = x, fixed_value, y
            else:
                r, g, b = y, x, fixed_value

            color = f'#{r:02x}{g:02x}{b:02x}'

            # 畫一個 2x2 像素的矩形
            canvas.create_rectangle(
                x * PIXEL_SIZE, y * PIXEL_SIZE,
                (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE,
                outline="", fill=color
            )

# 建立介面
root = tk.Tk()
root.title("放大漸層顯示")

canvas = tk.Canvas(root, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
canvas.pack()

generate_fixed_axis_gradient(canvas)

root.mainloop()
