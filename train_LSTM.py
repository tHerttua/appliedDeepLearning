import math
import os

import pandas as pd
import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense

DATASET_FILE = './dataset/cleaned20210501.csv'
MODELS_LOCATION = "./models/"

#Hyper parameters:
TRAIN_PERCENTAGE = 0.8

HIDDEN_NODES = 10
LOOK_BACK = 3
NUM_EPOCHS = 5
OPTIMIZER = 'adam'


def load_data(dataset_file):
    """
    :param dataset_file: must be of format [sequence_id, entry, entry, ..., entry]
    :return:
    """
    #dataset = pd.read_csv(dataset_file, index_col=0, header=None).T
    df = pd.read_csv(dataset_file, header=None)
    dataset = df.iloc[:, 1:]
    #dataset = dataset.drop_duplicates()
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



def create_model(train_set):
    """
    Incomplete
    """
    train_x, train_y = create_data_set_matrix(train_set, LOOK_BACK)

    model = Sequential()
    model.add(
        LSTM(HIDDEN_NODES,
             activation='softmax',
             input_shape=(LOOK_BACK, 1))
    )
    model.add(Dense(1))
    model.compile(optimizer=OPTIMIZER, loss='categorical_crossentropy')
    model.fit(train_x, train_y, epochs=NUM_EPOCHS, verbose=1)

    return model


def stack_models(train):
    """
    Incomplete
    #to do: model checkpoints rather than array of models
    """
    model_array = []
    for idx, entry in enumerate(train):
        train_entry = train.iloc[idx]
        train_set = train_entry.values.tolist()

        model = create_model(train_set)
        model_array.append(model)

    return model_array


def train_and_save_models():
    sequences_data = load_data(DATASET_FILE)
    train, test = split_data(sequences_data, TRAIN_PERCENTAGE)
    model_array = stack_models(train)
    for model in model_array:
        model.save(MODELS_LOCATION)



train_and_save_models()
