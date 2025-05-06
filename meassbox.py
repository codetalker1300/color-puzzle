import tkinter as tk
from tkinter import messagebox

def ask_user():
    answer = messagebox.askyesno("確認", "你確定要執行這個動作嗎？")
    if answer:
        print("使用者選擇了是")
        # 執行某個動作
    else:
        print("使用者選擇了否")
        # 執行其他動作

root = tk.Tk()
tk.Button(root, text="按我詢問", command=ask_user).pack()
root.mainloop()
