import app.models as Models
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import ProgrammingError
import random

class dbServices(object):
    # Creates and returns new user
    def insert_user(self, login = "", password = "", salt = "", email = ""):
        return Models.Person.objects.create(login = login, password = password, salt = salt, email = email)
    
    # Creates and returns new channel
    def insert_channel(self, name = "", page_url = "", stream_url = ""):
        return Models.Channel.objects.create(name = name, page_url = page_url, stream_url = stream_url)
    
    # Creates and returns new tag
    def add_tag(self, name = ""):
        return Models.Tag.objects.create(name = name)

    # Adds rating to channel for specified user
    def add_rating(self, login = "", channelName = "", value = 0):
        existingRating = self.get_rating(login, channelName);

        if (existingRating.id is not None and value != 0):
            Models.Ratings.objects.filter(id = existingRating.id).update(value = value);
        elif (existingRating.id is not None):
            Models.Ratings.objects.filter(id = existingRating.id).delete();
        else:
            user = self.get_user(login);
            chn = self.get_channel(channelName);
            
            if (user.id != None and chn.id != None):
                Models.Ratings.objects.create(person = user, channel = chn, value = value);
    
    # Adds favourite channel for user
    def add_fav(self, login = "", channelName = ""):
        user = self.get_user(login)
        chn = self.get_channel(channelName)


        if (user.id is not None and chn.id is not None and exis):
            existing_fav = Models.Favourites.objects.filter(person = user, channel = chn);
            if (existing_fav.id is not None):
                Models.Favourites.objects.create(person = user, channel = chn)
    
	# Add history log
    def add_history_log(self, userLogin= "", channelName ="", start = datetime.MINYEAR, end = datetime.MINYEAR, duration = 0):

        user = self.get_user(userLogin)
        chn = self.get_channel(channelName)
        startDate = start
        endDate = end
        dur = duration

        if (user.id is not None and chn.id is not None):
             return Models.History.objects.create(person = user, channel = chn, start_date = startDate, end_date = endDate, duration = dur);


    def delete_fav(self, login = "", channelName = ""):
        user = self.get_user(login);
        chn = self.get_channel(channelName);

        if (user.id is not None and chn.id is not None):
            try:
                return Models.Favourites.objects.filter(person = user, channel = chn).delete();
            except ObjectDoesNotExist:
                return None;

    # Gets user with specified login
    def get_user(self, login=""):
        try:
            return Models.Person.objects.get(login = login)
        except ObjectDoesNotExist:
            return Models.Person()
        
    # Gets channel with specified name
    def get_channel(self, name=""):
        try:
            return Models.Channel.objects.get(name = name)
        except ObjectDoesNotExist:
            return Models.Channel()
    
    # Gets random channel
    def get_random_channel(self):
        lastIndex = Models.Channel.objects.count() - 1;

        if lastIndex > 0:
            index = random.randint(0, lastIndex);

            return Models.Channel.objects.all()[index];
        else:
            return None;

    def get_all_channels(self):

        return Models.Channel.objects.all();

    # Gets user rating for specified channel
    def get_rating(self, login = "", channelName = ""):
        user = self.get_user(login)
        chn = self.get_channel(channelName)

        try:
            #return user.userRatings.get(name = chn.name)
            return Models.Ratings.objects.get(person = user, channel = chn)
        except ObjectDoesNotExist:
            return Models.Ratings()
        
    # Gets user's favourite channels
    def get_favs(self, login = ""):
        user = self.get_user(login)
        return user.favs.all()

    # Gets all tags from database
    def get_tags(self):
        return Models.Tag.objects.all()