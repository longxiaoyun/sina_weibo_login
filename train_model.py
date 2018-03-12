import numpy as np

from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

# include LR and MLP model
model_list = {"lr": LogisticRegression, "mlp": MLPClassifier}


def train_model(x_data, y_data, model_type):
    """ train model use x_data and y_data

    :param x_data: x train data like (n_sample, n_features)
    :param y_data: y train data like (n_sample, )
    :param model_type: what model type you can choose
    :return:
    """
    # def lr model object
    clr = None
    try:
        clr = model_list[model_type]()
    except Exception as e:
        print(e)
    # fit model
    clr.fit(x_data, y_data)
    # save model in pkl file
    try:
        joblib.dump(clr, "model/" + model_type + ".pkl")
    except Exception as e:
        print(e)
    return clr


def show_model(clr, y_data):
    """ show model result

    :return: None
    """
    # predict
    y_pred = clr.predict(x_data)
    print("acc: {}".format(accuracy_score(y_data, y_pred)))
    print("confusion_matrix: \n {}".format(confusion_matrix(y_data, y_pred)))


if __name__ == '__main__':
    # load data
    x_data = np.load("train_data/x_data.npy")
    y_data = np.load("train_data/y_data.npy")
    model = train_model(x_data, y_data, "lr")
    show_model(model, y_data)
