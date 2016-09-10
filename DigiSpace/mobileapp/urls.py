from django.conf.urls import patterns, include, url
from django.contrib import admin
from digispaceapp import views
from django.conf.urls.static import static
from DigiSpace import settings

#from django.views.generic import direct_to_template
from django.views.generic import TemplateView
mobileapp_urlpattern = patterns('',
    # Examples:
    # url(r'^$', 'DigiSpace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^signup/', 'mobileapp.views.consumer_signup',name='signup'),
   

) + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
