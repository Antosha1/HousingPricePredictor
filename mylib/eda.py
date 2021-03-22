import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.display.max_columns = 90
sns.set(rc={'figure.figsize': (11.7, 8.27)})


cat_dict1 = {
    'Ex': 5,
    'Gd': 4,
    'TA': 3,
    'Fa': 2,
    'Po': 1,
    'unk': 0
}

cat_dict2 = {
    'Gd': 4,
    'TA': 3,
    'Fa': 2,
    'Po': 1,
    'unk': 0
}
cat_dict3 = {
    'GLQ': 6,
    'ALQ': 5,
    'BLQ': 4,
    'Rec': 3,
    'LwQ': 2,
    'Unf': 1,
    'NA': 0
}
cat_dict4 = {
    'Fin': 3,
    'RFn': 2,
    'Unf': 1,
    'NA': 0,
}


def get_nan_features(dataframe):
    features = {}
    for feature in list(dataframe):
        nans = dataframe[feature].isna().sum()
        if nans > 0:
            features[feature] = nans
    return features


def split_features(dataframe):
    cat_df = dataframe.select_dtypes(include=['object'])
    cat_feats = list(cat_df)
    float_df = dataframe.select_dtypes(include=['float64'])
    float_feats = list(float_df)
    int_df = dataframe.select_dtypes(include=['int64']).drop(columns=['SalePrice'])
    int_feats = list(int_df)

    return cat_feats, float_feats, int_feats


def plot_num_features_pairplots(dataframe):
    cat_features, _, _ = split_features(dataframe)
    frame = dataframe.drop(columns=cat_features)

    for i in range(0, len(frame.columns), 5):
        sns.pairplot(data=frame,
                     x_vars=frame.columns[i:i + 5],
                     y_vars=['SalePrice'])


def plot_corr(dataframe, features, threshold=0.3):
    corr = dataframe[features].corr()

    plt.figure(figsize=(15, 15))

    sns.heatmap(corr[(corr >= threshold) | (corr <= -1*threshold)],
                cmap='viridis', vmax=1.0, vmin=-1.0, linewidths=0.1,
                annot=True, annot_kws={"size": 9}, square=True)


def plot_cat_features_countplots(dataframe):
    cat_features, _, _ = split_features(dataframe)
    fig, axes = plt.subplots(round(dataframe[cat_features].shape[1] / 3), 3, figsize=(12, 30))

    for i, ax in enumerate(fig.axes):
        if i < dataframe[cat_features].shape[1]:
            ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=90)
            sns.countplot(x=dataframe[cat_features].columns[i], alpha=0.7, data=dataframe[cat_features], ax=ax)

    fig.tight_layout()


def data_cleansing(dataframe):
    dataframe.drop(columns=['Alley', 'Fence', 'Misc Feature', 'Pool QC', 'Fireplace Qu', 'PID'], inplace=True)
    features = ['Bsmt Qual', 'Bsmt Cond', 'Bsmt Exposure', 'BsmtFin Type 1', 'BsmtFin Type 2',
                'Garage Type', 'Garage Finish', 'Garage Qual', 'Garage Cond']

    for feature in features:
        dataframe[feature].fillna('NA', inplace=True)

    dataframe['Garage Yr Blt'].fillna(dataframe['Garage Yr Blt'].median(), inplace=True)
    dataframe['MS SubClass'] = dataframe['MS SubClass'].astype('str')
    dataframe['Garage Yr Blt'] = dataframe['Garage Yr Blt'].astype('int64')
    cat_features, float_features, int_features = split_features(dataframe)

    for feature in float_features:
        dataframe[feature].fillna(dataframe[feature].mean(), inplace=True)

    for feature in int_features:
        dataframe[feature].fillna(dataframe[feature].median(), inplace=True)

    for feature in cat_features:
        dataframe[feature].fillna('unk', inplace=True)

    return dataframe


def filter_num_features(dataframe):

    dataframe = dataframe[dataframe['SalePrice'] < 5e5]
    dataframe = dataframe[dataframe['Lot Frontage'] < 300]
    dataframe = dataframe[dataframe['Total Bsmt SF'] < 5000]
    dataframe = dataframe[dataframe['BsmtFin SF 1'] < 3900]
    dataframe = dataframe[dataframe['1st Flr SF'] < 4000]
    dataframe = dataframe[dataframe['Gr Liv Area'] < 4500]
    dataframe = dataframe[(dataframe.index != 1342) & (dataframe.index != 1498)]
    dataframe = dataframe[dataframe['Bsmt Full Bath'] < 3]
    dataframe['Bsmt Full Bath'].astype('int64')
    dataframe = dataframe[dataframe['Bsmt Half Bath'] < 2]
    dataframe['Bsmt Half Bath'].astype('int64')
    dataframe = dataframe[dataframe['Full Bath'] < 4]
    dataframe = dataframe[dataframe['Bedroom AbvGr'] < 7.5]
    dataframe = dataframe[(dataframe['Kitchen AbvGr'] > 0) & (dataframe['Kitchen AbvGr'] < 3)]
    dataframe = dataframe[dataframe['TotRms AbvGrd'] <= 12]
    dataframe = dataframe[dataframe['Fireplaces'] < 4]
    dataframe = dataframe[dataframe['Garage Yr Blt'] < 2207]
    dataframe = dataframe[dataframe.index != 2237]
    dataframe['Garage Cars'].astype('int64')
    dataframe = dataframe[dataframe['Wood Deck SF'] < 1000]
    dataframe = dataframe[dataframe['Enclosed Porch'] < 1000]

    dataframe.drop(columns=['Garage Cars', 'TotRms AbvGrd', 'Garage Yr Blt', 'Year Remod/Add'], inplace=True)
    dataframe.drop(columns=['BsmtFin SF 1', 'BsmtFin SF 2', 'Bsmt Unf SF', '1st Flr SF'], inplace=True)
    return dataframe


def corr_analysis(dataframe):
    _, float_features, int_features = split_features(dataframe)
    num_feats = int_features + float_features + ['SalePrice']
    valuable_features = dataframe[num_feats].corr().nlargest(11, 'SalePrice').index
    return valuable_features


def filter_cat_features(dataframe):
    dataframe.drop(columns=['Street', 'Utilities', 'Land Slope', 'Condition 1', 'Condition 2', 'Roof Matl',
                            'Heating', 'Electrical', 'Functional', 'Garage Qual', 'Garage Cond', 'Sale Type'],
                   inplace=True)

    dataframe['Exter Qual'] = dataframe['Exter Qual'].apply(lambda x: cat_dict1[x])
    dataframe['Exter Cond'] = dataframe['Exter Cond'].apply(lambda x: cat_dict1[x])
    dataframe['Bsmt Qual'] = dataframe['Bsmt Qual'].apply(lambda x: cat_dict1[x])
    dataframe['Bsmt Cond'] = dataframe['Bsmt Cond'].apply(lambda x: cat_dict1[x])
    dataframe['Bsmt Exposure'] = dataframe['Bsmt Exposure'].apply(lambda x: cat_dict2[x])
    dataframe['BsmtFin Type 1'] = dataframe['BsmtFin Type 1'].apply(lambda x: cat_dict3[x])
    dataframe['BsmtFin Type 2'] = dataframe['BsmtFin Type 2'].apply(lambda x: cat_dict3[x])
    dataframe['Heating QC'] = dataframe['Heating QC'].apply(lambda x: cat_dict1[x])
    dataframe['Kitchen Qual'] = dataframe['Kitchen Qual'].apply(lambda x: cat_dict1[x])
    dataframe['Garage Finish'] = dataframe['Garage Finish'].apply(lambda x: cat_dict4[x])

    return dataframe


def encode_features(dataframe, num_feats, cat_feats):
    dummied_cat_features = pd.get_dummies(dataframe[cat_feats])
    encoded_df = pd.concat([dataframe[num_feats], dummied_cat_features], axis=1)
    return encoded_df


def main(data_path):
    df = pd.read_csv(data_path, sep='\t', index_col=0)
    df = data_cleansing(df)
    df = filter_num_features(df)

    value_num_features = corr_analysis(df)
    num_features = list(value_num_features)

    df = filter_cat_features(df)

    features = ['Exter Qual', 'Exter Cond', 'Bsmt Qual', 'Bsmt Cond', 'Bsmt Exposure',
                'BsmtFin Type 1', 'BsmtFin Type 2', 'Heating QC', 'Kitchen Qual', 'Garage Finish']

    num_features.extend(features)
    cat_features, _, _ = split_features(df)

    df = encode_features(df, num_features, cat_features)
    df.to_csv('../data/clean_data.csv', index=False)


if __name__ == '__main__':
    data_path = str(input())
    main(data_path)
