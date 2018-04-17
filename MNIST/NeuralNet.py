import FileReader
import numpy as np
from random import random
from math import exp
DEBUG = 0

def printImage(image, index):
    for i in range(784):
        if (i and i % 28 == 0): print()
        print((image[index][i] > 0) + 0, end='')

sigmoid = np.vectorize(lambda x: 1.0 / (1.0 + np.exp(-x)))

def getData():
    fr = FileReader.FileReader()
    image = fr.getImages("t10k-images-idx3-ubyte/data")
    label = fr.getLabels("t10k-labels-idx1-ubyte/data")
    for i in range(1):
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

def feedForward(aInput, weight, biases):
    for w, b in zip(weight, biases):
        aInput = sigmoid(np.dot(w, aInput) + b)
    return(aInput)

netSize = [784, 16, 16, 10]
weight, biases = [], []
for i in range(len(netSize) - 1):
    weight += [[[random() * 10] * netSize[i] for j in range(netSize[i + 1])]]
    biases += [[random() * 10 for j in range(netSize[i + 1])]]

if (DEBUG):
    for w, b in zip([weight], [biases]):
        print(len(w), "------")
        for j, k in zip(w, b):
            print("weight:", "col", len(j[0]), "| line", len(j))
            print("biases  :", "col", 1, "| line", len(k))

image, label = getData()
output = feedForward(image[0], weight, biases)
print(label[0], getAnswer(output)[1], getError(label[0], output), output)