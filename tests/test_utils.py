import pytest
from mylib.utils import read_data


@pytest.mark.parametrize('path', ['./data/clean_data.csv'])
def test_read_data(path):
    '''
    Check if function accepts .csv file and returns Dataframe object
    '''
    assert path.split('.')[-1] == 'csv'
    test_frame = read_data(path)
    assert test_frame is not None
    assert test_frame.shape == (2887, 167)
