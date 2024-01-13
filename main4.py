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


def get_trend(data: pd.DataFrame):
    """
    This function want to find out the percentage change of each kind of
    tobacco use in the United States over years. It will return a line
    graph that contain three lines, each will represent one kind of tobacco.
    """
    # Process the data to keep the value we are focusing on
    df = data_process.rate_dataFrame(data).copy()
    df['YEAR'] = df['YEAR'].astype('int')
    df = df.loc[(df['Race'] == "All Races") &
                (df['Gender'] == 'Overall'),
                ['YEAR', 'LocationDesc',
                'Data_Value', 'TopicDesc']]

    # Sum up the percentage of each kind of tobacco in each year
    # because in 2018, the dataset only 32 states have E-Cigarette Use (Adults)
    # data, so when we calcualte the average percentage, we divide the total
    # by 32 for the year 2018.
    sum_data = df.groupby(['TopicDesc', 'YEAR'])['Data_Value'].sum()
    sum_data = sum_data.reset_index()
    sum_data['Data_Value'] = sum_data.apply(
                        lambda x: x['Data_Value'] / 32
                        if (x['YEAR'] == 2018
                            and x['TopicDesc']
                            == 'E-Cigarette Use (Adults)')
                        else x['Data_Value'] / 52, axis=1)

    # Plot the line graph
    fig, ax = plt.subplots()
    for t in sum_data['TopicDesc'].unique():
        topic_data = sum_data[sum_data['TopicDesc'] == t]
        ax.plot(topic_data['YEAR'], topic_data['Data_Value'], label=t)

    # Add labels and legend to the graph
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage')
    ax.set_title('Trends in Different Type of Tobacco Use')
    ax.legend()

    # save the figure
    fig.savefig('tobacco_use_trends.png')


def main():
    data1 = pd.read_csv('rate_data.csv', low_memory=False, encoding='latin-1')
    get_trend(data1)


if __name__ == '__main__':
    main()
