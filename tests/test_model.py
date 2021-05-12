import pytest
from mylib.model import data_preprocessing, train, predict
import pickle

import warnings
warnings.filterwarnings('ignore')


@pytest.mark.parametrize('path', ['data/clean_data.csv'])
def test_data_preprocessing(path):
    '''
    Check if function works correctly
    '''
    X_train, y_train, X_test, y_test, lmbda = data_preprocessing(path)
    assert X_train is not None and y_train is not None
    assert X_test is not None and y_test is not None
    assert lmbda is not None

    assert X_train.shape == (2020, 167)
    assert y_train.shape == (2020,)
    assert X_test.shape == (867, 167)
    assert y_test.shape == (867,)


@pytest.mark.parametrize('path', ['data/clean_data.csv'])
def test_train(path):
    '''
    Check if function returns sklearn model
    '''
    test_model = train(path)
    assert test_model is not None


@pytest.mark.parametrize('model_path, data_path', [('models/model.pkl', 'data/clean_data.csv')])
def test_predict(model_path, data_path):
    '''
    Check if function returns right shape prediction
    '''
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    test_preds = predict(model, data_path)
    assert test_preds is not None
    assert test_preds.shape == (867,)
