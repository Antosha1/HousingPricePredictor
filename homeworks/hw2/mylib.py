import pandas as pd

from scipy.stats import boxcox
from scipy.special import inv_boxcox

from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings("ignore")


def data_preprocessing(data_path):
    df = pd.read_csv(data_path)
    y = df['SalePrice']
    X = df.drop(columns=['SalePrice'])

    num_features = []
    for feature in list(X):
        if X[feature].nunique() > 10:
            num_features.append(feature)

    y, lmbda = boxcox(y, lmbda=None)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=17)
    X_train.loc[:, 'const'] = 1
    X_test.loc[:, 'const'] = 1

    ss = StandardScaler()
    X_train[num_features] = ss.fit_transform(X_train[num_features])
    X_test[num_features] = ss.fit_transform(X_test[num_features])

    return X_train, y_train, X_test, y_test, lmbda


def train(data_path):
    X_train, y_train, _, _, _ = data_preprocessing(data_path)
    model = Ridge(alpha=31.1).fit(X_train, y_train)

    return model


def test(model, data_path):
    _, _, X_test, y_test, lmbda = data_preprocessing(data_path)
    preds = inv_boxcox(model.predict(X_test), lmbda)

    return preds
