from PIL import Image
import os

def printImage(image, index):
    for i in range(28):
        for j in image[index][i]:
            print((j > 0) + 0, end='')
        print()

testFile = open("t10k-images-idx3-ubyte/data", "rb")
testSize = os.path.getsize("t10k-images-idx3-ubyte/data")
test = list(bytes(testFile.read(testSize)))
print(len(test), testSize)

image = []
for i in range(len(test[16:]) // 784):
    lol = []
    for j in range(28):
        lol += [test[16 + 784*i + 28*j : 16 + 784*i + 28*(j + 1)]]
    image += [lol]

for i in range(100):
    printImage(image, i)
    print()