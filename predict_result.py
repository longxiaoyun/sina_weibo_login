from train_model import joblib
from process_picture import obtain_one_picture


def image_identification(image, model_type):
    """
    :param: image
    :param: model_type
    :return:
    """
    x_data = obtain_one_picture(image)
    # deal with picture
    clr = joblib.load("model/" + model_type +".pkl")
    return clr.predict([x_data])[0]

if __name__ == '__main__':
    # the picture come from img test
    result = image_identification("img/1234.jpg", "lr")
    m_dict = joblib.load("img/m_dict.pkl")
    print("The picture class is: {}, and number path is {}".format(result, m_dict[result]))
