import FileReader
from random import random

def printImage(image, index):
    for i in range(28):
        for j in image[index][i]:
            print((j > 0) + 0, end='')
        print()

def getData():
    fr = FileReader.FileReader()
    image = fr.getImages("t10k-images-idx3-ubyte/data")
    label = fr.getLabels("t10k-labels-idx1-ubyte/data")
    for i in range(5):
        printImage(image, i)
        print(label[i])
    return(image, label)

netSize = [784, 16, 16, 10]
net = []
for i in range(len(netSize) - 1):
    net += [[[random() * 10] * (netSize[i] + 1) for j in range(netSize[i + 1])]]
for i in net:
    print(len(i), "------")
    for j in i:
        print(len(j))
