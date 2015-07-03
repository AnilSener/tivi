__author__ = 'anil'
import config
import requests
import requests_oauthlib
import threading
import Queue
import ast
import time
import numpy as np
from tiviapp.models import *
import json
import datetime
from pytz import timezone
import string
import re
####################################################################
consumer_key="Vs7V2k4vPWMMyTFqLzqPkM6wE"
consumer_secret="aWNRzh74LUT1fuW35y6VzRDtvuimQ4LjFGMnMMkEXI0Y9LSpkf"

access_token="258113369-63Y2Cqr9q0Bo02WU4AS8Bjiv3JnHP2Us7HimK26G"
access_token_secret="Z4Sf9EyLbOJ4jPI5WlZPZUyv3OwluuZXiKXn0pamk8Dly"
auth = requests_oauthlib.OAuth1(consumer_key, consumer_secret,access_token,access_token_secret)
url = 'https://stream.twitter.com/1.1/statuses/filter.json'
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
        threads.append(threading.Thread(target=spark_stream, args=(sc, ssc, q)))
        threads.append(threading.Thread(target=store_data, args=(q,)))
        [t.start() for t in threads]
    except Exception as e:
        print e.message



def stream_twitter_data():
    """
    Only pull in tweets with location information
    :param response: requests response object
    This is the returned response from the GET request on the twitter endpoint
    """
    keywords=Show.objects.values_list("name")
    print keywords
    comma_sep_list=""
    for i,word in enumerate(keywords):
        comma_sep_list+=re.sub('[%s]' % re.escape(string.punctuation),'',word.encode('ascii','ignore'))+", " if i<len(keywords)-1 else re.sub('[%s]' % re.escape(string.punctuation),'',word.encode('ascii','ignore'))
    print(comma_sep_list)

    data = [('language', 'en'), ('locations', '-130,20,-60,50'),('track',comma_sep_list)]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in data])
    response = requests.get(query_url, auth=auth, stream=True)
    print(query_url, response) # 200 <OK>
    count = 0
    for line in response.iter_lines(): # Iterate over streaming tweets
        try:
            if count > BLOCKSIZE:
                break
            post = json.loads(line.decode('utf-8'))
            contents = [post['id_str'],post['text'],post['created_at'], post['coordinates'], post['place'], post['geo'],post["user"],post["entities"]]
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

def get_coord(line):
    """
    Converts each object into /just/ the associated coordinates
    :param line: list
    List from dataset
    """
    coord = tuple()
    try:
        if line[1] == None:
            coord = line[2]['bounding_box']['coordinates']
            coord = reduce(lambda agg, nxt: [agg[0] + nxt[0], agg[1] + nxt[1]], coord[0])
            coord = tuple(map(lambda t: t / 4.0, coord))
        else:
            coord = tuple(line[1]['coordinates'])
    except TypeError:
        print(line)
    return coord

def store_data(q):
    while True:
        if q.empty():
            print "Wait 5 seconds"
            time.sleep(5)
        else:
            data = np.array(q.get())
            try:
                for [id,text,createdAt,coordinates, place, geo,user,entities] in data[:,:]:
                    p=createPlace(place,geo)
                    tn=createTweet(id,text,createdAt,user,p)
                    u=createUser(user,tn)
                    extractHashtags(entities["hashtags"],tn,u)

            except IndexError: # Empty array
                pass


def createUser(user,tn):
        qs=TwitterUser.objects.filter(userID=user["id_str"])
        u = TwitterUser()
        if len(qs[:])>0:
            u=qs[:1].get()
        u.userID = user['id_str']
        u.userName = user["screen_name"]
        u.followersCount = user["followers_count"]
        u.friendsCount = user["friends_count"]
        #u.retweetCount = user["retweet_count"]
        u.isGeoEnabled = user['geo_enabled']
        u.language = user['lang']
        u.tweets.add(tn)
        print "User!!!!",u.userName
        u.save()
        return u

def createTweet(id,text,createdAt,user,p):
    print "start"
    t=Tweet()
    t.tweetID=str(id)
    t.text = text
    t.save()
    if p!=None:
        #print t._object_key['pk']
        updated = Tweet.objects(pk=t.tweetID).update_one(set__location=p)
        if not updated:
            print "location not updated"
    createdAt=datetime.datetime.strptime(str(createdAt).replace(str(createdAt)[createdAt.index("+"):len(createdAt)-4],''),'%a %b %d %H:%M:%S %Y').replace(tzinfo=timezone('UTC'))
    tn=TweetNode.objects.create(objectID=str(t._object_key),tweetID=str(id),createdAt=createdAt)
    #t.createdAt = data["created_at"]
    """t.isRetweeted = data["retweeted"]
    t.isFavorited= data["favorited"]
    t.favoriteCount = data["favorite_count"]
    t.retweetCount = data["retweet_count"]"""
    #t.trends = data["entities"]["trends"]
    """t.symbols = data["entities"]["symbols"]
    t.urls = data["entities"]["urls"]"""
    #t.cleaned_text = cleanTweet(t)

    return tn
def createPlace(place,geo):
    p=None
    if place!=None:
        try:
            p=Place()
            print "There is place"
            coord=place["bounding_box"]['coordinates'][0]
            if coord[0][0]==coord[1][0] and coord[0][1]==coord[1][1]:
                p.geopoint = coord[0];print "geom trick"
            else:
                p.geometry=[[coord[0],coord[1],coord[2],coord[3],coord[0]]]
            if geo!=None:
                p.geopoint = geo["coordinates"]

            p.placeId = place["id"]
            p.placeFullName = place["full_name"]
            p.placeName = place["name"]
            p.countryCode = place["country_code"]
            p.placeType = place["place_type"]
            p.save()
        except Exception as e:
            print e.message
    return p

def extractHashtags(hashtags,tn,u):
    try:
        if hashtags!=None:
            for word in [x["text"] for x in hashtags]:
                qs=HashTag.objects.filter(tag=word)
                hash_tag=None
                if len(qs[:])>0:
                    hash_tag=qs[0]
                else:
                    hash_tag=HashTag.objects.create(tag=word)
                tn.hashtags.add(hash_tag)
                tn.save()
                previous_user_tags=[obj.tag for obj in list(u.hashtags.all())]
                print "previous hashtags",previous_user_tags
                if not word in previous_user_tags:
                    u.tweets.add(tn)
                    u.hashtags.add(hash_tag)
                    u.save()
    except Exception as e:
        print e.message