#!/usr/bin/env python
# coding: utf-8

# In[1]:


#sparting spark and reading HackerNews
from pyspark.sql import SparkSession
from datetime import datetime
import pandas
import numpy
import sqlite3

spark = SparkSession.builder.appName("HackerNews").getOrCreate()
df = None
df = spark.read.csv("s3a://andrew-bierbaum-insight-test-dataset/HackerNews/hacker_news_full-000000*.csv.gz", header=True, multiLine=True, escape='"')


# In[ ]:


#Convert spark data to be readable using sql queries
#this could be likely spead up by sending all the keyword rows to pandas once, which is the slow step, then subsearching from there 
df.createOrReplaceTempView("HackerNews")
xamarin_results = spark.sql("SELECT time, text, id, parent FROM HackerNews WHERE text RLIKE 'xamarin|Xamarin' ORDER BY time ASC")
df_xamarin = xamarin_results.toPandas()
df_xamarin = df_xamarin[['time', 'text', 'id', 'parent']]
df_xamarin = df_xamarin.sort_values('time')

flutter_results = spark.sql("SELECT time, text, id, parent FROM HackerNews WHERE text RLIKE 'flutter|Flutter' ORDER BY time ASC")
df_flutter = flutter_results.toPandas()
df_flutter = df_flutter[['time', 'text', 'id', 'parent']]
df_flutter = df_flutter.sort_values('time')

react_native_results = spark.sql("SELECT time, text, id, parent FROM HackerNews WHERE text RLIKE 'react native|React native|React Native' ORDER BY time ASC")
df_react_native = react_native_results.toPandas()
df_react_native = df_react_native[['time', 'text', 'id', 'parent']]
df_react_native = df_react_native.sort_values('time')


# In[ ]:


conn = sqlite3.connect('TechGraph.db')
cur = conn.cursor()
conn.text_factory = str

df_xamarin.to_sql('HackerNews_xamarin', conn, if_exists='replace')
df_flutter.to_sql('HackerNews_flutter', conn, if_exists='replace')
df_react_native.to_sql('HackerNews_react_native', conn, if_exists='replace')

conn.commit()
conn.close()


# In[ ]:




