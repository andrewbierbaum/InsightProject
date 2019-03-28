"""
import csv
import sqlite3
import pandas
import numpy
import sys
import json
import os
import datetime
import matplotlib
import matplotlib.pyplot as plt
from pyspark import SparkContext, SparkConf, HiveContext


using sqlite and pandas to process data

#initialize the sql DB
conn = sqlite3.connect('twitter.db')
cur = conn.cursor()
DATASET_COLUMNS = ["target", "ids", "date", "flag", "user", "text"]

#don't rebuild the table if it already exists
cur.execute("SELECT count(*) FROM sqlite_master WHERE type ='table'")
if cur.fetchall()[0] == 0:
    cur.execute("CREATE TABLE twitter (target, ids, date, flag, user,text);")
    #read the csv  
    df = pandas.read_csv('TwitterSmall.csv', encoding='ISO-8859-1', names=DATASET_COLUMNS)
    #load into sql
    df.to_sql('twitter', conn, if_exists='replace', index=False)

#do SQL query and fetch results
cur.execute("SELECT date FROM twitter WHERE text LIKE '%c++%'")
times = cur.fetchall()

#clean data (data,) - has a useless touple & produce a count
cleantime = [i[0] for i in times]
#print(times)
count = numpy.arange(len(cleantime))
#print(count)

#clean up dates and time getting ready for matplotlib
DateData = matplotlib.dates.datestr2num(cleantime)
DateData.sort()

#plot the data
matplotlib.pyplot.plot_date(DateData,count,xdate=True, drawstyle = 'steps', linestyle = 'solid' )
matplotlib.pyplot.ylabel('Mentions')
matplotlib.pyplot.title('c++ twitter mentions')
plt.savefig('TwitterC.png')

#clean up sql
conn.commit()
cur.close
conn.close()

#getting it working with pyspark
conf = SparkConf().setAppName('test').setMaster('local[]')
sc = SparkContext(conf=conf)
shake = sc.textFile("TwitterSmall.csv")
acc = sc.accumulator(0)
def myFunc(s):
    words = s.split(" ")
    return len(words)
a = shake.map(myFunc).foreach(lambda x: acc.add(x))

print(a)

file = sc.textFile("TwitterSmall.csv")
counts = file.flatMap(lambda line: line.split(" "))\
           .map(lambda word: (word, 1))\
           .reduceByKey(lambda a, b: a + b)
res = counts.collect()
for val in res:
    print(val)
"""

import csv
import os
import sys
import datetime
import sqlite3
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
#from pyspark import SparkContext, SparkConf, HiveContext
from pyspark.sql import SparkSession


#from pyspark.conf import SparkConf
#SparkSession.builder.config(conf=SparkConf())


#spark = SparkSession.builder.master("local").appName("Word Count").config("spark.some.config.option", "some-value").getOrCreate()

spark = SparkSession.builder.appName('HackerNews').getOrCreate()
#df=spark.read.option("header", "True").csv('hacker_news_full-000000000000.csv.gz')
#df=spark.read.csv('hacker_news_full-000000000000.csv.gz',header=True, sep='\t')
df = spark.read.csv('hacker_news_full-000000000000.csv.gz', header=True)

#You can read from multiple files by feeding in a list of files:
#fpath1 = "file1.csv.gz"
#fpath2 = "file2.csv.gz"
#DF = spark.read.csv([fpath1, fpath2] header=True)

#You can also create a "temporary view" allowing for SQL queries:
#fpath1 = "file1.csv.gz"
#fpath2 = "file2.csv.gz"
#DF = spark.read.csv([fpath1, fpath2] header=True)
#DF.createOrReplaceTempView("table_name")
#DFres = spark.sql("SELECT * FROM table_name)


#read a ton of files from s3...
#rdd = sc.textFile("s3://bucket/project1/20141201/logtype1/logtype1.*.gz")
df.head(10)
df.show()
df.printSchema()
#this can be changed with I think .options(schema=sometihng) - see udemy section 8 #24 @ 9:40 python/spark jose
Df.columns
df.createOrReplaceTempView("HackerNews")
results = spark.sql("SELECT time, text FROM HackerNews WHERE text LIKE '% python %' SORT BY time ASC LIMIT 100")
results.show()
