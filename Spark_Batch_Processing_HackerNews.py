

#sparting spark and reading Reddit
from pyspark.sql import SparkSession
from pyspark.sql.types import (StructField,StringType,IntegerType,StructType,FloatType,DateType,TimestampType)

#"DataType", "NullType", "StringType", "BinaryType", "BooleanType", "DateType","TimestampType", "DecimalType", "DoubleType", "FloatType", "ByteType", "IntegerType","LongType", "ShortType", "ArrayType", "MapType", "StructField", "StructType"]
#data_schema = [StructField('time', FloatType(),True), StructField('text', StringType(),True), StructField('id', IntegerType(),True)]
#final_schema = StructType(data_schema)

spark = SparkSession.builder.appName("Reddit").getOrCreate()
df = None
df = spark.read.csv("s3a://andrew-bierbaum-insight-test-dataset/HackerNews/hacker_news_full-0000000*.csv.gz", header=True,multiLine=True, escape='"')


# In[2]:


#showing the start of the data and format
#df.show(5)
#df.printSchema()


# In[3]:


#Convert spark data to be readable using sql queries
df.createOrReplaceTempView("HackerNews")
xamarin_results = spark.sql("SELECT time, id, text FROM HackerNews WHERE text RLIKE 'xamarin|Xamarin'")
flutter_results = spark.sql("SELECT time, id, text FROM HackerNews WHERE text RLIKE 'flutter|Flutter'")
react_native_results = spark.sql("SELECT time, id, text FROM HackerNews WHERE text RLIKE 'react native|React native'")


# In[ ]:


#collect, convert dates to datetime format for later graphing, and sort data
#this logic should be moved to spark schema for faster processing!
from datetime import datetime
python_xamarin_results = xamarin_results.collect()
python_xamarin_results_cleaned = [(datetime.fromtimestamp(float(time)),int(id),body.encode('ascii',errors='ignore')) for time,id, body in python_xamarin_results]
python_xamarin_results_cleaned.sort()


# In[ ]:


#repeat collect, convert dates to datetime format for later graphing, and sort data for flutter results
python_flutter_results = flutter_results.collect()
python_flutter_results_cleaned = [(datetime.fromtimestamp(float(time)),int(id),body.encode('ascii',errors='ignore')) for time,id, body in python_flutter_results]
python_flutter_results_cleaned.sort()


# In[ ]:


#repeat collect, convert dates to datetime format for later graphing, and sort data for react native results
python_react_native_results = react_native_results.collect()
python_react_native_results_cleaned = [(datetime.fromtimestamp(float(time)),int(id),body.encode('ascii',errors='ignore')) for time,id, body in python_react_native_results]
python_react_native_results_cleaned.sort()


# In[ ]:


#sort, number, and then graph the data
#get_ipython().magic(u'matplotlib inline')
import numpy
import matplotlib
import matplotlib.pyplot as plt
count = numpy.arange(len(python_xamarin_results_cleaned))
#Date_Data = matplotlib.dates.datestr2num(clean_python_results_utc)
Date_Data = []
Body_Data = []
Id_Data = []
for date, id, body in python_xamarin_results_cleaned:
    Date_Data.append(date)
    Id_Data.append(id)
    Body_Data.append(body)
#matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
#matplotlib.pyplot.ylabel('Xamarin Mentions')
#matplotlib.pyplot.title('HackerNews Xamarin mentions')
#plt.show()
#plt.savefig('HackerNews_xamarin.png')


# In[ ]:


import pandas
pandas_df = pandas.DataFrame({'date':Date_Data,'id':Id_Data,'body':Body_Data})
pandas_df.to_csv("HackerNews_xamarin.csv")
pandas_df


# In[ ]:


#find flutter posts that already contain xamarin and export to csv
pandas_df[pandas_df['body'].str.contains('flutter')].to_csv('HackerNews_xamarin_flutter_cross.csv')


# In[ ]:


#repeat graphing and later csv export for flutter
count = numpy.arange(len(python_flutter_results_cleaned))
Date_Data = []
Body_Data = []
Id_Data = []
for date, id, body in python_flutter_results_cleaned:
    Date_Data.append(date)
    Id_Data.append(id)
    Body_Data.append(body)
#matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
#matplotlib.pyplot.ylabel('Flutter Mentions')
#matplotlib.pyplot.title('HackerNews Flutter mentions')
#plt.show()
#plt.savefig('HackerNews_flutter.png')

#print csv for flutter
pandas_df = pandas.DataFrame({'date':Date_Data,'id':Id_Data,'body':Body_Data})
pandas_df.head()
pandas_df.to_csv("HackerNews_flutter.csv")


# In[ ]:


#repeat graphing and later csv export for react native
count = numpy.arange(len(python_react_native_results_cleaned))
Date_Data = []
Body_Data = []
Id_Data = []
for date, id, body in python_react_native_results_cleaned:
    Date_Data.append(date)
    Id_Data.append(id)
    Body_Data.append(body)
#matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
#matplotlib.pyplot.ylabel('React Native Mentions')
#matplotlib.pyplot.title('HackerNews React Native mentions')
#plt.show()
#plt.savefig('HackerNews_react_native.png')

#print csv for flutter
pandas_df = pandas.DataFrame({'date':Date_Data,'id':Id_Data,'body':Body_Data})
pandas_df.head()
pandas_df.to_csv("HackerNews_react_native.csv")


# In[ ]:


# #building dash graph
# import dash
# import dash_core_components as dcc
# import dash_html_components as html

# df = pandas.read_csv("HackerNews_xamarin.csv")
# xamarin_Date_Data = df['date'].tolist()
# xamarin_Body_Data = df['body'].tolist()
# xamarin_count = df['Unnamed: 0'].tolist()
# df = None

# df = pandas.read_csv("HackerNews_flutter.csv")
# flutter_Date_Data = df['date'].tolist()
# flutter_Body_Data = df['body'].tolist()
# flutter_count = df['Unnamed: 0'].tolist()
# df = None

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app.layout = html.Div(children=[
#     html.H1(children='HackerNews Mentions'),
#     html.Div(children='''Comparing the mentions of Xamarin and Flutter on HackerNews'''),
    
#     #builds the year range selector
#     dcc.RangeSlider(id='year_slider', min=2008, max=2020, value=[2008, 2020]),
                    
#     #builds the graph                    
#     dcc.Graph(
#         id='HackerNews-graph',
#         figure={
#             'data': [
#                 {'x': xamarin_Date_Data, 'y': xamarin_count, 'text': xamarin_Body_Data,'type': 'scatter', 'name': 'HackerNews Xamarin Mentions'},
#                 {'x': flutter_Date_Data, 'y': flutter_count, 'text': flutter_Body_Data,'type': 'scatter', 'name': 'HackerNews Flutter Mentions'},
#             ],
#             'layout': {
#                 'title': 'Mentions'
#             }
#         }
#     )
# ])


# In[ ]:





