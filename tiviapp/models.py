from django.db import models
from mongoengine import *
from neo4django.db import models
from django.db import models as dbmodels

# Create your models here.
class TweetNode(models.NodeModel):
    tweetID= models.IntegerProperty()
    in_reply_to_status_id=models.IntegerProperty()
    owner = models.Relationship('TwitterUser',rel_type='tweeted_by',related_name="tweets")
    objectID=models.StringProperty()
    createdAt = models.DateTimeProperty()
    replies = models.Relationship('self',rel_type='replied_as')
    retweets = models.Relationship('self',rel_type='retweeted_as')

class Tweet(Document):
    tweetID= LongField()
    geometry = PolygonField()
    geopoint = GeoPointField()
    timestamp = DateTimeField()
    placeId = StringField()
    placeFullName = StringField()
    placeName = StringField()
    countryCode = StringField()
    placeType = StringField()
    language = StringField()
    text = StringField()
    cleaned_text = StringField()
    createdAt = DateTimeField()
    isRetweeted = BooleanField()
    isFavorited = BooleanField()
    retweetCount = LongField()
    favoriteCount = LongField()
    trends = ListField()
    symbols = ListField()
    urls = ListField()
    twitteruser = ReferenceField("TwitterUser")



class TwitterUser(models.NodeModel):
    userID = models.StringProperty()
    userName = models.StringProperty()
    retweetCount = models.IntegerProperty()
    friendsCount = models.IntegerProperty()
    favouriteCount = models.IntegerProperty()
    followersCount = models.IntegerProperty()
    isGeoEnabled = models.BooleanProperty()
    language = models.StringProperty()
    #account = models.Relationship('Subscriber',rel_type='owns',related_name="twitterusers")
    follower = models.Relationship('self', rel_type='follows',related_name='followed_by')
