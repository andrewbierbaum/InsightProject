import sqlite3
import pandas
# import s3fs

conn = sqlite3.connect('TechGraph.db')
cur = conn.cursor()
conn.text_factory = str

df = pandas.read_csv("/Users/andrewbierbaum/work/InsightProject/reddit_xamarin",compression='gzip')
df = df[['created_utc', 'body', 'subreddit_id', 'link_id', 'parent_id','score', 'id', 'subreddit']]
df.to_sql('Reddit_xamarin', conn, if_exists='replace')
df = None

df = pandas.read_csv("/Users/andrewbierbaum/work/InsightProject/reddit_react_native",compression='gzip')
df = df[['created_utc', 'body', 'subreddit_id', 'link_id', 'parent_id','score', 'id', 'subreddit']]
df.to_sql('Reddit_react_native', conn, if_exists='replace')
df = None

df = pandas.read_csv("/Users/andrewbierbaum/work/InsightProject/reddit_flutter",compression='gzip')
df = df[['created_utc', 'body', 'subreddit_id', 'link_id', 'parent_id','score', 'id', 'subreddit']]
df.to_sql('Reddit_flutter', conn, if_exists='replace')
df = None

# cur.execute("SELECT body FROM Reddit_flutter WHERE body LIKE '%xamarin%&%react native%'")
# cur.fetchall()

conn.commit()
conn.close()
