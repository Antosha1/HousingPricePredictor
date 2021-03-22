import pandas as pd
import seaborn as sns


def read_data(file_path):
    dataframe = pd.read_csv(file_path, sep='\t', index_col=0)
    return dataframe
