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
df.createOrReplaceTempView("HackerNews")
xamarin_results = spark.sql("SELECT time, text, id FROM HackerNews WHERE text RLIKE 'xamarin|Xamarin' ORDER BY time ASC")
df_xamarin = xamarin_results.toPandas()
df_xamarin.sort_values('time')

flutter_results = spark.sql("SELECT time, text, id FROM HackerNews WHERE text RLIKE 'flutter|Flutter' ORDER BY time ASC")
df_flutter = flutter_results.toPandas()
df_flutter.sort_values('time')

react_native_results = spark.sql("SELECT time, text, id FROM HackerNews WHERE text RLIKE 'react native|React native|React Native' ORDER BY time ASC")
df_react_native = react_native_results.toPandas()
df_react_native.sort_values('time')


# In[ ]:


conn = sqlite3.connect('TechGraph.db')
cur = conn.cursor()
conn.text_factory = str

df_xamarin.to_sql('HackerNews_xamarin.db', conn, if_exists='replace')
df_flutter.to_sql('HackerNews_flutter.db', conn, if_exists='replace')
df_react_native.to_sql('HackerNews_react_native.db', conn, if_exists='replace')

conn.commit()
conn.close()


# In[ ]:




