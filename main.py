import mnist_train_predict.predict as predictMnist
import mnist_train_predict.train as trainMnist
import app as mycassandra

# cassandra.deleteKeyspace()

mycassandra.createKeySpace()

tmpapp = trainMnist.Train()
tmpapp.train()
tmpapp.calculate_accuracy()

tmpapp = predictMnist.Predict()
for i in range(10):
    a = tmpapp.predict('mnist_train_predict/test_images/%d.png' %i)
    mycassandra.insertData('2018.4.17.%d' %i, '%d.png' %i, a)


