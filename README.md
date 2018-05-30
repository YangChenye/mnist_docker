
# Mnist in Docker
mnist-train-predict learnt from: 
https://github.com/gzdaijie/tensorflow-tutorial-samples.git

Flask:
http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application

## 一.&nbsp;环境配置
### 1.&nbsp;在macOS High Sierra 10.13.4上安装docker
在[Docker官网](https://www.docker.com)下载Docker Community Edition (CE)，可能需要VPN。<br>

### 2.&nbsp;在macOS High Sierra 10.13.4上配置Mnist运行环境
>本段一部分参考[MacOS 安装 tensorflow](https://www.cnblogs.com/GrantYu/p/6607514.html)
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
#### 1.&nbsp;一些基础知识
学习官方的[Get started with Docker](https://docs.docker.com/get-started/)对docker有一个初步的了解。

如果需要进一步学习如何写Dockerfile，点这个链接[Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)。

当然，这次的内容涉及docker容器间通信，还需要学习docker的网络结构：[Configure networking](https://docs.docker.com/network/)。

#### 2.&nbsp;遇到的一些问题及解决
##### 1)&nbsp;dockerfile与docker-compose的区别
docker-compose提供了一种很方便的方法来依次启动容器。

>我所理解的docker-compose是编排容器的。例如，你有一个php镜像，一个mysql镜像，一个nginx镜像。如果没有docker-compose，那么每次启动的时候，你需要敲各个容器的启动参数，环境变量，容器命名，指定不同容器的链接参数等等一系列的操作，相当繁琐。而用了docker-composer之后，你就可以把这些命令一次性写在docker-composer.yml文件中，以后每次启动这一整个环境（含3个容器）的时候，你只要敲一个docker-composer up命令就ok了。

dockerfile的作用是从无到有的构建镜像。

>[dockerfile 与 docker-compose的区别是什么?](https://segmentfault.com/q/1010000009883848)

##### 2)&nbsp;dockerfile中能否写docker-compose
在初学的时候，会疑惑，dockerfile中是否不能出现`RUN docker-compose up -d`这样的语句？是因为在形成镜像的时候不能把后续运行的服务放进去？我原来的理解是容器它可以把所有的东西打包进去，就比如说这次的将mnist部署到docker，原来理解的是可以将所有涉及的东西（包括三个Cassandra、mnist程序等）全部放到一个集装箱中。实际是否应该是：不同的东西（Cassandra、mnist）在不同的集装箱中，使用时依次启动这些集装箱？

>你想在Dockerfile里面运行docker-compose，那就需要你的容器里面安装了也安装了Docker容器，事实上我们一般都不这么做。

##### 3)&nbsp;docker端口映射
`docker run -p ip:hostPort:containerPort redis`
使用-p参数会分配宿主机的端口映射到虚拟机。<br>
IP表示主机的IP地址。<br>
hostPort表示宿主机的端口。<br>
containerPort表示虚拟机的端口。

>参考[Docker学习笔记-Docker端口映射](https://blog.csdn.net/qq_29994609/article/details/51730640)

##### 4)&nbsp;docker网络入门
如果你已经构建了一些多容器的应用程序，那么肯定需要定义一些网络规则来设置容器间的通信。有多种方式可以实现：可以通过--expose参数在运行时暴露端口，或者在Dockerfile里使用EXPOSE指令。还可以在Docker run的时候通过-p或者-P参数来发布端口。或者通过--link链接容器。虽然这些方式几乎都能达到一样的结果，但是它们还是有细微区别。那么到底应该使用哪一种呢？

>参考[Docker网络原则入门：EXPOSE，-p，-P，-link](http://dockone.io/article/455)

## 三.&nbsp;学习NoSQL中的Cassandra
能够按照[Cassandra Dockerhub](https://hub.docker.com/_/cassandra/)中的方法，将Cassandra容器和CQLSH启动，并且能够通过命令行建命名空间和表格。

根据[A Practical Introduction To Cassandra Query Language](http://abiasforaction.net/a-practical-introduction-to-cassandra-query-language/)中的内容，熟悉CQL的一些基本命令和操作。

按照[Playing with a Cassandra cluster via Docker](https://mannekentech.com/2017/01/02/playing-with-a-cassandra-cluster-via-docker/)中的方法，能够通过Cassandra的Python SDK对数据库进行操作，包括用Docker Swarm启动Cassandra容器集群。

## 四.&nbsp;将mnist部署到docker
#### 1.&nbsp;tensorflow使用mnist数据集识别新输入的手写数字

#### 2.&nbsp;通过Python SDK把识别结果写入Cassandra数据库
在第三节中，我们已经学习了如何[Playing with a Cassandra cluster via Docker](https://mannekentech.com/2017/01/02/playing-with-a-cassandra-cluster-via-docker/)，相信你已经能按照第三节的方法，在本地通过python编译器对Cassandra数据库进行写入和查看数据了。

## 五.&nbsp;连接mnist container和Cassandra container
















