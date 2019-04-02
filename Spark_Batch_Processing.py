#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib
matplotlib.use('Agg')

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("HackerNews").getOrCreate()

#spark = SparkSession.builder.appName("HackerNews").getOrCreate()

df = None
df = spark.read.csv("s3a://andrew-bierbaum-insight-test-dataset/HackerNews/hacker_news_full-00000000*.csv.gz", header=True)
print(df.show(10))


# In[3]:


df.createOrReplaceTempView("HackerNews")
#time >1000000000 just filters out 6 bad entries --double chedk this is a good way to do it
results = spark.sql("SELECT time, timestamp, text FROM HackerNews WHERE text LIKE '% python %' AND time >1000000000 SORT BY time ASC")
results.show()


# In[4]:


python_results = results.select('time').collect()
python_results_timestamp = results.select('timestamp').collect()
clean_python_results_timestamp = [i[0] for i in python_results_timestamp]
#print(clean_python_results_timestamp)


# In[9]:


#get_ipython().magic(u'matplotlib inline')
import numpy
import matplotlib
import matplotlib.pyplot as plt
count = numpy.arange(len(clean_python_results_timestamp))
Date_Data = matplotlib.dates.datestr2num(clean_python_results_timestamp)
matplotlib.pyplot.plot_date(Date_Data,count,xdate=True, drawstyle = 'steps-pre', linestyle = 'solid' )
matplotlib.pyplot.ylabel('Mentions')
matplotlib.pyplot.title('HackerNews python mentions')
plt.show()
plt.savefig('HackerNews.png')


# In[ ]:


