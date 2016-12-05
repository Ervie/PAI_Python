"""
Definition of views.
"""
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from RadioStreamer.utils import MetadataWorker as MW 

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