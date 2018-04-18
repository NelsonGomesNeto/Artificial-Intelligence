import FileReader
import numpy as np
import time
from random import random, shuffle
from math import exp
np.seterr(all="ignore")
DEBUG = 0
gamma = 10

def printImage(image, index):
    for i in range(784):
        if (i and i % 28 == 0): print()
        print((image[index][i] > 0) + 0, end='')

sigmoid = np.vectorize(lambda x: 1.0 / (1.0 + np.exp(-x)))
sigmoidPrime = np.vectorize(lambda x: sigmoid(x) * (1.0 - sigmoid(x)))

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

def getDerivative(output, answer, error):
    delta = []
    for i in range(len(output)):
        delta += [(output[i] - (answer == i)) * error]
    return(np.array(delta))

def feedForward(aInput, weight, biases):
    rawActivation, activation = [], [aInput]
    for w, b in zip(weight, biases):
        z = np.dot(w, aInput) + b
        rawActivation += [z]
        #print(*aInput)
        aInput = sigmoid(z)
        activation += [aInput]
    return(aInput, rawActivation, activation)

def backPropagation(rawActivation, activation, delta, weight, biases):
    delta *= sigmoidPrime(rawActivation[-1])
    nableBiases = [delta]
    nablaWeight = [np.dot(np.array([delta]).transpose(), np.array([activation[-2]]))]
    for i in range(2, 4):
        #print("before:", weight[i])
        z = rawActivation[-i]
        sp = sigmoidPrime(z)
        delta = np.dot(np.array(weight[-i+1]).transpose(), np.array(delta)) * sp
        #print(activation[i], delta)
        nableBiases += [delta]
        nablaWeight += [np.dot(np.array([delta]).transpose(), np.array([activation[-i-1]]))]
        #print("nablaWeight:", nablaWeight)
        #print("after:", weight[i])
    return(reversed(nablaWeight), reversed(delta))

def train(image, label, weight, biases, progress, batchSize):
    i, perfect = 0, 0
    while (i < len(image)):
        j, nablaWeight = 0, 0
        while (j < batchSize and j + i < len(image)):
            output, rawActivation, activation = feedForward(image[i + j], weight, biases)
            if (label[i + j] == getAnswer(output)[1]): perfect += 1
            error = getError(label[i + j], output)
            delta = getDerivative(output, label[i + j], error)
            newNablaWeight, newNablaBiases = backPropagation(rawActivation, activation, delta, weight, biases)
            if (j == 0): nablaWeight, nablaBiases = newNablaWeight, newNablaBiases
            else: nablaWeight, nablaBiases = [n + nn for n, nn in zip(nablaWeight, newNablaWeight)], [b + bn for b, bn in zip(nablaBiases, newNablaBiases)]
            if (progress and i + j < len(image)): print(i + j, perfect, "label: %d, prediction: %d" % (label[i + j], getAnswer(output)[1]), round(perfect / (i + j + 1), 5), lol(output))
            j += 1
        i += j
        #print("before:", weight)
        #print("nablaWeight:", *nablaWeight)
        weight = [w - nw/batchSize for w, nw in zip(weight, nablaWeight)]
        biases = [b - nb/batchSize for b, nb in zip(biases, nablaBiases)]
        #print("after:", weight)
    return(weight, biases, perfect / (i + j + 1))

def lol(arr):
    for i in range(len(arr)):
        arr[i] = round(arr[i], 3)
    return(arr)

def generateArray(size):
    arr = []
    for i in range(size):
        arr += [2*(0.5-random())]
    return(np.array(arr))

netSize = [784, 16, 16, 10]
weight, biases = [], []
for i in range(len(netSize) - 1):
    weight += [[generateArray(netSize[i]) for j in range(netSize[i + 1])]]
    biases += [[2*(0.5-random()) for j in range(netSize[i + 1])]] #0.5-random()

if (DEBUG):
    for w, b in zip([weight], [biases]):
        print(len(w), "------")
        for j, k in zip(w, b):
            print("weight:", "col", len(j[0]), "| line", len(j))
            print("biases  :", "col", 1, "| line", len(k))

image, label = getData()
print("Loaded data")
print("Training")
startTotal = time.time()
for i in range(20):
    start = time.time()
    qq = list(range(len(image)))
    shuffle(qq)
    newImage, newLabel = [], []
    for j in qq:
        newImage += [image[j]]
        newLabel += [label[j]]
    print(i)
    weight, biases, percentage = train(newImage, newLabel, weight, biases, 0, 100)
    print(percentage, " - ", time.time() - start, " seconds", sep='')

f = open("model", "w")
print(weight, file=f)
print(biases, file=f)
print(percentage, file=f)
print(time.time() - startTotal, "seconds", file=f)
f.close()
