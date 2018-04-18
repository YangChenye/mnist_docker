import tensorflow as tf
from mnist import input_data
from mnist.model import Network

'''
python 3.6
tensorflow 1.4

重点对保存模型的部分添加了注释
如果想看其他代码的注释，请移步 v1
v2 版本比 v1 版本增加了模型的保存和继续训练
'''

# CKPT_DIR = 'ckpt'                                   # 模型存储位置


class Train:
    def __init__(self, CKPT_DIR):
        self.CKPT_DIR = CKPT_DIR
        self.net = Network()
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
        self.data = input_data.read_data_sets('mnist_data', one_hot=True)

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


if __name__ == "__main__":
    app = Train()
    app.train()
    app.calculate_accuracy()