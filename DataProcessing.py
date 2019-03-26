import csv
import sqlite3
import pandas
import numpy
import sys
import json
import os
import sys
import datetime
import matplotlib
import matplotlib.pyplot as plt

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