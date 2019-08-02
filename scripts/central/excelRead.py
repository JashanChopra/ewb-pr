"""
This script contains general functions related to any aspect of the project
"""


def loadExcel(filename):
    """
    Reads an excel file
    :param filename: full filepath
    :return: dataframe
    """

    import pandas as pd
    data = pd.read_excel(filename)
    return data
