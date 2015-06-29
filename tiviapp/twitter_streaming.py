__author__ = 'anil'
####################################################################
consumer_key="Vs7V2k4vPWMMyTFqLzqPkM6wE"
consumer_secret="aWNRzh74LUT1fuW35y6VzRDtvuimQ4LjFGMnMMkEXI0Y9LSpkf"

access_token="258113369-63Y2Cqr9q0Bo02WU4AS8Bjiv3JnHP2Us7HimK26G"
access_token_secret="Z4Sf9EyLbOJ4jPI5WlZPZUyv3OwluuZXiKXn0pamk8Dly"
###################################################################

import config
import requests
BATCH_INTERVAL = 60 # How frequently to update (seconds)
BLOCKSIZE = 50 # How many tweets per update
def executeStreaming():
    try:
        from pyspark import SparkContext,SparkConf
        from pyspark.streaming import StreamingContext
        sc  = SparkContext('local[4]', 'TV Show Analysis')
        ssc = StreamingContext(sc, BATCH_INTERVAL)
        rdd = ssc.sparkContext.parallelize([0])
        stream = ssc.queueStream([], default=rdd)
    except Exception as e:
        print e.message



def stream_twitter_data():
"""
Only pull in tweets with location information
:param response: requests response object
This is the returned response from the GET request on the twitter endpoint
"""
data = [('language', 'en'), ('locations', '-130,20,-60,50')]
query_url = config.url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in data])
response = requests.get(query_url, auth=config.auth, stream=True)
print(query_url, response) # 200 <OK>
count = 0
for line in response.iter_lines(): # Iterate over streaming tweets
try:
if count > BLOCKSIZE:
break
post = json.loads(line.decode('utf-8'))
contents = [post['text'], post['coordinates'], post['place']]
count += 1
yield str(contents)
except:
print(line)