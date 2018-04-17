import mnist_train_predict.model as model
import mnist_train_predict.predict as predictMnist
import mnist_train_predict.train as trainMnist
import app as cassandra

app = trainMnist.Train()
app.train()
app.calculate_accuracy()

app = predictMnist.Predict()
for i in range(10):
    cassandra.insertData('2018.4.17.%d' %i, './test_images/%d.png' % i, app.predict('./test_images/%d.png' % i))


