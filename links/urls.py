'''
Created on Nov 26, 2013

@author: bavin_000
'''
from django.conf.urls import patterns, include, url
from links.views import home_view
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'head.views.home', name='home'),
    # url(r'^head/', include('head.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^home/',  login_required(home_view), name ='home'),
)