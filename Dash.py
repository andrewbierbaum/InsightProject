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
df_cross_posts = pandas.read_sql("SELECT Reddit_flutter.link_id, count(*) as link_id_count FROM Reddit_flutter JOIN Reddit_xamarin ON Reddit_flutter.link_id = Reddit_xamarin.link_id JOIN Reddit_react_native ON Reddit_xamarin.link_id = Reddit_react_native.link_id GROUP BY Reddit_flutter.link_id ORDER BY link_id_count DESC LIMIT 25", conn)

#distinc

# #sql query for top crossposts
# df_cross_posts = pandas.read_sql("SELECT Reddit_flutter.link_id, count(*) as link_id_count FROM Reddit_flutter JOIN Reddit_xamarin ON Reddit_flutter.link_id = Reddit_xamarin.link_id JOIN Reddit_react_native ON Reddit_xamarin.link_id = Reddit_react_native.link_id GROUP BY Reddit_flutter.link_id ORDER BY link_id_count DESC LIMIT 25", conn)


#get the webapi ready
s = ','
idlist = s.join(df_cross_posts['link_id'])
str(idlist)

#find and tabulate all the api data
cross_posts_url = "https://api.pushshift.io/reddit/search/submission/?ids={}".format(idlist)
cross_posts_file = urllib.request.urlopen(cross_posts_url)
cross_posts_data = cross_posts_file.read()
cross_posts_data_json = json.loads(cross_posts_data)
if cross_posts_data_json['data']:
    df_cross_posts_update = json_normalize(cross_posts_data_json['data'])
    df_cross_posts_update = df_cross_posts_update[['full_link','title']]
    df_cross_posts_full = pandas.concat([df_cross_posts, df_cross_posts_update], axis=1)
    
#close the SQL 
conn.close()



#setting up dash
external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True

#the main graph program, which simply links to the tabs below when selected
app.layout = html.Div([
    html.H1('TechGraph: www.AndrewBierbaum.com',style={'text-align': 'center'}),
    dcc.Tabs(id="tabs-navigation", value='momentum-graph', children=[
        dcc.Tab(label='Momentum Graph', value='momentum-graph'),
        #dcc.Tab(label='Weekly interest', value='weekly-interest'), inplement if there is more time
        dcc.Tab(label='Reddit Cross Posts', value='reddit-cross-posts'),
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
            html.H2(children='Top Posts Discussing all Three Technologies',style={'text-align': 'center'}),
            dash_table.DataTable(
                    style_data={'whiteSpace': 'normal'},
                    css=[{'selector': '.dash-cell div.dash-cell-value', 'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                id='table',
                columns=[{'name':"mentions", 'id':'link_id_count'},{'name':"Title", 'id':'title'},{'name':'url','id':'full_link'}],
                data=df_cross_posts_full.to_dict("rows"),
            )]
        )


#server = app.server # the Flask app, doing "gunicorn app:server -b :80" to get the app to port 80

#below is the logic for mousing over the graphs
@app.callback(
    dash.dependencies.Output('HackerNews-hover-text', 'children'),
    [dash.dependencies.Input('HackerNews-graph', 'hoverData')])
def update_text(hoverData):
    if hoverData['points'][0]['curveNumber']==0:
        return HP.HTMLParser.HTMLParser().unescape(hackernews_xamarin_Body_Data[hoverData['points'][0]['pointIndex']])
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
   

#server = app.server # the Flask app, doing "gunicorn app:server -b :80" to get the app to port 80

#this is the actual server call
if __name__ == '__main__':
    app.run_server(debug=True, port =9990, host ='0.0.0.0')
    
    
    
    # theme = {
#     'dark': False,
#     'detail': '#007439',
#     'primary': '#00EA64', 
#     'secondary': '#6E6E6E'
# }

# theme =  {
#     'dark': True,
#     'detail': '#007439',
#     'primary': '#00EA64',
#     'secondary': '#6E6E6E',
# }


# rootLayout = html.Div([
#     daq.BooleanSwitch(
#         on=True,
#         id='darktheme-daq-booleanswitch',
#         className='dark-theme-control'
#     ), html.Br(),
#     daq.ToggleSwitch(
#         id='darktheme-daq-toggleswitch',
#         className='dark-theme-control'
#     ), html.Br(),
# ])
   
    
#    #builds the year range selector
#    dcc.RangeSlider(id='year_slider', min=2008, max=2020, value=[2008, 2020])
#    May 16, 2011
    
#      daq.ToggleSwitch(
#         id='toggle-theme',
#         label=['Light', 'Dark'],
#         value=True
#     ),
    
#     daq.ToggleSwitch(
#         id='daq-light-dark-theme',
#         label=['Light', 'Dark'],
#         style={'width': '250px', 'margin': 'auto'}, 
#         value=False
#     ),

#     daq.DarkThemeProvider([
#   html.Link(
#     href="https://codepen.io/anon/pen/BYEPbO.css",
#     rel="stylesheet"
#   ),
#   html.Div([
#     html.Div([
#       html.H2('Controls'),
#       dark_controls
#     ], style={ 'width': '80%' })
#   ],
#   style={
#     'width': '100%',
#     'display': 'flex',
#     'flexDirection': 'column',
#     'alignItems': 'center',
#     'justifyContent': 'center'
#   })
# ]),
    
    
    
    
    
    
# crossposts = html.Div([
#      html.Div([
#         dcc.Link('Overview       ', href='/dash-techgraph-report/overview', className="tab first"),
#         dcc.Link('crossposts', href='/dash-techgraph-report/crossposts', className="tab"),
#     ], className="row "),
    
#     html.H1(children='Top Crossposts HackerNews and Reddit',style={'text-align': 'center'})
# ])


# overview = html.Div(id='dark-theme-feature',children=[
#     html.H1(children='Technology Mentions on HackerNews and Reddit',style={'text-align': 'center'}),
# #	html.Div(children ='user data',id='text-context'),
#     html.Div(children='''Hover and click data to display the user comment''',style={'text-align': 'center','font-size': 24}),
#     html.Br(),
    
#     html.Div([
#         dcc.Link('Overview', href='/dash-techgraph-report/overview', className="tab first"),
#         dcc.Link('crossposts', href='/dash-techgraph-report/crossposts', className="tab"),
#     ], className="row "),
# #    builds the graph                    
#      html.Div([
# #    builds the graph                    
#         dcc.Graph(
#             id='HackerNews-graph',
#             figure={
#                 'data': [
#                 {'x': hackernews_xamarin_Date_Data, 'y': hackernews_xamarin_count, 'type': 'scatter', 'name': 'Xamarin'},
#                 {'x': hackernews_react_native_Date_Data, 'y': hackernews_react_native_count,  'type': 'scatter', 'name': 'React Native'}, 
#                 {'x': hackernews_flutter_Date_Data, 'y': hackernews_flutter_count, 'type': 'scatter', 'name': 'Flutter'},
#             ],
#         'layout': {
#         #'clickmode': 'event+select',
# 	    'hovermode': 'closest',
#         'legend': {'orientation':'h','x':0,'y':-0.1},
#         'title': 'HackerNews'
#             }
#         }
#     )],
#     style={'width': '50%', 'display': 'inline-block'}),
    
    
    
#      html.Div([
#         dcc.Graph(
#             id='Reddit-graph',
#             figure={
#                 'data': [
#                 {'x': reddit_xamarin_Date_Data, 'y': reddit_xamarin_count, 'type': 'scatter', 'name': 'Xamarin'},
#                 {'x': reddit_react_native_Date_Data, 'y': reddit_react_native_count,  'type': 'scatter', 'name':'React Native'}, 
#                 {'x': reddit_flutter_Date_Data, 'y': reddit_flutter_count, 'type': 'scatter', 'name': 'Flutter'},
#             ],
#             'layout': {
# 	        #'clickmode': 'event+select',
# 	        'hovermode': 'closest',
#             #'xaxis': {'range':[]}
#             'legend': {'orientation':'h','x':0,'y':-0.1},
#             'title': 'Reddit'
#             }
#         }
#     )],
#     style={'width': '50%', 'display': 'inline-block'}),
    
#     html.H4(children ='Click data to Select',id='HackerNews-text',style={'width': '49%','display':'inline-block','vertical-align': 'top','height':'175px','overflow-y': 'scroll'}),
#     html.H4(children ='Click data to Select',id='Reddit-text',style={'width': '49%','display':'inline-block','vertical-align': 'top','height':'175px','overflow-y': 'scroll'}),
#     html.H4(children ='Hover over data to quick view',id='HackerNews-hover-text',style={'width': '49%','display':'inline-block','vertical-align': 'top','height':'175px','overflow': 'hidden'}),
#     html.H4(children ='Hover over data to quick view',id='Reddit-hover-text',style={'width': '49%','display':'inline-block','vertical-align': 'top','height':'175px','overflow': 'hidden'}),
# ]),


# noPage = html.Div([  # 404
#     html.P(["404 Page not found"])
#     ], className="no-page")


# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content'),
    
#     #I think I have to repeat these as empty to not have the callbacks be mad at me
#     html.Div(children ='',id='HackerNews-text',style={'width': '49%','display':'inline-block','vertical-align': 'top' }),
#     html.Div(children ='',id='Reddit-text',style={'width': '49%','display':'inline-block','vertical-align': 'top'}),
#     html.Div(children ='',id='HackerNews-hover-text',style={'width': '49%','display':'inline-block','vertical-align': 'top' }),
#     html.Div(children ='',id='Reddit-hover-text',style={'width': '49%','display':'inline-block','vertical-align': 'top'}),
# ])


# @app.callback(dash.dependencies.Output('page-content', 'children'),
#               [dash.dependencies.Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/dash-techgraph-report' or pathname == '/dash-techgraph-report/overview':
#         return overview
#     elif pathname == '/dash-techgraph-report/crossposts':
#         return crossposts
#     else:
#         return noPage
    
###Dark theme work!
# @app.callback(
#     [Output('dark-theme-feature','style'),
#     Output('HackerNews-graph','style'),
#     Output('Reddit-graph','style')],
#     [Input('toggle-theme', 'value')]
# )
# def change_bg(dark_theme):
#     if(dark_theme):
#         return {'background-color': '#303030', 'color': 'white'}, {'plot_bgcolor': '#111111', 'paper_bgcolor': '#111111', 'font':'#7FDBFF'}, {'plot_bgcolor': '#111111', 'paper_bgcolor': '#111111', 'font':'#7FDBFF'}
#     else:
#         return {'background-color': 'white', 'color': 'black'}, {'plot_bgcolor': 'white', 'paper_bgcolor': 'black', 'font':'black'}, {'plot_bgcolor': 'white', 'paper_bgcolor': 'black', 'font':'black'}
    
                    
# @app.callback(
    
# #    Output('Reddit-graph','style')],
#     [Input('daq-light-dark-theme', 'value')]
# )
# def change_bg(dark_theme):
#     if(dark_theme):
#         return {'plot_bgcolor': '#111111', 'paper_bgcolor': '#111111', 'font':'#7FDBFF'}
#     else:
#         return {'plot_bgcolor': 'white', 'paper_bgcolor': 'black', 'font':'black'}

    
    
# 'layout': {
#                 'plot_bgcolor': colors['background'],
#                 'paper_bgcolor': colors['background'],
#                 'font': {
#                     'color': colors['text']
    
#     colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
                    

#link_id     then    id
#https://new.reddit.com/comments/hct9b/_/c1ufen4    
    


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


