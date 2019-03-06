from numpy import exp

class Sigmoid:

    def __init__(self):
        pass

    def function(self, x):
        return(1.0 / (1.0 + exp(-x)))

    def derivative(self, x):
        return(self.function(x) * (1.0 - self.function(x)))
