__author__ = 'Blanca'
from tiviapp.models import Show,Programme,ProgrammeTopics
import requests as rq
import datetime
import json

def schedule(data):

    for i in range(len(data)):
        try:
            s = Show()
            s.type=data[i]['type']
            s.genres=data[i]["genres"]
            s.url = data[i]['url']
            s.summary = data[i]['summary']
            s.name = data[i]['name']
            s.number = data[i]['number']
            s.runtime = data[i]['runtime']
            s.image = data[i]['image']
            s.airdate = datetime.datetime.strptime(data[i]['airstamp'][:-4],"%Y-%m-%dT%H:%M:%S").replace(tzinfo=data[i]['airstamp'][-5:])
            #s.airstamp = data[i]['airstamp']
            s.id = data[i]['id']
            s.season = data[i]['season']
            s.show = data[i]['show']
            s.airtime = data[i]['airtime']
            s.links = data[i]['_links']
            s.save()
        except KeyError:
            continue
    return(schedule)

today_d = datetime.datetime.now().day
today_m = datetime.datetime.now().month

for i in range (0, 7):
    date = datetime.datetime.now() + datetime.timedelta(days=i)
    day = date.day
    month = date.month
    url = 'http://api.tvmaze.com/schedule?country=US&date={}'.format(date.date())
    request = rq.get(url)
    data = json.loads(request.text)
    schedule(data)

