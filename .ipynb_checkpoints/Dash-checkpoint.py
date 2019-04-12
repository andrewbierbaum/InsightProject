import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
import pandas
from datetime import datetime
import numpy
import sqlite3
import HTMLParser
import textwrap 

conn = sqlite3.connect('TechGraph.db')
cur = conn.cursor()

df = pandas.read_sql("SELECT * FROM HackerNews_xamarin", conn)
hackernews_xamarin_Date_Data = [datetime.fromtimestamp(float(time)) for time in df['time']]
hackernews_xamarin_Id_Data = df['id'].tolist()
hackernews_xamarin_Body_Data = df['text'].tolist()
hackernews_xamarin_count = numpy.arange(len(hackernews_xamarin_Id_Data))

#hackernews_xamarin_Date_Data = [datetime.fromtimestamp(float(time)) for time in df['time']]
#hackernews_xamarin['time'] = pandas.to_datetime(df_hackernews_xamarin['time'],unit = 's')
#hackernews_xamarin_Id_Data = df['id'].tolist()
#hackernews_xamarin_Body_Data = df['text'].tolist()
#hackernews_xamarin_count = numpy.arange(len(hackernews_xamarin_Id_Data))
df = None

df = pandas.read_sql("SELECT * FROM HackerNews_react_native", conn)
hackernews_react_native_Date_Data = [datetime.fromtimestamp(float(time)) for time in df['time']]
hackernews_react_native_Id_Data = df['id'].tolist()
hackernews_react_native_Body_Data = df['text'].tolist()
hackernews_react_native_count = numpy.arange(len(hackernews_react_native_Id_Data))
df = None


df = pandas.read_sql("SELECT * FROM HackerNews_flutter", conn)
hackernews_flutter_Date_Data = [datetime.fromtimestamp(float(time)) for time in df['time']]
hackernews_flutter_Id_Data = df['id'].tolist()
hackernews_flutter_Body_Data = df['text'].tolist()
hackernews_flutter_count = numpy.arange(len(hackernews_flutter_Id_Data))
df = None

#take in reddit data
df = pandas.read_sql("SELECT * FROM Reddit_xamarin", conn)
reddit_xamarin_Date_Data = [datetime.fromtimestamp(float(time)) for time in df['created_utc']]
reddit_xamarin_Id_Data = df['id'].tolist()
reddit_xamarin_Body_Data = df['body'].tolist()
reddit_xamarin_count = numpy.arange(len(reddit_xamarin_Id_Data))
df = None

df = pandas.read_sql("SELECT * FROM Reddit_react_native",conn)
reddit_react_native_Date_Data = [datetime.fromtimestamp(float(time)) for time in df['created_utc']]
reddit_react_native_Id_Data = df['id'].tolist()
reddit_react_native_Body_Data = df['body'].tolist()
reddit_react_native_count = numpy.arange(len(reddit_react_native_Id_Data))
df = None

df = pandas.read_sql("SELECT * FROM Reddit_flutter", conn)
reddit_flutter_Date_Data = [datetime.fromtimestamp(float(time)) for time in df['created_utc']]
reddit_flutter_Id_Data = df['id'].tolist()
reddit_flutter_Body_Data = df['body'].tolist()
reddit_flutter_count = numpy.arange(len(reddit_flutter_Id_Data))
df = None

#close the SQL 
conn.close()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1(children='Technology Mentions on HackerNews and Reddit',style={'text-align': 'center'}),
#	html.Div(children ='user data',id='text-context'),
    html.Div(children='''Hover and click data to display the user comment''',style={'text-align': 'center','font-size': 24}),
#    #builds the year range selector
#    dcc.RangeSlider(id='year_slider', min=2008, max=2020, value=[2008, 2020])
# May 16, 2011
    
    html.Div([
#    builds the graph                    
        dcc.Graph(
            id='HackerNews-graph',
            figure={
                'data': [
                {'x': hackernews_xamarin_Date_Data, 'y': hackernews_xamarin_count, 'type': 'scatter', 'name': 'Xamarin'}, #'text': hackernews_xamarin_Body_Data  ,
                {'x': hackernews_react_native_Date_Data, 'y': hackernews_react_native_count,  'type': 'scatter', 'name': 'React Native'}, #'text': hackernews_react_native_Body_Data,
                {'x': hackernews_flutter_Date_Data, 'y': hackernews_flutter_count, 'type': 'scatter', 'name': 'Flutter'},#'text': hackernews_flutter_Body_Data,
            ],
        'layout': {
        #'clickmode': 'event+select',
	    'hovermode': 'closest',
        'legend': {'orientation':'h','x':0,'y':-0.1},
        'title': 'HackerNews'
            }
        }
    )],
    style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(
            id='Reddit-graph',
            figure={
                'data': [
                {'x': reddit_xamarin_Date_Data, 'y': reddit_xamarin_count, 'type': 'scatter', 'name': 'Xamarin'},
                {'x': reddit_react_native_Date_Data, 'y': reddit_react_native_count,  'type': 'scatter', 'name':'React Native'}, 
                {'x': reddit_flutter_Date_Data, 'y': reddit_flutter_count, 'type': 'scatter', 'name': 'Flutter'},
            ],
            'layout': {
	        #'clickmode': 'event+select',
	        'hovermode': 'closest',
            #'xaxis': {'range':[]}
            'legend': {'orientation':'h','x':0,'y':-0.1},
            'title': 'Reddit'
            }
        }
    )],
    style={'width': '50%', 'display': 'inline-block'}),
    html.Div(children ='Click data to Select',id='HackerNews-text',style={'width': '49%','display':'inline-block','vertical-align': 'top' }),
    html.Div(children ='Click data to Select',id='Reddit-text',style={'width': '49%','display':'inline-block','vertical-align': 'top'}),
    html.Div(children ='Hover over data to quick view',id='HackerNews-hover-text',style={'width': '49%','display':'inline-block','vertical-align': 'top' }),
    html.Div(children ='Hover over data to quick view',id='Reddit-hover-text',style={'width': '49%','display':'inline-block','vertical-align': 'top'}),
])



@app.callback(
    dash.dependencies.Output('HackerNews-hover-text', 'children'),
    [dash.dependencies.Input('HackerNews-graph', 'hoverData')])
def update_text(hoverData):
    if hoverData['points'][0]['curveNumber']==0:
        return HTMLParser.HTMLParser().unescape(hackernews_xamarin_Body_Data[hoverData['points'][0]['pointIndex']])
    if hoverData['points'][0]['curveNumber']==1:
        return HTMLParser.HTMLParser().unescape(hackernews_react_native_Body_Data[hoverData['points'][0]['pointIndex']])
    if hoverData['points'][0]['curveNumber']==2:
        return HTMLParser.HTMLParser().unescape(hackernews_flutter_Body_Data[hoverData['points'][0]['pointIndex']])

@app.callback(
    dash.dependencies.Output('Reddit-hover-text', 'children'),
    [dash.dependencies.Input('Reddit-graph', 'hoverData')])
def update_text(hoverData):
    if hoverData['points'][0]['curveNumber']==0:
        return HTMLParser.HTMLParser().unescape(reddit_xamarin_Body_Data[hoverData['points'][0]['pointIndex']])
    if hoverData['points'][0]['curveNumber']==1:
        return HTMLParser.HTMLParser().unescape(reddit_react_native_Body_Data[hoverData['points'][0]['pointIndex']])
    if hoverData['points'][0]['curveNumber']==2:
        return HTMLParser.HTMLParser().unescape(reddit_flutter_Body_Data[hoverData['points'][0]['pointIndex']])
  

@app.callback(
     dash.dependencies.Output('HackerNews-text', 'children'),
     [dash.dependencies.Input('HackerNews-graph', 'clickData')])
def update_text(clickData):
    if clickData['points'][0]['curveNumber']==0:
        return HTMLParser.HTMLParser().unescape(hackernews_xamarin_Body_Data[clickData['points'][0]['pointIndex']])
    if clickData['points'][0]['curveNumber']==1:
        return HTMLParser.HTMLParser().unescape(hackernews_react_native_Body_Data[clickData['points'][0]['pointIndex']])
    if clickData['points'][0]['curveNumber']==2:
        return HTMLParser.HTMLParser().unescape(hackernews_flutter_Body_Data[clickData['points'][0]['pointIndex']])

@app.callback(
     dash.dependencies.Output('Reddit-text', 'children'),
     [dash.dependencies.Input('Reddit-graph', 'clickData')])
def update_text(clickData):
    if clickData['points'][0]['curveNumber']==0:
        return HTMLParser.HTMLParser().unescape(reddit_xamarin_Body_Data[clickData['points'][0]['pointIndex']])
    if clickData['points'][0]['curveNumber']==1:
        return HTMLParser.HTMLParser().unescape(reddit_react_native_Body_Data[clickData['points'][0]['pointIndex']])
    if clickData['points'][0]['curveNumber']==2:
        return HTMLParser.HTMLParser().unescape(reddit_flutter_Body_Data[clickData['points'][0]['pointIndex']])    
    
    
# @app.callback(
#     dash.dependencies.Output('Reddit-hover-text', 'children'),
#     [dash.dependencies.Input('Reddit-graph', 'hoverData')])
# def update_text(hoverData):
#     return HTMLParser.HTMLParser().unescape(hoverData['points'][0]['text'])






# @app.callback(
#     dash.dependencies.Output('Reddit-text', 'children'),
#     [dash.dependencies.Input('Reddit-graph', 'clickData')])
# def update_text(clickData):
#     return HTMLParser.HTMLParser().unescape(clickData['points'][0]['text'])


#@app.callback(
#    dash.dependencies.Output('HackerNews-text', 'children'),
#    [dash.dependencies.Input('HackerNews-graph', 'hoverData')])
#def update_text(hoverData):
#    return html.H3(hoverData)
#clickData['points'][0]    return html.H3(HTMLParser.HTMLParser().unescape(string))
#    return html.H3(df_hackernews_xamarin['text'][clickData['points'][0]['pointIndex']])
#u'curveNumber': 0, u'pointNumber': 2081, u'pointIndex': 2081


#@app.callback(
#    dash.dependencies.Output('Reddit-text', 'children'),
#    [dash.dependencies.Input('Reddit-graph', 'clickData')])
#def update_text(clickData):	
#    return html.H3(clickData['points'][0])

if __name__ == '__main__':
    app.run_server(debug=True, port = 9990, host ='0.0.0.0')

