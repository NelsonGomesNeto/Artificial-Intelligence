from PIL import Image
import os
import time
import numpy as np
import pickle

class FileManager:

    normalize = np.vectorize(lambda x: x / 255)

    def getImages(self, path):
        testFile = open(path, "rb")
        testSize = os.path.getsize(path)
        test = list(bytes(testFile.read(testSize)))
        #print(len(test), testSize)
        image = []
        for i in range(len(test[16:]) // 784):
            image += [self.normalize(test[16 + 784*i : 16 + 784*(i + 1)])]
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

    def saveModel(self, weight, bias, accuracy, startTotal):
        f = open("model.py", "w")
        print("import numpy as np", file=f)
        print("from numpy import array", file=f)
        print("weight =", weight, file=f)
        print("bias =", bias, file=f)
        print("accuracy =", accuracy, file=f)
        print("simTime =", time.time() - startTotal, file=f)
        f.close()

    def getNeuralNetworkModel(self):
        from model import weight, bias, accuracy, simTime
        return(weight, bias, accuracy, simTime)