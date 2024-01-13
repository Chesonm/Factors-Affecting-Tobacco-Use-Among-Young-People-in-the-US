"""
Guicheng Ma & Yuqing Li
CSE 163 Final Project
Title: Factors Affecting Tobacco Use Among Young People in the US.
This program will build a interactable plot that could show how the smoke rate
of states in the US changes these years.
"""
import pandas as pd

import data_process

from pyecharts import options as opts
from pyecharts.charts import Timeline, Map
from pyecharts.globals import ThemeType
from pyecharts.datasets import register_url
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Insert the map of the US json file.
register_url("https://echarts-maps.github.io/echarts-countries-js/")


def rate_file(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate the data we have to get the overall rate of people smoke(except
    E_cigarate) of states in the US.
    Return the aggregated data.
    """
    df['YEAR'] = df['YEAR'].astype('int')
    df = df.loc[(df['Race'] == "All Races") &
                (df['Gender'] == 'Overall')]
    df_aggr = df.groupby(['YEAR', 'LocationDesc'])['Data_Value'].sum()
    return df_aggr


def timeline_map(df: pd.DataFrame) -> Timeline:
    """
    Build a timeline plot that could represent the cigeratte using rate from
    2011 to 2019 of states in the US.
    Visualize the plot we build in rate_map.html file
    """
    tl = Timeline(init_opts=opts.InitOpts(page_title="Tobacco Use of 18-24",
                                          theme=ThemeType.CHALK,
                                          width="1000px", height="620px"))
    df = df.reset_index()
    df['YEAR'] = df['YEAR'].astype('int')
    for idx in range(0, 9):
        year = 2011 + idx
        states = list(df[df['YEAR'] == year]['LocationDesc'])
        percentage = list(df[df['YEAR'] == year]['Data_Value'])
        zipped = zip(states, percentage)
        f_map = (
            Map(init_opts=opts.InitOpts(width="900px",
                                        height="500px",
                                        page_title="Tobacco Use Rate of 18-24",
                                        bg_color=None))
            .add(series_name="Tobacco Use Percentage",
                             data_pair=[list(z) for z in zipped],
                             maptype="美国",
                             is_map_symbol_show=False)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Tobacco Use Rate of 18-24 in\
                    United States",
                                          pos_left="center"),
                legend_opts=opts.LegendOpts(is_show=True, pos_top="40px",
                                            pos_right="30px"),
                visualmap_opts=opts.VisualMapOpts(
                    is_piecewise=True, range_text=['high', 'low'], pieces=[
                        {"min": 30, "color": "#751d0d"},
                        {"min": 25, "max": 29.99, "color": "#ae2a23"},
                        {"min": 20, "max": 24.99, "color": "#d6564c"},
                        {"min": 15, "max": 19.99, "color": "#f19178"},
                        {"min": 10, "max": 14.99, "color": "#f7d3a6"},
                        {"min": 5, "max": 9.99, "color": "#fdf2d3"},
                        {"min": 0, "max": 4.99, "color": "#FFFFFF"}
                    ])
            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True),
                             markpoint_opts=opts.MarkPointOpts(
                                 symbol_size=[90, 90], symbol='circle'),
                             effect_opts=opts.EffectOpts(is_show='True'))
        )
        tl.add(f_map, "{}".format(idx + 2011))
        tl.add_schema(is_timeline_show=True,
                      play_interval=800,
                      symbol=None,
                      is_loop_play=True
                      )
    tl.render('rate_map.html')


def main():
    data1 = pd.read_csv('rate_data.csv', low_memory=False, encoding='latin-1')
    df_aggr = rate_file(data_process.rate_dataFrame(data1))
    timeline_map(df_aggr)


if __name__ == '__main__':
    main()
