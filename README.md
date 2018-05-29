
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


学习官方的[Get started with Docker文档](https://docs.docker.com/get-started/)对docker有一个初步的了解。<br>

