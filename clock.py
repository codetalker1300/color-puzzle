import tkinter as tk

def update_label():
    global count
    count += 1
    h = count // 3600
    m = (count % 3600) // 60
    s = count % 60
    formatted_time = f"{h:02}:{m:02}:{s:02}"
    time.config(text=f"時間：{formatted_time}")
    root.after(1000, update_label)  # 每1000毫秒呼叫自己

root = tk.Tk()
count = 0
time = tk.Label(root, text=f"時間：{0:02}:{0:02}:{0:02}")
time.pack(side='left')


root.after(1000, update_label)  # 開始計時
root.mainloop()
