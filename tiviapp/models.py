from django.db import models
from mongoengine import *
from neo4django.db import models
from django.db import models as dbmodels

# Create your models here.
class TweetNode(models.NodeModel):
    tweetID= models.StringProperty()
    in_reply_to_status_id=models.IntegerProperty()
    owner = models.Relationship('TwitterUser',rel_type='tweeted_by',related_name="tweets")
    objectID=models.StringProperty()
    createdAt = models.DateTimeProperty()
    replies = models.Relationship('self',rel_type='replied_as')
    retweets = models.Relationship('self',rel_type='retweeted_as')

class Place(EmbeddedDocument):
    geometry = PolygonField()
    geopoint = GeoPointField()
    placeId = StringField()
    placeFullName = StringField()
    placeName = StringField()
    countryCode = StringField()
    placeType = StringField()
    
class Tweet(Document):
    #_id = ObjectIdField()
    tweetID= StringField(primary_key=True)
    language = StringField()
    text = StringField()
    location= EmbeddedDocumentField('Place')
    isRetweeted = BooleanField()
    isFavorited = BooleanField()
    retweetCount = LongField()
    favoriteCount = LongField()
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

class HashTag(models.NodeModel):
    tag = models.StringProperty()
    tweets = models.Relationship('TweetNode',rel_type='tagged_in',related_name="hashtags")
    users = models.Relationship('TwitterUser',rel_type='tagged_for',related_name="hashtags")