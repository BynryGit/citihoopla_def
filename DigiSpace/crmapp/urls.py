from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib import admin
from digispaceapp import views
from django.conf.urls.static import static
from DigiSpace import settings
from mobileapp.mobile_urls import mobileapp_urlpattern


#from django.views.generic import direct_to_template
from django.views.generic import TemplateView
crm_urlpatterns = patterns('',
    # #CRM New Urls
    url(r'^crm_login_form/', 'crmapp.views.crm_login_form',name='crm_login_form'),
    url(r'^crm_login/', 'crmapp.views.crm_login',name='crm_login'),
    url(r'^crm_home/', 'crmapp.views.crm_home',name='crm_home'),
    url(r'^crm_details/', 'crmapp.views.crm_details',name='crm_details'),
    url(r'^get-consumer-detail/', 'crmapp.views.get_consumer_detail',name='get_consumer_detail'),
    url(r'^new_consumer/', 'crmapp.views.new_consumer',name='new_consumer'),
    url(r'^save_consumer_details/', 'crmapp.views.save_consumer_details',name='save_consumer_details'),
    url(r'^enquiry_form/', 'crmapp.views.enquiry_form',name='enquiry_form'),
    url(r'^enquiry_search_results/', 'crmapp.views.enquiry_search_results',name='enquiry_search_results'),
    url(r'^get-pincode-list/', 'crmapp.views.get_pincode_list',name='get_pincode_list'),
    url(r'^enquiry-search-details/', 'crmapp.views.enquiry_search_details',name='enquiry_search_details'),
    url(r'^demo_function/', 'crmapp.views.demo_function',name='demo_function'),
    url(r'^save-enquiry-details/', 'crmapp.views.save_enquiry_details',name='save_enquiry_details'),

    url(r'^callinfo/', 'crmapp.views.caller_details_api',name='caller_details_api'),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
