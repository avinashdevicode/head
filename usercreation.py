'''
Created on Nov 27, 2013

@author: bavin_000
'''
from django.contrib.auth.models import User

for i in range(25):
    user = User.objects.create_user(username='user'+str(i), email = 'email'+ str(i)+'@hot.com', password='goodpass')
    user.set_password('goodpass')
    user.is_staff = False
    user.save()