import numpy as np

class Layer():
    def __init__(self, input_layer_size=1, output_layer_size=1, activation = False, hidden = False):
        self.activation = activation
        if not self.activation:
            self.bias = np.zeros((1, output_layer_size))
            self.input = None
            self.output = None
            if hidden:
                self.weights = np.random.uniform(-1 / np.sqrt(input_layer_size), 1 / np.sqrt(input_layer_size), (input_layer_size, output_layer_size))
            else:
                self.weights = np.zeros((input_layer_size, output_layer_size))

    def forward(self, input_data):
        self.input = input_data
        if self.activation:
            self.output = self._sigmoid(self.input)
            return self.output
        else:
            self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    def backward(self, dE_dY, learn_rate):
        if self.activation:
            return self._dSigmoid(self.input) * dE_dY
        else:
            dE_dX = np.dot(dE_dY, self.weights.T)
            dE_dW = np.dot(self.input.T, dE_dY)
            self.weights -= learn_rate * dE_dW
            self.bias -= learn_rate * dE_dY
        return dE_dX

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def _dSigmoid(self, x):
        s = self._sigmoid(x)
        return s * (1 - s)