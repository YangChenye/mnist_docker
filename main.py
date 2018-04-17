import mnist_train_predict.model as model
import mnist_train_predict.predict as predictMnist
import mnist_train_predict.train as trainMnist
import app as cassandra

app = trainMnist.Train()
app.train()
app.calculate_accuracy()

app = predictMnist.Predict()
for i in range(10):
    a = app.predict('mnist_train_predict/test_images/%d.png' %i)
    cassandra.insertData('2018.4.17.%d' %i, '%d.png' %i, a)


