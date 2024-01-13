"""
Guicheng Ma & Yuqing Li
CSE 163 Final Project
Title: Factors Affect Tobacco Use Among Young People in the United States.
This file will filter the datasets we have to the one only contains the
data we need.
"""
import pandas as pd


def rate_dataFrame(data: pd.DataFrame) -> pd.DataFrame:
    """
    Selects coloums that will be used in analysis from smoke_rate.csv file.
    """
    # Coloums needed: YEAR LocationAbbr LocationDesc TopicDesc MeasureDesc
    # Data_Value Gender Race Age Education GeoLocation
    # Rows needed: MeasureDesc = (Current Smoking, Current Use)
    # Age = '18 to 24 Years'
    is_current = (data['MeasureDesc'] == 'Current Smoking') | \
                 (data['MeasureDesc'] == 'Current Use')
    is_young = data['Age'] == '18 to 24 Years'
    df_filtered = data.loc[is_current & is_young,
                           ['YEAR', 'LocationAbbr',
                            'LocationDesc', 'TopicDesc',
                            'MeasureDesc', 'Data_Value',
                            'Gender', 'Race', 'Age',
                            'Education', 'GeoLocation']]
    return df_filtered


def legis_dataFrame(data: pd.DataFrame) -> pd.DataFrame:
    """
    Selects columns that will be used in analysis from legislation.csv file.
    """
    is_quarter = data['Quarter'] == 4
    year_needed_upper = data['YEAR'] <= 2019
    year_needed_lower = data['YEAR'] >= 2011
    filtered_col = data.loc[is_quarter & year_needed_lower & year_needed_upper,
                            ['YEAR', 'Quarter', 'LocationAbbr', 'LocationDesc',
                             'ProvisionGroupDesc', 'ProvisionDesc',
                             'ProvisionValue', 'MeasureDesc',
                             'DataType', 'Effective_Date']]
    return filtered_col


def main():
    data1 = pd.read_csv('rate_data.csv', low_memory=False, encoding='latin-1')
    data2 = pd.read_csv('legislation.csv')
    rate_dataFrame(data1)
    legis_dataFrame(data2)


if __name__ == '__main__':
    main()
