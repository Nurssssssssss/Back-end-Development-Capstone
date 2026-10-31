"""Django views display local models or optional external Flask microservice data."""
import json
import logging
import os
from urllib.request import urlopen
from django.shortcuts import render
from django.conf import settings
from .models import Concert
from songs.models import Song
from photos.models import Photo
logger=logging.getLogger(__name__)

def fetch_api(base,endpoint):
    if not base:return None
    try:
        with urlopen(base.rstrip('/')+endpoint,timeout=3) as response:
            return json.load(response)
    except (OSError, ValueError) as exc:
        logger.warning('Microservice unavailable: %s',exc)
        return None

def home(request):
    return render(request,'home.html',{'concerts_count':Concert.objects.count()})

def songs(request):
    result=fetch_api(os.environ.get('SONGS_API_URL',''),'/song')
    if isinstance(result,dict) and isinstance(result.get('songs'),list):
        song_list=[{'id':str(i.get('id', '')),'title':i.get('title','Untitled'),'artist':i.get('artist',''),
                    'lyrics':i.get('lyrics','')} for i in result['songs']]
    else:
        song_list=list(Song.objects.values('id','title','artist','lyrics'))
    return render(request,'songs.html',{'songs':song_list})

def photos(request):
    result=fetch_api(os.environ.get('PICTURES_API_URL',''),'/picture')
    if isinstance(result,list):
        photo_list=[{'title':f"{p.get('event_city','Concert')} — {p.get('event_date','')}",'image_url':p.get('pic_url','')} for p in result]
    else:photo_list=list(Photo.objects.values('title','image_url'))
    return render(request,'photos.html',{'photos':photo_list})

def concerts(request):
    return render(request,'concerts.html',{'concerts':Concert.objects.order_by('date')})
