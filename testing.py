"""
Guicheng Ma & Yuqing Li
CSE 163 Final Project
Title: Factors Affecting Tobacco Use Among Young People in the US.

This is the file that conatin testing function to test the validity
"""

import pandas as pd
import helper_function
import main1
import main4
import data_process

def filtered_dataset(data: pd.DataFrame):
    df = data_process.rate_dataFrame(data).copy()
    df['YEAR'] = df['YEAR'].astype('int')
    df = df.loc[(df['Race'] == "All Races") &
                ((df['LocationDesc'] == "Colorado")|
                (df['LocationDesc'] == "California")|
                (df['LocationDesc'] == "Arkansas")|
                (df['LocationDesc'] == "Alaska")|
                (df['LocationDesc'] == "Arizona")|
                (df['LocationDesc'] == "Alabama")) &
                (df['Gender'] == 'Overall') &
                ((df['YEAR'] == 2011) | (df['YEAR'] == 2019)),
                ['YEAR', 'LocationDesc',
                'Data_Value']]
    main1.net_change(df)
    sum_data = df.groupby(['LocationDesc', 'YEAR'])['Data_Value']
    sum_data = sum_data.sum().reset_index()



def test_net_change() -> None:
    """
    Tests the net_change method
    """
    # The regular case
    helper_function.assert_equals(15, main1.net_change(data_process))
    


def main():
    data1 = pd.read_csv('rate_data.csv', low_memory=False, encoding='latin-1')
    filtered_dataset(data1)
    #test_net_change()
    


if __name__ == '__main__':
    main()
