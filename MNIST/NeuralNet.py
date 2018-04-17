import FileReader
import numpy as np
from random import random
from math import exp
np.seterr(all="ignore")
DEBUG = 0
gamma = 10

def printImage(image, index):
    for i in range(784):
        if (i and i % 28 == 0): print()
        print((image[index][i] > 0) + 0, end='')

sigmoid = np.vectorize(lambda x: 1.0 / (1.0 + np.exp(-x)))

def getData():
    fr = FileReader.FileReader()
    image = fr.getImages("train-images-idx3-ubyte/data")
    label = fr.getLabels("train-labels-idx1-ubyte/data")
    for i in range(0):
        printImage(image, i)
        print(" ", label[i])
    return(image, label)

def testAll(image, label, weight, biases):
    for i, j in zip(image, label):
        answer = feedForward(i, weight, biases)
        print(j, *answer)

def getAnswer(output):
    best = [0, 0]
    for i in range(len(output)):
        if (best[0] < output[i]):
            best = [output[i], i]
    return(best)

def getError(answer, output):
    c = 0
    for i in range(len(output)):
        c += ((answer == i) - output[i])**2
    return(c)

def getDerivative(output, answer):
    for i in range(len(output)):
        output[i] -= answer == i
    return(np.array(output)*(-1))

def feedForward(aInput, weight, biases):
    activation = []
    for w, b in zip(weight, biases):
        #print(aInput, w)
        activation += [aInput]
        aInput = sigmoid(np.dot(w, aInput) + b)
    return(aInput, activation)

def backPropagation(activation, output, delta, weight, biases):
    nabla = [np.dot(np.array([delta]).transpose(), np.array([activation[2]]))]
    for i in range(1, -1, -1):
        #print("before:", weight[i])
        delta = np.dot(np.array(weight[i+1]).transpose(), np.array(delta))
        #print(activation[i], delta)
        nabla += [np.dot(np.array([delta]).transpose(), np.array([activation[i]]))]
        #print("nabla:", nabla)
        #print("after:", weight[i])
    return(reversed(nabla))

def train(image, label, weight, biases, progress):
    i, perfect = 0, 0
    while (i < len(image)):
        j, nabla = 0, 0
        while (j < 10 and j + i < len(image)):
            output, activation = feedForward(image[i + j], weight, biases)
            if (label[i + j] == getAnswer(output)[1]): perfect += 1
            if (progress): print(i + j, perfect, "label: %d, prediction: %d" % (label[i + j], getAnswer(output)[1]))
            error, delta = getError(label[i + j], output), getDerivative(output, label[i + j])
            newNabla = backPropagation(activation, output, delta, weight, biases)
            if (j == 0): nabla = newNabla
            else: nabla = [n + nn for n, nn in zip(nabla, newNabla)]
            j += 1
        i += j
        #print("before:", weight)
        #print("nabla:", *nabla)
        weight = [w - 100*nw/10 for w, nw in zip(weight, nabla)]
        #print("after:", weight)

netSize = [784, 16, 16, 10]
weight, biases = [], []
for i in range(len(netSize) - 1):
    weight += [[np.array([100*(0.5-random())] * netSize[i]) for j in range(netSize[i + 1])]]
    biases += [[0 for j in range(netSize[i + 1])]] #0.5-random()

if (DEBUG):
    for w, b in zip([weight], [biases]):
        print(len(w), "------")
        for j, k in zip(w, b):
            print("weight:", "col", len(j[0]), "| line", len(j))
            print("biases  :", "col", 1, "| line", len(k))

image, label = getData()
print("Loaded data")
print("Training")
train(image, label, weight, biases, 1)
print("Testing")
train(image, label, weight, biases, 1)
print(weight[len(netSize) - 2], len(weight[len(netSize) - 2]))

