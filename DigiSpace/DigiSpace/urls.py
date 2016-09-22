from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib import admin
from digispaceapp import views
from django.conf.urls.static import static
from DigiSpace import settings
from mobileapp.mobile_urls import mobileapp_urlpattern
from subscriberapp.subscriber_urls import subscriber_urlpattern
from crmapp.urls import crm_urlpatterns

#from django.views.generic import direct_to_template
from django.views.generic import TemplateView
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DigiSpace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^mobileapp/', include(mobileapp_urlpattern)),
    url(r'^CTI-CRM/', include(crm_urlpatterns)),
    url(r'^subscriber-portal/', include(subscriber_urlpattern)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^rate-card/', 'Admin.views.rate_card',name='rate_card'),
    url(r'^backoffice/', 'Admin.views.backoffice',name='backoffice'),
    url(r'^reload-captcha/', 'Admin.captcha_mod.reload_captcha', name='captcha_reload'),
    url(r'^dashboard/', 'Admin.views.dashboard',name='dashboard'),
    url(r'^subscriber/', 'Admin.views.subscriber',name='subscriber'),
    url(r'^consumer/', 'Admin.views.consumer',name='consumer'),
    url(r'^user/', 'Admin.views.user',name='user'),
    url(r'^notification/', 'Admin.views.notification',name='notification'),
    url(r'^reference-data/', 'Admin.views.reference_data',name='reference_data'),
    url(r'^add-subscriber/', 'Admin.supplier.add_subscriber',name='add_subscriber'),
    url(r'^signin/', 'Admin.views.signin',name='signin'),
    url(r'^log-out/', 'Admin.views.signing_out',name='signing_out'),
    url(r'^add-user/', 'Admin.views.add_user',name='add_user'),
    url(r'^view-user-list/', 'Admin.views.view_user_list',name='view_user_list'),
    url(r'^delete-user/', 'Admin.views.delete_user',name='delete_user'),
    url(r'^view-user-detail/', 'Admin.views.view_user_detail',name='view_user_detail'),
    url(r'^add-city/', 'Admin.views.add_city',name='add_city'),
    url(r'^category/', 'Admin.views.category',name='category'),
    url(r'^user-role/', 'Admin.views.user_role',name='user_role'),
    url(r'^advert-management/', 'Admin.advert.advert_management',name='advert_management'),
    url(r'^add-advert/', 'Admin.views.add_advert',name='add_advert'),
    url(r'^consumer-detail/', 'Admin.views.consumer_detail',name='consumer_detail'),
    url(r'^deal-detail/', 'Admin.views.deal_detail',name='deal_detail'),
    url(r'^get-state/', 'Admin.views.get_state',name='get-state'),
    url(r'^add-currency/', 'Admin.views.add_currency',name='add_currency'),
    url(r'^get-city/', 'Admin.views.get_city',name='get-city'),
    url(r'^get-pincode/', 'Admin.views.get_pincode',name='get_pincode'),  
    url(r'^save-supplier/', 'Admin.supplier.save_supplier',name='save_supplier'),  
    url(r'^save-service/', 'Admin.supplier.save_service',name='save_service'),  
    url(r'^register-supplier/', 'Admin.supplier.register_supplier',name='register_supplier'),  
    url(r'^save-advert/', 'Admin.advert.save_advert',name='save_advert'),
    url(r'^upload-advert-image/', 'Admin.advert.main_listing_image_file_upload',name='main_listing_image_file_upload'),   
    url(r'^get-advert-list/', 'Admin.advert.get_advert_list',name='get_advert_list'),  
    url(r'^delete-advert/', 'Admin.advert.delete_advert',name='delete_advert'),
    url(r'^active-advert/', 'Admin.advert.active_advert',name='active_advert'),    
    url(r'^edit-advert/', 'Admin.advert.edit_advert',name='edit_advert'), 
    url(r'^update-advert/', 'Admin.advert.update_advert',name='update_advert'), 
    url(r'^remove-advert-image/', 'Admin.advert.remove_advert_image',name='remove_advert_image'), 
    url(r'^update-advert-image/', 'Admin.advert.update_advert_image',name='update-advert-image'), 
    url(r'^upload-advert-video/', 'Admin.advert.advert_video_upload',name='advert_video_upload'), 
    url(r'^update-advert-video/', 'Admin.advert.update_advert_video',name='update_advert_video'),   
    url(r'^remove-advert-video/', 'Admin.advert.remove_advert_video',name='remove_advert_video'), 

    # Advert Book
    url(r'^advert-booking-list/', 'Admin.advert.advert_booking_list',name='advert_booking_list'),

#shubham

    url(r'^register-city/', 'Admin.consumer.register_city',name='register_city'),
    url(r'^payment-city/', 'Admin.consumer.payment_city',name='payment_city'),


    # ankita
    url(r'^get-amount/', 'Admin.supplier.get_amount',name='get_amount'),  
    url(r'^view-subscriber-list/', 'Admin.supplier.view_subscriber_list',name='view_subscriber_list'),  
    url(r'^delete-subscriber/', 'Admin.supplier.delete_subscriber',name='delete_subscriber'),  
    url(r'^edit-subscriber/', 'Admin.supplier.edit_subscriber',name='edit_subscriber'),  
    url(r'^edit-service/', 'Admin.supplier.edit_service',name='edit_service'),  
    url(r'^update-subscriber-detail/', 'Admin.supplier.update_subscriber_detail',name='update_subscriber_detail'),  
    
    # payal
    url(r'^add-role/', 'Admin.views.add_role',name='add_role'),
    url(r'^add-user-role/', 'Admin.views.add_user_role',name='add_user_role'),
    url(r'^view-user-role-list/', 'Admin.views.view_user_role_list',name='view_user_role_list'),
    url(r'^edit-user-role/', 'Admin.views.edit_user_role',name='edit_user_role'),
    url(r'^update-user-role/', 'Admin.views.update_user_role',name='update_user_role'),
    url(r'^delete-user-role/', 'Admin.views.delete_user_role',name='delete_user_role'),
    url(r'^active-user-role/', 'Admin.views.active_user_role',name='active_user_role'),
    url(r'^save-city/', 'Admin.views.save_city',name='save_city'),
    url(r'^save-city-data/', 'Admin.views.save_city_data',name='save_place'),
    url(r'^view-city/', 'Admin.views.view_city',name='view_city'),   
    url(r'^delete-city/', 'Admin.views.delete_city',name='delete_city'),  
    url(r'^active-city/', 'Admin.views.active_city',name='active_city'),
    url(r'^edit-city/', 'Admin.views.edit_city',name='edit_city'), 
    url(r'^update-city/', 'Admin.views.update_city',name='update_city'),
    url(r'^update-city-data/', 'Admin.views.update_city_data',name='update_city_data'), 
    url(r'^update-subscriber/', 'Admin.supplier.update_subscriber',name='update_subscriber'),        
    url(r'^check-advert/', 'Admin.supplier.check_advert',name='check_advert'),        
    url(r'^add-category/', 'Admin.category.add_category',name='add_category'),        
    url(r'^save-category/', 'Admin.category.save_category',name='save_category'),        
    url(r'^category-list/', 'Admin.category.category_list',name='category_list'),        
    url(r'^delete-category/', 'Admin.category.delete_category',name='delete_category'),
    url(r'^delete-sub-category/', 'Admin.category.delete_sub_category',name='delete_sub_category'), 
    url(r'^active_category/', 'Admin.category.active_category',name='active_category'),          
    url(r'^edit-category/', 'Admin.category.edit_category',name='edit_category'),        
    url(r'^update-category/', 'Admin.category.update_category',name='update_category'),        
    url(r'^get_city/', 'Admin.category.get_city',name='get-city'),
    url(r'^get-cat-sequence/', 'Admin.category.get_cat_sequence',name='get_cat_sequence'),

    # rate card urls
    url(r'^add-rate-card/', 'Admin.ratecard.add_rate_card',name='add_rate_card'),
    url(r'^edit-rate-card/', 'Admin.ratecard.edit_rate_card',name='edit_rate_card'),
    url(r'^delete-rate-card/', 'Admin.ratecard.delete_rate_card',name='delete_rate_card'),
    url(r'^get-city-category-list/', 'Admin.ratecard.get_city_category_list',name='get_city_category_list'),
    url(r'^get-all-category-list/', 'Admin.ratecard.get_all_category_list',name='get_all_category_list'),
    url(r'^save-prem-sevice-rate-card/', 'Admin.ratecard.save_prem_sevice_ratecard',name='save_prem_sevice_ratecard'),
    url(r'^update-prem-sevice-rate-card/', 'Admin.ratecard.update_prem_sevice_ratecard',name='update_prem_sevice_ratecard'),
    url(r'^save-cat-wise-rate-card/', 'Admin.ratecard.save_cat_wise_ratecard',name='save_cat_wise_ratecard'),
    url(r'^update-cat-wise-rate-card/', 'Admin.ratecard.update_cat_wise_ratecard',name='update_cat_wise_ratecard'),
    url(r'^get-category-rate-card/', 'Admin.ratecard.get_category_ratecard',name='get_category_ratecard'),
    url(r'^get-sub-category-rate-card/', 'Admin.ratecard.get_subcategory_ratecard',name='get_subcategory_ratecard'),
    url(r'^get-city-rate-card/', 'Admin.ratecard.get_city_ratecard',name='get_city_ratecard'),

    url(r'^add-service/', 'Admin.ratecard.add_service',name='add_service'),
    url(r'^service-list/', 'Admin.ratecard.service_list',name='service_list'),
    url(r'^delete-service/', 'Admin.ratecard.delete_service',name='delete_service'),
    url(r'^active-service/', 'Admin.ratecard.active_service',name='active_service'),
    url(r'^add-premium-service/', 'Admin.ratecard.add_premium_service',name='add_premium_service'),
    url(r'^premium-service-list/', 'Admin.ratecard.premium_service_list',name='premium_service_list'),
    url(r'^delete-premium-service/', 'Admin.ratecard.delete_premium_service',name='delete_premium_service'),
    url(r'^active-premium-service/', 'Admin.ratecard.active_premium_service',name='active_premium_service'),
    url(r'^edit-service-ratecard/', 'Admin.ratecard.edit_service',name='edit_service'),
    url(r'^edit-premium-service/', 'Admin.ratecard.edit_premium_service',name='edit_premium_service'),
    url(r'^update-service/', 'Admin.ratecard.update_service',name='update-service'),
    url(r'^update-premium-service/', 'Admin.ratecard.update_premium_service',name='update-service'),
    url(r'^active-subscriber/', 'Admin.supplier.active_subscriber',name='active_subscriber'), 

    #kumar
    url(r'^check-category/', 'Admin.advert.check_category',name='check_category'),        
    url(r'^update-user-detail/', 'Admin.views.update_user_detail',name='update_user_detail'),   
    url(r'^activate-user/', 'Admin.views.activate_user',name='activate_user'),

    # new urls
    url(r'^check-subscription/', 'Admin.advert.check_subscription',name='check_subscriptiono'), 
    url(r'^add-subscription/', 'Admin.advert.add_subscription',name='add_subscription'), 
    url(r'^advert-detail/', 'Admin.advert.advert_detail',name='advert_detail'), 
    url(r'^update-subscription/', 'Admin.advert.update_subscription',name='update_subscription'), 
    url(r'^save-subscriber-detail/', 'Admin.advert.save_subscriber_detail',name='save_subscriber_detail'), 
    url(r'^edit-subscriber-detail/', 'Admin.supplier.edit_subscriber_detail',name='edit_subscriber_detail'), 

#updated changes
    url(r'^get-city-place/', 'Admin.advert.get_city_place',name='get-city-place'),
    url(r'^get-pincode-place/', 'Admin.advert.get_pincode_place',name='get-pincode-place'), 

#Consumer urls
    url(r'^consumer-list/', 'Admin.consumer.view_user_list',name='view_user_list'),
    url(r'^booking/', 'Admin.consumer.subscriber_bookings',name='subscriber_bookings'),
    url(r'^booking-list/', 'Admin.consumer.view_booking_list',name='view_booking_list'),
    url(r'^sms/', 'Admin.consumer.sms',name='sms'),
    url(r'^send_sms/', 'Admin.consumer.send_sms',name='send_sms'),
    url(r'^email/', 'Admin.consumer.email',name='email'),
    url(r'^send_email/', 'Admin.consumer.send_email',name='send_email'),
    url(r'^admin-send-email/', 'Admin.consumer.admin_send_email',name='admin_send_email'),
    url(r'^admin-send-sms/', 'Admin.consumer.admin_send_sms',name='admin_send_sms'),
    url(r'^advert_booking/', 'Admin.consumer.advert_booking',name='advert_booking'),

#Dashboard
    url(r'^get_advert_list/', 'Admin.dashboard.get_advert_list',name='get_advert_list'),
    url(r'^get_advert_date/', 'Admin.dashboard.get_advert_date',name='get_advert_date'),
    url(r'^get_advert_health/', 'Admin.dashboard.get_advert_health',name='get_advert_health'),
    url(r'^get_subscription_plan/', 'Admin.dashboard.get_subscription_plan',name='get_subscription_plan'),
    url(r'^my_subscribers_list/', 'Admin.dashboard.my_subscribers_list',name='my_subscribers_list'),
    url(r'^my_subscription_sale/', 'Admin.dashboard.my_subscription_sale',name='my_subscription_sale'),
    url(r'^get_advert_databse/', 'Admin.dashboard.get_advert_databse',name='get_advert_databse'),
    url(r'^get_new_registered_consumer/', 'Admin.dashboard.get_new_registered_consumer',name='get_new_registered_consumer'),
    url(r'^get_consumer_activity/', 'Admin.dashboard.get_consumer_activity',name='get_consumer_activity'),
    url(r'^get_consumer_usage/', 'Admin.dashboard.get_consumer_usage',name='get_consumer_usage'),
#rest_framewrok
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
