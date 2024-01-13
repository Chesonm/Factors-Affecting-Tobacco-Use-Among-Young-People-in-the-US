"""
Guicheng Ma & Yuqing Li
CSE 163 Final Project
Title: Factors Affecting Tobacco Use Among Young People in the US.
In this program, I am trying to build a machine learning model that will make
a best prediction on the precentage of people who smoke, based on the year,
location, which kind of cigerate they are using, gender, race and their
education level.
"""
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import data_process as dp
import matplotlib.pyplot as plt


def test_size_det(df: pd.DataFrame) -> float:
    """
    Train a best DecisionTreeRegressor model to predict the percentage of
    people who smoke for a given year, location, which kind of cigerate
    they are using, gender, race and their education level.
    Build a plot of the error versus the corresponding test size.
    Return the best test size that make the prediction most accurate.
    """
    df_filtered = df.loc[:, ['YEAR', 'LocationAbbr', 'MeasureDesc',
                             'Data_Value', 'Gender', 'Race', 'Education']]
    df_filtered = df_filtered.dropna()
    features = df_filtered.loc[:, df_filtered.columns != 'Data_Value']
    labels = df_filtered['Data_Value']
    features = pd.get_dummies(features)
    dict_error = dict()
    dict_error['error'] = []
    list_index = list()

    for size_num in range(1, 99):
        list_index.append(0.01*size_num)

        features_train, features_test, labels_train, labels_test = \
            train_test_split(features, labels, test_size=0.01*size_num)

        model = DecisionTreeRegressor()

        model.fit(features_train, labels_train)

        test_predictions = model.predict(features_test)

        test_error = mean_squared_error(test_predictions, labels_test)

        dict_error['error'].append(test_error)

    df_test = pd.DataFrame(dict_error, index=list_index)

    # Plot the error versus the test size we take
    df_test.plot()
    plt.show()
    return df_test['error'].idxmin()
    # There is always a minimum value between 0 and 0.1


def max_depth_det(df: pd.DataFrame, size):
    """
    Taking the the best test size that make the prediction most accurate
    Train a best DecisionTreeRegressor model to predict the percentage of
    people who smoke for a given year, location, which kind of cigerate they
    are using, gender, race and their education level by tring different
    depth we go.
    Plot the error versus the depth we go.
    """
    df_filtered = df.loc[:, ['YEAR', 'LocationAbbr', 'MeasureDesc',
                             'Data_Value', 'Gender', 'Race', 'Education']]
    df_filtered = df_filtered.dropna()
    features = df_filtered.loc[:, df_filtered.columns != 'Data_Value']
    labels = df_filtered['Data_Value']
    features = pd.get_dummies(features)
    dict_error = dict()
    dict_error['error'] = []
    list_index = list()

    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=size)

    for depth in range(1, 10):
        list_index.append(depth)

        model = DecisionTreeRegressor(max_depth=depth)

        model.fit(features_train, labels_train)

        test_predictions = model.predict(features_test)

        test_error = mean_squared_error(test_predictions, labels_test)

        dict_error['error'].append(test_error)

    df_test = pd.DataFrame(dict_error, index=list_index)

    df_test.plot()
    plt.show()


def main():
    data1 = pd.read_csv('rate_data.csv', low_memory=False, encoding='latin-1')
    data_rate_data = dp.rate_dataFrame(data1)

    best_test_size = test_size_det(data_rate_data)
    max_depth_det(data_rate_data, best_test_size)


if __name__ == '__main__':
    main()
