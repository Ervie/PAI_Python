"""
Definition of urls for RadioStreamer.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^about', app.views.about, name='about'),
    url(r'^metadata', app.views.metadata, name="metadata"),
    url(r'^logTime', app.views.logTime, name="logTime"),
    url(r'^additionalInfo', app.views.additionalInfo, name="additionalInfo"),
    url(r'^sidebar', app.views.sidebar, name="sidebar"),
    url(r'^suggestions', app.views.suggestions, name="suggestions"),
    url(r'^randomChannel', app.views.randomChannel, name="randomChannel"),
    url(r'^channelList', app.views.channelList, name="channelList"),
    url(r'^requestedChannel', app.views.requestedChannel, name="requestedChannel"),
    url(r'^addChannel', app.views.addChannel, name="addChannel"),
    url(r'^modifyChannelFile', app.views.modifyChannelFile, name="modifyChannelFile"),
    url(r'^privateChannelList', app.views.privateChannelList, name="privateChannelList"),
    url(r'^requestedPrivateChannel', app.views.requestedPrivateChannel, name="requestedPrivateChannel"),
    url(r'^favoriteList', app.views.favoriteList, name="favoriteList"),
    url(r'^registration', app.views.register, name="registration"),
    url(r'^postRegistration', app.views.postRegistration, name="postRegistration"),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Zaloguj',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
