import math
import keras
from sklearn.metrics import mean_squared_error
from train_LSTM import create_data_set_matrix


def predict(model, train_x, train_y, test_x, test_y):
    """
    Incomplete
    """
    train_predict = model.predict(train_x)
    test_predict = model.predict(test_x)

    train_score = math.sqrt(mean_squared_error(train_y[0], train_predict[:, 0]))
    test_score = math.sqrt(mean_squared_error(test_y[0], test_predict[:, 0]))

    return train_score, test_score


def predict_with_models_array(models, train_data, test_data):
    """
    Incomplete
    Source in Assignment_3_Delivery.md: Brownlee, 2016
    """
    best_result = []
    all_results = []
    i = 0

    train_x, train_y = create_data_set_matrix(train_data, LOOK_BACK)
    test_x, test_y = create_data_set_matrix(test_data, LOOK_BACK)
    for model in models:
        train_score, test_score = predict(model, train_x, train_y, test_x, test_y)
        result = [i, train_score, test_score]
        all_results.append(result)
        if train_score > best_result[1] and test_score > best_result[2]:
            best_result = result

    print(best_result)


def update_models_array():
    """
    Incomplete
    Train a new model for newly found bot sequence
    """
    pass


def display_results():
    """
    Incomplete
    """
    pass


def write_new_mappings(sequence):
    """
    Incomplete
    Upon finding an anomaly, that is considered a newly found, common command,
    it is indexed and written to the command mappings file
    """
    pass

def predict_on_data(data):
    """
    Incomplete
    """
    #list_of_models = os.listdir(MODELS_LOCATION)
    #model_array = []
    #for model_path in list_of_models:
    #    model = model = keras.models.load_model(model_path)
    #    model_array.append(model)
    #
    #predict_with_models_array(model_array, data)
    #display_results()
    pass