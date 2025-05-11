import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkinter import *
import random
from PIL import Image, ImageTk,ImageOps
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import os
import time

"""
資料結構，每個方塊一個物件，屬性為
1.圖片(img)
2.正確的座標(ans_coordinate)
3.目前這個方塊的座標(now_coordinate)
move_to:交換時更改座標
is_correct:目前座標與正確座標吻合
"""
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
        root.geometry("%dx%d+%d+%d"%(w,h,x-320,y-35))

        #畫面建構需要的變數
        #難度選擇
        self.difficulty=difficulty
        #模式選擇
        self.mode=mode
        #canva的長跟寬
        self.width=512
        self.height = 512
        #每一邊有幾個正方形
        self.grid_size = 8
        #每個小正方形的邊長
        self.square_size= self.width// self.grid_size
        #固定的邊緣點數量
        self.key_point=4
        #計時器的ID
        self.after_id=None
        #使用者選擇圖片的路徑
        self.filepath=None
        #設定難度
        
        #創立frame和其中的物件，每有包括事件與畫方塊
        self.create_gameState_panel()
        self.create_canva()
        self.create_operation_panel()
        
        #初始化變數，並畫出方塊
        self.reset()
    
    def reset(self):
        self.canvas.delete("all")
        #第一個Frame的變數
        self.running=False
        #先停止計時器
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
        #歸零秒數和步數
        self.play_second=0
        self.play_step=0
        self.play_real_step=0
        #第二個frame的變數
        self.blocks = []#裝分割後的圖片
        self.cubes = []#裝cube(資料結構)
        self.selected = []#紀錄被選取的cube
        self.outlines = {}#畫外框黑線的長方形對應cube(字典)
        self.correct_coords = []#正確的位址陣列，由左到右，由上到下
        self.fix_coords = []#存固定邊緣點的陣列
        #第三個frame的變數
        self.unmatch_dict={}#放所有幕前做標示錯誤的cube的字典
        self.help=True#找出所有不正確的cube的按鈕的flag，只能按一次
        self.keep_try = True#提供增加步數小遊戲，只能玩一次
        
        #歸零兩個counter
        self.timer.config(text=f"時間 : {0:02}:{0:02}:{0:02}")
        
        #生成漸層圖片
        if not self.filepath:
            self.generate_fixed_axis_gradient()
        self.handle_difficulty()
        #在canva上劃出方塊
        self.prepare_blocks()
        #綁定滑鼠
        self.bind_events()
        
    def create_gameState_panel(self):    
        # UI
        self.counter_frame =Frame(self.puzzle_frame)
        self.counter_frame.pack()
        self.back_btn=Button(self.counter_frame,text="back main page",command=self.back_menu)
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
                self.max_strp_level=5
            self.grid_size= 6
        elif self.difficulty=="中等":
            if self.mode=="挑戰":
                self.play_step=90
                self.max_strp_level=6
            self.grid_size= 8
        elif self.difficulty=="困難":
            if self.mode=="挑戰":
                self.play_step=110
                self.max_strp_level=8                
            self.grid_size= 9
        self.step_count.config(text=f"步數:{self.play_step}")
        self.square_size= self.width// self.grid_size
            
    def back_menu(self):
        self.root.title("色彩遊戲選單")
        self.root.geometry("420x320")
        self.puzzle_frame.destroy()
        self.menu_frame.pack(pady=40)
        
    def load_puzzle(self):
        #若計時器再跑，就停掉他
        if self.running:
            self.canvas.after_cancel(self.after_id)
            
        self.filepath = filedialog.askopenfilename(title="選擇圖片",filetypes=[("圖片檔案", "*.jpg *.jpeg *.png")])
        """
        讀圖片的長、寬
        先把它填成至少320*320的正方形
        再放到512*512
        最後再reset
        """
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
        self.timer.config(text=f"時間 : {formatted_time}")
        self.after_id=self.canvas.after(1000,self.update_time)  # 每1000毫秒呼叫自己
    
    def update_step(self):
        try:            
            if self.mode=="挑戰":
                self.play_step-=1
                self.play_real_step+=1
            else:
                self.play_step+=1
            self.step_count.config(text=f"步數:{self.play_step}")
        except Exception as e:
            print(f"EXCEPTION: {e}")
    
    #產生漸層的圖片
    def generate_fixed_axis_gradient(self):
        axes = ['R', 'G', 'B']
        fixed_axis = random.choice(axes)
        fixed_value = random.randint(50, 230)
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
    #將漸層的圖片根據座標(ex:(0,0),(0,1)...)分割出一個小方塊
    def get_block_image(self, block_x, block_y):
        left = block_x * self.square_size
        top = block_y * self.square_size
        box = (left, top, left + self.square_size, top + self.square_size)
        cropped = self.pil_image.crop(box)
        return ImageTk.PhotoImage(cropped)
    #開始畫方塊
    def prepare_blocks(self):
        edge_coords = []
        #根據由左至右，由上到下的順序，把指定座標的圖片分割並加入陣列，並記錄正確的座標順序，和邊緣點的座標
        for by in range(self.grid_size):
            for bx in range(self.grid_size):
                block = self.get_block_image(bx, by)
                self.blocks.append(block)
                coord = [bx * self.square_size, by * self.square_size]
                self.correct_coords.append(coord)
                if bx == 0 or by == 0 or bx == self.grid_size-1 or by == self.grid_size-1:
                    edge_coords.append(coord)
        #將正確的座標陣列打亂，產生新的座標陣列
        shuffled_coords = self.correct_coords[:]
        random.shuffle(shuffled_coords)

        # 固定邊緣方塊，把亂數座標陣列中北指定的邊緣座標換到正確的位置
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
    #畫十字  
    def draw_cross_on_image_center(self, x, y, width,cross_size=10):
        center_x = x + width // 2
        center_y = y + width // 2 

        # 白色外框線（寬度較粗）
        self.canvas.create_line(center_x - cross_size, center_y, center_x + cross_size, center_y, fill='white', width=3)
        self.canvas.create_line(center_x, center_y - cross_size, center_x, center_y + cross_size, fill='white', width=3)

        # 黑色主十字線（置中在白線上）
        self.canvas.create_line(center_x - cross_size, center_y, center_x + cross_size, center_y, fill='black', width=1)
        self.canvas.create_line(center_x, center_y - cross_size, center_x, center_y + cross_size, fill='black', width=1)
    #按下去會要觸發的
    def on_click(self, event):
        #找出所有跟游標重疊的物件
        overlapping = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        #對每個重疊的物件都尋訪一遍cube陣列(只選有重疊的cube)
        for item_id in overlapping:
            for cube in self.cubes:
                if cube.block == item_id:#若是其中有cube
                    if cube in self.selected:#如果已經被選取了
                        self.canvas.delete(self.outlines[cube])#先把outline的黑線刪掉(canva上的黑線刪除而已)
                        self.selected.remove(cube)#再把那個方塊從選取陣列中山調
                        del self.outlines[cube]#從資料上刪除這個outline的資訊
                    else:
                        if cube.now_coordinate in self.fix_coords:#固定點無法選取
                            break
                        if len(self.selected) < 2:#若被選取的方塊小於兩個
                            x, y = cube.now_coordinate#讀目前的位置，畫黑框
                            rect = self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size, outline="black", width=3)
                            self.outlines[cube] = rect #創建字典 cube->長方形
                            self.selected.append(cube) #加入選取陣列

                        if len(self.selected) == 2: #選到兩個
                            c1, c2 = self.selected#讀座標，互換位置，如果是一開始那就打開計時器並更新步數
                            coord1, coord2 = c1.now_coordinate, c2.now_coordinate
                            c1.move_to(self.canvas, coord2)
                            c2.move_to(self.canvas, coord1)
                            if not self.running:
                                self.after_id=self.canvas.after(1000,self.update_time)
                                self.running=True
                            self.update_step()
                            #刪掉黑線(畫面上)
                            self.canvas.delete(self.outlines[c1])
                            self.canvas.delete(self.outlines[c2])
                            #清空陣列
                            self.outlines.clear()
                            self.selected.clear()
                            #如果這兩個被選取的方塊有被畫紅線(找出位置錯誤的方塊)，就把紅線刪掉
                            if c1 in self.unmatch_dict and self.unmatch_dict[c1]:
                                self.canvas.delete(self.unmatch_dict[c1])
                                del self.unmatch_dict[c1]
                            if c2 in self.unmatch_dict and self.unmatch_dict[c2]:
                                self.canvas.delete(self.unmatch_dict[c2])
                                del self.unmatch_dict[c2]
                            if all(c.is_correct() for c in self.cubes):#如果全部座標一樣，先暫停計時器
                                if self.running:
                                    self.canvas.after_cancel(self.after_id)
                                    self.after_id = None
                                    self.running = False
                                #存檔
                                try:
                                    file_path=os.path.dirname(os.path.realpath(__file__))+"/puzzle_history.csv"
                                    with open(file_path, 'a', encoding='utf-8') as file:
                                        if self.mode == "無盡":
                                            self.play_real_step = self.play_step
                                        file.write(f"{self.difficulty},{self.mode},{self.play_second},{self.play_real_step}\n")
                                except Exception as e:
                                    print(f"EXCEPTION: {e}")
                                    messagebox.showerror("存檔錯誤", "儲存成績失敗")
                                #跳出破關訊息  
                                ans=messagebox.askyesno("確認", "恭喜破關，是否在玩一次？")
                                #看使用者要再玩一次還是回上一頁
                                if ans:
                                    self.reset()
                                else:
                                    self.back_menu()
                        #挑戰模式下看步數是否歸零
                        if self.play_step<=0 and self.mode=="挑戰":
                            self.canvas.after_cancel(self.after_id)
                            if self.keep_try:
                                continueTry=messagebox.askyesno("再試一下", "是否玩小遊戲以增加步數？\n(僅一次)")
                                #看使用者要不要增加步數
                                if continueTry:
                                    self.keep_try = False
                                    Stroop(self.max_strp_level, self.strp_back)
                                    return
                            messagebox.showerror("You Lose","步數用盡，你輸了")
                            self.back_menu()
                    break
    #找出所有位置錯誤的方塊並圈起來，但只能按一次，之後flag會反向
    def find_unmatch(self):
        if not self.help:
            return
        for i in self.cubes:
            if not i.is_correct():
                x, y = i.now_coordinate
                rect = self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size, outline="red", width=2)
                self.unmatch_dict[i]=rect
        self.help=False

    #從小遊戲回來
    def strp_back(self, add_step):
        self.play_step += add_step
        self.step_count.config(text=f"步數:{self.play_step}")
        self.after_id=self.canvas.after(1000,self.update_time)

    #顯示整張圖片     
    def show_whole_picture(self):
        plt.figure(figsize=(5.12, 5.12), dpi=100)
        plt.imshow(np.array(self.pil_image))
        plt.axis('off')
        plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02) 
        manager = plt.get_current_fig_manager()
        try:
            # 如果是 TkAgg 後端 (常見)
            manager.window.wm_geometry("+620+60")  # 設定視窗左上角位置為 (100, 100)
        except AttributeError:
            print("error")
            pass  # 其他後端不支援就略過 
        plt.show()
        
    def start(self):
        self.root.mainloop()

#增加步數小遊戲 -- 綠紅黃紫藍橘        
class Stroop:
    def __init__(self, max_level, back_to_puzzle):
        self.stroop_window = tk.Toplevel()
        self.max_level = max_level
        self.back_to_puzzle = back_to_puzzle
        self.stroop_window.grab_set() #阻止使用者與其他視窗互動
        self.stroop_window.title("增加步數--Stroop Game")
        self.add_step = 0
        self.strp_level = 0
        self.colors = [("紅色", "red"),("橘色", "orange"),("黃色", "gold"),
                       ("綠色","green"),("藍色", "blue"),("紫色", "purple")]

        tk.Label(self.stroop_window, text=f"選擇顯示的顏色，共{self.max_level}關，答對一題加2步", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.strp_level_label = tk.Label(self.stroop_window, text="", font=("Arial", 16))
        self.strp_level_label.grid(row=1, column=0, padx=5, pady=5)
        self.add_label = tk.Label(self.stroop_window, text="", font=("Arial", 16))
        self.add_label.grid(row=1, column=1, padx=5, pady=5)
        
        self.strp_canvas_size = 300
        self.strp_canvas = tk.Canvas(self.stroop_window, width=self.strp_canvas_size, height=self.strp_canvas_size/2, bg="white")
        self.strp_canvas.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        btn_frm = tk.Frame(self.stroop_window)
        btn_frm.grid(row=3, column=0, columnspan=2)
        btn1 = tk.Button(btn_frm, font=("Arial", 30), command=lambda: self.check_strp(0))
        btn1.grid(row=0, column=0, padx=5, pady=5)
        btn2 = tk.Button(btn_frm,font=("Arial", 30), command=lambda: self.check_strp(1))
        btn2.grid(row=0, column=1, padx=5, pady=5)
        btn3 = tk.Button(btn_frm,font=("Arial", 30), command=lambda: self.check_strp(2))
        btn3.grid(row=1, column=0, padx=5, pady=5)
        btn4 = tk.Button(btn_frm,font=("Arial", 30), command=lambda: self.check_strp(3))
        btn4.grid(row=1, column=1, padx=5, pady=5)
        self.btns = [btn1, btn2, btn3, btn4]

        self.stroop_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.next_strp_level()   
    
    def check_strp(self, btn_idx):
        if self.opt_word[btn_idx][0] == self.topic[1][0]: #選項的字等於題目的顏色
            self.add_step += 2
        self.next_strp_level()
    
    def next_strp_level(self):
        self.strp_canvas.delete("all")
        self.strp_level += 1
        self.add_label.config(text=f"目前增加步數：{self.add_step}")
        if self.strp_level >= self.max_level+1: #玩5關了
            for btn in self.btns: #讓按鍵不能能按
                btn.config(state="disabled")
            self.strp_canvas.create_text(self.strp_canvas_size/2, self.strp_canvas_size/4,
                            text=f"增加{self.add_step}步，\n關閉此視窗\n即可繼續遊戲", font=("Arial", 24), fill="red")
            return
        self.strp_level_label.config(text=f"第{self.strp_level}關")
        self.topic = random.sample(self.colors,2) #題目的字跟顏色
        self.strp_canvas.create_text(self.strp_canvas_size/2, self.strp_canvas_size/4,
                                    text=self.topic[0][0], font=("Arial", 60), fill=self.topic[1][1])
        remain_colors = [c for c in self.colors if c not in self.topic]
        self.opt_word = self.topic + random.sample(remain_colors,2) #選項的字，一定有兩個是題目上的
        random.shuffle(self.opt_word) 
        opt_color = [self.topic[0]] + random.choices(self.colors,k=3) #選項的顏色，重複隨機選，含題目顯示的文字作為顏色
        random.shuffle(opt_color)
        for idx, btn in enumerate(self.btns):
            btn.config(text=self.opt_word[idx][0], fg=opt_color[idx][1])
        return
    
    def on_closing(self):
        self.back_to_puzzle(self.add_step)
        self.stroop_window.destroy()

