#n[1]:
import matplotlib
matplotlib.use('Agg')

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Reddit").getOrCreate()

#spark = SparkSession.builder.appName("HackerNews").getOrCreate()

df = None
df = spark.read.csv("s3a://andrew-bierbaum-insight-test-dataset/Reddit/Reddit_Comments_2006*.csv.gz", header=True,multiLine=True, escape='"')

#print(df.show(10))


# In[2]:


df.createOrReplaceTempView("Reddit")
#time >1000000000 just filters out 6 bad entries --double chedk this is a good way to do it
results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body LIKE '% python %'")
#results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body LIKE '% python %'  SORT BY created_utc ASC")
#AND time >1000000000
results.show()


# In[ ]:


from datetime import datetime
python_results = results.select('created_utc').collect()
#python_results_timestamp = results.select('timestamp').collect()
clean_python_results = [datetime.fromtimestamp(float(i[0])) for i in python_results]
#print(clean_python_results_timestamp)


# In[ ]:


#get_ipython().magic(u'matplotlib inline')
import numpy
#import matplotlib
import matplotlib.pyplot as plt
clean_python_results.sort()
count = numpy.arange(len(clean_python_results))
#Date_Data = matplotlib.dates.datestr2num(clean_python_results_utc)
Date_Data = clean_python_results
matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
matplotlib.pyplot.ylabel('Mentions')
matplotlib.pyplot.title('Reddit 2018 python mentions')
#plt.show()
plt.savefig('Reddit2006.png')


import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Reddit 2006'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='Reddit 2006 python mentions',
        figure={
            'data': [
                {'x': Date_Data, 'y': count, 'type': 'scatter', 'name': 'SF'}
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port = 9990, host ='0.0.0.0')




