import pytest
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.pandas import column, columns, data_frames

from mylib.eda import get_nan_features, split_features
from mylib.model import data_preprocessing

import pickle
import pandas as pd

import warnings
warnings.filterwarnings('ignore')


def sublist(sublst, lst):
    return str(sublst).strip('[]') in str(lst).strip('[]')


@given(data_frames(columns=[
        column(name='first',
               elements=st.one_of(
                   st.just(float('nan')),
                   st.integers(),
                   st.text(),
                   st.floats())),
        column(name='second',
               elements=st.one_of(
                   st.just(float('nan')),
                   st.integers(),
                   st.text(),
                   st.floats())
               )
    ])
)
def test_get_nan_features_hypo(frame):
    result = get_nan_features(frame)
    assert isinstance(result, dict)
    for value in result.values():
        assert value > 0
    for key in result.keys():
        assert isinstance(key, str)


@given(data_frames(
    columns=columns(["first", "second", 'third'], dtype=float),
    rows=st.tuples(st.floats(allow_nan=False),
                   st.integers(),
                   st.text())
))
def test_split_features_hypo(frame):
    cat_feats, float_feats, int_feats = split_features(frame)
    features = list(frame)
    assert isinstance(cat_feats, list)
    assert isinstance(float_feats, list)
    assert isinstance(int_feats, list)

    assert sublist(cat_feats, features)
    assert sublist(float_feats, features)
    assert sublist(int_feats, features)


def calculate_residuals(model_path, data_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    _, _, X_test, y_test, _ = data_preprocessing(data_path)
    predictions = model.predict(X_test)
    df_results = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
    df_results['Residuals'] = abs(df_results['Actual']) - abs(df_results['Predicted'])

    return df_results


@pytest.mark.parametrize('model_path, data_path', [('models/model.pkl', 'data/clean_data.csv')])
def test_normal_errors_distribution(model_path, data_path):
    from statsmodels.stats.diagnostic import normal_ad

    df_results = calculate_residuals(model_path, data_path)
    p_value = normal_ad(df_results.Residuals)[1]
    assert p_value < 0.05


@pytest.mark.parametrize('model_path, data_path', [('models/model.pkl', 'data/clean_data.csv')])
def test_autocorrelation(model_path, data_path):
    from statsmodels.stats.stattools import durbin_watson

    df_results = calculate_residuals(model_path,data_path)
    durbinWatson = durbin_watson(df_results['Residuals'])

    assert durbinWatson > 1.5
    assert durbinWatson < 2.5


@pytest.mark.parametrize('model_path, data_path', [('models/model.pkl', 'data/clean_data.csv')])
def test_homoscedasticity(model_path, data_path):
    from statsmodels.stats.diagnostic import het_breuschpagan

    _, _, X_test, _, _ = data_preprocessing(data_path)

    df_results = calculate_residuals(model_path, data_path)
    _, p_value, _, _ = het_breuschpagan(df_results.Residuals, X_test)
    assert p_value < 0.05
