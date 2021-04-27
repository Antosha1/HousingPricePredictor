import pytest
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.pandas import column, columns, data_frames

from mylib.eda import get_nan_features, split_features


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
