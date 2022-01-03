import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def main():
    df = pd.read_csv('./lab5/wines.csv', delimiter=';')
    train_df, test_df = train_test_split(df, test_size=0.4, random_state=1)
    nn = NeuralNetwork(train_df, 11, 5, 11)
    nn.initialize()
    nn.forward()
    # nn.backward()
    # nn.forward()
    # nn.train()

class NeuralNetwork:

    def __init__(self, df, input_layer_size, hidden_layer_size, output_layer_size) -> None:
        self.Y = df['quality'].to_numpy()
        self.output = np.zeros_like(self.Y)
        self.X = df.drop(columns='quality').to_numpy().T
        self.input_layer_size = input_layer_size
        self.hidden_layer_size = hidden_layer_size
        self.output_layer_size = output_layer_size
        self.params = {}
        self.cache = {}
        self.learn_rate = 0.0005
        self.sample_count = self.Y.shape[0]
        self.loss = []
    
    def initialize(self):
        np.random.seed(1)
        self.params['W1'] = np.random.uniform(-1 / np.sqrt(self.input_layer_size), 1 / np.sqrt(self.input_layer_size), (self.hidden_layer_size, self.input_layer_size))
        self.params['b1'] = np.zeros((self.hidden_layer_size, 1))
        self.params['W2'] = np.zeros((self.output_layer_size, self.hidden_layer_size))
        # self.params['W2'] = np.random.uniform(-1 / np.sqrt(self.input_layer_size), 1 / np.sqrt(self.input_layer_size), (self.output_layer_size, self.hidden_layer_size))
        self.params['b2'] = np.zeros((self.output_layer_size, 1))

    def forward(self):
        Z1 = self.params['W1'].dot(self.X) + self.params['b1']
        A1 = self._sigmoid(Z1)
        Z2 = self.params['W2'].dot(A1) + self.params['b2']

        self.cache['Z1'] = Z1
        self.cache['A1'] = A1
        self.cache['Z2'] = Z2
        
        for i, out in enumerate(Z2.T):
            self.output[i] = np.argmax(out)
        loss = ((self.output - self.Y)**2).sum()
        return self.output, loss

    # def backward(self):
    #     dLoss_output = 2 * (self.output - self.Y)
    #     dLoss_A1 = np.dot(self.params['W2'].T, dLoss_output)
    #     dLoss_Z1 = dLoss_A1 * self._dSigmoid(self.cache['Z1'])
    #     dLoss_W1 = 1./self.X.shape[1] * np.dot(dLoss_Z1, self.X.T)
    #     dLoss_W2 = 1./self.cache['A1'].shape[1] * np.dot(dLoss_output, self.cache['A1'].T)
    #     dLoss_b2 = 1./self.cache['A1'].shape[1] * np.dot(dLoss_output, np.ones([dLoss_output.shape[1],1]))
    #     dLoss_b1 = 1./self.X.shape[1] * np.dot(dLoss_Z1, np.ones([dLoss_Z1.shape[1],1]))
    #     self.params["W1"] = self.params["W1"] - self.learn_rate * dLoss_W1
    #     self.params["b1"] = self.params["b1"] - self.learn_rate * dLoss_b1
    #     self.params["W2"] = self.params["W2"] - self.learn_rate * dLoss_W2
    #     self.params["b2"] = self.params["b2"] - self.learn_rate * dLoss_b2

    # def train(self, iter = 5000):
    #         np.random.seed(1)                         
    #         self.initialize()
    #         for i in range(0, iter):
    #             output, loss=self.forward()
    #             self.backward()
            
    #             if i % 500 == 0:
    #                 print (f"Error after {i} iterations: {loss}")
    #                 self.loss.append(loss)
    
    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def _dSigmoid(self,x):
        return np.exp(-x) / ((1 + np.exp(-x))**2)


if __name__ == '__main__':
    main()

