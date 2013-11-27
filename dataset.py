'''
Created on Nov 26, 2013

@author: bavin_000
'''
from django.contrib.auth.models import User
from links.models import Link

avinash = User.objects.get(username= 'avi')

for i in range(21):
    title = 'title auto' + str(i)
    description = 'Hey Google ' + title
    Link.objects.get_or_create(title=title, 
                               submitter= avinash,
                               url='https://www.google.com',
                               description = description)
    