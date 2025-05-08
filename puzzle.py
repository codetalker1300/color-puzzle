import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkinter import *
import random
from PIL import Image, ImageTk,ImageOps
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import os


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
    def __init__(self, root, menu_frame, difficulty, mode):
        self.root = root
        self.menu_frame = menu_frame
        self.puzzle_frame = Frame(root)
        self.puzzle_frame.pack()
        root.title("分割並打亂正方形")
        screenWidth = root.winfo_screenwidth() # 螢幕寬度
        screenHeight =root.winfo_screenheight() # 螢幕高度
        w = 600 # 視窗寬
        h = 600 # 視窗高
        x=(screenWidth-w) / 2 # 視窗左上角x軸位置
        y=(screenHeight-h) / 2 # 視窗左上角Y軸
        root.geometry("%dx%d+%d+%d"%(w,h,x,y))

        #畫面建構需要的變數
        self.difficulty=difficulty
        self.mode=mode
        self.width=512
        self.height = 512
        self.grid_size = 8
        self.square_size= self.width// self.grid_size
        self.key_point=4
        self.after_id=None
        self.filepath=None
        #設定難度
        
        self.create_gameState_panel()
        self.create_canva()
        self.create_operation_panel()
        
        self.reset()
    
    def reset(self):
        self.canvas.delete("all")
        #第一個Frame的變數
        self.running=False
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
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
        self.help=True
        
        #歸零兩個counter
        self.timer.config(text=f"時間 : {0:02}:{0:02}:{0:02}")
        
        #生成漸層圖片
        if not self.filepath:
            self.gradient_image = self.generate_fixed_axis_gradient()
        self.handle_difficulty()
        #在canva上劃出方塊
        self.prepare_blocks()
        #綁定滑鼠
        self.bind_events()
        
    def create_gameState_panel(self):    
        # UI
        self.counter_frame =Frame(self.puzzle_frame)
        self.counter_frame.pack()
        self.back_btn=Button(self.counter_frame,text="back previous page",command=self.back_menu)
        self.back_btn.pack(side=LEFT,padx=10)
        self.load_img=Button(self.counter_frame,text="load user picture",command=self.load_puzzle)
        self.load_img.pack(side=LEFT)
        self.timer=Label(self.counter_frame,text=f"時間 : {0:02}:{0:02}:{0:02}",font=("Helvetica", 20))
        self.timer.pack(side=LEFT,padx=10)
        self.step_count=Label(self.counter_frame,text=f"步數:{0}",font=("Helvetica", 20))
        self.step_count.pack(side=LEFT)
        
    def create_canva(self):
        # UI
        self.canva_frame = Frame(self.puzzle_frame)
        self.canva_frame.pack()
        self.canvas = tk.Canvas(self.canva_frame, width=self.width, height=self.height)
        self.canvas.pack()

    def create_operation_panel(self):
        # UI
        self.button_frame=Frame(self.puzzle_frame)
        self.button_frame.pack()
        self.unmatch_btn=Button(self.button_frame,text="find unmatch block",command=self.find_unmatch)
        self.unmatch_btn.pack(side=LEFT,padx=20)
        self.show_img=Button(self.button_frame,text="show picture",command=self.show_whole_picture)
        self.show_img.pack(side=LEFT)
        self.re_load=Button(self.button_frame,text="reload",command=self.reset)
        self.re_load.pack(side=LEFT,padx=10)
    
    def handle_difficulty(self):
        if self.difficulty=="簡單":
            if self.mode=="挑戰":
                self.play_step=50
            self.grid_size= 6
        elif self.difficulty=="中等":
            if self.mode=="挑戰":
                self.play_step=90
            self.grid_size= 8
        elif self.difficulty=="困難":
            if self.mode=="挑戰":
                self.play_step=110                
            self.grid_size= 9
        self.step_count.config(text=f"步數:{self.play_step}")
        self.square_size= self.width// self.grid_size
            
    def back_menu(self):
        self.root.title("色差遊戲")
        self.root.geometry("420x320")
        self.puzzle_frame.destroy()
        self.menu_frame.pack(pady=40)
    def load_puzzle(self):
        if self.running:
            self.canvas.after_cancel(self.after_id)
            
        self.filepath = filedialog.askopenfilename(title="選擇圖片",filetypes=[("圖片檔案", "*.jpg *.jpeg *.png")])
        if self.filepath:
            user_puzzle=Image.open(self.filepath)
            width, height = user_puzzle.size
            max_dim = max(height, width, 320)
            border_w=max_dim-width
            border_h=max_dim-height
            padding=(border_w//2,border_h//2,border_w-border_w//2,border_h-border_h//2)
            padded_image = ImageOps.expand(user_puzzle, border=padding, fill=(255,255,255))
            self.pil_image = padded_image.resize((512,512))
            self.canvas.delete("all")
            
            self.reset()
            self.filepath = None
        else:
            print("使用者取消選擇")
            if self.running:
                self.update_time()
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
        try:            
            if self.mode=="挑戰":
                self.play_step-=1
            else:
                self.play_step+=1
            self.step_count.config(text=f"步數:{self.play_step}")
        except Exception as e:
            print(f"EXCEPTION: {e}")
        
    def generate_fixed_axis_gradient(self):
        axes = ['R', 'G', 'B']
        fixed_axis = random.choice(axes)
        fixed_value = random.randint(0, 255)
        if fixed_value<=60:
            fixed_value+=50
        print(f"固定軸：{fixed_axis}, 固定值：{fixed_value}")

        img = Image.new("RGB", (self.width, self.height))
        pixels = img.load()

        for y in range(self.height):
            for x in range(self.width):
                if fixed_axis == 'R':
                    color = (fixed_value, int(y * 255 / self.height), int(x * 255 / self.width))
                elif fixed_axis == 'G':
                    color = (int(x * 255 / self.width), fixed_value, int(y * 255 / self.height))
                else:
                    color = (int(y * 255 / self.height), int(x * 255 / self.width), fixed_value)
                pixels[x, y] = color
        self.pil_image = img 
        return ImageTk.PhotoImage(img)

    def get_block_image(self, block_x, block_y):
        left = block_x * self.square_size
        top = block_y * self.square_size
        box = (left, top, left + self.square_size, top + self.square_size)
        cropped = self.pil_image.crop(box)
        return ImageTk.PhotoImage(cropped)

    def prepare_blocks(self):
        edge_coords = []
        for by in range(self.grid_size):
            for bx in range(self.grid_size):
                block = self.get_block_image( bx, by)
                self.blocks.append(block)
                coord = [bx * self.square_size, by * self.square_size]
                self.correct_coords.append(coord)
                if bx == 0 or by == 0 or bx == self.grid_size-1 or by == self.grid_size-1:
                    edge_coords.append(coord)

        shuffled_coords = self.correct_coords[:]
        random.shuffle(shuffled_coords)

        # 固定邊緣方塊
        self.fix_coords = random.sample(edge_coords, self.key_point)
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
            self.draw_cross_on_image_center(x, y, self.square_size, 10)

        # 防止圖片被回收
        self.canvas.images = self.blocks

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_click)
        
    def draw_cross_on_image_center(self, x, y, width,cross_size=10):
        center_x = x + width // 2
        center_y = y + width // 2 

        # 白色外框線（寬度較粗）
        self.canvas.create_line(center_x - cross_size, center_y, center_x + cross_size, center_y, fill='white', width=3)
        self.canvas.create_line(center_x, center_y - cross_size, center_x, center_y + cross_size, fill='white', width=3)

        # 黑色主十字線（置中在白線上）
        self.canvas.create_line(center_x - cross_size, center_y, center_x + cross_size, center_y, fill='black', width=1)
        self.canvas.create_line(center_x, center_y - cross_size, center_x, center_y + cross_size, fill='black', width=1)

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
                            rect = self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size, outline="black", width=2)
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
                                
                                try:
                                    file_path=os.path.dirname(os.path.realpath(__file__))+"\puzzle_history.csv"
                                    with open(file_path, 'a', encoding='utf-8') as file:
                                        file.write(f"{self.difficulty},{self.mode},{self.play_second},{self.play_step}\n")
                                except Exception as e:
                                    print(f"EXCEPTION: {e}")
                                    messagebox.showerror("存檔錯誤", "儲存成績失敗")
                                    
                                ans=messagebox.askyesno("確認", "恭喜破關，是否在玩一次？")
                                if ans:
                                    self.reset()
                                else:
                                    self.back_menu()
                        if self.play_step<=0:
                            messagebox.showerror("You Lose","步數用盡，你輸了")
                            self.back_menu()
                    break
            break
        
    def find_unmatch(self):
        if not self.help:
            return
        for i in self.cubes:
            if not i.is_correct():
                x, y = i.now_coordinate
                rect = self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size, outline="red", width=2)
                self.unmatch_dict[i]=rect
        self.help=False
                
    def show_whole_picture(self):
        plt.imshow(np.array(self.pil_image))       
        plt.axis('off')
        plt.show()
                
    def start(self):
        self.root.mainloop()
        
'''# 主程式
if __name__ == "__main__":
    app = PuzzleApp()
    app.start()'''
