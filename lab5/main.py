from sklearn.metrics import confusion_matrix, accuracy_score
from neural_network import NeuralNetwork
import pandas as pd
from layer import Layer
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def main():

    input_layer_size = 11
    hidden_layer_size = 15
    output_layer_size = 6
    learn_rate = 0.2

    df = pd.read_csv('winequality-red.csv', delimiter=';')
    train_df, test_df = train_test_split(df, test_size=0.4, random_state=1)

    scaler = StandardScaler()
    test_x = test_df.drop(columns='quality')
    scaler.fit(test_x)

    test_y = pd.DataFrame(test_df['quality']).to_numpy()
    test_x = scaler.transform(test_x)

    train_x = train_df.drop(columns='quality')
    train_y = pd.DataFrame(train_df['quality'])

    scaler.fit(train_x)
    train_x_scaled = scaler.transform(train_x)
    scaler.fit(train_y)
    train_y_scaled = scaler.transform(train_y)

    y_train = train_y_scaled
    x_train = train_x_scaled.reshape(train_x_scaled.shape[0], 1, train_x_scaled.shape[1])
    y_train = pd.get_dummies(train_y['quality']).to_numpy()

    layers = [Layer(input_layer_size, hidden_layer_size, hidden=True), Layer(activation=True), Layer(hidden_layer_size, output_layer_size), Layer(activation=True)]
    nn = NeuralNetwork(layers)

    nn.train(x_train, y_train, epochs=100, learn_rate=learn_rate)

    output = nn.predict(test_x)
    print(confusion_matrix(test_y, output))
    print(f"accuracy: {accuracy_score(test_y, output)}")
    plt.plot(nn.err_log)
    plt.title(f"error(epoch) learn_rate={learn_rate}")
    plt.xlabel("epoch")
    plt.ylabel("error")
    plt.show()
    
if __name__ == '__main__':
    main()