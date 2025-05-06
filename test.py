import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkinter import *
import random
from PIL import Image, ImageTk,ImageOps
from tkinter import filedialog

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
    def __init__(self):
        self.root = Tk()
        self.root.title("分割並打亂正方形")
        screenWidth = self.root.winfo_screenwidth() # 螢幕寬度
        screenHeight =self.root.winfo_screenheight() # 螢幕高度
        w = 600 # 視窗寬
        h = 600 # 視窗高
        x=(screenWidth-w) / 2 # 視窗左上角x軸位置
        y=(screenHeight-h) / 2 # 視窗左上角Y軸
        self.root.geometry("%dx%d+%d+%d"%(w,h,x,y))

        self.first_frame_init()
        self.second_frame_init()
        self.third_frame_init()

        #第一個Frame的變數
        self.running=False
        self.after_id=None
        self.play_second=0
        self.play_step=0
        #第二個frame的變數
        self.blocks = []
        self.cubes = []
        self.selected = []
        self.outlines = {}
        self.correct_coords = []
        self.fix_coords = []
        #第三個frame的變數
        self.unmatch_dict={}
        
        #生成漸層圖片
        self.gradient_image = self.generate_fixed_axis_gradient()
        #在canva上劃出方塊
        self.prepare_blocks()
        #綁定滑鼠
        self.bind_events()
    def reset(self):
        self.canvas.delete("all")
        #第一個Frame的變數
        self.running=False
        self.after_id=None
        self.play_second=0
        self.play_step=0
        #第二個frame的變數
        self.blocks = []
        self.cubes = []
        self.selected = []
        self.outlines = {}
        self.correct_coords = []
        self.fix_coords = []
        #第三個frame的變數
        self.unmatch_dict={}
        
        #生成漸層圖片
        self.gradient_image = self.generate_fixed_axis_gradient()
        #在canva上劃出方塊
        self.prepare_blocks()
        #綁定滑鼠
        self.bind_events()
        
        #歸零兩個counter
        self.timer.config(text=f"時間 : {0:02}:{0:02}:{0:02}")
        self.step_count.config(text=f"步數:{0}")
        
    def first_frame_init(self):    
        #第一個frame
        self.counter_frame =Frame(self.root)
        self.counter_frame.pack()
        self.load_img=Button(self.counter_frame,text="load user picture",command=self.load_puzzle)
        self.load_img.pack(side=LEFT)
        self.timer=Label(self.counter_frame,text=f"時間 : {0:02}:{0:02}:{0:02}",font=("Helvetica", 24))
        self.timer.pack(side=LEFT,padx=10)
        self.step_count=Label(self.counter_frame,text=f"步數:{0}",font=("Helvetica", 24))
        self.step_count.pack(side=LEFT)
        
    def second_frame_init(self):
        # 第二個Frame + Canvas
        self.canva_frame = Frame(self.root)
        self.canva_frame.pack()
        self.canvas = tk.Canvas(self.canva_frame, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        
    def third_frame_init(self):
        #第三個frame
        self.button_frame=Frame(self.root)
        self.button_frame.pack()
        self.unmatch_btn=Button(self.button_frame,text="find unmatch block",command=self.find_unmatch)
        self.unmatch_btn.pack()
    
    def load_puzzle(self):
        if self.running:
            self.canvas.after_cancel(self.after_id)
        filepath = filedialog.askopenfilename(title="選擇圖片",filetypes=[("圖片檔案", "*.jpg *.jpeg *.png")])
        if filepath:
            user_puzzle=Image.open(filepath)
            width, height = user_puzzle.size
            max_dim = max(height, width, 320)
            border_w=max_dim-width
            border_h=max_dim-height
            padding=(border_w//2,border_h//2,border_w-border_w//2,border_h-border_h//2)
            padded_image = ImageOps.expand(user_puzzle, border=padding, fill=(255,255,255))
            self.pil_image = padded_image.resize((512,512))
            self.canvas.delete("all")
            #第一個Frame的變數
            self.running=False
            self.after_id=None
            self.play_second=0
            self.play_step=0
            #第二個frame的變數
            self.blocks = []
            self.cubes = []
            self.selected = []
            self.outlines = {}
            self.correct_coords = []
            self.fix_coords = []
            #第三個frame的變數
            self.unmatch_dict={}
        
            #在canva上劃出方塊
            self.prepare_blocks()
            #綁定滑鼠
            self.bind_events()
            
            #歸零兩個counter
            self.timer.config(text=f"時間 : {0:02}:{0:02}:{0:02}")
            self.step_count.config(text=f"步數:{0}")
        else:
            print("使用者取消選擇")
            return
    
    def update_time(self):
        self.play_second+=1
        h = self.play_second // 3600
        m = (self.play_second % 3600) // 60
        s = self.play_second % 60
        formatted_time = f"{h:02}:{m:02}:{s:02}"
        self.timer.config(text=f"時間 ： {formatted_time}")
        self.after_id=self.canvas.after(1000,self.update_time)  # 每1000毫秒呼叫自己
    
    def update_step(self):
        self.play_step+=1
        self.step_count.config(text=f"步數:{self.play_step}")
        
    def generate_fixed_axis_gradient(self):
        axes = ['R', 'G', 'B']
        fixed_axis = random.choice(axes)
        fixed_value = random.randint(0, 255)
        if fixed_value<=50:
            fixed_value+=30
        print(f"固定軸：{fixed_axis}, 固定值：{fixed_value}")

        img = Image.new("RGB", (WIDTH, HEIGHT))
        pixels = img.load()

        for y in range(HEIGHT):
            for x in range(WIDTH):
                if fixed_axis == 'R':
                    color = (fixed_value, int(y * 255 / HEIGHT), int(x * 255 / WIDTH))
                elif fixed_axis == 'G':
                    color = (int(x * 255 / WIDTH), fixed_value, int(y * 255 / HEIGHT))
                else:
                    color = (int(y * 255 / HEIGHT), int(x * 255 / WIDTH), fixed_value)
                pixels[x, y] = color
        self.pil_image = img 
        return ImageTk.PhotoImage(img)

    def get_block_image(self, block_x, block_y):
        left = block_x * SQUARE_SIZE
        top = block_y * SQUARE_SIZE
        box = (left, top, left + SQUARE_SIZE, top + SQUARE_SIZE)
        cropped = self.pil_image.crop(box)
        return ImageTk.PhotoImage(cropped)

    def prepare_blocks(self):
        edge_coords = []
        for by in range(GRID_SIZE):
            for bx in range(GRID_SIZE):
                block = self.get_block_image( bx, by)
                self.blocks.append(block)
                coord = [bx * SQUARE_SIZE, by * SQUARE_SIZE]
                self.correct_coords.append(coord)
                if bx == 0 or by == 0 or bx == 7 or by == 7:
                    edge_coords.append(coord)

        shuffled_coords = self.correct_coords[:]
        random.shuffle(shuffled_coords)

        # 固定邊緣方塊
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
                            if not self.running:
                                self.after_id=self.canvas.after(1000,self.update_time)
                                self.running=True
                            self.update_step()
                            
                            self.canvas.delete(self.outlines[c1])
                            self.canvas.delete(self.outlines[c2])
                            self.outlines.clear()
                            self.selected.clear()
                            if c1 in self.unmatch_dict and self.unmatch_dict[c1]:
                                self.canvas.delete(self.unmatch_dict[c1])
                                del self.unmatch_dict[c1]
                            if c2 in self.unmatch_dict and self.unmatch_dict[c2]:
                                self.canvas.delete(self.unmatch_dict[c2])
                                del self.unmatch_dict[c2]
                            if all(c.is_correct() for c in self.cubes):
                                if self.running:
                                    self.canvas.after_cancel(self.after_id)
                                    self.after_id = None
                                    self.running = False
                                ans=messagebox.askyesno("確認", "恭喜破關，是否在玩一次？")
                                if ans:
                                    self.reset()
                                else:
                                    self.canvas.delete("all")
                                    self.timer.config(text=f"時間 : {0:02}:{0:02}:{0:02}")
                                    self.step_count.config(text=f"\t步數:{0}")    
                    break
            break
        
    def find_unmatch(self):
        for i in self.cubes:
            if not i.is_correct():
                x, y = i.now_coordinate
                rect = self.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, outline="red", width=2)
                self.unmatch_dict[i]=rect
                
    def start(self):
        self.root.mainloop()
        

# 主程式
if __name__ == "__main__":
    app = PuzzleApp()
    app.start()
