__author__ = 'anil'
import config
import requests
import requests_oauthlib
import threading
import Queue
import ast
####################################################################
consumer_key="Vs7V2k4vPWMMyTFqLzqPkM6wE"
consumer_secret="aWNRzh74LUT1fuW35y6VzRDtvuimQ4LjFGMnMMkEXI0Y9LSpkf"

access_token="258113369-63Y2Cqr9q0Bo02WU4AS8Bjiv3JnHP2Us7HimK26G"
access_token_secret="Z4Sf9EyLbOJ4jPI5WlZPZUyv3OwluuZXiKXn0pamk8Dly"
auth = requests_oauthlib.OAuth1(consumer_key, consumer_secret,access_token,access_token_secret)
# url = 'https://stream.twitter.com/1.1/statuses/filter.json'
###################################################################


BATCH_INTERVAL = 60 # How frequently to update (seconds)
BLOCKSIZE = 50 # How many tweets per update
def executeStreaming():
    try:
        from pyspark import SparkContext,SparkConf
        from pyspark.streaming import StreamingContext
        threads = []
        q = Queue.Queue()
        sc  = SparkContext('local[4]', 'TV Show Analysis')
        ssc = StreamingContext(sc, BATCH_INTERVAL)
        rdd = ssc.sparkContext.parallelize([0])
        stream = ssc.queueStream([], default=rdd)
        threads.append(threading.Thread(target=spark_stream, args=(sc, ssc, q)))
        #threads.append(threading.Thread(target=data_plotting, args=(q,)))
        [t.start() for t in threads]
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
    response = requests.get(query_url, auth=auth, stream=True)
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

def tfunc(t, rdd):
    """
    Transforming function. Converts our blank RDD to something usable
    :param t: datetime
    :param rdd: rdd
    Current rdd we're mapping to
    """
    return rdd.flatMap(lambda x: stream_twitter_data())

def spark_stream(sc, ssc, q):
    """
    Establish queued spark stream.
    For a **rough** tutorial of what I'm doing here, check this unit test
    https://github.com/databricks/spark-perf/blob/master/pyspark-tests/streaming_tests.py
    * Essentially this establishes an empty RDD object filled with integers [0, BLOCKSIZE).
    * We then set up our DStream object to have the default RDD be our empty RDD.
    * Finally, we transform our DStream by applying a map to each element (remember these
    were integers) and setting the next element to be the next element from the Twitter
    stream.
    * Afterwards we perform the analysis
    1. Convert each string to a literal python object
    2. Filter by keyword association (sentiment analysis)
    3. Convert each object to just the coordinate tuple
    :param sc: SparkContext
    :param ssc: StreamingContext
    """
    # Setup Stream
    rdd = ssc.sparkContext.parallelize([0])
    stream = ssc.queueStream([], default=rdd)
    stream = stream.transform(tfunc)
    # Analysis
    coord_stream = stream.map(lambda line: ast.literal_eval(line)) \
                                            #.filter(filter_posts) \
                                            #.map(get_coord)
    # Convert to something usable....
    coord_stream.foreachRDD(lambda t, rdd: q.put(rdd.collect()))
    # Run!
    ssc.start()
    ssc.awaitTermination()