__author__ = 'Blanca'
from tiviapp.models import Show,Programme,Topic
import requests as rq
import datetime
import json
from tivi.celery import app
from pytz import timezone

def setSchedule(data):
    for i in range(len(data)):
        #try:
        print data[i]['name']
        s = Show()
        s.id = str(data[i]['id'])
        s.type=data[i]['show']['type']
        s.genres=data[i]['show']["genres"]
        s.url = data[i]['url']
        s.summary = data[i]['summary']
        s.name = data[i]['show']['name']
        s.number = data[i]['number']
        s.runtime = data[i]['runtime']
        if data[i]['image']!=None:
            s.image = data[i]['image']['original']
        s.airdate = datetime.datetime.strptime(data[i]['airstamp'][:-6],"%Y-%m-%dT%H:%M:%S")#.replace(tzinfo=timezone(data[i]['network']['country']['timezone']))
        #s.airstamp = data[i]['airstamp']
        s.season = int(data[i]['season'])
        #s.show = data[i]['show']
        #s.links = data[i]['_links']
        s.save()
        """except KeyError:
            pass"""

@app.task()
def executeTVListingAPI():
    now=datetime.datetime.now()
    today_d = now.day
    today_m = now.month
    for i in range (0, 7):
        date = now + datetime.timedelta(days=i)
        day = date.day #?????
        month = date.month #???
        url = 'http://api.tvmaze.com/schedule?country=US&date={}'.format(date.date())
        request = rq.get(url)
        data = json.loads(request.text)
        setSchedule(data)

