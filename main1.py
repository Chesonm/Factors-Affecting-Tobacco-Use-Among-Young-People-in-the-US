"""
Name: Yuqing Li & Guicheng Ma
CSE 163 Final Project
Title: Factors Affecting Tobacco Use Among Young People in the US.
Description: This is the file with all the functions that
             help us answer our research question 1 which
             is to investigate the relationship between
             legislation change and the change in overall
             tobacco use among young people.
"""


import pandas as pd
import data_process
from matplotlib import pyplot as plt


def net_change(data: pd.DataFrame) -> dict:
    """
    This function find out the net change of each state in
    each year, then return a result dictonary with the state
    that has highest net change over years and the state with
    the lowest net change over year.
    """
    # Process the data and only keep the columns we focus on
    df = data_process.rate_dataFrame(data).copy()
    df['YEAR'] = df['YEAR'].astype('int')
    df = df.loc[(df['Race'] == "All Races") &
                (df['Gender'] == 'Overall') &
                ((df['YEAR'] == 2011) | (df['YEAR'] == 2019)),
                ['YEAR', 'LocationDesc',
                'Data_Value']]

    # Group data by state and year and find the sum of Data_Value
    sum_data = df.groupby(['LocationDesc', 'YEAR'])['Data_Value']
    sum_data = sum_data.sum().reset_index()

    # Pivot the table to get one row per state and year
    pivoted_data = pd.pivot_table(sum_data, values='Data_Value',
                                  index='LocationDesc',
                                  columns='YEAR').reset_index()

    # Reset the pivoted_data columns
    pivoted_data.columns = ['LocationDesc',
                            'Data_Value_2011',
                            'Data_Value_2019']

    # Calculate net change in Data_Value between 2011 and 2019
    pivoted_data['net_change'] = pivoted_data['Data_Value_2019']\
        - pivoted_data['Data_Value_2011']

    # Sort the data from highest to lowest, because some data are positive
    # and some are negative, we sort from higest(mostly positive) to lowest
    # (mostly negative)
    pivoted_data = pivoted_data.sort_values('net_change', ascending=False)

    # Get the top 3 states that might have positive net change or smallest
    # negative net change, then put them in dictionary
    lowest_net_change = pivoted_data.head(3)[['LocationDesc', 'net_change']]

    lowest_net_change = lowest_net_change.rename(
        columns={'LocationDesc': 'state'})
    lowest_net_change = lowest_net_change.to_dict('records')

    # Get the top 3 states that might have largest
    # negative net change, then put them in dictionary
    highest_net_change = pivoted_data.tail(3)[['LocationDesc', 'net_change']]
    highest_net_change = highest_net_change.rename(
        columns={'LocationDesc': 'state'})
    highest_net_change = highest_net_change.to_dict('records')

    # Combine 2 dictionaries into 1 and return it
    result = {'lowest_net_change': lowest_net_change,
              'highest_net_change': highest_net_change}
    return result


def extract_state_names(output_dict: dict) -> list:
    """
    This function can extract the state names from the dictionary
    that last function return, and it will return a list of state
    names.
    """
    # Make a empty list
    state_names = []

    # Append the state name extracted from the dictionary to list
    for i in output_dict['lowest_net_change'] +\
            output_dict['highest_net_change']:
        state_names.append(i['state'])
    return state_names


def legis_change(data: pd.DataFrame, state_list: list) -> dict:
    """
    This function will find out if the tital of 6 states
    that with the positive increase or smallest negative
    decrease or largest negative decrease in total net
    change of tobacco use within the year 2011 to 2019,
    experience legislation change within the same time
    range. If they do experience the change, the function
    will return a dictionary that contain the state name
    and the effective date of the new legislation.
    """
    # Process the data to keep the value we are focusing on
    df = data_process.legis_dataFrame(data).copy()
    df = df.loc[df['LocationDesc'].isin(state_list) &
                ((df['ProvisionGroupDesc'] == 'Penalties') |
                 (df['ProvisionGroupDesc'] == 'Restrictions')),
                ['YEAR', 'LocationDesc',
                 'Effective_Date', 'ProvisionGroupDesc',
                 'MeasureDesc', 'ProvisionDesc',
                 'ProvisionValue']]

    # Filter the dataframe to keep the row that with the effective
    # date within the year of 2011 to 2019.
    df['Effective_Date'] = pd.to_datetime(df['Effective_Date'])
    df = df[(df['Effective_Date'].dt.year >= 2011) &
            (df['Effective_Date'].dt.year <= 2019)]
    df = df.dropna(subset=['Effective_Date'])

    # Find out the name of state that has effective date in the
    # range of 2011 to 2019, put them in a dictionary and as the keys
    # then the effective date each state has would be the values for each key
    unique_states = df['LocationDesc'].unique()
    state_dict = {}
    for i in unique_states:
        state_dates = (df[df['LocationDesc'] == i]
                         ['Effective_Date'].unique())
        state_dates_formatted = pd.to_datetime(state_dates)
        state_dict[i] = state_dates_formatted.tolist()
    return state_dict


def state_graph(data: pd.DataFrame, state_dict: dict):
    """
    This function will return the line graph about the
    total smoke rate for each state that experience
    legislation change over years. The y-axis of each
    graph would be the total smoke rate, then the x-axis
    of each graph would be the year.
    """
    # Process the data to keep the value we are focusing on
    df = data_process.rate_dataFrame(data).copy()
    df['YEAR'] = df['YEAR'].astype('int')
    df = df.loc[(df['Race'] == "All Races") &
                (df['Gender'] == 'Overall') &
                (df['LocationDesc'].isin(state_dict.keys())),
                ['YEAR', 'LocationDesc',
                'Data_Value']]

    # Plotting Subplots in a Loop, by print the state name list
    # we could know that there are 4 tstaes that experience
    # legislation change, so we make 4 subplots to show the
    # trend of smoke rate in each state over years
    fig, axs = plt.subplots(2, 2, figsize=(10, 5))
    for i, state in enumerate(df['LocationDesc'].unique()):
        state_data = df.loc[df['LocationDesc'] == state, :]
        state_sum_data = (state_data.groupby(['YEAR'])
                          ['Data_Value'].sum().reset_index())

        row_idx = i // 2
        col_idx = i % 2

        # Chart formatting
        axs[row_idx, col_idx].plot(state_sum_data['YEAR'],
                                   state_sum_data['Data_Value'])
        axs[row_idx, col_idx].set_title(state)
        axs[row_idx, col_idx].set_xlabel('Year')
        axs[row_idx, col_idx].set_ylabel('Data Value Sum')
    plt.tight_layout()

    # save the figure
    fig.savefig('specified_state_rate_change.png')


def main():
    data1 = pd.read_csv('rate_data.csv', low_memory=False, encoding='latin-1')
    data2 = pd.read_csv('legislation.csv')
    net_change(data1)
    print(net_change(data1))
    state_list = extract_state_names(net_change(data1))
    legis_change(data2, state_list)
    print(legis_change(data2, state_list))
    state_dict = legis_change(data2, state_list)
    state_graph(data1, state_dict)


if __name__ == '__main__':
    main()
