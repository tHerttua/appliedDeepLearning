import math
import pandas as pd
import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error

DATASET_FILE = './dataset/cleaned20210501.csv'
TRAIN_PERCENTAGE = 0.8
#Hyper parameters:
HIDDEN_NODES = 10
LOOK_BACK = 3
NUM_EPOCHS = 5


def load_data(dataset_file):
    """
    :param dataset_file: must be of format [sequence_id, entry, entry, ..., entry]
    :return:
    """
    #dataset = pd.read_csv(dataset_file, index_col=0, header=None).T
    df = pd.read_csv(dataset_file, header=None)
    dataset = df.iloc[:, 1:]
    #dataset.info()
    #print(dataset.head())
    return dataset


def drop_sequences(length):
    """
    Drop sequences that are below certain length
    & other criteria
    """
    pass


def split_data(dataset, train_percentage):

    train_size = int(np.floor(int(len(dataset) * train_percentage)))
    train_data = dataset.sample(train_size)
    test_data = dataset.drop(train_data.index)

    return train_data, test_data


def create_data_set_matrix(sequence, look_back):
    """
    Creates features - output matrix according to the look_back.
    For example sequence full sequence [1 4 6 8 9] with look back 2 turns into:
      X   Y
    [1,4][6]
    [4,6][8]
    [6,8][9]
    """
    features, result = [], []
    for i in range(len(sequence) - look_back - 1):
        a = sequence[i:(i + look_back)]
        features.append(a)
        result.append(sequence[i + look_back])
    return np.array(features), np.array(result)



def create_model(train_set, test_set, look_back, num_epochs):
    """
    :param look_back: Look back is the number of previous entries in the sequence to consider
                  in order to predict the next one
    :return: a trained model to be used for stacking
    """

    # a test with one sequence
    # needs solution to learn multiple different sequences
    # -> train a model for those unique sequences that appear x% in the data?
    #for train_entry in train_set:
    train_entry = train_set.head(1).values[0].tolist()
    X,Y = create_data_set_matrix(train_entry, look_back)

    model = Sequential()
    model.add(
        LSTM(HIDDEN_NODES,
             activation='softmax',
             input_shape=(look_back, 1))
    )
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    #needs validation set as well?
    model.fit(X, Y, epochs=num_epochs, verbose=1)

    return model


def stack_models(models):
    """
    """
    pass


def predict(model, train_x, train_y, test_x, test_y):
    #Source in Assignment_2_Hacking.md: Brownlee, 2016
    train_predict = model.predict(train_x)
    test_predict = model.predict(test_x)

    trainScore = math.sqrt(mean_squared_error(train_y[0], train_predict[:, 0]))
    testScore = math.sqrt(mean_squared_error(test_y[0], test_predict[:, 0]))

    return trainScore, testScore

def display_results():
    pass


def do_magic():
    sequences_data = load_data(DATASET_FILE)
    train, test = split_data(sequences_data, TRAIN_PERCENTAGE)
    model = create_model(train, test, LOOK_BACK, NUM_EPOCHS)


do_magic()
