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
from RadioStreamer.utils import XmlHelper as Xml
from RadioStreamer.database.services import dbServices
from app.forms import OwnRadioChannelForm as channelForm


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
    """Odświeżanie widoku metadanych"""
    channelUrl = request.GET['currentChannelUrl'] 

    newMetadata = "";
    
    if not (channelUrl == ""):
        worker = MW.MetadataWorker();
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
    """Odświeżanie sidebara z polecankami"""
    # ToDo: Logika do polecanek: wczytać obiekty typu channel z DB i załadować nazwę i url, ścieżki do obrazków wziąć na podstawie nazwy stacji. Algorytm w osobnej klasie (tagi, historia odsłuchań itp.). Można odliczyć ulubione.

    return render(
        request,
        'app/sidebarPartial.html', 
            {
                'firstImagePath': "static/app/image/icons/300px/RMF FM Classic.png",
                'firstImagePathSmall': "static/app/image/icons/120px/RMF FM Classic120.png",
                'firstChannelName': "RMF FM Classic",
                'firstChannelUrl': "http://195.150.20.243:8000/rmf_classic",
                'secondImagePath': "static/app/image/icons/300px/Gensokyo Radio.png",
                'secondImagePathSmall': "static/app/image/icons/120px/Gensokyo Radio120.png",
                'secondChannelName': "Gensokyo Radio",
                'secondChannelUrl': "http://stream.gensokyoradio.net:8000/stream/1/",
                'thirdImagePath': "static/app/image/icons/300px/VGM Radio.png",
                'thirdImagePathSmall': "static/app/image/icons/120px/VGM Radio120.png",
                'thirdChannelName': "VGM Radio",
                'thirdChannelUrl': "http://radio.vgmradio.com:8040/stream",
            }
        )

def logTime(request):

	# ToDo: Odkomentować gdy logowanie/rejestracja zostaną zaimplementowane
	#username = None
	#if request.user.is_authenticated():
		#username = request.user.username
    username = "Forczu";

    db = dbServices.dbServices();

    channelName = request.POST['currentChannelName'];
    start = datetime.strptime(request.POST['startTimestamp'], '%Y-%m-%dT%H:%M:%S.%fZ');
    end = datetime.strptime(request.POST['endTimestamp'], '%Y-%m-%dT%H:%M:%S.%fZ');
    duration = abs((end - start).seconds);
    db.add_history_log(username, channelName, start, end, duration);

    return HttpResponse(status=204);

def rating(request):

    # ToDo: Odkomentować gdy logowanie/rejestracja zostaną zaimplementowane
	#username = None
	#if request.user.is_authenticated():
		#username = request.user.username
    username = "Forczu";
    
    db = dbServices.dbServices();
    if (request.method == "GET"):
        channelRating = db.get_rating(username, request.GET['currentChannelName']);
        
        if (channelRating.id is None):
            value = 0;
        else:
            value = channelRating.value / 2.0;

        return HttpResponse(value);

    elif (request.method == "POST"):
        adjustedRating = float(request.POST['value']) * 2;

        db.add_rating(username, request.POST['currentChannelName'], adjustedRating);
        return HttpResponse(status=204);

    else:
        return HttpResponse(0);

def randomChannel(request):

    db = dbServices.dbServices();

    randomChannel = db.get_random_channel();

    if (randomChannel is not None):

        imgSrc = "static/app/image/icons/300px/" + randomChannel.name + ".png";

        jsonData = {};
        jsonData['channelName'] = randomChannel.name;
        jsonData['channelUrl'] = randomChannel.stream_url;
        jsonData['imagePath'] = imgSrc;

        return HttpResponse(json.dumps(jsonData), content_type = "application/json");

    else:
        return HttpResponse(status=400);

def channelList(request):

    db = dbServices.dbServices();

    channelList = db.get_all_channels();

    json_string = json.dumps(sorted([ob.name for ob in channelList]))

    return HttpResponse(json_string, content_type = "application/json");

def requestedChannel(request):

    db = dbServices.dbServices();

    requestedChannel = db.get_channel(request.GET['channelName']);
    
    imgSrc = "static/app/image/icons/300px/" + requestedChannel.name + ".png";

    jsonData = {};
    jsonData['channelName'] = requestedChannel.name;
    jsonData['channelUrl'] = requestedChannel.stream_url;
    jsonData['imagePath'] = imgSrc;
    
    return HttpResponse(json.dumps(jsonData), content_type = "application/json");

def addChannel(request):
	"""Wyświetlanie widoku formatki do uzupełnienia"""
	form_class = channelForm()

	return render(request, 'app/addChannel.html', {'form': form_class })

def modifyChannelFile(request):
	"""Konkretne uruchomienie procedury dodawanie do pliku"""
	
	channelName = request.POST['name'];
	siteUrl = request.POST['siteUrl'];
	streamUrl = request.POST['streamUrl'];

	xmlHelper = Xml.XmlHelper()

	isValid = xmlHelper.appendNewChannel(channelName, siteUrl, streamUrl);

	if (isValid):
		return HttpResponse(status=204);
	else:
		return HttpResponse(status=403);

def privateChannelList(request):
	"""Wczytywanie własnych stacji z pliku"""

	xmlHelper = Xml.XmlHelper();

	channelList = xmlHelper.readAllChannels();

	json_string = json.dumps(sorted([ob.name for ob in channelList]))

	return HttpResponse(json_string, content_type = "application/json");

def requestedPrivateChannel(request):
	"""Załadowanie stacji z pliku"""

	xmlHelper = Xml.XmlHelper();

	requestedChannel = xmlHelper.getChannelUrl(request.GET['channelName']);

	jsonData = {};
	jsonData['channelName'] = requestedChannel.name;
	jsonData['channelUrl'] = requestedChannel.stream_url;
	
	return HttpResponse(json.dumps(jsonData), content_type = "application/json");