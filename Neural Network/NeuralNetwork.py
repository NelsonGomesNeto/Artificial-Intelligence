import numpy
dataPath = "NeuralNetworkData/"

class NeuralNetwork:

    def __init__(self, layersSize, activationFunction):
        self.layers = len(layersSize) - 1
        self.weights, self.weightsNudge = [], []
        self.biases, self.biasesNudge = [], []
        self.zs, self.activations = [], [numpy.mat(numpy.zeros((layersSize[0], 1)))]
        for i in range(len(layersSize) - 1):
            self.weights += [numpy.random.rand(layersSize[i], layersSize[i + 1]).transpose() / 10]
            self.weightsNudge += [numpy.mat(numpy.zeros((layersSize[i], layersSize[i + 1]))).transpose()]
            self.zs += [numpy.mat(numpy.zeros((layersSize[i + 1], 1)))]
            self.activations += [numpy.mat(numpy.zeros((layersSize[i + 1], 1)))]
            self.biases += [numpy.mat(numpy.zeros((layersSize[i + 1], 1)))]
            self.biasesNudge += [numpy.mat(numpy.zeros((layersSize[i + 1], 1)))]
        self.activationFunction = activationFunction
        self.activationFunction.function = numpy.vectorize(self.activationFunction.function)
        self.activationFunction.derivative = numpy.vectorize(self.activationFunction.derivative)

    def __str__(self):
        # string = str(self.layers)
        string = "\n\tWeight: " + str(self.weights[0].shape)
        for weight in self.weights[1:]:
            string += " " + str(weight.shape)
        string += "\n\tBias: " + str(self.biases[0].shape)
        for bias in self.biases:
            string += " " + str(bias.shape)
        return(string)

    def save(self):
        l = [self.weights[0].shape[1]]
        for i in range(self.layers): l += [self.weights[i].shape[0]]
        f = open(dataPath + "config.config", "w")
        print(l, file=f)
        f.close()
        numpy.save(dataPath + "weights.npy", self.weights)
        numpy.save(dataPath + "biases.npy", self.biases)

    def load(self):
        self.weights = numpy.load(dataPath + "weights.npy")
        self.biases = numpy.load(dataPath + "biases.npy")

    def feedForward(self, data):
        i = 0
        self.activations[0] = data
        for w, b in zip(self.weights, self.biases):
            data = w * data + b
            self.zs[i] = data
            data = self.activationFunction.function(data)
            i += 1
            self.activations[i] = data
        return(data)

    def backPropagation(self, delta):
        self.weightsNudge[self.layers - 1] += delta * self.activations[-2].transpose()
        self.biasesNudge[self.layers - 1] += delta
        for i in range(self.layers - 2, -1, -1):
            delta = self.weights[i + 1].transpose() * delta
            self.weightsNudge[i] += delta * self.activations[i].transpose()
            self.biasesNudge[i] += delta

    def answerDelta(self, neuralNetworkAnswer, correctAnswer):
        diff = 2*numpy.array(neuralNetworkAnswer - correctAnswer)
        return(numpy.mat(diff * numpy.array(self.activationFunction.derivative(self.zs[-1]))))

    def train(self, database, batchSize = 10, verbose = False):
        total, correct = 0, 0
        while (total < len(database)):
            for wn, bn in zip(self.weightsNudge, self.biasesNudge):
                wn *= 0
                bn *= 0
            for i in range(batchSize):
                if (total >= len(database)): break
                answer = self.feedForward(database[total][0].copy())
                correct += answer.argmax() == database[total][1].argmax()
                if (verbose): print(answer.argmax(), database[total][1].argmax())
                self.backPropagation(self.answerDelta(answer, database[total][1]))
                total += 1
            for w, b, wn, bn in zip(self.weights, self.biases, self.weightsNudge, self.biasesNudge):
                w -= wn / batchSize
                b -= bn / batchSize

        return(correct)

    def predict(self, database, verbose = False):
        correct = 0
        for data in database:
            answer = self.feedForward(data[0].copy())
            correct += answer.argmax() == data[1].argmax()
            if (verbose): print(answer.argmax(), data[1].argmax())
        return(correct / len(database))