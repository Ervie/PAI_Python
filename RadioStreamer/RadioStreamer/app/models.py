"""
Definition of models.
"""

from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError

class Channel(models.Model):
    name = models.TextField()
    page_url = models.TextField()
    stream_url = models.TextField()

    class Meta:
        db_table = 'channel'


class Person(models.Model):
    id = models.BigAutoField(primary_key=True)                                                          # domyslnie tworzy sie id typu Serial, wiec tutaj trzeba sprecyzowac, bo jest inny typ
    login = models.TextField(unique=True)
    password = models.TextField()
    salt = models.TextField()
    email = models.TextField(unique=True, blank=True, null=True)

    favs = models.ManyToManyField(Channel, through = "Favourites", related_name = "favs")               # tworzy relacje M x N z tabela Channel z tablica posrednia Favourites
    userRatings = models.ManyToManyField(Channel, through = "Ratings", related_name = "userRatings")    # related_name wymagane, jesli istnieje wiecej niz jeden klucz obcy wskazujacy na ta tabele
    userHistory = models.ManyToManyField(Channel, through = "History", related_name = "userHistory")

    class Meta:
        db_table = 'person'
        

class Tag(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        db_table = 'tag'


class TagsChannels(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tags_channels'
        #unique_together = (('tag_id', 'channel_id'),)


class Favourites(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        db_table = 'favourites'
        #unique_together = (('channel', 'person'),)
        

class History(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.IntegerField()

    class Meta:
        db_table = 'history'
        #unique_together = (('channel_id', 'person_id'),)
                

class Ratings(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    value = models.SmallIntegerField()

    #def clean(self):
    #    if (self.value < 1 or self.value > 10):
    #        raise ValidationError("Provided value not in range <1; 10>")

    #    return super(Ratings, self).clean()

    class Meta:
        db_table = 'ratings'
        #unique_together = (('channel_id', 'person_id'),)
                

#class DjangoMigrations(models.Model):
#    app = models.CharField(max_length=255)
#    name = models.CharField(max_length=255)
#    applied = models.DateTimeField()

#    class Meta:
#        managed = False
#        db_table = 'django_migrations'