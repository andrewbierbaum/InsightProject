import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
import pandas
from datetime import datetime

df = pandas.read_csv("dash.csv")
timestamps = df['timestamp'].tolist()
count = df['Unnamed: 0'].tolist()
datetimes = [datetime.fromtimestamp(i) for i in timestamps]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': datetimes, 'y': count, 'type': 'scatter', 'name': 'SF'}
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port = 9990, host ='0.0.0.0')
