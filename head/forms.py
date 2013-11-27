'''
Created on Nov 27, 2013

@author: bavin_000
'''
from django import forms

class ProfileUpdateForm(forms.Form):
    email = forms.EmailField(required= True)