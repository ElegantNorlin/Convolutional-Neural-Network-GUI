from tensorflow.keras import datasets, layers, optimizers, Sequential,callbacks,losses
import os
import numpy as np

np.set_printoptions(threshold=np.inf)

(x_train, y_train), (x_test, y_test) = datasets.mnist.load_data("mnist.pkl")
x_train, x_test = x_train / 255.0, x_test / 255.0

model = Sequential([
    # 输入层
    layers.InputLayer(input_shape=(28, 28)),
    # 裁剪数据
    layers.Reshape((28, 28, 1)),
    # 第一卷积层
    # 卷积核大小为3，步距为1，选择SAME填充，激活函数为ReLU，过滤器个数为16
    layers.Conv2D(kernel_size=3, strides=1, filters=16,padding='same', activation='relu', name='layer_conv1'),
    # 池化层，选择2 × 2最大池化
    layers.MaxPooling2D(pool_size=2, strides=2),
    # BN减少梯度消失，加快了收敛过程。起到类似dropout一样的正则化能力，一定程度上防止过拟合。
    layers.BatchNormalization(),
    # 第二卷积层，与第一层相似
    # 卷积核个数为36
    layers.Conv2D(kernel_size=3, strides=1, filters=36,padding='same', activation='relu', name='layer_conv2'),
    layers.MaxPooling2D(pool_size=2, strides=2),
    layers.BatchNormalization(),
    # 将卷积层输出结果（四维）通过Flatten降到一维
    layers.Flatten(),
    # 第一全连接层，使用SELU作为激活函数
    layers.Dense(units=128, activation='selu'),
    layers.BatchNormalization(),

    # 第二全连接层，使用softmax对输出结果进行归一化
    layers.Dense(units=10, activation='softmax')
])



# 选择自适应梯度下降（Adam）和交叉熵误差函数
model.compile(optimizer=optimizers.Adam(lr=1e-3),loss=losses.SparseCategoricalCrossentropy(from_logits=False),metrics=['sparse_categorical_accuracy'])

checkpoint_save_path = "./checkpoint/mnist.ckpt"
if os.path.exists(checkpoint_save_path + '.index'):
    print('-------------load the model-----------------')
    model.load_weights(checkpoint_save_path)

cp_callback = callbacks.ModelCheckpoint(filepath=checkpoint_save_path,
                                                 save_weights_only=True,
                                                 save_best_only=True)
# 训练5轮
model.fit(x=x_train, y=y_train,batch_size=32,epochs=5,validation_data=(x_test, y_test), validation_freq=1,callbacks=[cp_callback])

model.summary()
file = open('weights.txt', 'w')
for v in model.trainable_variables:
    file.write(str(v.name) + '\n')
    file.write(str(v.shape) + '\n')
    file.write(str(v.numpy()) + '\n')
file.close()