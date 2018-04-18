import FileReader

def printImage(image, index):
    for i in range(784):
        if (i and i % 28 == 0): print()
        print((image[index][i] > 0) + 0, end='')

def getData():
    fr = FileReader.FileReader()
    image = fr.getImages("t10k-images-idx3-ubyte/data")
    label = fr.getLabels("t10k-labels-idx1-ubyte/data")
    for i in range(0):
        printImage(image, i)
        print(" ", label[i])
    return(image, label)

image, label = getData()
printImage(image, 0)
print(" ", label[0], sep='')