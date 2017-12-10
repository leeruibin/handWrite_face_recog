from tkinter import *
import tkinter.filedialog
import tkinter.font as tkFont
from tkinter.messagebox import *
from PIL import Image, ImageTk  # pillow 模块
import os
import json
from aip import AipFace
import camare

config = json.load(open('./config/config.json'))

""" 你的 APPID AK SK """
APP_ID = config['APP']['APP_ID']
API_KEY = config['APP']['API_KEY']
SECRET_KEY = config['APP']['SECRET_KEY']
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

class Demo:
    #一些基础变量
    startX = 0
    startY = 0
    status = 0
    def __init__(self):
        #模式定义 1划词识别 2整体识别 3人脸识别
        self.model = 1
        #背景与窗口设置
        self.root = Tk()
        self.root.title('write hand')
        size = config['window']['size']
        geo = config['window']['geometry']
        self.root.geometry('%sx%s+%s+%s' % (str(size[0]),str(size[1]),str(geo[0]),str(geo[1]) ) )
        self.root.iconbitmap('./picture/bitbug_favicon.ico')
        im = Image.open('./picture/background.jpg')
        im.resize(size,Image.ANTIALIAS)
        background_image = ImageTk.PhotoImage(im)
        background_label = Label(self.root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #菜单栏
        menuBar = Menu(self.root)
        self.root.config(menu=menuBar)
        fileMenu = Menu(menuBar)
        menuBar.add_cascade(label="Info", menu=fileMenu)
        fileMenu.add_command(label="About",command=self.about)
        fileMenu.add_command(label="Exit",command=self.quit)
        modelMenu = Menu(menuBar)
        menuBar.add_cascade(label="Model", menu=modelMenu)
        modelMenu.add_command(label="Word1", command=lambda :self.changModel(1))
        modelMenu.add_command(label="Word2", command=lambda :self.changModel(2))
        modelMenu.add_command(label="Face", command=lambda :self.changModel(3))
        #图片显示地区初始化
        ##480*858  441*759+139     35+134
        self.canvas = Canvas(self.root, width=441, height=898, bg="white")
        self.canvas.grid(row=0,column=0, rowspan=10)
        im = Image.open('./picture/bk1.jpg')

        self.bkImg = ImageTk.PhotoImage(im)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bkImg, tags='background')
        self.canvas.create_oval(config['ovalRange'],fill='red',tags='circle')
        self.canvas.bind('<Button-1>', self.press)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.release)
        self.canvas.bind('<Button-3>', self.clear)

        #按钮初始化
        ft = tkFont.Font(family='Fixdsys', size=40, weight=tkFont.BOLD)
        self.btChoose = Button(self.root, text="选择图片",width=13,relief=GROOVE,font=ft, command=self.choosePic)
        self.btChoose.grid(row=0, column=1)
        #字体显示区初始化
        self.showLabel = Label(self.root,relief=GROOVE,height=3,width=13,font=ft,text = '你好')
        self.showLabel.grid(row=1,column=1)
        #字体图片显示区初始化
        self.wordCav = Canvas(self.root,height=382,bg="white")
        self.wordCav.grid(row=2,column=1,rowspan=8)

        self.root.mainloop()

    #弹出文件选择对话框
    def choosePic(self):
        self.canvas.create_oval(config['ovalRange'], fill='red', tags='circle')
        filename = tkinter.filedialog.askopenfilename()
        self.im = Image.open(filename)
        self.im = self.im.resize(config['showImg']['size'],Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(config['showImg']['geometry'],anchor='nw',image=self.img,tags='img')

    def changModel(self,model):
        if model==1:
            self.model=1
        elif model == 2:
            self.model=2
        else:
            self.model=3
            if self.status==0:
                self.status = 1
                camare.func()
                result = client.identifyUser(
                    'group1',
                    get_file_content('./picture/face.jpg'),
                )
                self.im = Image.open('./picture/face.jpg')
                self.im = self.im.resize(config['showImg']['size'], Image.ANTIALIAS)
                self.img = ImageTk.PhotoImage(self.im)
                self.canvas.create_image(config['showImg']['geometry'], anchor='nw', image=self.img, tags='img')
                try:
                    self.showLabel['text']=result['result'][0]['user_info']
                except:
                    self.showLabel['text']='unkonwn'
                self.status = 0


    #about详情页
    def about(self):
        showinfo('Hello', 'Writer : robbin\n'+'使用说明:\nmodel1:圈图识字模式\nmodel2:单字识字模式\nmodel3:人脸识别课堂点名功能')

    #关闭窗口
    def quit(self):
        self.root.quit()  # 关闭窗口
        self.root.destroy()  # 将所有的窗口小部件进行销毁，应该有内存回收的意思
        exit()

    #按下事件 圆心222*877  半径45
    def press(self,event):
        if self.inCircle(event):
            #按下按钮开始进行图像识别
            self.doRecognition()
        else:
            if self.inRec(event):
                self.startX=event.x
                self.startY=event.y
            self.canvas.create_oval(config['ovalRange'], fill='red', tags='circle')

    #画图事件
    def draw(self,event):
        #不在按钮区在方框区
        if not self.inCircle(event) :
            try:
                self.canvas.delete('rec')
                range=config['rectRange']
                endX = self.fitData(event.x,'x',range=range)
                endY = self.fitData(event.y,'y',range=range)
                self.canvas.create_rectangle(self.startX, self.startY, endX,endY, tags='rec',width='3',outline='green')
            except:
                print("请先进行框图选择")

    #确定图片选区
    def release(self,event):
        if not self.inCircle(event) :
            try:
                range = config['imgRange']
                self.picStartX = self.startX-35
                self.picStartX = self.fitData(self.picStartX,'x',range)

                self.picStartY = self.startY-135
                self.picStartY = self.fitData(self.picStartY, 'y',range)

                #379,676
                self.picEndX = event.x-35
                self.picEndX = self.fitData(self.picEndX, 'x',range)

                self.picEndY = event.y - 135
                self.picEndY = self.fitData(self.picEndY, 'y',range)

                print("选区为:\n( %(x1)d, %(y1)d),\n( %(x2)d, %(y2)d) " %
                      {'x1':self.picStartX,
                       'y1':self.picStartY,
                       'x2':self.picEndX,
                       'y2':self.picEndY
                       })
            except:
                print("没有选区")

    #判断是否在按钮区
    def inCircle(self,event):
        radius = ((event.x - 222) ** 2 + (event.y - 877) ** 2) ** 0.5
        if radius<45:
            return True
        else:
            return False

    #判断是否在方框画图区
    def inRec(self,event):
        if event.x > 35 and event.x < 414 and event.y > 135 and event.y < 811:
            return True
        else:
            return False

    #修正选框数值，若超范围则修正
    def fitData(self,data,type,range):
        if type=='x':
            if data<range[0]:
                return range[0]
            elif data>range[1]:
                return range[1]
            else:
                return data
        else:
            if data<range[2]:
                return range[2]
            elif data>range[3]:
                return range[3]
            else:
                return data

    #清除画图边框
    def clear(self,event):
        self.canvas.delete('rec')

    #获取截图区域，由于截图函数要求从左上角到右下角因而需要调整
    def getBox(self,x1,y1,x2,y2):
        if x1 <= x2 and y1 <= y2:
            return (x1,y1,x2,y2)
        elif x1 <= x2:
            return (x1,y2,x2,y1)
        elif y1 <= y2:
            return (x2,y1,x1,y2)
        else:
            return (x2,y2,x1,y1)

    def doRecognition(self):
        if self.model==1:
            ##裁剪图片
            box = self.getBox(self.picStartX,self.picStartY,self.picEndX,self.picEndY)
            #同比压缩图片
            width=box[2]-box[0]
            height = box[3]-box[1]
            scale = 80 / height
            self.newImg = self.im.crop(box=box)
            self.newImg = self.newImg.resize((int(width*scale),int(height*scale)),Image.ANTIALIAS)
            print(str(int(width*scale))+":"+str(int(height*scale)))
            self.newImg.convert('L').save(r'./picture/crop.jpg')
            # self.newImg.save(r'./crop.jpg')
            #在字体展示区显示图片
            # self.newImg = Image.open('./crop.jpg')
            width = self.wordCav.winfo_width()
            height = self.wordCav.winfo_height()
            self.newImg = self.newImg.resize((width, height), Image.ANTIALIAS)
            self.newImg = ImageTk.PhotoImage(self.newImg)
            self.wordCav.create_image(0,0,anchor='nw',image=self.newImg,tags='newWord')
            #获取字编号
            word = os.popen("python chinese_rec.py --mode=inference")
            text = word.read()
            index = text.split('\n')[1]
            words = json.load(open('./config/char_dict.txt'))
            if index in words.keys():
                self.showLabel['text'] = words[index]
            else:
                self.showLabel['text'] = "error"
            #初始化按钮
            self.canvas.create_oval(config['ovalRange'], fill='green', tags='circle')
        elif self.model==2:#单图识别
            #(379,676)
            scale = 80 / 676
            self.newImg = self.im.resize((int(379*scale),int(676*scale)),Image.ANTIALIAS)
            self.newImg.convert('L').save(r'./picture/crop.jpg')
            word = os.popen("python chinese_rec.py --mode=inference")
            text = word.read()
            index = text.split('\n')[1]
            words = json.load(open('./config/char_dict.txt'))
            if index in words.keys():
                self.showLabel['text'] = words[index]
            else:
                self.showLabel['text'] = "error"
        else:#人脸识别
            pass


Demo()
