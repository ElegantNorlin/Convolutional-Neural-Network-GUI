from tkinter import *
from time import *
import tkinter.filedialog
import io
import cv2
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf

def fun(a):
    model_save_path = './checkpoint/mnist.ckpt'

    model = tf.keras.Sequential([
        # 输入层，将数据整形为特定格式28 × 28 × 1进行处理
        tf.keras.layers.InputLayer(input_shape=(28, 28)),
        tf.keras.layers.Reshape((28, 28, 1)),

        # 第一卷积层
        # 卷积核大小为3，步距为1，选择SAME填充，激活函数为ReLU，过滤器个数为16
        tf.keras.layers.Conv2D(kernel_size=3, strides=1, filters=16,
                      padding='same', activation='relu', name='layer_conv1'),
        # 池化层，选择2 × 2最大池化
        tf.keras.layers.MaxPooling2D(pool_size=2, strides=2),
        # BN减少梯度消失，加快了收敛过程。起到类似dropout一样的正则化能力，一定程度上防止过拟合。
        tf.keras.layers.BatchNormalization(),

        # 第二卷积层，与第一层相似
        # 过滤器个数为36
        tf.keras.layers.Conv2D(kernel_size=3, strides=1, filters=36,
                      padding='same', activation='relu', name='layer_conv2'),
        tf.keras.layers.MaxPooling2D(pool_size=2, strides=2),
        tf.keras.layers.BatchNormalization(),

        # 将卷积层输出结果（四维）通过Flatten降到一维
        tf.keras.layers.Flatten(),

        # 第一全连接层，使用SELU作为激活函数
        tf.keras.layers.Dense(units=128, activation='selu'),
        tf.keras.layers.BatchNormalization(),

        # 第二全连接层，使用softmax对输出结果进行归一化
        tf.keras.layers.Dense(units=10, activation='softmax')
    ])

    model.load_weights(model_save_path)

    for i in range(30):
        image_path = a
        img = Image.open(image_path)
        img = img.resize((28, 28), Image.ANTIALIAS)
        img_arr = np.array(img.convert('L'))

        for i in range(28):
            for j in range(28):
                if img_arr[i][j] < 200:
                    img_arr[i][j] = 255
                else:
                    img_arr[i][j] = 0

        img_arr = img_arr / 255.0
        x_predict = img_arr[tf.newaxis, ...]
        result = model.predict(x_predict)

        pred = tf.argmax(result, axis=1)

        print('\n')
        print(pred)
        print("--------------------")
        a = np.array(pred)
        b = a
        print(b)
        d = b.tolist()
        print(d)
        c = tf.convert_to_tensor(a, tf.int64)
        return d