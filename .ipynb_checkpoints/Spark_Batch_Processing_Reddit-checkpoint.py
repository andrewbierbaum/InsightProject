#!/usr/bin/env python
# coding: utf-8

# In[1]:

#sparting spark and reading Reddit
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Reddit").getOrCreate()
df = None
df = spark.read.csv("s3a://andrew-bierbaum-insight-test-dataset/Reddit/Reddit_Comments_2018-000000000000.csv.gz", header=True,multiLine=True, escape='"')


# In[2]:


#spark.sql.caseSensitive = False
#sqlContext.sql("set spark.sql.caseSensitive=false")


# In[3]:


#showing the start of the data and format
df.show(5)
df.printSchema()


# In[4]:


#Convert spark data to be readable using sql queries
df.createOrReplaceTempView("Reddit")
# happy_results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body LIKE '%happy%'")
# happy_results.show()


# In[5]:


xamarin_results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body LIKE '%xamarin%'")
flutter_results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body LIKE '%flutter%'")
react_native_results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body LIKE '%react native%'")
#cross_xamarin_flutter_results.show()


# In[6]:


#collect, convert dates to datetime format for later graphing, and sort data
from datetime import datetime
python_xamarin_results = xamarin_results.collect()
python_xamarin_results_cleaned = [(datetime.fromtimestamp(float(i)),body.encode('ascii',errors='ignore')) for i, body in python_xamarin_results]
python_xamarin_results_cleaned.sort()


# In[7]:


#repeat collect, convert dates to datetime format for later graphing, and sort data for flutter results
python_flutter_results = flutter_results.collect()
python_flutter_results_cleaned = [(datetime.fromtimestamp(float(i)),body.encode('ascii',errors='ignore')) for i, body in python_flutter_results]
python_flutter_results_cleaned.sort()


# In[8]:


#repeat collect, convert dates to datetime format for later graphing, and sort data for react native results
python_react_native_results = react_native_results.collect()
python_react_native_results_cleaned = [(datetime.fromtimestamp(float(i)),body.encode('ascii',errors='ignore')) for i, body in python_react_native_results]
python_react_native_results_cleaned.sort()


# In[9]:


#sort, number, and then graph the data
#get_ipython().magic(u'matplotlib inline')
import numpy
import matplotlib
import matplotlib.pyplot as plt
count = numpy.arange(len(python_xamarin_results_cleaned))
#Date_Data = matplotlib.dates.datestr2num(clean_python_results_utc)
Date_Data = []
Body_Data = []
for date, body in python_xamarin_results_cleaned:
    Date_Data.append(date)
    Body_Data.append(body)
matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
matplotlib.pyplot.ylabel('Xamarin Mentions')
matplotlib.pyplot.title('Reddit Xamarin mentions')
#plt.show()
plt.savefig('Reddit_xamarin.png')


# In[10]:


import pandas
pandas_df = pandas.DataFrame({'date':Date_Data,'body':Body_Data})
pandas_df.to_csv("Reddit_xamarin.csv")
pandas_df


# In[11]:


#find flutter posts that already contain xamarin and export to csv
pandas_df[pandas_df['body'].str.contains('flutter')].to_csv('Reddit_xamarin_flutter_cross.csv')


# In[12]:


#repeat graphing and later csv export for flutter
count = numpy.arange(len(python_flutter_results_cleaned))
Date_Data = []
Body_Data = []
for date, body in python_flutter_results_cleaned:
    Date_Data.append(date)
    Body_Data.append(body)
matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
matplotlib.pyplot.ylabel('Flutter Mentions')
matplotlib.pyplot.title('Reddit Flutter mentions')
#plt.show()
plt.savefig('Reddit_flutter.png')

#print csv for flutter
pandas_df = pandas.DataFrame({'date':Date_Data,'body':Body_Data})
pandas_df.head()
pandas_df.to_csv("Reddit_flutter.csv")


# In[13]:


#repeat graphing and later csv export for react native
count = numpy.arange(len(python_react_native_results_cleaned))
Date_Data = []
Body_Data = []
for date, body in python_react_native_results_cleaned:
    Date_Data.append(date)
    Body_Data.append(body)
matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
matplotlib.pyplot.ylabel('React Native Mentions')
matplotlib.pyplot.title('Reddit React Native mentions')
#plt.show()
plt.savefig('Redditreact_native.png')

#print csv for flutter
pandas_df = pandas.DataFrame({'date':Date_Data,'body':Body_Data})
pandas_df.head()
pandas_df.to_csv("Reddit_react_native.csv")


# In[ ]:





# In[ ]:




