from PIL import Image, ImageColor
import os
import FileManager
fm = FileManager.FileManager()

class VisualizationManager:

    image, label = 0, 0

    def getData(self):
        image = fm.getImages("t10k-images-idx3-ubyte/data")
        label = fm.getLabels("t10k-labels-idx1-ubyte/data")
        return(image, label)

    def consolePrint(self, image, label):
        for i in range(784):
            if (i and i % 28 == 0): print()
            print((image[i] > 0) + 0, end='')
        print("", label)

    def generateImage(self, image, label):
        im = Image.new("L", [784, 784])
        for i in range(784):
            for j in range(784):
                im.putpixel([j, i], int(image[((i // 28) * 28) + j // 28] * 255))
        im.show()
        return(im)

