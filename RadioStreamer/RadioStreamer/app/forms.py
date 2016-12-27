"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from app.models import Channel


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Nazwa użytkownika'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Hasło'}))

class OwnRadioChannelForm(forms.Form):
    """Formatka do zapisywania własnej stacji"""
    name = forms.CharField(max_length=254,
                            label='Nazwa stacji',
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Nazwa stacji'}))

    siteUrl = forms.CharField(max_length=254,
                            label='Adres strony',
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Adres strony'}))

    streamUrl = forms.CharField(max_length=254,
                            label='Strumień',
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Adres strumienia'}))