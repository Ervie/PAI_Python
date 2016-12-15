"""
Definition of views.
"""
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
import json

from RadioStreamer.utils import MetadataWorker as MW
from RadioStreamer.database.services import dbServices


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def metadata(request):

    channelUrl = request.POST['currentChannelUrl'] 

    worker = MW.MetadataWorker()

    newMetadata = worker.sendRequest(channelUrl);

    return render(
        request,
        'app/metadata.html', 
            {
                'metadata': newMetadata,
            }
        )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    # ----------------- przykladowe operacja na bazie. Do usunięcia
    #db = dbServices()
    #user = db.get_user("Forczu")
    #channel = db.get_channel("Radio Wpierdol")
    #tags = db.get_tags()
    #rating = db.get_rating(user.login, channel.name)

    #if (user.login == ""):
    #    user = db.insert_user("Forczu", "Kotori1", "asdf12345", "tenshissienanawi104@gmail.com")
    #if (channel.name == ""):
    #    channel = db.insert_channel("Radio Wpierdol", "http://spinka.cupsell.pl/", "https://www.youtube.com/user/SPInkafilmstudio/videos")
    #if (tags.count() == 0):
    #    db.add_tag("xxx")
    #if (rating.value == None):
    #    db.add_rating(user.login, channel.name, 9)

    #favs = db.get_favs(user.login)
    
    #if (favs.count() == 0):
    #    favs = db.add_fav(user.login, channel.name)
    # -----------------


    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def sidebar(request):

    # ToDo: Logika do polecanek: wczytać obiekty typu channel z DB i załadować nazwę i url, ścieżki do obrazków wziąć na podstawie nazwy stacji. Algorytm w osobnej klasie (tagi, historia odsłuchań itp.). Można odliczyć ulubione.

    return render(
        request,
        'app/sidebarPartial.html', 
            {
                'firstImagePath': "static/app/image/icons/300px/classic.png",
                'firstImagePathSmall': "static/app/image/icons/120px/classic120.png",
                'firstChannelName': "RMF Classic",
                'firstChannelUrl': "http://195.150.20.243:8000/rmf_classic",
                'secondImagePath': "static/app/image/icons/300px/gensokyo.png",
                'secondImagePathSmall': "static/app/image/icons/120px/gensokyo120.png",
                'secondChannelName': "Gensokyo Radio",
                'secondChannelUrl': "http://stream.gensokyoradio.net:8000/stream/1/",
                'thirdImagePath': "static/app/image/icons/300px/vgm.png",
                'thirdImagePathSmall': "static/app/image/icons/120px/vgm120.png",
                'thirdChannelName': "VGM Radio",
                'thirdChannelUrl': "http://radio.vgmradio.com:8040/stream",
            }
        )

def logTime(request):

	# ToDo: Odkomentować gdy logowanie/rejestracja zostaną zaimplementowane
	#username = None
	#if request.user.is_authenticated():
		#username = request.user.username

    db = dbServices.dbServices()

    channelName = request.POST['currentChannelName'] 
    start = datetime.strptime(request.POST['startTimestamp'], '%Y-%m-%dT%H:%M:%S.%fZ');
    end = datetime.strptime(request.POST['endTimestamp'], '%Y-%m-%dT%H:%M:%S.%fZ');
    duration = abs((end - start).seconds);
    db.add_history_log("Forczu", channelName, start, end);

    return HttpResponse(status=204)

