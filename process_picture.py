import numpy as np
from pickle import dump
from PIL import Image


def obtain_one_picture(image):
    """ obtain one picture vector from picture

    :param image: read image from img file
    :return: one picture vector
    """
    if isinstance(image, str):
        try:
            image = Image.open(image)
        except Exception as e:
            print(e)
    mat = np.array(image)
    # remove background
    mat[mat >= 200] = 0
    mat[mat > 0] = 1
    return mat.ravel()


def create_train_data(path):
    """ create train data for model

    :return: None
    """
    x = []
    y = []
    m_dict = {}
    num_set = set(range(1, 5))
    w = 0
    for i in num_set:
        for j in (num_set - {i}):
            for k in (num_set - {i, j}):
                for p in (num_set - {i, j, k}):
                    num_str = str(i) + str(j) + str(k) + str(p)
                    try:
                        l = obtain_one_picture(path + "/" + num_str + ".jpg").tolist()
                        if l[0] is not None:
                            x.append(l)
                            y.append(w)
                            m_dict[w] = num_str
                            w += 1
                    except Exception as e:
                        print(e)

    # create array for x data and y data
    x_data = np.array(x)
    y_data = np.array(y)
    # save x_data and y_data into the npy file
    np.save("train_data/x_data.npy", x_data)
    np.save("train_data/y_data.npy", y_data)
    # # save m_dict
    with open("img/m_dict.pkl", "wb") as f:
        dump(m_dict, f)

if __name__ == '__main__':
    img_path = "img"
    # create train data and save image map
    create_train_data(img_path)
