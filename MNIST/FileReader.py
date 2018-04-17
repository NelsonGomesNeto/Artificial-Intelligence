from PIL import Image
import os
import numpy as np

class FileReader:

    def getImages(self, path):
        testFile = open(path, "rb")
        testSize = os.path.getsize(path)
        test = list(bytes(testFile.read(testSize)))
        #print(len(test), testSize)
        image = []
        for i in range(len(test[16:]) // 784):
            image += [test[16 + 784*i : 16 + 784*(i + 1)]]
        return(np.array(image))

    def getLabels(self, path):
        testFile = open(path, "rb")
        testSize = os.path.getsize(path)
        test = list(bytes(testFile.read(testSize)))
        #print(len(test), testSize)
        label = []
        for i in test[8:]:
            label += [i]
        return(np.array(label))