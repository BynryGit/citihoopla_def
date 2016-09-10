from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib import auth
from digispaceapp.models import *
import urllib
import smtplib
from smtplib import SMTPException
from captcha_form import CaptchaForm
from django.shortcuts import *

# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction
import pdb
import csv
import json
#importing exceptions
from django.db import IntegrityError

import operator
from django.db.models import Q
from datetime import date, timedelta
import string
import random
# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect

SERVER_URL = "http://52.40.205.128"   
#SERVER_URL="http://192.168.0.126:8080"

def advert_management(request):
    user_id = request.GET.get('user_id')
    data = {'username':request.session['login_user'],'user_id':user_id}
    return render(request,'Admin/advert_management.html',data)  

# TO GET THE CATEGOTRY
def get_phone_category(request):
##    pdb.set_trace()
    phone_cat_list = []
    try:
        ph_category = PhoneCategory.objects.filter(phone_category_status='1')
        for ph_cat in ph_category:
            phone_cat_list.append(
                {'ph_category_id': ph_cat.phone_category_id, 'ph_category_name': ph_cat.phone_category_name})

    except Exception, e:
        print 'Exception ', e
    return phone_cat_list

# TO GET THE CITY
def get_city_place(request):
   # pdb.set_trace()
   state_id=request.GET.get('state_id')
   city_list=[]
   try:
      city_objs=City_Place.objects.filter(state_id=state_id,city_status='1')

      print "======city_objs",city_objs
      for city in city_objs:
         options_data = '<option value=' + str(
                   city.city_place_id) + '>' + city.city_id.city_name + '</option>'
         city_list.append(options_data)
         print city_list
      data = {'city_list': city_list}

   except Exception, ke:
      print ke
      data={'city_list': 'none','message':'No city available'}
   return HttpResponse(json.dumps(data), content_type='application/json')


# TO GET THE PINCODE
def get_pincode_place(request):
   #pdb.set_trace()

   pincode_list=[]
   try:
      city_id = request.GET.get('city_id')
      city_id1  = City_Place.objects.get(city_place_id=str(city_id))
      city_id2  = City.objects.get(city_id=str(city_id1.city_id))
      pincode_list1=Pincode.objects.filter(city_id=city_id2.city_id).order_by('pincode')
      pincode_objs = pincode_list1.values('pincode').distinct()
      for pincode in pincode_objs:
         options_data = '<option>' +pincode['pincode']+ '</option>'
         pincode_list.append(options_data)
         print pincode_list
      data = {'pincode_list': pincode_list}

   except Exception, ke:
      print ke
      data={'city_list': 'none','message':'No city available'}
   return HttpResponse(json.dumps(data), content_type='application/json')   

# TO GET THE STATE
def get_state(request):
##    pdb.set_trace()
    state_list = []
    try:
        state = State.objects.filter(state_status='1')
        for sta in state:
            state_list.append(
                {'state_id': sta.state_id, 'state': sta.state_name})

    except Exception, e:
        print 'Exception ', e
    return state_list



@csrf_exempt
def save_advert(request):
##    pdb.set_trace()
    print "IN SAVE ADVERT METHOD"
    try:
        if request.method == "POST":
                    print '===request========',request.POST
                    advert_obj=Advert(
                        supplier_id=Supplier.objects.get(supplier_id=request.POST.get('user_id')),
                        category_id=Category.objects.get(category_id=request.POST.get('categ')),
                        advert_name=request.POST.get('advert_title'),
                        website=request.POST.get('website'),
                        latitude=request.POST.get('lat'),
                        longitude=request.POST.get('lng'),
                        short_description=request.POST.get('short_discription'),
                        product_description=request.POST.get('product_discription'),
                        currency_id= Currency.objects.get(currency_id=request.POST.get('currency')) if request.POST.get('currency') else None,
                        product_price=request.POST.get('product_price'),
                        discount_description=request.POST.get('discount_discription'),
                        email_primary=request.POST.get('email_primary'),
                        email_secondary =request.POST.get('email_secondary'),
                        address_line_1=request.POST.get('address_line1'),
                        address_line_2=request.POST.get('address_line2'),
                        area   =request.POST.get('area'),     
                        landmark=request.POST.get('landmark'),
                        state_id= State.objects.get(state_id=request.POST.get('statec')) if request.POST.get('statec') else None, 
                        city_place_id =City_Place.objects.get(city_place_id=request.POST.get('city')) if request.POST.get('city') else None,
                        pincode_id=Pincode.objects.get(pincode=request.POST.get('pincode')) if request.POST.get('pincode') else None,
                        property_market_rate=request.POST.get('pro_mark_rate'),
                        possesion_status=request.POST.get('possesion_status'),
                        any_other_details=request.POST.get('any_other_details'),
                        date_of_delivery=request.POST.get('date_of_delivery'),
                        distance_frm_railway_station=request.POST.get('dis_rail_stat'),
                        distance_frm_railway_airport=request.POST.get('dis_airport'),
                        speciality=request.POST.get('speciality')
                    );
                    advert_obj.save()
                    if request.POST.get('subscription_id'):
                      map_subscription(request.POST.get('subscription_id'),advert_obj)

                    subcat_list = request.POST.get('subcat_list')
                    subcat_lvl = 1
                    #String to list
                    if subcat_list!='':
                      sc_list = subcat_list.split(',')
                      for subcat in sc_list:
                          print 'Subcat: ',subcat
                          ac_map_obj = Advert_Category_Map(
                              advert_id = advert_obj,
                              category_id = Category.objects.get(category_id=subcat),
                              category_level = subcat_lvl 
                              )
                          ac_map_obj.save()
                          print 'Advert Subcat Mapping saved'
                          subcat_lvl+=1
                    if request.POST['check_image'] == "1":
                        advert_obj.display_image = request.FILES['display_image']
                        advert_obj.save()

                        
                    attachment_list = []
                    attachment_list = request.POST.get('attachments')
                    save_attachments(attachment_list, advert_obj)


                    video_list = []
                    video_list = request.POST.get('ac_attachment')                    
                    save_video(video_list, advert_obj)
                    
                    phone_category_list = request.POST.get('phone_category_list')
                    phone_category_list = phone_category_list.split(',')
                    phone_number_list = request.POST.get('phone_number_list')
                    phone_number_list = phone_number_list.split(',')
                    zipped = zip(phone_category_list,phone_number_list)
                    save_phone_number(zipped,advert_obj) 
                    
                    opening_day_list = request.POST.get('opening_day_list')
                    opening_day_list = opening_day_list.split(',')

                    start_time_list = request.POST.get('start_time_list')
                    start_time_list = start_time_list.split(',')

                    end_time_list = request.POST.get('end_time_list')
                    end_time_list = end_time_list.split(',')
                    
                    zipped_wk = zip(opening_day_list,start_time_list,end_time_list)
                    save_working_hours(zipped_wk,advert_obj) 
                    
                    amenity_list = request.POST.get('amenity_list')
                    amenity_list = amenity_list.split(',')
                    save_amenity(amenity_list,advert_obj)
                    
                    exe_amenity_list = request.POST.get('additional_amenity')
                    exe_amenity_list = exe_amenity_list.split(',')
                    save_exe_amenity(exe_amenity_list,advert_obj)
                    
                    near_attr_list = request.POST.get('near_attraction')
                    near_attr_list = near_attr_list.split(',')
                    save_near_attr(near_attr_list,advert_obj)
                    
                    near_shopnmal = request.POST.get('near_shopnmal')
                    near_shopnmal = near_shopnmal.split(',')

                    near_shonmald = request.POST.get('near_shonmald')
                    near_shonmald = near_shonmald.split(',')
                    
                    zipped_shopmal = zip(near_shopnmal,near_shonmald)
                    save_shpnmal(zipped_shopmal,advert_obj) 
                    
                    cat =advert_obj.category_id.category_name
                    if cat == 'Property':
                        print "SCHOOL",request.POST.get('near_schol')
                        near_schol = request.POST.get('near_schol')
                        near_schol = near_schol.split(',')
                        
                        print "SCHOOL DI SORTING",request.POST.get('near_schold')
                        near_schold = request.POST.get('near_schold')
                        near_schold = near_schold.split(',')
                        
                        print "AFTER SCHOOL"
                        
                        zipped_school = zip(near_schol,near_schold)
                        save_school(zipped_school,advert_obj) 
                        
                        near_hosp = request.POST.get('near_hosp')
                        near_hosp = near_hosp.split(',')

                        near_hospd = request.POST.get('near_hospd')
                        near_hospd = near_hospd.split(',')
                        
                        zipped_hospital = zip(near_hosp,near_hospd)
                        save_hospital(zipped_hospital,advert_obj) 
                    advert_add_mail(advert_obj)
                    data = {'success': 'true'}

    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def add_subscription(request):
##    pdb.set_trace()
    print "IN SAVE ADVERT METHOD"
    try:
        if request.method == "POST":
                    print '==========request==========',request.POST
                    try:
                      serv_obj = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration'))   
                      try:
                        premium_service_list = request.POST.get('premium_service')
                        no_of_days_list = request.POST.get('premium_day_list')
                        if(premium_service_list):
                          print '------------after premium servuice------------'
                          final_data = check_subscription_detail(premium_service_list,no_of_days_list)
                          if final_data['success']=='true':
                            advert_obj=Advert(
                                  supplier_id=Supplier.objects.get(supplier_id=request.POST.get('user_id')),
                                  category_id=Category.objects.get(category_id=request.POST.get('categ')),
                                  advert_name=request.POST.get('advert_title'),
                                  website=request.POST.get('website'),
                                  latitude=request.POST.get('lat'),
                                  longitude=request.POST.get('lng'),
                                  short_description=request.POST.get('short_discription'),
                                  product_description=request.POST.get('product_discription'),
                                  currency_id= Currency.objects.get(currency_id=request.POST.get('currency')) if request.POST.get('currency') else None,
                                  product_price=request.POST.get('product_price'),
                                  discount_description=request.POST.get('discount_discription'),
                                  email_primary=request.POST.get('email_primary'),
                                  email_secondary =request.POST.get('email_secondary'),
                                  address_line_1=request.POST.get('address_line1'),
                                  address_line_2=request.POST.get('address_line2'),
                                  area   =request.POST.get('area'),     
                                  landmark=request.POST.get('landmark'),
                                  state_id= State.objects.get(state_id=request.POST.get('statec')) if request.POST.get('statec') else None, 
                                  city_place_id =City_Place.objects.get(city_place_id=request.POST.get('city')) if request.POST.get('city') else None,
                                  pincode_id=Pincode.objects.get(pincode=request.POST.get('pincode')) if request.POST.get('pincode') else None,
                                  property_market_rate=request.POST.get('pro_mark_rate'),
                                  possesion_status=request.POST.get('possesion_status'),
                                  any_other_details=request.POST.get('any_other_details'),
                                  date_of_delivery=request.POST.get('date_of_delivery'),
                                  distance_frm_railway_station=request.POST.get('dis_rail_stat'),
                                  distance_frm_railway_airport=request.POST.get('dis_airport'),
                                  speciality=request.POST.get('speciality')
                              );
                            advert_obj.save()
                            print '===============after save advert================='
                            subcat_list = request.POST.get('subcat_list')
                            subcat_lvl = 1
                            #String to list
                            if subcat_list!='':
                              sc_list = subcat_list.split(',')
                              for subcat in sc_list:
                                  print 'Subcat: ',subcat
                                  ac_map_obj = Advert_Category_Map(
                                      advert_id = advert_obj,
                                      category_id = Category.objects.get(category_id=subcat),
                                      category_level = subcat_lvl 
                                      )
                                  ac_map_obj.save()
                                  print 'Advert Subcat Mapping saved'
                                  subcat_lvl+=1
                            if request.POST['check_image'] == "1":
                                advert_obj.display_image = request.FILES['display_image']
                                advert_obj.save()

                                
                            attachment_list = []
                            attachment_list = request.POST.get('attachments')
                            save_attachments(attachment_list, advert_obj)


                            video_list = []
                            video_list = request.POST.get('ac_attachment')                    
                            save_video(video_list, advert_obj)
                            
                            phone_category_list = request.POST.get('phone_category_list')
                            phone_category_list = phone_category_list.split(',')
                            phone_number_list = request.POST.get('phone_number_list')
                            phone_number_list = phone_number_list.split(',')
                            zipped = zip(phone_category_list,phone_number_list)
                            save_phone_number(zipped,advert_obj) 
                            
                            opening_day_list = request.POST.get('opening_day_list')
                            opening_day_list = opening_day_list.split(',')

                            start_time_list = request.POST.get('start_time_list')
                            start_time_list = start_time_list.split(',')

                            end_time_list = request.POST.get('end_time_list')
                            end_time_list = end_time_list.split(',')
                            
                            zipped_wk = zip(opening_day_list,start_time_list,end_time_list)
                            save_working_hours(zipped_wk,advert_obj) 
                            
                            amenity_list = request.POST.get('amenity_list')
                            amenity_list = amenity_list.split(',')
                            save_amenity(amenity_list,advert_obj)
                            
                            exe_amenity_list = request.POST.get('additional_amenity')
                            exe_amenity_list = exe_amenity_list.split(',')
                            save_exe_amenity(exe_amenity_list,advert_obj)
                            
                            near_attr_list = request.POST.get('near_attraction')
                            near_attr_list = near_attr_list.split(',')
                            save_near_attr(near_attr_list,advert_obj)
                            
                            near_shopnmal = request.POST.get('near_shopnmal')
                            near_shopnmal = near_shopnmal.split(',')

                            near_shonmald = request.POST.get('near_shonmald')
                            near_shonmald = near_shonmald.split(',')
                            
                            zipped_shopmal = zip(near_shopnmal,near_shonmald)
                            save_shpnmal(zipped_shopmal,advert_obj) 

                            cat =advert_obj.category_id.category_name
                            if cat == 'Property':
                                print "SCHOOL",request.POST.get('near_schol')
                                near_schol = request.POST.get('near_schol')
                                near_schol = near_schol.split(',')
                                
                                print "SCHOOL DI SORTING",request.POST.get('near_schold')
                                near_schold = request.POST.get('near_schold')
                                near_schold = near_schold.split(',')
                                
                                print "AFTER SCHOOL"
                                
                                zipped_school = zip(near_schol,near_schold)
                                save_school(zipped_school,advert_obj) 
                                
                                near_hosp = request.POST.get('near_hosp')
                                near_hosp = near_hosp.split(',')

                                near_hospd = request.POST.get('near_hospd')
                                near_hospd = near_hospd.split(',')
                                
                                zipped_hospital = zip(near_hosp,near_hospd)
                                save_hospital(zipped_hospital,advert_obj) 
                            data = {'success': 'true'}

                            print '============after save==========='
                            chars= string.digits
                            pwdSize = 8
                            password = ''.join(random.choice(chars) for _ in range(pwdSize))
                            supplier_obj = Supplier.objects.get(supplier_id = request.POST.get('user_id'))
                            business_obj = Business(
                              category = Category.objects.get(category_id=request.POST.get('categ')),
                              service_rate_card_id = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration')),
                              duration = request.POST.get('selected_duration'),
                              start_date = request.POST.get('duration_start_date'),
                              end_date = request.POST.get('duration_end_date'),
                              supplier= supplier_obj,
                              transaction_code = "TID" + str(password),
                              is_active = 0
                            )
                            business_obj.save()
                            map_subscription(business_obj,advert_obj)

                            premium_service_list = request.POST.get('premium_service')
                            if(premium_service_list!=['']):
                              premium_service_list = str(premium_service_list).split(',')
                              no_of_days_list = request.POST.get('premium_day')
                              no_of_days_list = str(no_of_days_list).split(',')
                              start_date_list = request.POST.get('premium_start_date')
                              start_date_list = str(start_date_list).split(',')

                              end_date_list = request.POST.get('premium_end_date')
                              end_date_list = str(end_date_list).split(',')
                              zipped_wk = zip(premium_service_list,no_of_days_list,start_date_list,end_date_list)
                              save_premium_service(zipped_wk,business_obj)

                            data={
                              'success':'true',
                              'message':"Supplier added successfully",
                              'transaction_code': str(business_obj.transaction_code),
                              'subscriber_id': str(supplier_obj.supplier_id),
                              'business_id' : str(business_obj.business_id)
                              }
                          else:
                            data={
                              'success':'false',
                              'message':final_data['message']
                            } 
                        else:
                            print ""
                            advert_obj=Advert(
                                  supplier_id=Supplier.objects.get(supplier_id=request.POST.get('user_id')),
                                  category_id=Category.objects.get(category_id=request.POST.get('categ')),
                                  advert_name=request.POST.get('advert_title'),
                                  website=request.POST.get('website'),
                                  latitude=request.POST.get('lat'),
                                  longitude=request.POST.get('lng'),
                                  short_description=request.POST.get('short_discription'),
                                  product_description=request.POST.get('product_discription'),
                                  currency_id= Currency.objects.get(currency_id=request.POST.get('currency')) if request.POST.get('currency') else None,
                                  product_price=request.POST.get('product_price'),
                                  discount_description=request.POST.get('discount_discription'),
                                  email_primary=request.POST.get('email_primary'),
                                  email_secondary =request.POST.get('email_secondary'),
                                  address_line_1=request.POST.get('address_line1'),
                                  address_line_2=request.POST.get('address_line2'),
                                  area   =request.POST.get('area'),     
                                  landmark=request.POST.get('landmark'),
                                  state_id= State.objects.get(state_id=request.POST.get('statec')) if request.POST.get('statec') else None, 
                                  city_place_id =City_Place.objects.get(city_place_id=request.POST.get('city')) if request.POST.get('city') else None,
                                  pincode_id=Pincode.objects.get(pincode=request.POST.get('pincode')) if request.POST.get('pincode') else None,
                                  property_market_rate=request.POST.get('pro_mark_rate'),
                                  possesion_status=request.POST.get('possesion_status'),
                                  any_other_details=request.POST.get('any_other_details'),
                                  date_of_delivery=request.POST.get('date_of_delivery'),
                                  distance_frm_railway_station=request.POST.get('dis_rail_stat'),
                                  distance_frm_railway_airport=request.POST.get('dis_airport'),
                                  speciality=request.POST.get('speciality')
                              );
                            advert_obj.save()
                            subcat_list = request.POST.get('subcat_list')
                            subcat_lvl = 1
                            #String to list
                            if subcat_list!='':
                              sc_list = subcat_list.split(',')
                              for subcat in sc_list:
                                  print 'Subcat: ',subcat
                                  ac_map_obj = Advert_Category_Map(
                                      advert_id = advert_obj,
                                      category_id = Category.objects.get(category_id=subcat),
                                      category_level = subcat_lvl 
                                      )
                                  ac_map_obj.save()
                                  print 'Advert Subcat Mapping saved'
                                  subcat_lvl+=1
                            if request.POST['check_image'] == "1":
                                advert_obj.display_image = request.FILES['display_image']
                                advert_obj.save()

                                
                            attachment_list = []
                            attachment_list = request.POST.get('attachments')
                            save_attachments(attachment_list, advert_obj)


                            video_list = []
                            video_list = request.POST.get('ac_attachment')                    
                            save_video(video_list, advert_obj)
                            
                            phone_category_list = request.POST.get('phone_category_list')
                            phone_category_list = phone_category_list.split(',')
                            phone_number_list = request.POST.get('phone_number_list')
                            phone_number_list = phone_number_list.split(',')
                            zipped = zip(phone_category_list,phone_number_list)
                            save_phone_number(zipped,advert_obj) 
                            
                            opening_day_list = request.POST.get('opening_day_list')
                            opening_day_list = opening_day_list.split(',')

                            start_time_list = request.POST.get('start_time_list')
                            start_time_list = start_time_list.split(',')

                            end_time_list = request.POST.get('end_time_list')
                            end_time_list = end_time_list.split(',')
                            
                            zipped_wk = zip(opening_day_list,start_time_list,end_time_list)
                            save_working_hours(zipped_wk,advert_obj) 
                            
                            amenity_list = request.POST.get('amenity_list')
                            amenity_list = amenity_list.split(',')
                            save_amenity(amenity_list,advert_obj)
                            
                            exe_amenity_list = request.POST.get('additional_amenity')
                            exe_amenity_list = exe_amenity_list.split(',')
                            save_exe_amenity(exe_amenity_list,advert_obj)
                            
                            near_attr_list = request.POST.get('near_attraction')
                            near_attr_list = near_attr_list.split(',')
                            save_near_attr(near_attr_list,advert_obj)
                            
                            near_shopnmal = request.POST.get('near_shopnmal')
                            near_shopnmal = near_shopnmal.split(',')

                            near_shonmald = request.POST.get('near_shonmald')
                            near_shonmald = near_shonmald.split(',')
                            
                            zipped_shopmal = zip(near_shopnmal,near_shonmald)
                            save_shpnmal(zipped_shopmal,advert_obj) 

                            cat =advert_obj.category_id.category_name
                            if cat == 'Property':
                                print "SCHOOL",request.POST.get('near_schol')
                                near_schol = request.POST.get('near_schol')
                                near_schol = near_schol.split(',')
                                
                                print "SCHOOL DI SORTING",request.POST.get('near_schold')
                                near_schold = request.POST.get('near_schold')
                                near_schold = near_schold.split(',')
                                
                                print "AFTER SCHOOL"
                                
                                zipped_school = zip(near_schol,near_schold)
                                save_school(zipped_school,advert_obj) 
                                
                                near_hosp = request.POST.get('near_hosp')
                                near_hosp = near_hosp.split(',')

                                near_hospd = request.POST.get('near_hospd')
                                near_hospd = near_hospd.split(',')
                                
                                zipped_hospital = zip(near_hosp,near_hospd)
                                save_hospital(zipped_hospital,advert_obj) 
                            data = {'success': 'true'}

                            chars= string.digits
                            pwdSize = 8
                            password = ''.join(random.choice(chars) for _ in range(pwdSize))
                            supplier_obj = Supplier.objects.get(supplier_id = request.POST.get('user_id'))
                            business_obj = Business(
                              category = Category.objects.get(category_id=request.POST.get('categ')),
                              service_rate_card_id = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration')),
                              duration = request.POST.get('selected_duration'),
                              start_date = request.POST.get('duration_start_date'),
                              end_date = request.POST.get('duration_end_date'),
                              supplier= supplier_obj,
                              transaction_code = "TID" + str(password),
                              is_active = 0
                            )
                            business_obj.save()
                            map_subscription(business_obj,advert_obj)
   
                            data={
                                'success':'true',
                                'message':"Supplier added successfully",
                                'transaction_code': str(business_obj.transaction_code),
                                'subscriber_id': str(supplier_obj.supplier_id)

                              }
                      except Exception, e:
                        data={
                          'success':'false',
                          'message':str(e)
                        }
                    except:
                      data={
                          'success':'false',
                          'message':'Package ' + str(request.POST.get('service')) + ' ' +'(' + str(request.POST.get('selected_duration')) + ' Days)' + ' not available' 
                        }   

    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    print '======data================',data    
    return HttpResponse(json.dumps(data), content_type='application/json')


def check_video_size(user_id,status):
    print '=============user_id========',user_id
    if status=='1':
            subscription_obj = Business.objects.get(supplier=user_id)
            service = subscription_obj.service_rate_card_id.service_name
            print '========servcie========',service
            if(service=='Bronze'):
                size = 10
            if(service=='Silver'):
                size = 20 
            if(service=='Gold'):
                size = 10
            if(service=='Platinum'):
                size = 20
            return 'true';     
    else:
        return 'true';     



def save_phone_number(zipped,advert_id):
##    pdb.set_trace()
    print "IN SAVE PHONE NUMBER"
    try:
        for phone_no_id,phone_no in zipped:
            if phone_no_id != '' and phone_no !='':
                print 'Phone number ID: ',phone_no_id
                phoneno_obj = PhoneNo(
                advert_id = advert_id,
                phone_category_id=PhoneCategory.objects.get(phone_category_id=phone_no_id),
                phone_no=phone_no
                )
                phoneno_obj.save()
            data = {'success': 'true'}
        
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_working_hours(zipped_wk,advert_id):
##    pdb.set_trace()
    print "IN SAVE WORKING HOURS"
    try:
        for wk_day,strt_tm,end_tm in zipped_wk:
            if wk_day != '' and strt_tm != '' and end_tm != '':
                wk_obj = WorkingHours(
                advert_id = advert_id,
                day=wk_day,
                start_time=strt_tm,
                end_time=end_tm
                )
                wk_obj.save()
            data = {'success': 'true'}
        
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def save_amenity(amenity_list,advert_id):
##    pdb.set_trace()
    print "IN SAVE AMENITY"
    try:
        print "Advert Id",advert_id
        for amenity in amenity_list:
            if amenity == 'car':
                ame='Car Parking'
            elif amenity == 'club':
                ame="Club House"
            elif amenity == 'swim':
                ame="Swimming Pool" 
            elif amenity == 'power':
                ame="24 Hours Power Backup" 
            elif amenity == 'gym':
                ame="Gymanasium" 

            elif amenity == 'kids':
                ame="Kids Play Area" 
            elif amenity == 'rain_water':
                ame="Rain Water Harvesting"
            else:
                ame="Garden"
            ame_obj = Amenities(
            advert_id = advert_id,
            amenity=ame
            )
            ame_obj.save()
            data = {'success': 'true'}
        
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def save_exe_amenity(exe_amenity_list,advert_id):
##    pdb.set_trace()
    print "IN SAVE EXTRA AMENITY"
    try:
        for exe_am in exe_amenity_list:
            if exe_am != '' :
                ame_obj = AdditionalAmenities(
                advert_id = advert_id,
                extra_amenity= exe_am
                )
                ame_obj.save()
            data = {'success': 'true'}
        
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def save_near_attr(near_attr_list,advert_id):
##    pdb.set_trace()
    print "IN SAVE NEAR ATTRACTION"
    try:
        for ner_attr in near_attr_list:
            if ner_attr != '' :
                ner_attr_obj = NearByAttraction(
                advert_id = advert_id,
                attraction= ner_attr
                )
                ner_attr_obj.save()
            data = {'success': 'true'}
        
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_shpnmal(zipped_shopmal,advert_id):
##    pdb.set_trace()
    print "IN SAVE SHOP N MAL"
    try:
        for shpnml,shpnmld in zipped_shopmal:
            if shpnml != '' and  shpnmld != '':
                shopnmal_obj = NearestShopping(
                advert_id = advert_id,
                shop_name=shpnml,
                distance_frm_property=shpnmld
                )
                shopnmal_obj.save()
            data = {'success': 'true'}
        
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_school(zipped_school,advert_id):
##    pdb.set_trace()
    print "IN SAVE SCHOOL"
    try:
        for school,schoold in zipped_school:
            if school != '' and  schoold != '':
                school_obj = NearestSchool(
                advert_id = advert_id,
                school_name=school,
                distance_frm_property=schoold
                )
                school_obj.save()
            data = {'success': 'true'}
        
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def save_hospital(zipped_hospital,advert_id):
##    pdb.set_trace()
    print "IN SAVE HOSPITAL"
    try:
        for hospital,hospitald in zipped_hospital:
            if hospital != '' and  hospitald != '':            
                hospital_obj = NearestHospital(
                advert_id = advert_id,
                hospital_name=hospital,
                distance_frm_property=hospitald
                )
                hospital_obj.save()
            data = {'success': 'true'}
        
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def main_listing_image_file_upload(request):
##    pdb.set_trace()
    try:
        if request.method == 'POST':
            attachment_file   =   AdvertImage(advert_image   = request.FILES['file[]'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.advert_image_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except MySQLdb.OperationalError, e:
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_attachments(attachment_list, advert_id):
    try:
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        print attachment_list
        for attached_id in attachment_list:
            attachment_obj = AdvertImage.objects.get(advert_image_id=attached_id)
            attachment_obj.advert_id = advert_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def advert_video_upload(request):
##    pdb.set_trace()
    print "IN UPLOAD VIDEO"
    try:
        if request.method == 'POST':
            attachment_file   =   Advert_Video(advert_video_name   = request.FILES['file[]'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.advert_video_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except MySQLdb.OperationalError, e:
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_video(video_list, advert_id):
    try:
        video_list = video_list.split(',')
        video_list = filter(None, video_list)
        print video_list
        for attached_id in video_list:
            attachment_obj = Advert_Video.objects.get(advert_video_id=attached_id)
            attachment_obj.advert_id = advert_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


# for get the client-list
def get_advert_list(request):
    try:
        # pdb.set_trace()
        print '=request=====',request
        
        print 'Advert List'
        user_id=request.GET.get('user_id')
        advert_list = Advert.objects.filter(supplier_id=request.GET.get('user_id'))
        adv_list = []
        for adv in advert_list: 
            if adv.status == '1':  
                edit = '<a style="text-align: center;letter-spacing: 5px;width:40%;" href="/edit-advert/?advert_id='+str(
                adv.advert_id) + '"<i class="fa fa-pencil "></i> ' + '</a>'
                    
                delete = '<a id="'+str(adv.advert_id)+'" onclick="delete_user_detail(this.id)" style="text-align: center;letter-spacing: 5px;width:15%;"<i class="fa fa-trash "  ></i></a>'    
     


##                mark = '<input type="checkbox" class="checkboxes" value="1" />'
                
                # if adv.status == '1':
                #     status="Active"
                    
                # if adv.status == '0':
                #     status="Inactive"  

                if adv.area == None:
                    area= '--'
                else:
                    area=adv.area  
                map_id = AdvertSubscriptionMap.objects.get(advert_id=str(adv.advert_id))
                business_obj = Business.objects.get(business_id=str(map_id.business_id))
                temp_obj = {
                   'advert_id':adv.advert_id,
                   'advert_name':adv.advert_name,
                    'category':adv.category_id.category_name,
                    'subscription': business_obj.service_rate_card_id.service_name,
                    'start_date':business_obj.start_date,
                    'end_date':business_obj.end_date,
                    'area':area,
                    'action':edit + delete,
                    # 'status':status
                }
                adv_list.append(temp_obj)
            if adv.status == '0':

                active = '<a class="col-md-2" id="'+str(adv.advert_id)+'" onclick="active_service(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;margin-left: 20px !important;" title="Activate" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-repeat"></i></a>' 
     
##                mark = '<input type="checkbox" class="checkboxes" value="1" />'
               
                if adv.area == None:
                    area= '--'
                else:
                    area=adv.area   

                if adv.status == '1':
                    status="Active"
                    
                if adv.status == '0':
                    status="Inactive"    
                
                temp_obj = {
                   'advert_id':adv.advert_id,
                   'advert_name':adv.advert_name,
                    'category':adv.category_id.category_name,
                    'subscription':'--',
                    'start_date':'--',
                    'end_date':'--',
                    'area':area,
##                    'mark':mark,
                    'action':active,
                    'status':status
                }
                adv_list.append(temp_obj)
                    
        data = {'data':adv_list}
    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'none'}
    print '=========dat===========',data    
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def delete_advert(request):
        try:
            print "ADV_ID",request.POST.get('advert_id')
            adv_obj = Advert.objects.get(advert_id=request.POST.get('advert_id'))
            adv_obj.status = '0'
            adv_obj.save()
            advert_inactive_mail(adv_obj)

            data = {'message': 'Advert Inactivated Successfully', 'success':'true'}
        except IntegrityError as e:
          print e
        except Exception,e:
            print e
        print "Final Data: ",data
        return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def active_advert(request):
        # pdb.set_trace()
        try:
            adv_obj = Advert.objects.get(advert_id=request.POST.get('advert_id'))
            adv_obj.status = '1'
            adv_obj.save()
            advert_active_mail(adv_obj)

            data = {'message': 'Advert activated Successfully', 'success':'true'}

        except IntegrityError as e:
          print e
        except Exception,e:
            print e
        print "Final Data: ",data
        return HttpResponse(json.dumps(data), content_type='application/json')

def advert_active_mail(adv_obj):
    gmail_user =  "cityhoopla2016"
    gmail_pwd =  "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    #pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nAdvert " + str(adv_obj.advert_name) + " "+ "for Subscriber " + str(adv_obj.supplier_id.contact_person)+ " " +"has been added successfully.\nTo view complete details visit portal and follow - Customers -> Subscribers -> Adverts\n\n Thank You,"+'\n'+"CityHoopla Team"
        SUBJECT = "Advert Activated Successfully!"
        #server = smtplib.SMTP_SSL()
        server = smtplib.SMTP("smtp.gmail.com", 587) 
        server.ehlo()
        server.starttls()

        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException,e:
        print e
    return 1    

def get_category(request):
##    pdb.set_trace()
    cat_list = []
    try:
        category = Category.objects.filter(category_status='1',level='0')
        for cat in category:
            cat_list.append(
                {'category_id': cat.category_id, 'category': cat.category_name})

    except Exception, e:
        print 'Exception ', e
    return cat_list

# TO GET THE CURRENCY
def get_currency(request):
##    pdb.set_trace()
    currency_list = []
    try:
        currency = Currency.objects.filter(status='1')
        for cur in currency:
            currency_list.append(
                {'currency_id': cur.currency_id, 'currency': cur.currency})

    except Exception, e:
        print 'Exception ', e
    return currency_list

def edit_advert(request):
    # pdb.set_trace()
    try:
        tax_list = Tax.objects.all()
        service_rate_card_list = ServiceRateCard.objects.filter(service_rate_card_status='1').values('service_name').distinct()

        advert_obj = Advert.objects.get(advert_id=request.GET.get('advert_id'))
        
        if advert_obj.currency_id == None:
            cur = '0'
##            cur1 = ""
        else:
            cur = str(advert_obj.currency_id.currency_id)
##            cur1 = advert_obj.currency_id.currency
         
        if advert_obj.state_id == None:
            state = '0'
        else:
            state = advert_obj.state_id.state_id  
          
        if advert_obj.city_place_id == None:
            city = '0'
        else:
            city = advert_obj.city_place_id.city_place_id
            
        if advert_obj.pincode_id == None:
            pincode = '0'
        else:
            pincode = advert_obj.pincode_id.pincode_id
            
        if advert_obj.display_image == "":
            display_image = ""
            file_name  = ""
        else:
            display_image = SERVER_URL + advert_obj.display_image.url
            file_name = display_image[51:]

        img_data = ""
        image_list = []
        attach_id=[]
        attch_paths =[]
        attch_files =[]
        sub_category1_list = []
        sub_category2_list = []
        sub_category3_list = []
        sub_category4_list = []
        sub_category5_list = []
        att = ""
        img_list = AdvertImage.objects.filter(advert_id = advert_obj)
        if img_list.count()>0:
            for img in img_list:
                attch_path = SERVER_URL + img.advert_image.url
                attch_file = str(img.advert_image)
                attahment_id =str(img.advert_image_id)
                
                attch_paths.append(attch_path)
                attch_files.append(attch_file)
                attach_id.append(attahment_id)
                att=','.join(attach_id)


        video_list = []
        video_id=[]
        video_paths =[]
        video_files =[]
        vi = ""
        video_list = Advert_Video.objects.filter(advert_id = advert_obj)
        if video_list.count()>0:
            for vid in video_list:
                vid_path = SERVER_URL + vid.advert_video_name.url
                vid_file = str(vid.advert_video_name)
                vid_id =str(vid.advert_video_id)
                
                video_paths.append(vid_path)
                video_files.append(vid_file)
                video_id.append(vid_id)
                vi=','.join(video_id)


        category = Category.objects.get(category_id=str(advert_obj.category_id))        
        sub_category1 = Category.objects.filter(has_category=category,level='1')
        if sub_category1:
            for cat in sub_category1:
                category1_list = {'category_name':cat.category_name}

                sub_category1_list.append(category1_list)

        sub_category2 = Category.objects.filter(has_category=category,level='2')
        if sub_category2:
            for cat in sub_category2:
                category2_list = {'category_name':cat.category_name}    
                sub_category2_list.append(category2_list) 

        sub_category3 = Category.objects.filter(has_category=category,level='3')
        if sub_category3:
            for cat in sub_category3:
                category3_list = {'category_name':cat.category_name}    
                sub_category3_list.append(category3_list)

        sub_category4 = Category.objects.filter(has_category=category,level='4')
        if sub_category4:
            for cat in sub_category4:
                category4_list = {'category_name':cat.category_name}    
                sub_category4_list.append(category4_list)

        sub_category5 = Category.objects.filter(has_category=category,level='5')
        if sub_category5:
            for cat in sub_category5:
                category5_list = {'category_name':cat.category_name}    
                sub_category5_list.append(category5_list)       

        subcat_list = Advert_Category_Map.objects.filter(advert_id = advert_obj)
        print 'Subcat List: ',subcat_list
        print 'Subcat L1: ',sub_category1_list
        print 'Subcat L2: ',sub_category2_list
        print 'Subcat L3: ',sub_category3_list
        print 'Subcat L4: ',sub_category4_list
        print 'Subcat L5: ',sub_category5_list

        advert_dict = {
            'success': 'true',
            'user_id':advert_obj.supplier_id.supplier_id,
            'adv_id':advert_obj.advert_id,
            'lat':advert_obj.latitude,
            'lng':advert_obj.longitude,
            'cat_id':advert_obj.category_id.category_name,
            'categ': advert_obj.category_id.category_id,
            'advert_tit': advert_obj.advert_name,
            'website': advert_obj.website or '',
            'short_discription': advert_obj.short_description,
            'product_discription': advert_obj.product_description or '',
            'discount_discription': advert_obj.discount_description or '',
            'currency': cur ,
##            'currency1': cur1 ,
            'product_price': advert_obj.product_price or '',
            'display_image': display_image,
            'filename': file_name,
            'email_primary': advert_obj.email_primary,
            'email_secondary': advert_obj.email_secondary or '',
            'address_line1': advert_obj.address_line_1,
            'address_line2': advert_obj.address_line_2 or '',
            'area': advert_obj.area or '',
            'landmark': advert_obj.landmark or '',
            'statec': state,
            'city': city,
            'pincode': pincode,
            'any_other_details': advert_obj.any_other_details or '' ,
            'pro_mark_rate':advert_obj.property_market_rate or '',
            'possesion_status':advert_obj.possesion_status,
            'date_of_delivery':advert_obj.date_of_delivery,
            'dis_rail_stat':advert_obj.distance_frm_railway_station,
            'dis_airport':advert_obj.distance_frm_railway_airport,
            'attachment': attch_paths,
            'file_name':attch_files,
            'attachment_id':att,
            'video_path': video_paths,
            'video_file_name':video_files,
            'video_id':vi,
            'speciality':advert_obj.speciality
        }
        
        city_objs = ""
        city_objs=City_Place.objects.filter(state_id=advert_obj.state_id)
        print "==========city_objs",city_objs
        
        pin_objs = ""
        pin_objs=Pincode.objects.filter(city_id=advert_obj.city_place_id.city_id)
        
        cur_objs = ""
        #cur_objs = Currency.objects.filter(city_id=advert_obj.city_id)

        phone_number = PhoneNo.objects.filter(advert_id=advert_obj)
        phone_list = []
        for ph_no in phone_number:
            phone_data = {
                'phone_cat': ph_no.phone_category_id.phone_category_name,    
                'phone_number':ph_no.phone_no
                }
            phone_list.append(phone_data)
            

        workout_list1 = []
        wkhr_list = WorkingHours.objects.filter(advert_id = advert_obj)
        if wkhr_list>0:
            for wkday in wkhr_list:
                workinghr_data = {
                    'wk_day':wkday.day,
                    'wk_strt_tm':wkday.start_time,
                    'wk_end_tm':wkday.end_time
                }
                workout_list1.append(workinghr_data)    
        print "wk",workout_list1

         
        ame = ""
        ame1 =""
        ame2 =""
        ame3 =""
        ame4 =""
        ame5 =""
        ame6 =""
        ame7 =""  
        #amenity_list = []
        amenity_lis = Amenities.objects.filter(advert_id=advert_obj)
        if amenity_lis.count()>0:
            for amenities in amenity_lis:
                if amenities.amenity == 'Car Parking':
                    ame='Car Parking'
                elif amenities.amenity == 'Club House':
                    ame1='Club House'
                elif amenities.amenity == 'Swimming Pool':
                    ame2="Swimming Pool" 
                elif amenities.amenity == '24 Hours Power Backup':
                    ame3="24 Hours Power Backup" 
                elif amenities.amenity == 'Gymanasium':
                    ame4="Gymanasium" 
                elif amenities.amenity == 'Kids Play Area':
                    ame5="Kids Play Area" 
                elif amenities.amenity == 'Rain Water Harvesting':
                    ame6="Rain Water Harvesting"
                elif amenities.amenity == 'Garden':
                    ame7="Garden"
        
        amenity_list = {'ame':ame,'ame1':ame1,'ame2':ame2,'ame3':ame3,'ame4':ame4,'ame5':ame5,'ame6':ame6,'ame7':ame7}
        
        
        extra_ame = AdditionalAmenities.objects.filter(advert_id=advert_obj)
        extra_ame_list = []
        
        if extra_ame.count()>0:
            for ex_am in extra_ame:
                ex_am_data = {   
                    'ex_amenity':ex_am.extra_amenity
                    }
                extra_ame_list.append(ex_am_data)
            print  extra_ame_list

                
        near_attr = NearByAttraction.objects.filter(advert_id=advert_obj)
        attr_list = []
        
        if near_attr.count()>0:
            for attr in near_attr:
                attr_data = {   
                    'attraction':attr.attraction
                    }
                attr_list.append(attr_data)
            print  attr_list       

        shop_data = ""  
        shop_list1 = []      
        shop_list = NearestShopping.objects.filter(advert_id = advert_obj)
        if shop_list.count()>0:
            for shop in shop_list:
                print "IN SHOP VIEW"
                shop_data = {
                    'shop_name':shop.shop_name,
                    'dist_frm_prp':shop.distance_frm_property,
                }
                shop_list1.append(shop_data) 
            print "shopLIS",shop_list1       
        
        school_data = ""
        school_list1 = [] 
        school_list = NearestSchool.objects.filter(advert_id = advert_obj)
        if school_list.count()>0:
            for school in school_list:
                school_data = {
                    'school_name':school.school_name,
                    'dist_frm_school':school.distance_frm_property
                }
                school_list1.append(school_data)    
        
        hospital_data =""
        hospital_list1 = [] 
        hospital_list = NearestHospital.objects.filter(advert_id = advert_obj)
        if hospital_list.count()>0:
            for hospital in hospital_list:
                hospital_data = {
                    'hospital_name':hospital.hospital_name,
                    'dist_frm_hospital':hospital.distance_frm_property
                }
                hospital_list1.append(hospital_data) 

        duration_list = {}
        category = ''
        duration = 0
        start_date = ''
        end_date = ''
        subscription = ''
        service_list = []
        payment_mode = ''
        note = ''
        paid_amount = ''
        payable_amount = ''
        total_amount = ''
        tax_type = '0'
        service_code = ''

        advert_map = AdvertSubscriptionMap.objects.get(advert_id=str(advert_obj))
        try:
          business_obj = Business.objects.get(business_id=str(advert_map.business_id))
          category = business_obj.category.category_name
          subscription = business_obj.service_rate_card_id.service_name
          duration = business_obj.duration
          if duration=='3':
            duration_list = {3}
          elif duration=='7':
            duration_list = {3,7}
          elif duration=='30':
            duration_list = {3,7,30}
          elif duration=='90':
            duration_list = {3,7,30,90}
          elif duration=='180':
            duration_list = {3,7,30,90,180}

          start_date = business_obj.start_date
          end_date = business_obj.end_date
          premium_service_list = PremiumService.objects.filter(business_id=business_obj)
          for service in premium_service_list:
            service_list = {'service':service}
        except Exception,e:
          pass

        advert_service_list, item_ids = [], []
        for item in AdvertRateCard.objects.filter(advert_rate_card_status='1'):
            if item.advert_service_name not in item_ids:
                advert_service_list.append(str(item.advert_rate_card_id))
                item_ids.append(item.advert_service_name)

        print '=======advert service list===',advert_service_list
        advert_service_list = AdvertRateCard.objects.filter(advert_rate_card_id__in=advert_service_list)        

        advert_length = len(advert_service_list)
        final_advert_list = []
        for advert in advert_service_list:
          advert_rate_card_id = str(advert.advert_rate_card_id)
          advert_service_name = advert.advert_service_name
          try:
            premium_service_obj = PremiumService.objects.get(business_id=business_obj,premium_service_name=advert.advert_service_name)     
            advert_start_date = premium_service_obj.start_date
            advert_end_date = premium_service_obj.end_date
            advert_days = premium_service_obj.no_of_days
            status = 'true'
          
          except:
            advert_start_date = ''
            advert_end_date = ''
            advert_days = ''
            status = 'false'
          advert_list = {'advert_rate_card_id':advert_rate_card_id,'advert_service_name':advert_service_name,'advert_start_date':advert_start_date,'advert_end_date':advert_end_date,'advert_days':advert_days,'status':status}
          final_advert_list.append(advert_list)

        try:
          payement_obj = PaymentDetail.objects.get(business_id=business_obj)
          payment_mode = payement_obj.payment_mode
          note = payement_obj.note
          paid_amount = payement_obj.paid_amount
          payable_amount = payement_obj.payable_amount
          total_amount = payement_obj.total_amount
          tax_type = payement_obj.tax_type
        except Exception, e:
          print '===========e==============',e
          pass  
   
        data = {'username':request.session['login_user'],'service_rate_card_list':service_rate_card_list,'subscription':subscription,'duration':duration,'duration_list':duration_list,'start_date':start_date,'end_date':end_date,'service_list':service_list,'advert_length':advert_length,'final_advert_list':final_advert_list,'payment_mode':payment_mode,'note':note,'paid_amount':paid_amount,'payable_amount':payable_amount,'total_amount':total_amount,'tax_type':tax_type,'tax_list':tax_list,'sub_category1_list':sub_category1_list,'sub_category2_list':sub_category2_list,'sub_category3_list':sub_category3_list,'sub_category4_list':sub_category4_list,'sub_category5_list':sub_category5_list,'advert':advert_dict,'category_list':get_category(request),'subcat_list':subcat_list,'selected_pincode':pin_objs,'selected_city':city_objs,'phone_list':phone_list,'workout_list':workout_list1,'attractions':attr_list,'shop_list':shop_list1,'amenity_list':amenity_list,'extra_amenity':extra_ame_list,
           'school_list':school_list1,'hospital_list':hospital_list1,'currency':get_currency(request),'currency':get_currency(request),'phone_category':get_phone_category(request),'state_list':get_state(request)}
          
    except Exception,e:
        print 'Exception:',e
        data = {'data':'none'}
    print '====================data===============',data        
    return render(request,'Admin/edit_advert.html',data)  



@csrf_exempt
def update_advert(request):
    print 'in update advert'
##    pdb.set_trace()
    try:
        if request.method == "POST":
            # try:
            #     advert_video = request.FILES['advert_video']
            #     print '========advert_video======',advert_video
            # except:
            #     advert_video = 0    

            # if(check_video_size(request.POST.get('user_id'),request.POST['check_video'])):
                    advert_obj = Advert.objects.get(advert_id=request.POST.get('adv_id'))
                    
                    advert_obj.advert_name = request.POST.get('advert_title')
                    advert_obj.website =  request.POST.get('website')    
                    advert_obj.latitude =  request.POST.get('lat')    
                    advert_obj.longitude =  request.POST.get('lng')    
                    advert_obj.short_description=request.POST.get('short_discription')
                    advert_obj.product_description=request.POST.get('product_discription')
                    advert_obj.product_price=request.POST.get('product_price')
                    if request.POST.get('currency') != '0':
                        advert_obj.currency_id= Currency.objects.get(currency_id=request.POST.get('currency')) if request.POST.get('currency') else None
                    advert_obj.discount_description=request.POST.get('discount_discription')
                    advert_obj.email_primary=request.POST.get('email_primary')
                    advert_obj.email_secondary =request.POST.get('email_secondary')
                    advert_obj.address_line_1=request.POST.get('address_line1')
                    advert_obj.address_line_2=request.POST.get('address_line2')
                    advert_obj.area   =request.POST.get('area')    
                    advert_obj.landmark=request.POST.get('landmark')
                    if request.POST.get('statec') != '0':
                        advert_obj.state_id= State.objects.get(state_id=request.POST.get('statec')) if request.POST.get('statec') else None
                    if request.POST.get('city') != '0':
                        advert_obj.city_place_id =City_Place.objects.get(city_place_id=request.POST.get('city')) if request.POST.get('city') else None
                    print "PIN",request.POST.get('pincode')
                    if request.POST.get('pincode') != '0':
                        advert_obj.pincode_id=Pincode.objects.get(pincode=request.POST.get('pincode')) if request.POST.get('pincode') else None
                    advert_obj.property_market_rate=request.POST.get('pro_mark_rate')
                    advert_obj.possesion_status=request.POST.get('possesion_status')
                    advert_obj.any_other_details=request.POST.get('any_other_details')
                    advert_obj.date_of_delivery=request.POST.get('date_of_delivery')    
                    advert_obj.distance_frm_railway_station=request.POST.get('dis_rail_stat')
                    advert_obj.distance_frm_railway_airport=request.POST.get('dis_airport')  
                    advert_obj.speciality=request.POST.get('speciality')        
                    advert_obj.save()
                    
                    if request.POST['check_image'] == "1":
                        advert_obj.display_image = request.FILES['display_image']
                        advert_obj.save()


                    attachment_list = []
                    attachment_list = request.POST.get('attachment1')
                    save_attachments(attachment_list, advert_obj)


                    attachment_list1 = []
                    attachment_list1 = request.POST.get('attachment2')
                    save_video(attachment_list1, advert_obj)

                    phone_number = PhoneNo.objects.filter(advert_id=advert_obj)
                    phone_number.delete()
                    
                    phone_category_list = request.POST.get('phone_category_list')
                    phone_category_list = phone_category_list.split(',')
                    phone_number_list = request.POST.get('phone_number_list')
                    phone_number_list = phone_number_list.split(',')
                    zipped = zip(phone_category_list,phone_number_list)
                    save_phone_number(zipped,advert_obj) 
                    
                    wkhr_list = WorkingHours.objects.filter(advert_id = advert_obj)
                    wkhr_list.delete()
                    
                    opening_day_list = request.POST.get('opening_day_list')
                    opening_day_list = opening_day_list.split(',')

                    start_time_list = request.POST.get('start_time_list')
                    start_time_list = start_time_list.split(',')

                    end_time_list = request.POST.get('end_time_list')
                    end_time_list = end_time_list.split(',')
                    
                    zipped_wk = zip(opening_day_list,start_time_list,end_time_list)
                    save_working_hours(zipped_wk,advert_obj) 
                    
                    amenity_lis = Amenities.objects.filter(advert_id=advert_obj)
                    amenity_lis.delete()
                    
                    amenity_list = request.POST.get('amenity_list')
                    amenity_list = amenity_list.split(',')
                    save_amenity(amenity_list,advert_obj)
                    
                    extra_ame = AdditionalAmenities.objects.filter(advert_id=advert_obj)
                    extra_ame.delete()
                    
                    exe_amenity_list = request.POST.get('additional_amenity')
                    exe_amenity_list = exe_amenity_list.split(',')
                    save_exe_amenity(exe_amenity_list,advert_obj)
                    
                    near_attr = NearByAttraction.objects.filter(advert_id=advert_obj)
                    near_attr.delete()
                    
                    near_attr_list = request.POST.get('near_attraction')
                    near_attr_list = near_attr_list.split(',')
                    save_near_attr(near_attr_list,advert_obj)
                    
                    shop_list = NearestShopping.objects.filter(advert_id = advert_obj)
                    shop_list.delete()
                    
                    near_shopnmal = request.POST.get('near_shopnmal')
                    near_shopnmal = near_shopnmal.split(',')

                    near_shonmald = request.POST.get('near_shonmald')
                    near_shonmald = near_shonmald.split(',')
                    
                    zipped_shopmal = zip(near_shopnmal,near_shonmald)
                    save_shpnmal(zipped_shopmal,advert_obj) 
                    
                    
                    cat =advert_obj.category_id.category_name
                    if cat == 'Property':
                        near_schol = request.POST.get('near_schol')
                        near_schol = near_schol.split(',')
                        
                        near_schold = request.POST.get('near_schold')

                        near_schold = near_schold.split(',')
                        
                        zipped_school = zip(near_schol,near_schold)
                        save_school(zipped_school,advert_obj) 
                        
                        hospital_list = NearestHospital.objects.filter(advert_id = advert_obj)
                        hospital_list.delete()
                        
                        near_hosp = request.POST.get('near_hosp')
                        near_hosp = near_hosp.split(',')

                        near_hospd = request.POST.get('near_hospd')
                        near_hospd = near_hospd.split(',')
                        
                        zipped_hospital = zip(near_hosp,near_hospd)
                        save_hospital(zipped_hospital,advert_obj) 
                    advert_edit_mail(advert_obj)
                    data = {'success': 'true'}
            # else:
            #     data = {'success': 'false'}

        else:
            data = {'success': 'false'}
    except Exception,e:
        print 'Exception:',e
        data = {'data':'none'}
    print '==data=======',data    
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def remove_advert_image(request):
##    pdb.set_trace()
    print "in the remove image"
    print request.GET
    try:
        image_id=request.GET.get('image_id')
##        temp=str(image_id).replace("L]", "")
##        print 'image id : - >',temp.replace("L]", "")
        image= AdvertImage.objects.get(advert_image_id=image_id)
        image.delete()
        
        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')



@csrf_exempt
def remove_advert_video(request):
    # pdb.set_trace()
    print "in the remove video"
    print request.GET
    try:
        image_id=request.GET.get('image_id')
##        temp=str(image_id).replace("L]", "")
##        print 'image id : - >',temp.replace("L]", "")
        image= Advert_Video.objects.get(advert_video_id=image_id)
        image.delete()
        
        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_advert_image(request):
    print "in the upload image"
##    pdb.set_trace()
    try:
        print request.FILES['file']
        if request.method == 'POST':
            attachment_file   =   AdvertImage(advert_image   = request.FILES['file'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.advert_image_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except Exception as e:
        print 'Error ------------> ',e
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_advert_video(request):
    print "in the upload video"
##    pdb.set_trace()
    try:
        print request.FILES['file']
        if request.method == 'POST':
            attachment_file   =   Advert_Video(advert_video_name   = request.FILES['file'])
            attachment_file.save()
            data = {'success' : 'true','attachid':attachment_file.advert_video_id}
            print data
        else:
            data = {'success': 'false'}
            print data
    except Exception as e:
        print 'Error ------------> ',e
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def advert_add_mail(advert_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nAdvert " + str(advert_obj.advert_name) + " "+ "for Subscriber " + str(advert_obj.supplier_id.contact_person)+ " " +"has been added successfully.\nTo view complete details visit portal and follow - Customers -> Subscribers -> Adverts\n\n Thank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Advert Added Successfully!"
		#server = smtplib.SMTP_SSL()
		server = smtplib.SMTP("smtp.gmail.com", 587) 
		server.ehlo()
		server.starttls()

		server.login(gmail_user, gmail_pwd)
		message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
		server.sendmail(FROM, TO, message)
		server.quit()
	except SMTPException,e:
		print e
	return 1		



def advert_edit_mail(advert_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nAdvert " + str(advert_obj.advert_name) + " "+ "for Subscriber " + str(advert_obj.supplier_id.contact_person)+ " " +"has been updated successfully.\nTo view complete details visit portal and follow - Customers -> Subscribers -> Adverts\n\n Thank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Advert Updated Successfully!"
		#server = smtplib.SMTP_SSL()
		server = smtplib.SMTP("smtp.gmail.com", 587) 
		server.ehlo()
		server.starttls()

		server.login(gmail_user, gmail_pwd)
		message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
		server.sendmail(FROM, TO, message)
		server.quit()
	except SMTPException,e:
		print e
	return 1		


def advert_inactive_mail(advert_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nAdvert " + str(advert_obj.advert_name) + " "+ "for Subscriber " + str(advert_obj.supplier_id.contact_person)+ " " +"has been deactivated successfully.\n\n Thank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Advert Deactivated Successfully!"
		#server = smtplib.SMTP_SSL()
		server = smtplib.SMTP("smtp.gmail.com", 587) 
		server.ehlo()
		server.starttls()

		server.login(gmail_user, gmail_pwd)
		message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
		server.sendmail(FROM, TO, message)
		server.quit()
	except SMTPException,e:
		print e
	return 1		

@csrf_exempt
def check_category(request):
    print request.POST
    try:
        cat_obj = Category.objects.filter(has_category=request.POST.get('category_id'),level=request.POST.get('cat_level'))
        print cat_obj
        cat_list = []      
        if cat_obj:
            for cat in cat_obj:
                options_data = '<option value=' + str(cat.category_id) + '>' + cat.category_name + '</option>'
                cat_list.append(options_data)
            data = {'category_list': cat_list}
        else:
            data={'success':'false'}   
        print data
    except Exception, e:
        print e
    return HttpResponse(json.dumps(data), content_type='application/json')    


@csrf_exempt
def check_subscription(request):
    print request.POST
    try:
        business_obj = Business.objects.get(supplier=request.POST.get('subscriber_id'),is_active=0)
        subscription_id = str(business_obj.business_id)
        subscription_name = business_obj.service_rate_card_id.service_name
        duration = str(business_obj.start_date) + " to " + str(business_obj.end_date)
        data = {'duration':duration,'subscription_id': subscription_id,'subscription_name':subscription_name,'success':'true'}
    except Exception, e:
        print '====e===========',e
        data={'success':'false'}
    print '=========data===========',data       
    return HttpResponse(json.dumps(data), content_type='application/json') 


def map_subscription(subscription_id,advert_obj):
  business_obj = Business.objects.get(business_id=str(subscription_id))
  business_obj.is_active = 1
  business_obj.save()
  sub_obj = AdvertSubscriptionMap(
    business_id = Business.objects.get(business_id=str(subscription_id)),
    advert_id = advert_obj
  )
  sub_obj.save()



def check_subscription_detail(premium_service_list,premium_day):
  premium_service_list = premium_service_list
  premium_service_list = str(premium_service_list).split(',')

  premium_day = premium_day
  premium_day = str(premium_day).split(',')
  zipped_wk = zip(premium_service_list,premium_day)
  service_list= []
  duration_list= []

  false_status = 0  

  for serv,day in zipped_wk:
    try:
      service_rate_card_obj = AdvertRateCard.objects.get(advert_service_name=serv,duration=day)

    except Exception,e:
      service_list.append(str(serv))
      duration_list.append(day)
      false_status = 1
  if false_status == 0:
    data={
        'success':'true',
    }
  else:
    zipped_list = zip(service_list,duration_list)
    message = "Package "
    for i,j in zipped_list:
      message = message + str(i) + " " + "("+str(j)+" Days)" + ", "  
    

    message = message[:-2] + ' not available'

    data={
        'success':'false',
        'message':message
      }
  return data                       


@csrf_exempt
def advert_detail(request):
  try:
    print '==========request=========',request.POST
    advert_map_obj = AdvertSubscriptionMap.objects.get(business_id=request.POST.get('business_id'))
    chars= string.digits
    pwdSize = 8
    password = ''.join(random.choice(chars) for _ in range(pwdSize))
    supplier_obj = Supplier.objects.get(supplier_id=str(advert_map_obj.advert_id.supplier_id))      


    payment_obj = PaymentDetail(
      business_id = Business.objects.get(business_id = str(advert_map_obj.business_id)),
      note = request.POST.get('note'),
      payment_mode = request.POST.get('payment_mode'),
      paid_amount = request.POST.get('paid_amount'),
      payable_amount = request.POST.get('payable_amount'),
      total_amount = request.POST.get('generated_amount'),
      tax_type = Tax.objects.get(tax_type=request.POST.get('selected_tax_type')),
      payment_code = "PMID" + str(password)
      )
    payment_obj.save()
    print '=================after payment=============='
    data={
    'success':'true',
    'message':"Supplier added successfully",
    'payment_code': str(payment_obj.payment_code),
    'user_id': str(supplier_obj.supplier_id)
      }

  except Exception, e:
    data={
        'success':'false',
        'message':str(e)
    }
  print '=========data============',data  
  return HttpResponse(json.dumps(data),content_type='application/json')  



def save_premium_service(zipped_wk,business_obj):
    try:
        for wk_serv,wk_day,strt_tm,end_tm in zipped_wk:
            wk_obj = PremiumService(
            business_id = business_obj,
            premium_service_name=wk_serv,
            no_of_days=wk_day,
            start_date=strt_tm,
            end_date=end_tm,
            premium_service_status='1',
            premium_service_created_date=datetime.now(),
            premium_service_created_by="Admin",
            premium_service_updated_by="Admin",
            premium_service_updated_date=datetime.now()
            )
            wk_obj.save()
            data = {'success': 'true'}
        
    except Exception, e:
        print 'Exception ', e    
    return HttpResponse(json.dumps(data), content_type='application/json')      


@csrf_exempt
def update_subscription(request):
  print '========request===========',request.POST
  try:
    serv_obj = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration'))
    try:
      advert_map_obj = AdvertSubscriptionMap.objects.get(advert_id= request.POST.get('adv_id'))
      premium_service_list = request.POST.get('premium_service')
      no_of_days_list = request.POST.get('premium_day_list')
      if(premium_service_list):
        final_data = check_subscription_detail(premium_service_list,no_of_days_list)
        if final_data['success']=='true':
   
          business_obj = Business.objects.get(business_id=str(advert_map_obj.business_id))
          business_obj.category = Category.objects.get(category_id=request.POST.get('category')) 
          business_obj.service_rate_card_id = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration'))
          business_obj.duration = request.POST.get('selected_duration')
          business_obj.start_date = request.POST.get('duration_start_date')
          business_obj.end_date = request.POST.get('duration_end_date')
          business_obj.save()

          premium_service_obj = PremiumService.objects.filter(business_id=business_obj).delete()
          premium_service_list = request.POST.get('premium_service')
          premium_service_list = str(premium_service_list).split(',')
          no_of_days_list = request.POST.get('premium_day_list')
          no_of_days_list = str(no_of_days_list).split(',')
          start_date_list = request.POST.get('premium_start_date')
          start_date_list = str(start_date_list).split(',')
          end_date_list = request.POST.get('premium_end_date')
          end_date_list = str(end_date_list).split(',')
          zipped_wk = zip(premium_service_list,no_of_days_list,start_date_list,end_date_list)
          save_premium_service(zipped_wk,business_obj)
          data={
            'success':'true',
            'message':"Supplier profile edited successfully",
            'transaction_code' : str(business_obj.transaction_code),
          }
          
        else:
          data={
            'success':'false',
            'message':final_data['message']
          } 
      else:
 
        business_obj = Business.objects.get(business_id=str(advert_map_obj.business_id))
        business_obj.category = Category.objects.get(category_id=request.POST.get('category')) 
        business_obj.service_rate_card_id = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration'))
        business_obj.duration = request.POST.get('selected_duration')
        business_obj.start_date = request.POST.get('duration_start_date')
        business_obj.end_date = request.POST.get('duration_end_date')
        business_obj.save()
        premium_service_obj = PremiumService.objects.filter(business_id=business_obj).delete()

        data={
            'success':'true',
            'message':"Supplier profile edited successfully",
            'transaction_code' : str(business_obj.transaction_code),
        } 
    except Exception, e:
      data={
        'success':'false',
        'message':str(e)
      }
  except:
    data={
        'success':'false',
        'message':'Package ' + str(request.POST.get('service')) + ' ' +'(' + str(request.POST.get('selected_duration')) + ' Days)' + ' not available' 
      }
  return HttpResponse(json.dumps(data),content_type='application/json')


@csrf_exempt
def save_subscriber_detail(request):
  try:
    advert_map_obj = AdvertSubscriptionMap.objects.get(advert_id = Advert.objects.get(advert_id=request.POST.get('adv_id'))) 
    try:
      payment_obj = PaymentDetail.objects.get(business_id = str(advert_map_obj.business_id))
      payment_obj.note = request.POST.get('note')
      payment_obj.payment_mode = request.POST.get('payment_mode')
      if(request.POST.get('paid_amount')!='None'):
        payment_obj.paid_amount = request.POST.get('paid_amount')
      else:
        payment_obj.paid_amount = ''
      payment_obj.payable_amount = request.POST.get('payable_amount')
      payment_obj.total_amount = request.POST.get('generated_amount')
      try:
        payment_obj.tax_type = Tax.objects.get(tax_type=request.POST.get('selected_tax_type'))
      except:
        pass
      payment_obj.save()
    except:
      chars= string.digits
      pwdSize = 8
      password = ''.join(random.choice(chars) for _ in range(pwdSize))
      payment_obj = PaymentDetail(
      business_id = Business.objects.get(business_id=str(advert_map_obj.business_id)),
      note = request.POST.get('note'),
      payment_mode = request.POST.get('payment_mode'),
      paid_amount = request.POST.get('paid_amount'),
      payable_amount = request.POST.get('payable_amount'),
      total_amount = request.POST.get('generated_amount'),
      tax_type = Tax.objects.get(tax_type=request.POST.get('selected_tax_type')),
      payment_code = "PMID" + str(password)
      )
      payment_obj.save()  
    data={
    'success':'true',
    'message':"Supplier added successfully",
    'payment_code': str(payment_obj.payment_code),
    }
  except Exception, e:
    data={
        'success':'false',
        'message':str(e)
    }
  print '=======data============',data
  return HttpResponse(json.dumps(data),content_type='application/json')
