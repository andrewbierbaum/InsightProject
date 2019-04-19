import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_table
import csv
import pandas
from datetime import datetime
import numpy
import sqlite3
import html.parser as HP
import textwrap 
import urllib
import json
from pandas.io.json import json_normalize

#open the sql to get the data
conn = sqlite3.connect('TechGraph.db')
cur = conn.cursor()


#take in HackerNews Data
df = pandas.read_sql("SELECT * FROM HackerNews_xamarin", conn)
hackernews_xamarin_Date_Data = [datetime.fromtimestamp(float(time)) for time in df['time']]
hackernews_xamarin_Id_Data = df['id'].tolist()
hackernews_xamarin_Body_Data = df['text'].tolist()
hackernews_xamarin_count = numpy.arange(len(hackernews_xamarin_Id_Data))
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
reddit_xamarin_link_Id_Data = df['link_id'].tolist()
reddit_xamarin_Id_Data = df['id'].tolist()
reddit_xamarin_Body_Data = df['body'].tolist()
reddit_xamarin_count = numpy.arange(len(reddit_xamarin_Id_Data))
df = None

df = pandas.read_sql("SELECT * FROM Reddit_react_native",conn)
reddit_react_native_Date_Data = [datetime.fromtimestamp(float(time)) for time in df['created_utc']]
reddit_react_native_link_Id_Data = df['link_id'].tolist()
reddit_react_native_Id_Data = df['id'].tolist()
reddit_react_native_Body_Data = df['body'].tolist()
reddit_react_native_count = numpy.arange(len(reddit_react_native_Id_Data))
df = None

df = pandas.read_sql("SELECT * FROM Reddit_flutter", conn)
reddit_flutter_Date_Data = [datetime.fromtimestamp(float(time)) for time in df['created_utc']]
reddit_flutter_link_Id_Data = df['link_id'].tolist()
reddit_flutter_Id_Data = df['id'].tolist()
reddit_flutter_Body_Data = df['body'].tolist()
reddit_flutter_count = numpy.arange(len(reddit_flutter_Id_Data))
df = None


#sql query for top crossposts
df_xamarin_cross_posts = pandas.read_sql("SELECT xamarin_table.link_id, xamarin_table.link_id_count as total_link_id_count FROM (SELECT Reddit_flutter.link_id, count(*) as link_id_count FROM Reddit_flutter GROUP BY Reddit_flutter.link_id) as flutter_table JOIN (SELECT Reddit_xamarin.link_id, count(*) as link_id_count FROM Reddit_xamarin GROUP BY Reddit_xamarin.link_id) as xamarin_table ON flutter_table.link_id = xamarin_table.link_id JOIN (SELECT Reddit_react_native.link_id, count(*) as link_id_count FROM Reddit_react_native GROUP BY Reddit_react_native.link_id) as react_native_table ON flutter_table.link_id = react_native_table.link_id ORDER BY total_link_id_count DESC LIMIT 25",conn)

#get the webapi ready
s = ','
idlist = s.join(df_xamarin_cross_posts['link_id'])
str(idlist)

#find and tabulate all the api data
cross_posts_url = "https://api.pushshift.io/reddit/search/submission/?ids={}".format(idlist)
cross_posts_file = urllib.request.urlopen(cross_posts_url)
cross_posts_data = cross_posts_file.read()
cross_posts_data_json = json.loads(cross_posts_data)
if cross_posts_data_json['data']:
    df_cross_posts_update = json_normalize(cross_posts_data_json['data'])
    df_cross_posts_update = df_cross_posts_update[['full_link','title']]
    df_xamarin_cross_posts_full = pandas.concat([df_xamarin_cross_posts, df_cross_posts_update], axis=1)

df_react_native_cross_posts = pandas.read_sql("SELECT react_native_table.link_id, react_native_table.link_id_count as total_link_id_count FROM (SELECT Reddit_flutter.link_id, count(*) as link_id_count FROM Reddit_flutter GROUP BY Reddit_flutter.link_id) as flutter_table JOIN (SELECT Reddit_xamarin.link_id, count(*) as link_id_count FROM Reddit_xamarin GROUP BY Reddit_xamarin.link_id) as xamarin_table ON flutter_table.link_id = xamarin_table.link_id JOIN (SELECT Reddit_react_native.link_id, count(*) as link_id_count FROM Reddit_react_native GROUP BY Reddit_react_native.link_id) as react_native_table ON flutter_table.link_id = react_native_table.link_id ORDER BY total_link_id_count DESC LIMIT 25",conn)

#get the webapi ready
s = ','
idlist = s.join(df_react_native_cross_posts['link_id'])
str(idlist)

#find and tabulate all the api data
cross_posts_url = "https://api.pushshift.io/reddit/search/submission/?ids={}".format(idlist)
cross_posts_file = urllib.request.urlopen(cross_posts_url)
cross_posts_data = cross_posts_file.read()
cross_posts_data_json = json.loads(cross_posts_data)
if cross_posts_data_json['data']:
    df_cross_posts_update = json_normalize(cross_posts_data_json['data'])
    df_cross_posts_update = df_cross_posts_update[['full_link','title']]
    df_react_native_cross_posts_full = pandas.concat([df_react_native_cross_posts, df_cross_posts_update], axis=1)

df_flutter_cross_posts = pandas.read_sql("SELECT flutter_table.link_id, flutter_table.link_id_count as total_link_id_count FROM (SELECT Reddit_flutter.link_id, count(*) as link_id_count FROM Reddit_flutter GROUP BY Reddit_flutter.link_id) as flutter_table JOIN (SELECT Reddit_xamarin.link_id, count(*) as link_id_count FROM Reddit_xamarin GROUP BY Reddit_xamarin.link_id) as xamarin_table ON flutter_table.link_id = xamarin_table.link_id JOIN (SELECT Reddit_react_native.link_id, count(*) as link_id_count FROM Reddit_react_native GROUP BY Reddit_react_native.link_id) as react_native_table ON flutter_table.link_id = react_native_table.link_id ORDER BY total_link_id_count DESC LIMIT 25",conn)

#get the webapi ready
s = ','
idlist = s.join(df_flutter_cross_posts['link_id'])
str(idlist)

#find and tabulate all the api data
cross_posts_url = "https://api.pushshift.io/reddit/search/submission/?ids={}".format(idlist)
cross_posts_file = urllib.request.urlopen(cross_posts_url)
cross_posts_data = cross_posts_file.read()
cross_posts_data_json = json.loads(cross_posts_data)
if cross_posts_data_json['data']:
    df_cross_posts_update = json_normalize(cross_posts_data_json['data'])
    df_cross_posts_update = df_cross_posts_update[['full_link','title']]
    df_flutter_cross_posts_full = pandas.concat([df_flutter_cross_posts, df_cross_posts_update], axis=1)



#close the SQL 
conn.close()

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#setting up dash
external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True

#the main graph program, which simply links to the tabs below when selected
app.layout = html.Div([
    html.H1('TechGraph: www.AndrewBierbaum.com',style={'text-align': 'center'}),
    dcc.Tabs(id="tabs-navigation", value='momentum-graph', children=[
        dcc.Tab(label='Momentum Graph', value='momentum-graph'),
        dcc.Tab(label='Reddit Cross Posts', value='reddit-cross-posts'),
#         dcc.Tab(label='Topic Search', value='topic-search'),
    ]),
    html.Div(id='tech-graph-tabs')
])




#These are the main and secondary pages in tab 1 and 2
@app.callback(Output('tech-graph-tabs', 'children'),
              [Input('tabs-navigation', 'value')])
def render_content(tab):
    if tab == 'momentum-graph':
        return html.Div(id='dark-theme-feature',children=[
            html.H2(children='Technology Mentions on HackerNews and Reddit',style={'text-align': 'center'}),
#	html.Div(children ='user data',id='text-context'),
            html.Div(children='''Hover and Click to Display User Comments''',style={'text-align': 'center','font-size': 22}),
            html.Br(),
            html.Div([
            #builds the HackerNews graph                    
                dcc.Graph(
                    id='HackerNews-graph', 
                    animate = True,
                    figure={
                    'data': [
                    {'x': hackernews_xamarin_Date_Data, 'y': hackernews_xamarin_count, 'type': 'scatter', 'name': 'Xamarin'},
                    {'x': hackernews_react_native_Date_Data, 'y': hackernews_react_native_count,  'type': 'scatter', 'name': 'React Native'}, 
                    {'x': hackernews_flutter_Date_Data, 'y': hackernews_flutter_count, 'type': 'scatter', 'name': 'Flutter'},
                    ],
                    'layout': {
                    'hovermode': 'closest',
                    'legend': {'orientation':'h','x':0,'y':-0.1},
                    'title': 'HackerNews'
                    }
                    }
                )], style={'width': '50%', 'display': 'inline-block'}), 
            #builds the 2nd graph for reddit below
            html.Div([
                dcc.Graph(
                    id='Reddit-graph',
                    animate=True,
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
                )], style={'width': '50%', 'display': 'inline-block'}),
  

            
#these are the click and mouseover 
            #dcc.Textarea(placeholder='Click data to Select',value='This is a TextArea component',style={'width': '100%'})
            #html.Div(dcc.Textarea(placeholder='Click data to Select',value='This is a TextArea component',id='HackerNews-text',style={'width': '50%'})),
            
            html.H4(children ='Hover over data to quick view',id='HackerNews-hover-text',style={'width': '49%','display':'inline-block','vertical-align': 'top','height':'175px','overflow': 'hidden','border':'groove', 'border-radius': '5px','margin-top': '5px','margin-bottom':'5px'}),
            html.H4(children ='Hover over data to quick view',id='Reddit-hover-text',style={'width': '49%','display':'inline-block','vertical-align': 'top','height':'175px','overflow': 'hidden','border':'groove', 'border-radius': '5px','margin-top': '5px','margin-bottom':'5px'}),
            html.H4(children ='Click data to Select',id='HackerNews-text',style={'width': '49%','display':'inline-block','vertical-align': 'top','height':'200px','overflow-y': 'scroll','border':'groove', 'border-radius': '5px','margin-top': '5px','margin-bottom':'5px'}),
            html.H4(children ='Click data to Select',id='Reddit-text',style={'width': '49%','display':'inline-block','vertical-align': 'top','height':'200px','overflow-y': 'scroll','border':'groove', 'border-radius': '5px','margin-top': '5px','margin-bottom':'5px'}),
    ])

    #building the crossposts tab
    elif tab == 'reddit-cross-posts':
        return html.Div(
            [
            html.H2(children='Top Xamarin Posts Discussing all Three Technologies',style={'text-align': 'center'}),
            dash_table.DataTable(
                    style_data={'whiteSpace': 'normal'},
                    css=[{'selector': '.dash-cell div.dash-cell-value', 'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                id='table',
                columns=[{'name':"mentions", 'id':'total_link_id_count'},{'name':"Title", 'id':'title'},{'name':'url','id':'full_link'}],
                data=df_xamarin_cross_posts_full.to_dict("rows"),
            ),
            html.Br(),
            html.H2(children='Top React Native Posts Discussing all Three Technologies',style={'text-align': 'center'}),
            dash_table.DataTable(
                    style_data={'whiteSpace': 'normal'},
                    css=[{'selector': '.dash-cell div.dash-cell-value', 'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                id='table',
                columns=[{'name':"mentions", 'id':'total_link_id_count'},{'name':"Title", 'id':'title'},{'name':'url','id':'full_link'}],
                data=df_react_native_cross_posts_full.to_dict("rows"),
            ),
            html.Br(),
            html.H2(children='Top Flutter Posts Discussing all Three Technologies',style={'text-align': 'center'}),
            dash_table.DataTable(
                    style_data={'whiteSpace': 'normal'},
                    css=[{'selector': '.dash-cell div.dash-cell-value', 'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                id='table',
                columns=[{'name':"mentions", 'id':'total_link_id_count'},{'name':"Title", 'id':'title'},{'name':'url','id':'full_link'}],
                data=df_flutter_cross_posts_full.to_dict("rows"),
            )]            
        )
#     elif tab == 'topic-search':
#         return html.Div([
#             html.Div(dcc.Input(id='input-box-1', type='text')),
#             html.Div(dcc.Input(id='input-box-2', type='text')),
#             html.Div(dcc.Input(id='input-box-3', type='text')),
#             html.Button('Submit', id='button'),
#             html.Div(id='container-button-basic', children='Enter a value and press submit')
# ])

#server = app.server # the Flask app, doing "gunicorn app:server -b :80" to get the app to port 80

#below is the logic for mousing over the graphs
@app.callback(
    dash.dependencies.Output('HackerNews-hover-text', 'children'),
    [dash.dependencies.Input('HackerNews-graph', 'hoverData')])
def update_text(hoverData):
    if hoverData['points'][0]['curveNumber']==0:
        return HP.HTMLParser().unescape(hackernews_xamarin_Body_Data[hoverData['points'][0]['pointIndex']])
    if hoverData['points'][0]['curveNumber']==1:
        return HP.HTMLParser().unescape(hackernews_react_native_Body_Data[hoverData['points'][0]['pointIndex']])
    if hoverData['points'][0]['curveNumber']==2:
        return HP.HTMLParser().unescape(hackernews_flutter_Body_Data[hoverData['points'][0]['pointIndex']])

@app.callback(
    dash.dependencies.Output('Reddit-hover-text', 'children'),
    [dash.dependencies.Input('Reddit-graph', 'hoverData')])
def update_text(hoverData):
    if hoverData['points'][0]['curveNumber']==0:
        return HP.HTMLParser().unescape(reddit_xamarin_Body_Data[hoverData['points'][0]['pointIndex']])
    if hoverData['points'][0]['curveNumber']==1:
        return HP.HTMLParser().unescape(reddit_react_native_Body_Data[hoverData['points'][0]['pointIndex']])
    if hoverData['points'][0]['curveNumber']==2:
        return HP.HTMLParser().unescape(reddit_flutter_Body_Data[hoverData['points'][0]['pointIndex']])
  

#below is the logic for clicking on the graphs
@app.callback(
     dash.dependencies.Output('HackerNews-text', 'children'),
     [dash.dependencies.Input('HackerNews-graph', 'clickData')])
def update_text(clickData):
    if clickData['points'][0]['curveNumber']==0:
        return html.Div([
            html.A("Direct link to HackerNews user comment", href="https://news.ycombinator.com/item?id="+str(hackernews_xamarin_Id_Data[clickData['points'][0]['pointIndex']]),target="_blank"),
            html.H3(HP.HTMLParser().unescape(hackernews_xamarin_Body_Data[clickData['points'][0]['pointIndex']]))
        ])
    if clickData['points'][0]['curveNumber']==1:
        return html.Div([
            html.A("Direct link to HackerNews user comment", href="https://news.ycombinator.com/item?id="+str(hackernews_react_native_Id_Data[clickData['points'][0]['pointIndex']]),target="_blank"),
            html.H3(HP.HTMLParser().unescape(hackernews_react_native_Body_Data[clickData['points'][0]['pointIndex']]))
        ])
    if clickData['points'][0]['curveNumber']==2:
        return html.Div([
            html.A("Direct link to HackerNews user comment", href="https://news.ycombinator.com/item?id="+str(hackernews_flutter_Id_Data[clickData['points'][0]['pointIndex']]),target="_blank"),
            html.H3(HP.HTMLParser().unescape(hackernews_flutter_Body_Data[clickData['points'][0]['pointIndex']]))
        ])

@app.callback(
     dash.dependencies.Output('Reddit-text', 'children'),
     [dash.dependencies.Input('Reddit-graph', 'clickData')])
def update_text(clickData):
    if clickData['points'][0]['curveNumber']==0:
        return html.Div([
            html.A("Direct link to Reddit user comment", href="https://new.reddit.com/comments/"+str(reddit_xamarin_link_Id_Data[clickData['points'][0]['pointIndex']]).replace("t3_","")+ "/_/" + str(reddit_xamarin_Id_Data[clickData['points'][0]['pointIndex']]),target="_blank"),
            html.H3(HP.HTMLParser().unescape(reddit_xamarin_Body_Data[clickData['points'][0]['pointIndex']]))  
        ])
    if clickData['points'][0]['curveNumber']==1:
        return html.Div([
            html.A("Direct link to Reddit user comment", href="https://new.reddit.com/comments/"+str(reddit_react_native_link_Id_Data[clickData['points'][0]['pointIndex']]).replace("t3_","")+ "/_/" + str(reddit_react_native_Id_Data[clickData['points'][0]['pointIndex']]),target="_blank"),
            html.H3(HP.HTMLParser().unescape(reddit_react_native_Body_Data[clickData['points'][0]['pointIndex']]))  
        ])
    if clickData['points'][0]['curveNumber']==2:
        return html.Div([
            html.A("Direct link to Reddit user comment", href="https://new.reddit.com/comments/"+str(reddit_flutter_link_Id_Data[clickData['points'][0]['pointIndex']]).replace("t3_","")+ "/_/" + str(reddit_flutter_Id_Data[clickData['points'][0]['pointIndex']]),target="_blank"),
            html.H3(HP.HTMLParser().unescape(reddit_flutter_Body_Data[clickData['points'][0]['pointIndex']]))  
        ])   
   


# @app.callback(
#     dash.dependencies.Output('container-button-basic', 'children'),
#     [dash.dependencies.Input('button', 'n_clicks')],[dash.dependencies.State('input-box-1', 'value'),dash.dependencies.State('input-box-2', 'value'),dash.dependencies.State('input-box-3', 'value')])
# def update_output(n_clicks,value1,value2,value3):
  
    
#     return 'You are searching for {}'.format(searches)



#port 80 was forwarded to 9990 with "sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 9990"

#this is the actual server call
if __name__ == '__main__':
    app.run_server(debug=True, port =9990, host ='0.0.0.0')
    
