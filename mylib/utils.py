import pandas as pd
import seaborn as sns


def read_data(file_path):
    """
    Read data from .csv file

    :param file_path: a path to data
    :return: pandas-like dataframe contains data
    """
    dataframe = pd.read_csv(file_path, sep='\t', index_col=0)
    return dataframe
