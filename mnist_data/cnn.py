# -*- coding: UTF-8 -*-
import os

import imutils
import numpy as np
import tensorflow as tf
from skimage import measure

is_train = False

# 训练阶段

# 下载并载入 MNIST 手写数字库（55000 * 28 * 28）55000 张训练图像
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('mnist_data', one_hot=True)  # 读取数据集

# one_hot 独热码的编码（encoding）形式
# 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 的十位数字
# 0 : 1000000000
# 1 : 0100000000
# 2 : 0010000000
# 3 : 0001000000
# 4 : 0000100000
# 5 : 0000010000
# 6 : 0000001000
# 7 : 0000000100
# 8 : 0000000010
# 9 : 0000000001

# None 表示张量（Tensor）的第一个维度可以是任何长度
input_x = tf.placeholder(tf.float32, [None, 28 * 28]) / 255.  # 输入为 0-255内规定的范围
output_y = tf.placeholder(tf.int32, [None, 10])  # 输出：10个数字的标签
input_x_images = tf.reshape(input_x, [-1, 28, 28, 1])  # 改变输入的形状  本来是一个784的样式

# 从 Test（测试）数据集里选取 3000 个手写数字的图片和对应标签
test_x = mnist.test.images[:3000]  # 图片
test_y = mnist.test.labels[:3000]  # 标签

# 构建我们的卷积神经网络：
# 第 1 层卷积 conv2d2维卷积 输入是一个 2维的 28*28这样的样式
conv1 = tf.layers.conv2d(
    inputs=input_x_images,  # 形状 [28, 28, 1]
    filters=32,  # 32 个过滤器，输出的深度（depth）是32，一个过滤器会产生1层，将输出32层
    kernel_size=[5, 5],  # 过滤器在二维的大小是(5 * 5)
    strides=1,  # 步长是1
    padding='same',  # same 表示输出的大小不变，因此需要在外围补零 2 圈， 输出还是28*28 如果不补零 valid
    activation=tf.nn.relu  # 激活函数是 Relu
)  # 输出的形状 [28, 28, 32]

# 第 1 层池化（亚采样层）采用最大化的采样 后输出的数据会是其原来的一部分
pool1 = tf.layers.max_pooling2d(
    inputs=conv1,  # 形状 [28, 28, 32]
    pool_size=[2, 2],  # 过滤器在二维的大小是（2 * 2）
    strides=2  # 步长是 2
)  # 形状 [14, 14, 32]

# 第 2 层卷积
conv2 = tf.layers.conv2d(
    inputs=pool1,  # 形状 [14, 14, 32]
    filters=64,  # 64 个过滤器，输出的深度（depth）是64
    kernel_size=[5, 5],  # 过滤器在二维的大小是(5 * 5)
    strides=1,  # 步长是1
    padding='same',  # same 表示输出的大小不变，因此需要在外围补零 2 圈
    activation=tf.nn.relu  # 激活函数是 Relu
)  # 会变成形状 [14, 14, 64]

# 第 2 层池化（亚采样）
pool2 = tf.layers.max_pooling2d(
    inputs=conv2,  # 形状 [14, 14, 64]
    pool_size=[2, 2],  # 过滤器在二维的大小是（2 * 2）
    strides=2  # 步长是 2
)  # 形状 [7, 7, 64]
# http://www.360doc.com/content/18/0715/20/54525756_770633128.shtml
# 平坦化（flat）变成一个 扁平 条形的
flat = tf.reshape(pool2, [-1, 7 * 7 * 64])  # 形状 [7 * 7 * 64, ]  -1 根据之后确定的因素推断

# 1024 个神经元的全连接层 张量inputs
dense = tf.layers.dense(inputs=flat, units=1024, activation=tf.nn.relu)

# Dropout : 丢弃 50%的数据, rate=0.5
dropout = tf.layers.dropout(inputs=dense, rate=0.25)

# 10 个神经元的全连接层，这里不用激活函数来做非线性化了
logits = tf.layers.dense(inputs=dropout, units=10)  # 输出。形状[1, 1, 10]

# 神经网络中用 交叉熵来衡量损失
# 损失函数 计算误差（计算 Cross entropy（交叉熵），再用 Softmax 计算百分比概率）
# loss = tf.losses.softmax_cross_entropy(onehot_labels=output_y, logits=logits)
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=output_y, logits=logits))
# Adam 优化器来最小化误差，学习率 0.001，minimize使之最小化，让误差最小化，让真实值和预测值误差越小越好
train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

# 精度。计算 预测值 和 实际标签 的匹配程度
# 返回(accuracy, update_op), 会创建两个局部变量 下面开启会话也需要进行初始化
# accuracy = tf.metrics.accuracy(
# 	labels=tf.argmax(output_y, axis=1),  # tf.argmax返回最大值的下标
# 	predictions=tf.argmax(logits, axis=1), )[1]
equal_list = tf.equal(tf.argmax(output_y, axis=1), tf.argmax(logits, axis=1))
accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))
# 定义存储路径
ckpt_dir = "./cnn_dir5/"
if not os.path.exists(ckpt_dir):
    os.makedirs(ckpt_dir)
# # 创建会话
sess = tf.Session()
init = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
sess.run(init)
# 定义一个saver
saver = tf.train.Saver(max_to_keep=1)
# 就是 max_to_keep 参数，这个是用来设置保存模型的个数，默认为5，即 max_to_keep=5，保存最近的5个模型。
# 如果你想每训练一代（epoch)就想保存一次模型，则可以将 max_to_keep设置为None或者0
if is_train:
    for i in range(8500):
        batch = mnist.train.next_batch(50)  # 从 Train（训练）数据集里取“下一个” 50 个样本
        train_loss, train_op_ = sess.run([loss, train_op], {input_x: batch[0], output_y: batch[1]})
        if i % 30 == 0:
            test_accuracy = sess.run(accuracy, {input_x: test_x, output_y: test_y})
            print('i', i, train_loss, test_accuracy)
        # 保存模型
        saver.save(sess, ckpt_dir + "/model.ckpt", global_step=4)  # 第三个参数将训练的次数作为后缀加入到模型名字中。

else:
    """-----加载模型，用导入的图片进行测试--------https://www.cnblogs.com/adong7639/p/7764769.html"""
    import cv2

    # 载入图片
    src = cv2.imread('./img/7.png')
    cv2.imshow("your photo", src)

    # if src.shape[0] > 800:
    # 	image = imutils.resize(src, height=800)  # 如果图像太大局部阈值分割速度会稍慢些，因此图像太大时进行降采样
    #
    # img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)  # convert to gray picture
    # m1, n1 = img.shape
    # k = int(m1 / 19) + 1
    # l = int(n1 / 19) + 1
    # img = cv2.GaussianBlur(img, (3, 3), 0)  # 高斯滤波
    # imm = img.copy()
    # # 基于Niblack的局部阈值分割法，对于提取文本类图像分割效果比较好
    # for x in range(k):
    # 	for y in range(l):
    # 		s = imm[19 * x:19 * (x + 1), 19 * y:19 * (y + 1)]
    # 		me = s.mean()  # 均值
    # 		var = np.std(s)  # 方差
    # 		t = me * (1 - 0.2 * ((125 - var) / 125))
    # 		ret, imm[19 * x:19 * (x + 1), 19 * y:19 * (y + 1)] = cv2.threshold(
    # 			imm[19 * x:19 * (x + 1), 19 * y:19 * (y + 1)], t, 255, cv2.THRESH_BINARY_INV)
    # label_image = measure.label(imm)  # 连通区域标记
    # for region in measure.regionprops(label_image):  # 循环得到每一个连通区域属性集
    # 	# 忽略小区域
    # 	if region.area < 100:
    # 		continue
    # 	minr, minc, maxr, maxc = region.bbox  # 得到外包矩形参数
    # 	cv2.rectangle(src, (minc, minr), (maxc, maxr), (0, 255, 0), 2)  # 绘制连通区域
    # 	im2 = imm[minr - 5:maxr + 5, minc - 5:maxc + 5]  # 获得感兴趣区域，也即每个数字的区域
    # 	im = cv2.resize(im2, (28, 28), interpolation=cv2.INTER_CUBIC)
    # 	x_img = np.reshape(im, [-1, 784])
    # 	output = sess.run(logits, feed_dict={input_x: x_img})
    # 	print('您输入的数字是 %d' % (np.argmax(output)))

    # 将图片转化为28*28的灰度图
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.resize(src, (28, 28), interpolation=cv2.INTER_CUBIC)

    # 将灰度图转化为1*784的能够输入的网络的数组
    picture = np.zeros((28, 28))
    for i in range(0, 28):
        for j in range(0, 28):
            picture[i][j] = (255 - dst[i][j])
    print('picture', picture)
    picture = picture.reshape(-1, 784)
    # picture = picture.reshape(-1, 28, 28, 1)
    #
    # # 载入模型
    # # saver = tf.train.import_meta_graph(ckpt_dir+'/model.ckpt-270.meta')
    # # saver.restore(sess,tf.train.latest_checkpoint(ckpt_dir))
    # saver.restore(sess, ckpt_dir + "/model.ckpt-499")
    model_file = tf.train.latest_checkpoint(ckpt_dir)
    print('model_file', model_file)
    saver.restore(sess, model_file)
    #
    # 进行预测
    test_output = sess.run(logits, {input_x: test_x[55:85]})  # test_x[:20]
    inferenced_y = np.argmax(test_output, 1)
    predict_result = sess.run(logits, feed_dict={input_x: picture, })
    inferenced_y1 = np.argmax(predict_result, 1)
    print(inferenced_y, 'Inferenced numbers')  # 推测的数字
    print(np.argmax(test_y[55:85], 1), 'Real numbers')  # 真实的数字
    print("你导入的图片是：", inferenced_y1)

# 关闭回话
sess.close()
