import FileManager
import VisualizationManager
import numpy as np
import time
import pickle
from random import random, shuffle
from math import exp
np.set_printoptions(threshold=np.inf)
np.seterr(all="ignore")
DEBUG = 0
fm = FileManager.FileManager()
vm = VisualizationManager.VisualizationManager()

def printImage(image, index):
    for i in range(784):
        if (i and i % 28 == 0): print()
        print((image[index][i] > 0) + 0, end='')

sigmoid = np.vectorize(lambda x: 1.0 / (1.0 + np.exp(-x)))
sigmoidPrime = np.vectorize(lambda x: sigmoid(x) * (1.0 - sigmoid(x)))

def getData():
    image = fm.getImages("train-images-idx3-ubyte/data")
    label = fm.getLabels("train-labels-idx1-ubyte/data")
    return(image, label)

def generateArray(size):
    arr = []
    for i in range(size):
        arr += [2*(0.5-random())]
    return(np.array(arr))

def randomNeuralNetWork(netKind):
    weight, bias = [], []
    for i in range(len(netKind) - 1):
        weight += [[generateArray(netKind[i]) for j in range(netKind[i + 1])]]
        bias += [[2*(0.5-random()) for j in range(netKind[i + 1])]] #0.5-random()
    return(weight, bias)

def testAll(image, label, weight, bias):
    for i, j in zip(image, label):
        answer = feedForward(i, weight, bias)
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
        delta += [(output[i] - (answer[i])) * 1]
    return(np.array(delta))

def feedForward(aInput, weight, bias):
    rawActivation, activation = [], [aInput]
    print("input:", aInput)
    for w, b in zip(weight, bias):
        z = np.dot(w, aInput) + b
        rawActivation += [z]
        print("mid:", w, ".", aInput, "=", z)
        aInput = z
        activation += [aInput]
    print("output:", z)
    return(aInput, rawActivation, activation)

def backPropagation(rawActivation, activation, delta, weight, bias):
    #delta *= sigmoidPrime(rawActivation[-1])
    nablebias = [delta]
    print(np.array([delta]).transpose(), ".", np.array([activation[-2]]), "=", np.dot(np.array([delta]).transpose(), np.array([activation[-2]])))
    nablaWeight = [np.dot(np.array([delta]).transpose(), np.array([activation[-2]]))]
    for i in range(2, len(activation)):
        #print("before:", weight[i])
        z = rawActivation[-i]
        sp = sigmoidPrime(z)
        print()
        print(np.array(weight[-i+1]).transpose(), ".", np.array(delta), "=", np.dot(np.array(weight[-i+1]).transpose(), np.array(delta)))
        delta = np.dot(np.array(weight[-i+1]).transpose(), np.array(delta))
        #print(activation[i], delta)
        nablebias += [delta]
        print(np.array([delta]).transpose(), ".", np.array([activation[-i-1]]), "=", np.dot(np.array([delta]).transpose(), np.array([activation[-i-1]])))
        nablaWeight += [np.dot(np.array([delta]).transpose(), np.array([activation[-i-1]]))]
        #print("nablaWeight:", nablaWeight)
        #print("after:", weight[i])
    return(reversed(nablaWeight), reversed(delta))

def iteration(image, label, weight, bias, viewProgress, batchSize):
    i, perfect = 0, 0
    while (i < len(image)):
        j, nablaWeight = 0, 0
        while (j < batchSize and j + i < len(image)):
            output, rawActivation, activation = feedForward(image[i + j], weight, bias)
            if (label[i + j] == getAnswer(output)[1]): perfect += 1
            error = getError(label[i + j], output)
            delta = getDerivative(output, label[i + j], error)
            newNablaWeight, newNablabias = backPropagation(rawActivation, activation, delta, weight, bias)
            if (j == 0): nablaWeight, nablabias = newNablaWeight, newNablabias
            else: nablaWeight, nablabias = [n + nn for n, nn in zip(nablaWeight, newNablaWeight)], [b + bn for b, bn in zip(nablabias, newNablabias)]
            if (viewProgress and i + j < len(image)): print(i + j, perfect, "label: %d, prediction: %d" % (label[i + j], getAnswer(output)[1]), round(perfect / (i + j + 1), 5), lol(output))
            j += 1
        i += j
        #print("before:", weight)
        #print("nablaWeight:", *nablaWeight)
        weight = [w - nw/batchSize for w, nw in zip(weight, nablaWeight)]
        bias = [b - nb/batchSize for b, nb in zip(bias, nablabias)]
        #print("after:", weight)
    return(weight, bias, perfect / (i + j + 1))

def train(batchSize, netKind, viewProgress, iterations):
    weight, bias = [[np.array([1, 2])], [np.array([0]), np.array([1])]], [0, [0, 0]]
    print(weight)
    inin, y = [0, 1], [1, 0]
    output, rawActivation, activation = feedForward(inin, weight, bias)
    delta = getDerivative(output, y, 0)
    print("target:", y)
    print("delta:", delta)
    newNablaWeight, newNablaBias = backPropagation(rawActivation, activation, delta, weight, bias)
    weight = [w - nw for w, nw in zip(weight, newNablaWeight)]
    print(weight)
    print("new iteration")
    inin, y = [0, 1], [1, 0]
    output, rawActivation, activation = feedForward(inin, weight, bias)
    delta = getDerivative(output, y, 0)
    print("target:", y)
    print("delta:", delta)
    newNablaWeight, newNablaBias = backPropagation(rawActivation, activation, delta, weight, bias)
    weight = [w - nw for w, nw in zip(weight, newNablaWeight)]
    print(weight)
    output, rawActivation, activation = feedForward(inin, weight, bias)
    print("result:", output)

def test(weight, bias):
    image, label = fm.getImages("t10k-images-idx3-ubyte/data"), fm.getLabels("t10k-labels-idx1-ubyte/data")
    accuracy = 0
    for i in range(len(image)):
        output, rawActivation, activation = feedForward(image[i], weight, bias)
        print(output, getAnswer(output)[1])
        vm.generateImage(image[i], label[i])
        input()
        if (label[i] == getAnswer(output)[1]): accuracy += 1
    accuracy /= len(image)
    print("accuracy =", accuracy)

def lol(arr):
    for i in range(len(arr)):
        arr[i] = round(arr[i], 3)
    return(arr)

train(10, [784, 10, 10], 0, 30)
#weight, bias, accuracy, simTime = fm.getNeuralNetworkModel()
#test(weight, bias)