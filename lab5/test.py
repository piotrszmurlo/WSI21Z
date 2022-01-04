import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from layer import Layer
from neural_network import NeuralNetwork

def main():

    df = pd.read_csv('wines.csv', delimiter=';')
    train_df, test_df = train_test_split(df, test_size=0.4, random_state=1)
    train_x = df.drop(columns='quality').to_numpy().reshape((4898,1,11))
    train_y = df['quality'].to_numpy()
    # train_x = np.array([[[0, 0]], [[0,1]], [[1,0]], [[1,1]]])
    # train_y = np.array([0, 1, 1, 0])

    print(train_x)
    print(train_y.shape)

    layers = [Layer(11, 10, hidden=True), Layer(activation=True), Layer(10, 11)]
    nn = NeuralNetwork(layers)

    nn.train(train_x, train_y, epochs=1000, learn_rate=0.5)

    print(nn.predict(train_x))
    

if __name__ == '__main__':
    main()