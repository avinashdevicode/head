'''
Created on Nov 29, 2013

@author: bavin_000
'''
from links.models import Link, comment 

from django.forms import ModelForm
from django import forms
from django.forms.widgets import Textarea

class update_form(forms.Form):
    title = forms.CharField(max_length=250)
    url = forms.URLField(required= True)
    description = forms.CharField(widget=Textarea)

class Comment(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('description',)

class link_creation_form(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ('submitted_on', 'rank_score', 'submitter')
        
class link_update_form(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ('submitted_on', 'rank_score', 'submitter')    
    