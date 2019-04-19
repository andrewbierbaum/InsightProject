#!/usr/bin/env python
# coding: utf-8

# In[1]:


#sparting spark and reading Reddit
from pyspark.sql import SparkSession
from datetime import datetime
import pandas
import numpy
import sqlite3


# In[ ]:


#set up spark
spark = SparkSession.builder.appName("Reddit").getOrCreate()
df = None
df = spark.read.csv("s3a://andrew-bierbaum-insight-test-dataset/Reddit_Fix/Reddit_Comments_20*.csv.gz", header=True,multiLine=True, escape='"')


# In[2]:


# #Convert spark data to be readable using sql queries and query for the keyword terms
df.createOrReplaceTempView("Reddit")

#these could be combined into one search to only have to access the table once and be much faster, but they work as written
#query the spark data, transfer to pandas, and confirm the sorting
xamarin_results = spark.sql("SELECT created_utc, body, subreddit_id, link_id, parent_id, id, subreddit FROM Reddit WHERE body RLIKE 'xamarin|Xamarin' ORDER BY created_utc ASC")
df_xamarin = xamarin_results.toPandas()
df_xamarin = df_xamarin.sort_values('created_utc')

#repeat for flutter
flutter_results = spark.sql("SELECT created_utc, body, subreddit_id, link_id, parent_id, id, subreddit FROM Reddit WHERE body RLIKE 'flutter|Flutter' ORDER BY created_utc ASC")
df_flutter = flutter_results.toPandas()
df_flutter = df_flutter.sort_values('created_utc')

#repeat for react native
react_native_results = spark.sql("SELECT created_utc, body, subreddit_id, link_id, parent_id, id, subreddit FROM Reddit WHERE body RLIKE 'react native|React native|React Native' ORDER BY created_utc ASC")
df_react_native = react_native_results.toPandas()
df_react_native = df_react_native.sort_values('created_utc')


# In[2]:


#setup sqlite
conn = sqlite3.connect('TechGraph.db')
cur = conn.cursor()
conn.text_factory = str


# In[3]:


#transfer to sqlite
df_xamarin.to_sql('Reddit_xamarin', conn, if_exists='replace')
df_flutter.to_sql('Reddit_flutter', conn, if_exists='replace')
df_react_native.to_sql('Reddit_react_native', conn, if_exists='replace')


# In[3]:


#get rid of flutter comments before flutter was posted to github
conn.execute("DELETE FROM Reddit_flutter WHERE created_utc<1305578972")

#delete subreddits not whitelisted
conn.execute("DELETE FROM Reddit_flutter WHERE subreddit NOT IN ('FlutterDev','androiddev','programming','Android','techsupport','dartlang','technology','reactnative','Flutter','ProgrammerHumor','xamarindevelopers','Xamarin')")
conn.execute("DELETE FROM Reddit_flutter WHERE subreddit NOT IN ('csparp','learnprogramming','dotnet','windowsphone','gamedev','cscareerquestions','Unity3d','apple','linux','webdev','appdev','fsharp')")
conn.execute("DELETE FROM Reddit_flutter WHERE subreddit NOT IN ('reactjs','javascript','iOSProgramming','startups','Entrepreneur','swift','vuejs','AskProgramming','Clojure','AskReddit','learnjavascript','web_design','golang','forhire')")


# In[4]:


conn.commit()
conn.close()


# In[ ]:




