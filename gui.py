from tkinter import *
from time import *
import tkinter.filedialog
import io
import cv2
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import recognition

a = [""]
root = Tk()
w_box = 700
h_box = 500
root.title('Tensorflow实现手写数字识别---2020数字图像识别与理解11组')
# 获取此电脑的横向分辨率
sw = root.winfo_screenwidth()
# 获取此电脑的纵向分辨率
sh = root.winfo_screenheight()
w1 = (sw - 700) / 2
w2 = (sh - 500) /2
# 使GUI界面居中
root.geometry('700x500+%d+%d'%(w1,w2))
e = StringVar()
print(e)
e_entry = Entry(root, textvariable=e)
e_entry.grid(row=6, column=1, padx=10, pady=5)
print(e_entry.get())
root.resizable(0,0)

submit_button = Button(root, text="选择文件", command=root.quit)
Label3 = Label(root,background="#8C8476", text='识别结果:',width=11,relief="sunken").grid(row=3, column=0)

v2 = StringVar()
v2.set(a[0])
e3 = Entry(root, textvariable=v2)
# e4 = Entry(root, textvariable=p2)
e3.grid(row=3, column=1, padx=10, pady=5)
# e4.grid(row=4, column=1, padx=10, pady=5)
global imgGl
imgGl = Label(root, image=None)
imgGl.place(x=300, y=0)

selectFileName = ""
image_path = ""
def resize(w_box, h_box, pil_image):
    global image_path
    w, h = pil_image.size
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


def choose_file():
    global  selectFileName
    selectFileName = tkinter.filedialog.askopenfilename(title='选择文件')
    print(selectFileName)
    e.set(selectFileName)
    image_path = selectFileName
    a = recogniition.fun(image_path)
    showImg(e_entry.get())
    v2.set(a[0])
    print("识别结果是：%d" % a[0])



def showImg(img1):
    imgGl.config(image='')
    load = Image.open(img1)
    pil_image_resized = resize(w_box, h_box, load)
    render = ImageTk.PhotoImage(pil_image_resized)
    imgGl.image = render
    imgGl.config(image=render)


def showImgAgain(img2):
    img = cv2.imread(img2)
    # x = float(e1.get())
    # y = float(e2.get())
    w = float(e3.get())
    # h = float(e4.get())
    size = img.shape
    sz0 = size[0]
    sz1 = size[1]
    # cv2.rectangle(img, (int(x * sz1), int(y * sz0)), (int((x + w) * sz1), int((y + h) * sz0)), (0, 255, 0), 4)
    cv2.imwrite('completed.jpg', img)
    showImg('completed.jpg')


Button(root, text='退出', width=10,background="#8C8476", command=root.quit) \
    .grid(row=9, column=0, sticky=W, padx=10, pady=5)
Button(root, text="选择文件", width=10, background="#8C8476",command=choose_file) \
    .grid(row=6, column=0, sticky=W, padx=10, pady=5)
# Button(root, bg = "#D6D0D4",text="显示图片", width=10, command=lambda: showImg(e_entry.get())) \
#     .grid(row=7, column=0, sticky=W, padx=10, pady=5)
# Button(root, text="画坐标框", width=10, command=lambda: showImgAgain(e_entry.get())) \
#     .grid(row=8, column=0, sticky=W, padx=10, pady=5)

#更换GUI图标
root.iconbitmap("icon.ico")
root.configure(background = "#3C3F41")
mainloop()

