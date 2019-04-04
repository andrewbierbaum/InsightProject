import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
import pandas
from datetime import datetime
import numpy

df = pandas.read_csv("HackerNews_xamarin.csv")
xamarin_Date_Data = df['date'].tolist()
xamarin_Body_Data = df['body'].tolist()
xamarin_count = df['Unnamed: 0'].tolist()
df = None

df = pandas.read_csv("HackerNews_flutter.csv")
flutter_Date_Data = df['date'].tolist()
flutter_Body_Data = df['body'].tolist()
flutter_count = df['Unnamed: 0'].tolist()
df = None


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='HackerNews Mentions'),
    html.Div(children='''Comparing the mentions of Xamarin and Flutter on HackerNews'''),
    
#    #builds the year range selector
#    dcc.RangeSlider(id='year_slider', min=2008, max=2020, value=[2008, 2020])
                    
    #builds the graph                    
    dcc.Graph(
        id='HackerNews-graph',
        figure={
            'data': [
                {'x': xamarin_Date_Data, 'y': xamarin_count, 'text': xamarin_Body_Data,'type': 'scatter', 'name': 'HackerNews Xamarin Mentions'},
                {'x': flutter_Date_Data, 'y': flutter_count, 'text': flutter_Body_Data,'type': 'scatter', 'name': 'HackerNews Flutter Mentions'},
            ],
            'layout': {
                'title': 'Mentions'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port = 9990, host ='0.0.0.0')
    
    
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