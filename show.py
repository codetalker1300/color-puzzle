import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# 假設這是你已經有的圖片 (範例：產生一張 NumPy 圖片)
img_array = np.random.rand(100, 100, 3)  # 假設你已經有這張圖片

def show_image():
    plt.figure()
    plt.imshow(img_array)  # 如果是 PIL image 可用 plt.imshow(np.array(img))
    plt.axis('off')        # 不顯示座標軸
    plt.title("已產生的圖片")
    plt.show()

root = tk.Tk()
btn = tk.Button(root, text="顯示圖片", command=show_image)
btn.pack(pady=20)

root.mainloop()
