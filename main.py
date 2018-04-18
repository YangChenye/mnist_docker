import app as mycassandra
import tensorflow as tf
import numpy as np
from PIL import Image
from mnist import input_data

'''
python 3.6
tensorflow 1.4
pillow(PIL) 4.3.0
使用tensorflow的模型来预测手写数字
输入是28 * 28像素的图片，输出是个具体的数字
'''


'''模型存储路径'''
CKPT_DIR = 'mnist/ckpt'
DATA_DIR = 'mnist/mnist_data'


'''网络'''
class NetworkMnist:
    def __init__(self):
        self.learning_rate = 0.001                                          # 学习速率，一般在 0.00001 - 0.5 之间

        self.global_step = tf.Variable(0, trainable=False)                  # 记录已经训练的次数

        self.x = tf.placeholder(tf.float32, [None, 784])                    # 输入张量 28 * 28 = 784个像素的图片一维向量
        self.label = tf.placeholder(tf.float32, [None, 10])                 # 标签值，即图像对应的结果，如果对应数字是8，则对应label是 [0,0,0,0,0,0,0,0,1,0]
                                                                            # 这种方式称为 one-hot编码
                                                                            # 标签是一个长度为10的一维向量，值最大的下标即图片上写的数字

        self.w = tf.Variable(tf.zeros([784, 10]))                           # 权重，初始化全 0
        self.b = tf.Variable(tf.zeros([10]))                                # 偏置 bias， 初始化全 0
        self.y = tf.nn.softmax(tf.matmul(self.x, self.w) + self.b)          # 输出 y = softmax(X * w + b)

        self.loss = -tf.reduce_sum(self.label * tf.log(self.y + 1e-10))     # 损失，即交叉熵，最常用的计算标签(label)与输出(y)之间差别的方法

        # 反向传播，采用梯度下降的方法。调整w与b，使得损失(loss)最小
        # loss越小，那么计算出来的y值与标签(label)值越接近，准确率越高
        # minimize 可传入参数 global_step， 每次训练 global_step的值会增加1
        # 因此，可以通过计算self.global_step这个张量的值，知道当前训练了多少步
        self.train = tf.train.GradientDescentOptimizer(self.learning_rate).minimize(
            self.loss, global_step=self.global_step)

        # 以下代码验证正确率时使用
        # argmax 返回最大值的下标，最大值的下标即答案
        # 例如 [0,0,0,0.9,0,0.1,0,0,0,0] 代表数字3
        predict = tf.equal(tf.argmax(self.label, 1), tf.argmax(self.y, 1))

        # predict -> [true, true, true, false, false, true]
        # reduce_mean即求predict的平均数 即 正确个数 / 总数，即正确率
        self.accuracy = tf.reduce_mean(tf.cast(predict, "float"))



'''训练'''
class TrainMnist:
    def __init__(self, CKPT_DIR):
        self.CKPT_DIR = CKPT_DIR
        self.net = NetworkMnist()
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
        self.data = input_data.read_data_sets(DATA_DIR, one_hot=True)

    def train(self):
        batch_size = 64                             # batch_size 是指每次迭代训练，传入训练的图片张数。
                                                    # 数据集小，可以使用全数据集，数据大的情况下，
                                                    # 为了提高训练速度，用随机抽取的n张图片来训练，效果与全数据集相近
        train_step = 10000                          # 总的训练次数

        step = 0                                    # 记录训练次数, 初始化为0

        save_interval = 1000                        # 每隔1000步保存模型

        saver = tf.train.Saver(max_to_keep=10)      # tf.train.Saver是用来保存训练结果的。
                                                    # max_to_keep 用来设置最多保存多少个模型，默认是5
                                                    # 如果保存的模型超过这个值，最旧的模型将被删除

        # 开始训练前，检查ckpt文件夹，看是否有checkpoint文件存在。
        # 如果存在，则读取checkpoint文件指向的模型，restore到sess中。
        ckpt = tf.train.get_checkpoint_state(self.CKPT_DIR)  # check point
                                                        # Returns a CheckpointState if the state was available, None otherwise.
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(self.sess, ckpt.model_checkpoint_path)    # 加载已经训练好的模型
            step = self.sess.run(self.net.global_step)              # 读取网络中的global_step的值，即当前已经训练的次数
            print('Continue from')                                  # 从已经训练好的模型继续训练
            print('        -> Minibatch update : ', step)

        while step < train_step:
            x, label = self.data.train.next_batch(batch_size)                           # 从数据集中获取 输入 和 标签
            _, loss = self.sess.run([self.net.train, self.net.loss],                    # 每次计算train，更新整个网络
                                    feed_dict={self.net.x: x, self.net.label: label})   # loss只是为了看到损失的大小，方便打印
            step = self.sess.run(self.net.global_step)

            # 打印 loss，训练过程中将会看到，loss有变小的趋势
            # 代表随着训练的进行，网络识别图像的能力提高
            # 但是由于网络规模较小，后期没有明显下降，而是有明显波动
            if step % 1000 == 0:
                print('第%5d步，当前loss：%.2f' % (step, loss))

            # 模型保存在ckpt文件夹下
            # 模型文件名最后会增加global_step的值，比如1000的模型文件名为 model-1000
            if step % save_interval == 0:
                saver.save(self.sess, CKPT_DIR + '/model', global_step=step)

    def calculate_accuracy(self):
        test_x = self.data.test.images
        test_label = self.data.test.labels
        # 注意：与训练不同的是，并没有计算 self.net.train
        # 只计算了accuracy这个张量，所以不会更新网络
        # 最终准确率约为0.91
        accuracy = self.sess.run(self.net.accuracy,
                                 feed_dict={self.net.x: test_x, self.net.label: test_label})
        print("准确率: %.2f，共测试了%d张图片 " % (accuracy, len(test_label)))



'''预测'''
class PredictMnist:
    def __init__(self, CKPT):
        self.CKPT_DIR = CKPT
        self.net = NetworkMnist()
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

        # 加载模型到sess中
        self.restore()

    def restore(self):
        saver = tf.train.Saver()                                    # tf.train.Saver是用来保存训练结果的。
        ckpt = tf.train.get_checkpoint_state(self.CKPT_DIR)              # check point
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(self.sess, ckpt.model_checkpoint_path)    # 加载已经训练好的模型
        else:
            raise FileNotFoundError("未保存任何模型")

    def predict(self, image_path):
        img = Image.open(image_path).convert('L')                   # 读图片并转为黑白的
        flatten_img = np.reshape(img, 784)                          # 将28X28矩阵改成一个784维向量
        x = np.array([1 - flatten_img])
        y = self.sess.run(self.net.y, feed_dict={self.net.x: x})    # 测试结果

        # 因为x只传入了一张图片，取y[0]即可
        # np.argmax()取得独热编码最大值的下标，即代表的数字
        print(image_path)
        print('        -> Predict digit', np.argmax(y[0]))
        return np.argmax(y[0])




if __name__ == "__main__":

    mycassandra.createKeySpace()
    # trainApp = TrainMnist(CKPT_DIR)
    # trainApp.train()
    # trainApp.calculate_accuracy()

    predictApp = PredictMnist(CKPT_DIR)

    for i in range(10):
        a = predictApp.predict('mnist/test_images/%d.png' % i)
        mycassandra.insertData("2018.4.17_%d" % i, "%d.png" % i, a)