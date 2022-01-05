import numpy as np

class NeuralNetwork:

    def __init__(self, layers):
        self.layers = layers
        self.err_log = None

    def predict(self, input_data):
        samples = input_data.shape[0]
        result = []
        for i in range(samples):
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward(output)
            result.append(np.argmax(output) + 3)
        return result

    def train(self, x_train, y_train, epochs, learn_rate=0.1):
        samples = x_train.shape[0]
        self.err_log = np.zeros(epochs)
        for i in range(epochs):
            loss = 0
            for j in range(samples):
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward(output)
                loss += self.loss(y_train[j], output)
                dE_dY = self.dloss(y_train[j], output)
                for layer in reversed(self.layers):
                    dE_dY = layer.backward(dE_dY, learn_rate)
            loss /= samples
            self.err_log[i] = loss
            print(f"epoch: {i}, loss: {loss}")

    def loss(self, y_true, y_pred):
        return np.mean((y_true - y_pred)**2)

    def dloss(self, y_true, y_pred):
        return 2 * (y_pred - y_true) / y_true.size