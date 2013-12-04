from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from links import urls as URL
from django.contrib.auth.decorators import login_required 
from  links.views import profile_view, profile_update_view

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'head.views.home', name='home'),
    # url(r'^head/', include('head.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^links/', include(URL)),
    url(r'^accounts/login/', 'links.views.login_view', name ='login'),
    url(r'logout/', 'links.views.logout_view', name='logout'),
    url(r'register/', 'links.views.register_view', name= 'register'),
    url(r'profile/', login_required(profile_view), name='profile'),
    url(r'profile_update/', login_required(profile_update_view), name = 'profile_update' ),
    url(r'link/(?P<pk>\d+)', 'links.views.detail_view', name = 'detail_view'),
    url(r'link/up/(?P<pk>\d+)', 'links.views.update_link_view', name = 'update_link'),
    url(r'link/de/(?P<pk>\d+)', 'links.views.delete_link_view', name = 'delete_link'),
    
)
