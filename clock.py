import tkinter as tk

def update_label():
    global count, after_id
    count += 1
    h = count // 3600
    m = (count % 3600) // 60
    s = count % 60
    formatted_time = f"{h:02}:{m:02}:{s:02}"
    time.config(text=f"時間：{formatted_time}")
    after_id = root.after(1000, update_label)

def start_timer():
    global running, after_id
    if not running:
        running = True
        after_id = root.after(1000, update_label)

def stop_timer():
    global running, after_id
    if running and after_id:
        root.after_cancel(after_id)
        after_id = None
        running = False

def reset_timer():
    global count, running, after_id
    stop_timer()  # 先停止計時
    count = 0
    time.config(text="時間：00:00:00")

# GUI 主視窗
root = tk.Tk()
root.title("碼表")
count = 0
running = False
after_id = None

# 時間顯示
time = tk.Label(root, text="時間：00:00:00", font=("Helvetica", 20))
time.pack(pady=10)

# 控制按鈕
start_btn = tk.Button(root, text="開始", command=start_timer)
start_btn.pack(side="left", padx=10)

stop_btn = tk.Button(root, text="停止", command=stop_timer)
stop_btn.pack(side="left", padx=10)

reset_btn = tk.Button(root, text="重置", command=reset_timer)
reset_btn.pack(side="left", padx=10)

root.mainloop()
