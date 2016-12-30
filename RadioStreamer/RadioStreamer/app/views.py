"""
Definition of views.
"""
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, redirect
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

    if request.user.is_authenticated:
        return render(
            request,
            'app/index.html',
            {
                'title':'Home Page',
                'year':datetime.now().year,
            }
        )
    else:
        return redirect('/login')

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

    if request.user.is_authenticated:
        return render(
            request,
            'app/about.html',
            {
                'title':'About',
                'message':'Your application description page.',
                'year':datetime.now().year,
            }
        )
    else:
        return redirect('/login')

def register(request):
    assert isinstance(request, HttpRequest)
    
    return render(
        request,
        'app/registration.html',
        {
            'year':datetime.now().year
        }
    )

def postRegistration(request):
    assert isinstance(request, HttpRequest)

    userName = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    email = request.POST['email']

    if (password != password2):
        color = "red"
        text = "Podane hasła nie są identyczne!"
    else:
        db = dbServices.dbServices()
        doesUserExist = db.check_user_exists(userName)

        if (doesUserExist):
            color = "red"
            text = "Podany użytkownik istnieje już w bazie."
        else:
            db.add_user(userName, password, email)
            color = "green"
            text = "Użytkownik został zarejestrowany pomyślnie! Za chwilę nastąpi przekierowanie na stronę logowania."

    if (color == "red"):
        redirectUrl = "/registration"
    else:
        redirectUrl = "/login"

    return render(
        request,
        'app/postRegistration.html',
        {
            'year': datetime.now().year,
            'text': text,
            'textColor': color,
            'redirectUrl': redirectUrlz
        }
    )

def suggestions(request):
    """Odświeżanie sidebara z polecankami"""
    # ToDo: Zaciągnąć polecanki z procedury bazodanowej.

    db = dbServices.dbServices();

    # suggestions = db.get_suggestions();

    jsonData = {};
    jsonData['FirstChannelName'] = "RMF FM Classic"; # suggestions[0].ChannelName itp.
    jsonData['FirstChannelUrl'] = "http://195.150.20.243:8000/rmf_classic";
    jsonData['SecondChannelName'] = "Gensokyo Radio";
    jsonData['SecondChannelUrl'] = "http://stream.gensokyoradio.net:8000/stream/1/";
    jsonData['ThirdChannelName'] = "VGM Radio";
    jsonData['ThirdChannelUrl'] = "http://radio.vgmradio.com:8040/stream";

    return HttpResponse(json.dumps(jsonData), content_type = "application/json");

def sidebar(request):
    """Wczytanie polecanek"""

    return render(
        request,
        'app/sidebarPartial.html', 
            {
                'firstImagePathSmall': "static/app/image/icons/120px/" + request.GET['firstChannelName'] +  "120.png",
                'secondImagePathSmall': "static/app/image/icons/120px/" + request.GET['secondChannelName'] +  "120.png",
                'thirdImagePathSmall': "static/app/image/icons/120px/" + request.GET['thirdChannelName'] +  "120.png"
            }
        )

def logTime(request):
    username = None

    if request.user.is_authenticated:
        username = request.user.username

    db = dbServices.dbServices();

    channelName = request.POST['currentChannelName'];
    start = datetime.strptime(request.POST['startTimestamp'], '%Y-%m-%dT%H:%M:%S.%fZ');
    end = datetime.strptime(request.POST['endTimestamp'], '%Y-%m-%dT%H:%M:%S.%fZ');
    duration = abs((end - start).seconds);
    db.add_history_log(username, channelName, start, end, duration);

    return HttpResponse(status=204);

def additionalInfo(request):
    username = None

    if request.user.is_authenticated:
        username = request.user.username
    
    db = dbServices.dbServices();
    if (request.method == "GET"):
        channelRating = db.get_rating(username, request.GET['currentChannelName']);
        isFavorite = db.get_fav(username, request.GET['currentChannelName']);

        if (channelRating.id is None):
            value = 0;
        else:
            value = channelRating.value / 2.0;

        jsonData = {};
        jsonData['value'] = value;
        jsonData['isFavorite'] = False if isFavorite is None else True;

        return HttpResponse(json.dumps(jsonData), content_type = "application/json");

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

	if request.user.is_authenticated:
		return render(request, 'app/addChannel.html', {'form': form_class })
	else:
		return redirect('/login')

def modifyChannelFile(request):
	"""Konkretne uruchomienie procedury dodawanie do pliku"""
	
	channelName = request.POST['name'];
	siteUrl = request.POST['siteUrl'];
	streamUrl = request.POST['streamUrl'];

	xmlHelper = Xml.XmlHelper(request.user.username)
	isValid = xmlHelper.appendNewChannel(channelName, siteUrl, streamUrl);

	if (isValid):
		redirectUrl = "/"
		color = "green"
		text = "Kanał został dodany prawidłowo."
	else:
		redirectUrl = "/addChannel"
		color = "red"
		text = "Wystąpił błąd podczas dodawania kanału. Upewnij się, że podałeś prawidłowe adresy URL oraz że stacja nie istnieje już w naszej bazie."

	return render(request,
        'app/postAddChannel.html',
        {
            'year': datetime.now().year,
            'text': text,
            'textColor': color,
            'redirectUrl': redirectUrl
        }
	)

def privateChannelList(request):
	"""Wczytywanie własnych stacji z pliku"""

	xmlHelper = Xml.XmlHelper(request.user.username);

	channelList = xmlHelper.readAllChannels();

	json_string = json.dumps(sorted([chnName for chnName in channelList]))

	return HttpResponse(json_string, content_type = "application/json");

def requestedPrivateChannel(request):
	"""Załadowanie stacji z pliku"""

	xmlHelper = Xml.XmlHelper(request.user.username);
	channelName = request.GET['channelName']

	requestedStreamUrl = xmlHelper.getStreamUrl(channelName);

	jsonData = {};
	jsonData['channelName'] = channelName;
	jsonData['channelUrl'] = requestedStreamUrl;
	
	return HttpResponse(json.dumps(jsonData), content_type = "application/json");

def favoriteList(request):
    """Przeładowanie listy ulubionych stacji"""
    username = None

    if request.user.is_authenticated:
        username = request.user.username

    db = dbServices.dbServices();

    if (request.method == "POST"):
        if (request.POST['currentChannelName']):
            if (request.POST['operation'] == "Add"):
                db.add_fav(username, request.POST['currentChannelName']);
            elif (request.POST['operation'] == "Delete"):
                db.delete_fav(username, request.POST['currentChannelName']);


    favoritesList = db.get_favs(username);

    json_string = json.dumps(sorted([ob.name for ob in favoritesList]))

    return HttpResponse(json_string, content_type = "application/json");