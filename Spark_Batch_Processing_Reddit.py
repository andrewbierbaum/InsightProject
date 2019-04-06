#!/usr/bin/env python
# coding: utf-8

# In[1]:


#sparting spark and reading Reddit
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Reddit").getOrCreate()
df = None
df = spark.read.csv("s3a://andrew-bierbaum-insight-test-dataset/Reddit_Fix/Reddit_Comments_2014*.csv.gz", header=True,multiLine=True, escape='"')


# In[2]:


#spark.sql.caseSensitive = False
#sqlContext.sql("set spark.sql.caseSensitive=false")


# In[3]:


#showing the start of the data and format
#df.show(5)
#df.printSchema()


# In[4]:


#this logic takes datetime data in the format "2018-06-14 16:00:51 UTC" and makes it useful
#from pyspark.sql.functions import to_timestamp
#df = df.withColumn("created_utc", to_timestamp("created_utc", "yyyy-MM-dd HH:mm:ss z")) #time format is = "2018-06-14 16:00:51 UTC"
#df.printSchema()


# In[5]:


# #Convert spark data to be readable using sql queries
df.createOrReplaceTempView("Reddit")
# happy_results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body RLIKE 'finesse|Finesse'")
# happy_results.show()
# Happy_results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body LIKE '%Finesse%'")
# Happy_results.show()


# In[6]:


xamarin_results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body RLIKE 'xamarin|Xamarin'")
flutter_results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body RLIKE 'flutter|Flutter'")
react_native_results = spark.sql("SELECT created_utc, body FROM Reddit WHERE body RLIKE 'react native|React native'")


# In[7]:


#flutter_results.show()


# In[8]:


#repeat collect, convert dates to datetime format for later graphing, and sort data for flutter results
from datetime import datetime
python_flutter_results = flutter_results.collect()
python_flutter_results_cleaned = [(datetime.fromtimestamp(float(date)),body.encode('ascii',errors='ignore')) for date, body in python_flutter_results]
python_flutter_results_cleaned.sort()


# In[9]:


#collect, convert dates to datetime format for later graphing, and sort data
from datetime import datetime
python_xamarin_results = xamarin_results.collect()
python_xamarin_results_cleaned = [(datetime.fromtimestamp(float(date)), body.encode('ascii',errors='ignore')) for date, body in python_xamarin_results]
python_xamarin_results_cleaned.sort()


# In[10]:


#repeat collect, convert dates to datetime format for later graphing, and sort data for react native results
python_react_native_results = react_native_results.collect()
python_react_native_results_cleaned = [(datetime.fromtimestamp(float(date)),body.encode('ascii',errors='ignore')) for date, body in python_react_native_results]
python_react_native_results_cleaned.sort()


# In[11]:


#sort, number, and then graph the data
#get_ipython().magic(u'matplotlib inline')
import numpy
import matplotlib
import matplotlib.pyplot as plt
import pandas


# In[12]:


#repeat graphing and later csv export for flutter
count = numpy.arange(len(python_flutter_results_cleaned))
Date_Data = []
Body_Data = []
for date, body in python_flutter_results_cleaned:
    Date_Data.append(date)
    Body_Data.append(body)
# matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
# matplotlib.pyplot.ylabel('Flutter Mentions')
# matplotlib.pyplot.title('Reddit Flutter mentions')
# plt.show()
# plt.savefig('Reddit_flutter.png')

#print csv for flutter

pandas_df = pandas.DataFrame({'date':Date_Data,'body':Body_Data})
with open('Reddit_flutter.csv', 'a') as f:
    pandas_df.to_csv(f, header=False)


# In[13]:


count = numpy.arange(len(python_xamarin_results_cleaned))
#Date_Data = matplotlib.dates.datestr2num(clean_python_results_utc)
Date_Data = []
Body_Data = []
for date, body in python_xamarin_results_cleaned:
    Date_Data.append(date)
    Body_Data.append(body)
# matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
# matplotlib.pyplot.ylabel('Xamarin Mentions')
# matplotlib.pyplot.title('Reddit Xamarin mentions')
# plt.show()
# plt.savefig('Reddit_xamarin.png')

pandas_df = pandas.DataFrame({'date':Date_Data,'body':Body_Data})
with open('Reddit_xamarin.csv', 'a') as f:
    pandas_df.to_csv(f, header=False)


# In[14]:


#repeat graphing and later csv export for react native
count = numpy.arange(len(python_react_native_results_cleaned))
Date_Data = []
Body_Data = []
for date, body in python_react_native_results_cleaned:
    Date_Data.append(date)
    Body_Data.append(body)
# matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
# matplotlib.pyplot.ylabel('React Native Mentions')
# matplotlib.pyplot.title('Reddit React Native mentions')
# plt.show()
# plt.savefig('Reddit_react_native.png')

#print csv for flutter
pandas_df = pandas.DataFrame({'date':Date_Data,'body':Body_Data})
with open('Reddit_react_native.csv', 'a') as f:
    pandas_df.to_csv(f, header=False)


