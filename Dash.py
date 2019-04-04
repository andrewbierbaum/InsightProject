import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
import pandas
from datetime import datetime
import numpy

df = pandas.read_csv("dash.csv")
Date_Data = df['date'].tolist()
Body_Data = df['body'].tolist()
count = df['Unnamed: 0'].tolist()

#i think I already did this and Its not needed
#datetimes = [datetime.fromtimestamp(i) for i in timestamps]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Reddit Mentions'),

    html.Div(children='''
        Tracking the number of mentions microsoft got on Reddit
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': Date_Data, 'y': count, 'text': Body_Data,'type': 'scatter', 'name': 'Reddit Microsoft Mentions'}
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port = 9990, host ='0.0.0.0')
