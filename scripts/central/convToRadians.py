import numpy as np


def conv(item):
    """
    Converts a list to a numpy array and then converts each degree value in the array to radian datatype
    :param item: a list of degree values
    :return: a numpy array of radia values
    """

    arr = np.asarray(item)
    radlist = np.deg2rad(arr)

    return radlist
