import pytest
from mylib.eda import get_nan_features, split_features, encode_features
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')


def test_get_nan_features():
    '''
    Check if function returns correct dict
    '''
    test_frame_int = pd.DataFrame([[6, np.nan, 6], [3, np.nan, np.nan], [2, np.nan, 5]],
                                  columns=['ball', 'mug', 'pen'])
    test_nan_features_int = get_nan_features(test_frame_int)

    assert isinstance(test_nan_features_int, dict)
    assert test_nan_features_int == {'mug': 3, 'pen': 1}

    test_frame_float = pd.DataFrame([[6.3, np.nan, 6.1], [2.5, np.nan, 2.2], [np.nan, np.nan, np.nan]],
                                    columns=['ball', 'mug', 'pen'])
    test_nan_features_float = get_nan_features(test_frame_float)

    assert isinstance(test_nan_features_float, dict)
    assert test_nan_features_float == {'ball': 1, 'mug': 3, 'pen': 1}

    test_frame_str = pd.DataFrame([['smth1', np.nan, 'smth2'], ['smth3', np.nan, 'smth4'], ['smth5', np.nan, np.nan]],
                                  columns=['ball', 'mug', 'pen'])
    test_nan_features_str = get_nan_features(test_frame_str)

    assert isinstance(test_nan_features_str, dict)
    assert test_nan_features_str == {'mug': 3, 'pen': 1}


def test_split_features():
    '''
    Check if function returns correctly lists
    '''
    test_frame = pd.DataFrame([['smth1', 6.2, np.nan], ['smth3', 13.1, 3], ['smth5', 0.5, 1]],
                              columns=['ball', 'mug', 'pen'])
    cat_feats, float_feats, int_feats = split_features(test_frame)
    assert isinstance(cat_feats, list)
    assert isinstance(float_feats, list)
    assert isinstance(int_feats, list)


def test_encode_features():
    '''
    Check if function return right shape dataframe
    '''
    test_frame = pd.DataFrame({'A': ['a', 'b', 'a'], 'B': ['b', 'a', 'c'],
                               'C': [1, 2, 3]})
    test_num_features = ['C']
    test_cat_features = ['A', 'B']
    test_encoded_frame = encode_features(test_frame, test_num_features, test_cat_features)
    assert test_encoded_frame.shape == (3, 6)
