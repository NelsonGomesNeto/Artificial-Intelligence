from PIL import Image
import os
import FileManager
fm = FileManager.FileManager()

def printImage(image, label):
    for i in range(784):
        if (i and i % 28 == 0): print()
        print((image[i] > 0) + 0, end='')
    print("", label)

image = fm.getImages("train-images-idx3-ubyte")
label = fm.getLabels("train-labels-idx1-ubyte")

printImage(image[0], label[0])