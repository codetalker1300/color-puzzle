import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("多畫面切換範例")
        self.geometry("400x300")

        # 建立 container，所有 Frame 都放進這裡
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # 初始化所有畫面
        for F in (HomePage, Page1, Page2, Page3):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        """顯示指定的頁面"""
        frame = self.frames[page_name]
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="首頁", font=("Arial", 20)).pack(pady=20)

        tk.Button(self, text="前往子頁面 1",
                  command=lambda: controller.show_frame("Page1")).pack(pady=10)
        tk.Button(self, text="前往子頁面 2",
                  command=lambda: controller.show_frame("Page2")).pack(pady=10)
        tk.Button(self, text="前往子頁面 3",
                  command=lambda: controller.show_frame("Page3")).pack(pady=10)


class PageTemplate(tk.Frame):
    def __init__(self, parent, controller, page_number):
        super().__init__(parent)
        self.controller = controller

        tk.Button(self, text="回首頁",
                  command=lambda: controller.show_frame("HomePage")).place(x=10, y=10)

        tk.Label(self, text=f"這是子頁面 {page_number}", font=("Arial", 16)).pack(expand=True)


class Page1(PageTemplate):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, page_number=1)


class Page2(PageTemplate):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, page_number=2)


class Page3(PageTemplate):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, page_number=3)


if __name__ == "__main__":
    app = App()
    app.mainloop()
