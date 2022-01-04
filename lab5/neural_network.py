import numpy as np

class NeuralNetwork:

    def __init__(self, layers):
        self.layers = layers

    def predict(self, input_data):
        samples = input_data.shape[0]
        result = []
        for i in range(samples):
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward(output)
            result.append(output)
        return result

    def train(self, x_train, y_train, epochs, learn_rate=0.1):
        samples = x_train.shape[0]
        for i in range(epochs):
            error = 0
            for j in range(samples):
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward(output)
                error += self.loss(y_train[j], output)
                dE_dY = self.dloss(y_train[j], output)
                for layer in reversed(self.layers):
                    dE_dY = layer.backward(dE_dY, learn_rate=0.1)
            # print(error)

            print(f"Epoch {i}, error: {error}")

    def loss(self, y_true, y_pred):
        return np.mean(np.power(y_true - y_pred, 2))

    def dloss(self, y_true, y_pred):
        return 2*(y_pred - y_true) / y_true.size