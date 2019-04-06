import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
import pandas
from datetime import datetime
import numpy


df = pandas.read_csv("HackerNews_xamarin.csv")
hackernews_xamarin_Date_Data = df['date'].tolist()
hackernews_xamarin_Body_Data = df['body'].tolist()
hackernews_xamarin_count = df['Unnamed: 0'].tolist()
df = None

df = pandas.read_csv("HackerNews_flutter.csv")
hackernews_flutter_Date_Data = df['date'].tolist()
hackernews_flutter_Body_Data = df['body'].tolist()
hackernews_flutter_count = df['Unnamed: 0'].tolist()
df = None

df = pandas.read_csv("HackerNews_react_native.csv")
hackernews_react_native_Date_Data = df['date'].tolist()
hackernews_react_native_Body_Data = df['body'].tolist()
hackernews_react_native_count = df['Unnamed: 0'].tolist()
df = None

df = pandas.read_csv("Reddit_xamarin.csv",header = None)
reddit_xamarin_Date_Data = df[2].tolist()
reddit_xamarin_Body_Data = df[1].tolist()
reddit_xamarin_count = df[0].tolist()
df = None

df = pandas.read_csv("Reddit_flutter.csv",header = None)
reddit_flutter_Date_Data = df[2].tolist()
reddit_flutter_Body_Data = df[1].tolist()
reddit_flutter_count = df[0].tolist()
df = None

# df = pandas.read_csv("Reddit_react_native.csv",header = None)
# reddit_react_native_Date_Data = df[2].tolist()
# reddit_react_native_Body_Data = df[1].tolist()
# reddit_react_native_count = df[0].tolist()
# df = None

# df = pandas.read_csv("HackerNews_xamarin_flutter_cross.csv")
# cross_Date_Data = df['date'].tolist()
# cross_Body_Data = df['body'].tolist()
# cross_count = df['Unnamed: 0'].tolist()
# df = None


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='HackerNews Mentions'),
    html.Div(children='''Comparing the mentions of Xamarin, Flutter, and React Native on HackerNews'''),
    
#    #builds the year range selector
#    dcc.RangeSlider(id='year_slider', min=2008, max=2020, value=[2008, 2020])
                    
    #builds the graph                    
    dcc.Graph(
        id='HackerNews-graph',
        figure={
            'data': [
                {'x': hackernews_xamarin_Date_Data, 'y': hackernews_xamarin_count, 'text': hackernews_xamarin_Body_Data,'type': 'scatter', 'name': 'HackerNews Xamarin Mentions'},
                {'x': hackernews_flutter_Date_Data, 'y': hackernews_flutter_count, 'text': hackernews_flutter_Body_Data,'type': 'scatter', 'name': 'HackerNews Flutter Mentions'},
                {'x': hackernews_react_native_Date_Data, 'y': hackernews_react_native_count, 'text': hackernews_react_native_Body_Data,'type': 'scatter', 'name': 'HackerNews React Native Mentions'},
            ],
            'layout': {
                'title': 'HackerNews Mentions'
            }
        }
    ),
    dcc.Graph(
        id='Reddit-graph',
        figure={
            'data': [
                {'x': reddit_xamarin_Date_Data, 'y': reddit_xamarin_count, 'text': reddit_xamarin_Body_Data,'type': 'scatter', 'name': 'Reddit Xamarin Mentions'},
                {'x': reddit_flutter_Date_Data, 'y': reddit_flutter_count, 'text': reddit_flutter_Body_Data,'type': 'scatter', 'name': 'Reddit Flutter Mentions'},
#                 {'x': reddit_react_native_Date_Data, 'y': reddit_react_native_count, 'text': reddit_react_native_Body_Data,'type': 'scatter', 'name':'Reddit  React Native Mentions'},
            ],
            'layout': {
                'title': 'Reddit Mentions'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port = 9990, host ='0.0.0.0')

    
    
#https://plot.ly/python/time-series/   
    
#https://stackoverflow.com/questions/46519518/how-to-range-slider-and-selector-with-plotly-dash

# import dash_core_components as dcc

# app.layout = html.Div(children=[
#     html.H1('My Dash App'),
#     html.Div(
#         [
#             html.Label('From 2007 to 2017', id='time-range-label'),
#             dcc.RangeSlider(
#                 id='year_slider',
#                 min=1991,
#                 max=2017,
#                 value=[2007, 2017]
#             ),
#         ],
#         style={'margin-top': '20'}
#     ), 
#     html.Hr(),
#     dcc.Graph(id='my-graph')
# ])
# Now you just have to define a callback that gets called every time the value of the RangeSlider changes. This is the Input that causes _update_graph to get called. You could have multiple inputs (e.g. a Dropdown, another RangeSlider, etc).

# The Output is always a single one. In this example it's the figure attribute of the Graph component.

# # the value of RangeSlider causes Graph to update
# @app.callback(
#     output=Output('my-graph', 'figure'),
#     inputs=[Input('year_slider', 'value')]
#     )
# def _update_graph(year_range):
#     date_start = '{}-01-01'.format(year_range[0])
#     date_end = '{}-12-31'.format(year_range[1])
#     # etc...
# A Dash Core Component could cause several components to update. For example, a RangeSlider could cause a Label to change.

# # the value of RangeSlider causes Label to update
# @app.callback(
#     output=Output('time-range-label', 'children'),
#     inputs=[Input('year_slider', 'value')]
#     )
# def _update_time_range_label(year_range):
#     return 'From {} to {}'.format(year_range[0], year_range[1])
