import csv
import sqlite3
import pandas
import sys
import json
import os
import sys
import datetime
import matplotlib
import matplotlib.pyplot as plt

#https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
#REDDIT data
#https://github.com/dewarim/reddit-data-tools
#initialize sqlite and dump reddit data into it
conn = sqlite3.connect('twitter.db')
cur = conn.cursor()
DATASET_COLUMNS = ["target", "ids", "date", "flag", "user", "text"]
cur.execute("CREATE TABLE twitter (target, ids, date, flag, user,text);")

#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
#https://www.kaggle.com/kazanova/sentiment140/version/2
df = pandas.read_csv('TwitterSmall.csv', encoding='ISO-8859-1', names=DATASET_COLUMNS)

#testing to see if loading is working
#print(len(df))
#print(df.head(5))
df.to_sql('twitter', conn, if_exists='replace', index=False)

cur.execute("SELECT date FROM twitter WHERE text LIKE '%c++%'")
times = cur.fetchall()
cleantime = [i[0] for i in times]


#print(cleantime)
DateData = matplotlib.dates.datestr2num(cleantime)
DateData.sort()
#print(DateData)

#count = [i for i in range(0,cleantime)]
count = []
for i in range(len(DateData)):
    count.append(i)


#there is a better way to do this
#maybe come back to for counting data
# DateAndCount = []
# #reverse enumberate that is non-iterable
# count = 0
# for date in DataData
#     DateAndCount = date
# CountAndDate = enumerate(DateData)
# print(CountAndDate)

#plot the data
matplotlib.pyplot.plot_date(DateData,count,xdate=True, drawstyle = 'steps', linestyle = 'solid' )
matplotlib.pyplot.ylabel('Mentions')
matplotlib.pyplot.title('c++ twitter mentions')
plt.show()

#clean up sql
conn.commit()
cur.close
conn.close()