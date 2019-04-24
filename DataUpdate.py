cccimport requests
import json
from datetime import datetime
import sqlite3
import pandas
from pandas.io.json import json_normalize
#set up sql connection to get ready to write the data
conn = sqlite3.connect('TechGraph.db')
cur = conn.cursor()
conn.text_factory = str

#find the time of the last entry
cur.execute("SELECT max(time) FROM HackerNews_xamarin")
last_timestamp = cur.fetchall()[0][0]

#retreave, process, and store new data in sqlite
xamarin_url = "https://hn.algolia.com/api/v1/search?query=xamarin&numericFilters=created_at_i>{}&hitsPerPage=1000&tags=comment".format(last_timestamp)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
xamarin_file = requests.get(xamarin_url,headers=headers)
xamarin_data = xamarin_file.content
xamarin_data_json = json.loads(xamarin_data)
if xamarin_data_json['nbHits']>0:
    df = json_normalize(xamarin_data_json['hits'])
    df = df.rename(index=str, columns={"created_at_i":"time", "comment_text":"text", "story_id":"id", "parent_id":"parent"})
    df = df[['time', 'text', 'id', 'parent']]
    df = df.sort_values('time')
    df.to_sql("HackerNews_xamarin",conn, if_exists='append', index = False) 
df = None


#repeat for HackerNews react native
cur.execute("SELECT max(time) FROM HackerNews_react_native")
last_timestamp = cur.fetchall()[0][0]
react_native_url = "https://hn.algolia.com/api/v1/search?query=react%20native&numericFilters=created_at_i>{}&hitsPerPage=1000&tags=comment".format(last_timestamp)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
react_native_file = requests.get(react_native_url,headers=headers)
react_native_data = react_native_file.content
react_native_data_json = json.loads(react_native_data)
if react_native_data_json['nbHits']>0:
    df = json_normalize(react_native_data_json['hits'])
    df = df.rename(index=str, columns={"created_at_i":"time", "comment_text":"text", "story_id":"id", "parent_id":"parent"})
    df = df[['time', 'text', 'id', 'parent']]
    df = df.sort_values('time')
    df.to_sql("HackerNews_react_native",conn, if_exists='append', index = False)
df = None


#repeat for HackerNews flutter
cur.execute("SELECT max(time) FROM HackerNews_flutter")
last_timestamp = cur.fetchall()[0][0]
flutter_url = "https://hn.algolia.com/api/v1/search?query=flutter&numericFilters=created_at_i>{}&hitsPerPage=1000&tags=comment".format(last_timestamp)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
flutter_file = requests.get(flutter_url,headers=headers)
flutter_data = flutter_file.content
flutter_data_json = json.loads(flutter_data)
if flutter_data_json['nbHits']>0:
    df = json_normalize(flutter_data_json['hits'])
    df = df.rename(index=str, columns={"created_at_i":"time", "comment_text":"text", "story_id":"id", "parent_id":"parent"})
    df = df[['time', 'text', 'id', 'parent']]
    df = df.sort_values('time')
    df.to_sql("HackerNews_flutter",conn, if_exists='append', index = False)
df = None    


#Repeat for Reddit xamarin
cur.execute("SELECT max(created_utc) FROM Reddit_xamarin")
last_timestamp = cur.fetchall()[0][0] 
xamarin_url = "https://api.pushshift.io/reddit/search/comment/?q=xamarin&after={}&sort=asc&sort_type=created_utc&limit=5000".format(last_timestamp)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
xamarin_file = requests.get(xamarin_url,headers=headers)
xamarin_data = xamarin_file.content
xamarin_data_json = json.loads(xamarin_data)
if xamarin_data_json['data']:
    df = json_normalize(xamarin_data_json['data'])
    df = df[['created_utc', 'body', 'subreddit_id', 'link_id', 'parent_id','score', 'id', 'subreddit']]
    df.to_sql("Reddit_xamarin",conn, if_exists='append', index = False)
df = None


#Repeat for Reddit react native
cur.execute("SELECT max(created_utc) FROM Reddit_react_native")
last_timestamp = cur.fetchall()[0][0]
react_native_url = "https://api.pushshift.io/reddit/search/comment/?q=react%20native&after={}&sort=asc&sort_type=created_utc&limit=5000".format(last_timestamp)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
react_native_file = requests.get(react_native_url,headers=headers)
react_native_data = react_native_file.content
react_native_data_json = json.loads(react_native_data)
if react_native_data_json['data']:
    df = json_normalize(react_native_data_json['data'])
    df = df[['created_utc', 'body', 'subreddit_id', 'link_id', 'parent_id','score', 'id', 'subreddit']]
    df.to_sql("Reddit_react_native",conn, if_exists='append', index = False)
df = None


#Repeat for Reddit flutter
cur.execute("SELECT max(created_utc) FROM Reddit_flutter")
last_timestamp = cur.fetchall()[0][0]
flutter_url = "https://api.pushshift.io/reddit/search/comment/?q=flutter&after={}&sort=asc&sort_type=created_utc&limit=10000".format(last_timestamp)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
flutter_file = requests.get(flutter_url,headers=headers)
flutter_data = flutter_file.content
flutter_data_json = json.loads(flutter_data)
if flutter_data_json['data']:
    df = json_normalize(flutter_data_json['data'])
    df = df[['created_utc', 'body', 'subreddit_id', 'link_id', 'parent_id','score', 'id', 'subreddit']]
    df.to_sql("Reddit_flutter",conn, if_exists='append', index = False)
df = None


#clean up sql
conn.commit()
conn.close()
