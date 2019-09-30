import sqlite3
import pandas
# import s3fs

conn = sqlite3.connect('TechGraph.db')
cur = conn.cursor()
conn.text_factory = str

df = pandas.read_csv("/Users/andrewbierbaum/work/InsightProject/hackernews_xamarin",compression='gzip')
df = df[['time', 'id', 'text']] # ideally, this would have parent as could be futher processed 
df.to_sql('HackerNews_xamarin', conn, if_exists='replace')
df = None

df = pandas.read_csv("/Users/andrewbierbaum/work/InsightProject/hackernews_react_native",compression='gzip')
df = df[['time', 'id', 'text']]
df.to_sql('HackerNews_react_native', conn, if_exists='replace')
df = None

df = pandas.read_csv("/Users/andrewbierbaum/work/InsightProject/hackernews_flutter",compression='gzip')
df = df[['time', 'id', 'text']]
df.to_sql('HackerNews_flutter', conn, if_exists='replace')
df = None

# cur.execute("SELECT body FROM Reddit_flutter WHERE body LIKE '%xamarin%&%react native%'")
# cur.fetchall()

conn.commit()
conn.close()
