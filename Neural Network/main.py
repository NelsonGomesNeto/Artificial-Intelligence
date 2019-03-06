import time
import numpy
from NeuralNetwork import NeuralNetwork
from ImageGenerator import ImageGenerator
from ActivationFunctions.Sigmoid import Sigmoid
from random import shuffle
folder = "D:/ProgrammingBigFiles/Generated Numbers/"
size = 10000
episodes = 20
GENERATE = True
TRAIN = True
myDigits = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9}
# myDigits = {5: 0, 6: 1, 7: 2}
# myDigits = {6: 0, 7: 1}

imageGenerator = ImageGenerator("Arial")
startTime = time.time()
if (GENERATE): imageGenerator.generateImages(size)
print("Generated Numbers: %.5lfs" % (time.time() - startTime))

database = []
for i in range(size):
    f = open(folder + "%d.ans" % i, "r")
    answer = numpy.mat(numpy.zeros((len(myDigits), 1)))
    answer[myDigits[int(f.readline())]] = 1
    database += [[imageGenerator.imageToMatrix(i) / 255, answer]]
    f.close()
shuffle(database)
train, test = database[:int(len(database)*0.75)], database[int(len(database)*0.75):]

neuralNetwork = NeuralNetwork([28*28, 28, len(myDigits)], Sigmoid())
# neuralNetwork.load()
print("Neural Network layers:", neuralNetwork)
if (TRAIN):
    startTime, currentTime = time.time(), time.time()
    for i in range(episodes):
        s = time.time()
        ans = neuralNetwork.train(train, 10) # Try 10
        print("episode: %4d | precision: %.5lf | executionTime: %.5lf | totalTime: %.5lf" % (i, ans / len(train), time.time() - s, time.time() - currentTime))
    print("Trained Neural Network %.5lf precision: %.5lfs" % (neuralNetwork.predict(test), time.time() - startTime))
    neuralNetwork.save()
else:
    print("Precision: %.5lf" % (neuralNetwork.predict(test, True)))