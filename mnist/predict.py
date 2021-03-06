import tensorflow as tf
import numpy as np
from PIL import Image

from mnist.model import Network

'''
python 3.6
tensorflow 1.4
pillow(PIL) 4.3.0
使用tensorflow的模型来预测手写数字
输入是28 * 28像素的图片，输出是个具体的数字
'''

# CKPT_DIR = 'ckpt'


class Predict:
    def __init__(self, CKPT):
        self.CKPT_DIR = CKPT
        self.net = Network()
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
    app = Predict()
    for i in range(10):
        app.predict('test_images/%d.png' %i)