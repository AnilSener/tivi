__author__ = 'anil'
from twython import TwythonStreamer,Twython,TwythonError
from tivi import celery_app
from tiviapp.models import *
import time
####################################################################
consumer_key="Vs7V2k4vPWMMyTFqLzqPkM6wE"
consumer_secret="aWNRzh74LUT1fuW35y6VzRDtvuimQ4LjFGMnMMkEXI0Y9LSpkf"

access_token="258113369-63Y2Cqr9q0Bo02WU4AS8Bjiv3JnHP2Us7HimK26G"
access_token_secret="Z4Sf9EyLbOJ4jPI5WlZPZUyv3OwluuZXiKXn0pamk8Dly"
###################################################################
twitter = Twython(consumer_key, consumer_secret,access_token,access_token_secret)
@celery_app.task()
def exec_User_Follows():
    twitter_users=TwitterUser.objects.all()
    if len(twitter_users)==0:
        print "No users available Wait 5 minutes for the next API call"
        time.sleep(300)
    else:

        for i,user in enumerate(twitter_users):
            print user.userName,"!!!"
            try:
                print "!!!TIME FOR FOLLOWERS!!!"
                followers=twitter.get_followers_list(screen_name=user.userName,include_user_entities=True,count=200)
                for f in followers:
                    print f
            except TwythonError as e:
                print e.message