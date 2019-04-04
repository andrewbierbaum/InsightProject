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

    html.Div(children='''
        comparing the mentions of xamarin and flutter on HackerNews
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': xamarin_Date_Data, 'y': xamarin_count, 'text': xamarin_Body_Data,'type': 'scatter', 'name': 'HackerNews Xamarin Mentions'},
                {'x': flutter_Date_Data, 'y': flutter_count, 'text': flutter_Body_Data,'type': 'scatter', 'name': 'HackerNews Flutter Mentions'},
            ],
            'layout': {
                'title': 'Posts'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port = 9990, host ='0.0.0.0')
