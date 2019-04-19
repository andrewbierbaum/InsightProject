#!/usr/bin/env python
# coding: utf-8

# In[6]:


#sparting spark and reading HackerNews
from pyspark.sql import SparkSession
from datetime import datetime
import pandas
import numpy
import sqlite3


# In[ ]:


#set up spark 
spark = SparkSession.builder.appName("HackerNews").getOrCreate()
df = None
df = spark.read.csv("s3a://andrew-bierbaum-insight-test-dataset/HackerNews/hacker_news_full-000000*.csv.gz", header=True, multiLine=True, escape='"')


# In[ ]:


#Convert spark data to be readable using sql queries

df.createOrReplaceTempView("HackerNews")

#these could be combined into one search to only have to access the table once and be much faster, but they work as written
#query the spark data, transfer to pandas, and confirm the sorting
xamarin_results = spark.sql("SELECT time, text, id, parent,  FROM HackerNews WHERE text RLIKE 'xamarin|Xamarin' ORDER BY time ASC")
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


# In[12]:


#setup sqlite
conn = sqlite3.connect('TechGraph.db')
cur = conn.cursor()
conn.text_factory = str


# In[ ]:


#transfter data to sqlite
df_xamarin.to_sql('HackerNews_xamarin', conn, if_exists='replace')
df_flutter.to_sql('HackerNews_flutter', conn, if_exists='replace')
df_react_native.to_sql('HackerNews_react_native', conn, if_exists='replace')


# In[13]:


#get rid of flutter comments before flutter was posted to github
cur.execute("DELETE FROM HackerNews_flutter WHERE time<1305578972")


# In[14]:


conn.commit()
conn.close()


# In[ ]:




