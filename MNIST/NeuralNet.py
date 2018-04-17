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
        print(label[i])
    return(image, label)

def feedForward(aInput, weight, bias):
    for w, b in zip(weight, bias):
        aInput = sigmoid(np.dot(w, aInput) + b)
    return(aInput)

netSize = [784, 16, 16, 10]
weight, bias = [], []
for i in range(len(netSize) - 1):
    weight += [[[random() * 10] * netSize[i] for j in range(netSize[i + 1])]]
    bias += [[random() * 10 for j in range(netSize[i + 1])]]

if (DEBUG):
    for w, b in zip([weight], [bias]):
        print(len(w), "------")
        for j, k in zip(w, b):
            print("weight:", "col", len(j[0]), "| line", len(j))
            print("bias  :", "col", 1, "| line", len(k))

image, label = getData()
answer = feedForward(image[0], weight, bias)
print(answer)