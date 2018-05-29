
# Mnist in Docker
mnist-train-predict learnt from: 
https://github.com/gzdaijie/tensorflow-tutorial-samples.git

Flask:
http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application

通过Cassandra的Python SDK对数据库进行操作:
https://mannekentech.com/2017/01/02/playing-with-a-cassandra-cluster-via-docker/

## 一.&nbsp;环境配置
### 1.&nbsp;在macOS High Sierra 10.13.4上安装docker
在[Docker官网](https://www.docker.com)下载Docker Community Edition (CE)，可能需要VPN。<br>

### 2.&nbsp;在macOS High Sierra 10.13.4上配置Mnist运行环境
>本段部分参考[MacOS 安装 tensorflow](https://www.cnblogs.com/GrantYu/p/6607514.html)
#### 安装Python 3.6.4：
在[Python官网](https://www.python.org)下载Python 3.6.4，安装在电脑上，Python 3.6.4默认路径是
`/Library/Frameworks/Python.framework/Versions/3.6`

在终端中，可以通过`python3`直接启动Python 3.6.4。
```
MacBook-Pro:~ apple$ python3
Python 3.6.4 (v3.6.4:d48ecebad5, Dec 18 2017, 21:07:28) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
#### 安装pip -- Python包管理工具：
根据[官方说法](https://pip.readthedocs.io/en/stable/installing/)通过Python官网安装的Python 3.6.4已经自带了pip。
> pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from [python.org](https://www.python.org)

在终端中，可以通过`pip3`直接启动pip，macOS中对应Python 3的工具一般末尾都有‘3’这样的标示。
```
MacBook-Pro:~ apple$ pip3

Usage:   
  pip3 <command> [options]
```
#### 安装tensorflow -- 作为Python软件包
在终端中，使用pip直接安装tensorflow：
`pip3 install  tensorflow`

该命令将tensorflow作为Python软件包安装在路径：
`/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/tensorflow`

由于我的MacBook Pro(Early 2015)没有独立GPU，因此没有安装GPU支持的tensorflow，不过可以通过以下命令安装：
`pip3 install  tensorflow-gpu       #GPU support version#`

#### 测试tensorflow
```
MacBook-Pro:~ apple$ python3
Python 3.6.4 (v3.6.4:d48ecebad5, Dec 18 2017, 21:07:28) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import tensorflow as tf
>>> hello = tf.constant('Hello, TensorFlow!')
>>> sess = tf.Session()
>>> print(sess.run(hello))
b'Hello, TensorFlow!'
>>> a = tf.constant(10)
>>> b = tf.constant(32)
>>> print(sess.run(a + b))
42
>>> tf.__version__
'1.5.0'
>>> tf.__path__
['/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/tensorflow']
>>> 
```
可以看到tensorflow的版本号和安装位置。

#### 安装 keras
在终端中，输入`pip3 install keras`，将安装 keras theano scipy等。

## 二.&nbsp;本地调试Mnist
#### mnist_softmax & mnist_deep
tensorflow安装好后，会自带tensorflow的经典例子mnist的部分文件，这些文件中没有可以直接运行的mnist程序，都是一些函数的定义，路径如下：

`/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/tensorflow/examples/tutorials/mnist`

我们需要在这个文件夹中自己创建两个mnist例程`mnist_softmax.py`和`mnist_deep.py`，这两个文件可以分别在tensorflow官方的GitHub中下载，[mnist_softmax.py](https://github.com/tensorflow/tensorflow/blob/r1.4/tensorflow/examples/tutorials/mnist/mnist_softmax.py) / [mnist_deep.py](https://github.com/tensorflow/tensorflow/blob/r1.4/tensorflow/examples/tutorials/mnist/mnist_deep.py)。虽然它们对应的是tensorflow 1.4，不过目前并不影响我们使用。

创建完成后可以尝试运行，在终端中：
```
MacBook-Pro:~ apple$ cd /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/tensorflow/examples/tutorials/mnist
MacBook-Pro:mnist apple$ python3 mnist_softmax.py
Successfully downloaded train-images-idx3-ubyte.gz 9912422 bytes.
Extracting /tmp/tensorflow/mnist/input_data/train-images-idx3-ubyte.gz
Successfully downloaded train-labels-idx1-ubyte.gz 28881 bytes.
Extracting /tmp/tensorflow/mnist/input_data/train-labels-idx1-ubyte.gz
Successfully downloaded t10k-images-idx3-ubyte.gz 1648877 bytes.
Extracting /tmp/tensorflow/mnist/input_data/t10k-images-idx3-ubyte.gz
Successfully downloaded t10k-labels-idx1-ubyte.gz 4542 bytes.
Extracting /tmp/tensorflow/mnist/input_data/t10k-labels-idx1-ubyte.gz
WARNING:tensorflow:From mnist_softmax.py:57: softmax_cross_entropy_with_logits (from tensorflow.python.ops.nn_ops) is deprecated and will be removed in a future version.
Instructions for updating:

Future major versions of TensorFlow will allow gradients to flow
into the labels input on backprop by default.

See tf.nn.softmax_cross_entropy_with_logits_v2.

2018-05-29 11:53:52.564786: I tensorflow/core/platform/cpu_feature_guard.cc:137] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.2 AVX AVX2 FMA
0.9181
```
最终可以输出识别的正确率，说明mnist在本地测试成功。

mnist_deep.py同理，通过`python3 mnist_deep.py`运行并查看输出。

#### 本地调试中的一些问题
当在运行softmax和deep时，如果遇到如下问题：
```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)
During handling of the above exception, another exception occurred:
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)>
```
说明是mnist数据集不能下载，不能连接到下载网址。

阅读目录：

`/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/tensorflow/examples/tutorials/mnist`

中的`imput_data.py`文件可以发现，当程序在本地找不到mnist数据集时，会在网上下载（如果没有提前下载数据集，第一次使用都会发生“在网上下载”这个事件）。

这些都没有问题，出问题的地方是在下载的网址。顺着`imput_data.py`文件中的引用，可以找到下载数据集调用的函数文件的存放地址：

`/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/tensorflow/contrib/learn/python/learn/datasets`

在该文件夹中的`mnist.py`中，发现下载链接是Google的服务https://storage.googleapis.com/cvdf-datasets/mnist/ ，该网址在国内如果不通过VPN是访问不了的，不过该文档还提供了另一种官方的链接http://yann.lecun.com/exdb/mnist/ 可以正常访问，只需要将Google的链接注释掉，换成yann的链接，即可解决上述遇到的问题，正常下载数据集、运行程序。

问题解决。

## 三.&nbsp;学习Docker
学习官方的[Get started with Docker文档](https://docs.docker.com/get-started/)对docker有一个初步的了解。<br>

