import csv
import sqlite3
import pandas
import sys
import json
import os
import sys

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
print(len(df))
print(df.head(5))
df.to_sql('twitter', conn, if_exists='replace', index=False)

cur.execute("SELECT text FROM twitter WHERE text LIKE '%cry%' LIMIT 10")
print(cur.fetchall())

conn.commit()
cur.close
conn.close()
print('done')