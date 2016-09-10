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

# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction
import pdb
import csv
import json
# importing exceptions
from django.db import IntegrityError

import operator
from django.db.models import Q
from datetime import date, timedelta

# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import string
import random
from django.views.decorators.cache import cache_control
import ast

from geopy.geocoders import Nominatim
import datetime
from datetime import datetime
from datetime import date, timedelta

#SERVER_URL = "http://52.40.205.128"
SERVER_URL = "http://192.168.0.151:9090"

@csrf_exempt
def get_advert_list(request):
    supplier_id = request.GET.get('supplier_id')
    advert_obj = Advert.objects.filter(supplier_id = supplier_id)
    advert_list = []
    for advert in advert_obj:
        advert_data = {
            'advert_obj_name' : advert.advert_name,
            'advert_obj_id' : advert.advert_id
        }
        advert_list.append(advert_data)
    data = {
        'success': 'true',
        'advert_list':advert_list
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def get_advert_date(request):
    advert_id = request.GET.get('advert_id')
    advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
    start_date = advert_sub_obj.business_id.start_date
    start_date = start_date
    pre_date = datetime.now().strftime("%m/%d/%Y")
    data = {
        'success': 'true',
        'start_date':str(start_date),
        'present_date':str(pre_date)
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_advert_health(request):
    try:
        data = {}
        final_list = []
        try:
            if request.GET.get('advert_id'):
                from_date = request.GET.get('from_date')
                to_date = request.GET.get('to_date')
                from_date = datetime.strptime(from_date, "%m/%d/%Y")
                to_date = datetime.strptime(to_date, "%m/%d/%Y")
                from_date = from_date.strftime("%Y-%m-%d")
                to_date = to_date.strftime("%Y-%m-%d")
                advert = Advert.objects.get(advert_id=request.GET.get('advert_id'))
                coupon_objs = CouponCode.objects.filter(advert_id=str(advert.advert_id),creation_date__range=[from_date, to_date])
                advert_fav_objs = AdvertFavourite.objects.filter(advert_id=str(advert.advert_id),creation_date__range=[from_date, to_date])
                advert_like_objs = AdvertLike.objects.filter(advert_id=str(advert.advert_id),creation_date__range=[from_date, to_date])
                if advert.advert_views:
                    advert_views = advert.advert_views
                else:
                    advert_views = 0
                advert_data = {
                    'advert_id': advert.advert_id,
                    'advert_title': advert.advert_name,
                    'advert_views': advert_views,
                    'advert_likes': advert_like_objs.count(),
                    'advert_favourites': advert_fav_objs.count(),
                    'advert_calls': '0',
                    'advert_call_backs': '0',
                    'advert_emails': '0',
                    'advert_coupons': coupon_objs.count(),
                    'advert_reviews': '0',
                    'advert_sms': '0',
                    'advert_whatsapp': '0',
                    'advert_facebook': '0',
                    'advert_twitter': '0'
                }
                final_list.append(advert_data)
            else:
                advert_list = Advert.objects.filter(status = '1')
                for advert in advert_list:
                    coupon_objs = CouponCode.objects.filter(advert_id = str(advert.advert_id))
                    advert_fav_objs = AdvertFavourite.objects.filter(advert_id = str(advert.advert_id))
                    advert_like_objs = AdvertLike.objects.filter(advert_id = str(advert.advert_id))
                    if advert.advert_views:
                        advert_views = advert.advert_views
                    else:
                        advert_views = 0
                    advert_data={
                        'advert_id':advert.advert_id,
                        'advert_title':advert.advert_name,
                        'advert_views':advert_views,
                        'advert_likes':advert_like_objs.count(),
                        'advert_favourites':advert_fav_objs.count(),
                        'advert_calls':'0',
                        'advert_call_backs':'0',
                        'advert_emails':'0',
                        'advert_coupons':coupon_objs.count(),
                        'advert_reviews':'0',
                        'advert_sms':'0',
                        'advert_whatsapp':'0',
                        'advert_facebook':'0',
                        'advert_twitter': '0'
                    }
                    final_list.append(advert_data)
            data = {'success': 'true', 'data': final_list}
        except IntegrityError as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_subscription_plan(request):
    try:
        data = {}
        final_list = []
        try:
            if request.GET.get('subscriber_id'):
                business_obj = Business.objects.filter(supplier=request.GET.get('subscriber_id'))
                for business in business_obj:
                    advert_sub_obj = AdvertSubscriptionMap.objects.get(business_id=str(business.business_id))
                    start_date = advert_sub_obj.business_id.start_date
                    end_date = advert_sub_obj.business_id.end_date

                    pre_ser_obj_list = PremiumService.objects.filter(business_id=str(advert_sub_obj.business_id))
                    premium_service, advert_slider, top_advert = 'N/A', 'No', 'No'
                    premium_start_date, slider_start_date, top_advert_start_date = 'N/A', 'N/A', 'N/A'
                    premium_end_date, slider_end_date, top_advert_end_date = 'N/A', 'N/A', 'N/A'

                    for pre_ser_obj in pre_ser_obj_list:
                        if pre_ser_obj.premium_service_name != "Advert Slider" and pre_ser_obj.premium_service_name != "Top Advert":
                            premium_service = pre_ser_obj.premium_service_name
                            premium_start_date = pre_ser_obj.start_date
                            premium_end_date = pre_ser_obj.end_date
                        if pre_ser_obj.premium_service_name == "Advert Slider":
                            advert_slider = 'Yes'
                            slider_start_date = pre_ser_obj.start_date
                            slider_end_date = pre_ser_obj.end_date
                        if pre_ser_obj.premium_service_name == "Top Advert":
                            top_advert = 'No'
                            top_advert_start_date = pre_ser_obj.start_date
                            top_advert_end_date = pre_ser_obj.end_date
                    try:
                        payment_obj = PaymentDetail.objects.get(business_id=str(advert_sub_obj.business_id))
                        if payment_obj.total_amount:
                            total_amount = payment_obj.payable_amount
                        else:
                            total_amount = 0
                        if payment_obj.paid_amount:
                            paid_amount = payment_obj.paid_amount
                        else:
                            paid_amount = 0
                    except Exception as e:
                        total_amount = 0
                        paid_amount = 0
                    video_count = Advert_Video.objects.filter(advert_id=str(advert_sub_obj.advert_id)).count()
                    image_count = AdvertImage.objects.filter(advert_id=str(advert_sub_obj.advert_id)).count()

                    advert_data = {
                        'advert_id': str(advert_sub_obj.advert_id),
                        'advert_title': advert_sub_obj.advert_id.advert_name,
                        'category': advert_sub_obj.advert_id.category_id.category_name,
                        'start_date': start_date,
                        'end_date': end_date,
                        'premium_service': premium_service,
                        'premium_start_date': premium_start_date,
                        'premium_end_date': premium_end_date,
                        'advert_slider': advert_slider,
                        'slider_start_date': slider_start_date,
                        'slider_end_date': slider_end_date,
                        'top_advert': top_advert,
                        'top_advert_start_date': top_advert_start_date,
                        'top_advert_end_date': top_advert_end_date,
                        'uploaded_pictures': image_count,
                        'uploaded_videos': video_count,
                        'memory_usages': '0',
                        'total_service_cost': total_amount,
                        'total_amount_paid': paid_amount,
                        'saleman_name': '',
                        'saleman_number': ''
                    }
                    final_list.append(advert_data)
            else:
                supplier_list = Supplier.objects.filter(supplier_status = '1')
                for supplier in supplier_list:
                    business_obj = Business.objects.filter(supplier=str(supplier.supplier_id))
                    for business in business_obj:
                        try:
                            advert_sub_obj = AdvertSubscriptionMap.objects.get(business_id=str(business.business_id))
                            start_date = advert_sub_obj.business_id.start_date
                            end_date = advert_sub_obj.business_id.end_date

                            pre_ser_obj_list = PremiumService.objects.filter(business_id=str(advert_sub_obj.business_id))
                            premium_service, advert_slider, top_advert = 'N/A', 'No', 'No'
                            premium_start_date, slider_start_date, top_advert_start_date = 'N/A', 'N/A', 'N/A'
                            premium_end_date, slider_end_date, top_advert_end_date = 'N/A', 'N/A', 'N/A'

                            for pre_ser_obj in pre_ser_obj_list:
                                if pre_ser_obj.premium_service_name != "Advert Slider" and pre_ser_obj.premium_service_name != "Top Advert":
                                    premium_service = pre_ser_obj.premium_service_name
                                    premium_start_date = pre_ser_obj.start_date
                                    premium_end_date = pre_ser_obj.end_date
                                if pre_ser_obj.premium_service_name == "Advert Slider":
                                    advert_slider = 'Yes'
                                    slider_start_date = pre_ser_obj.start_date
                                    slider_end_date = pre_ser_obj.end_date
                                if pre_ser_obj.premium_service_name == "Top Advert":
                                    top_advert = 'No'
                                    top_advert_start_date = pre_ser_obj.start_date
                                    top_advert_end_date = pre_ser_obj.end_date
                            try:
                                payment_obj = PaymentDetail.objects.get(business_id=str(advert_sub_obj.business_id))
                                if payment_obj.total_amount:
                                    total_amount = payment_obj.payable_amount
                                else:
                                    total_amount = 0
                                if payment_obj.paid_amount:
                                    paid_amount = payment_obj.paid_amount
                                else:
                                    paid_amount = 0
                            except Exception as e:
                                total_amount = 0
                                paid_amount = 0
                            video_count = Advert_Video.objects.filter(advert_id=str(advert_sub_obj.advert_id)).count()
                            image_count = AdvertImage.objects.filter(advert_id=str(advert_sub_obj.advert_id)).count()

                            advert_data={
                                'advert_id':str(advert_sub_obj.advert_id),
                                'advert_title':advert_sub_obj.advert_id.advert_name,
                                'category':advert_sub_obj.advert_id.category_id.category_name,
                                'start_date':start_date,
                                'end_date':end_date,
                                'premium_service':premium_service,
                                'premium_start_date':premium_start_date,
                                'premium_end_date':premium_end_date,
                                'advert_slider':advert_slider,
                                'slider_start_date':slider_start_date,
                                'slider_end_date':slider_end_date,
                                'top_advert':top_advert,
                                'top_advert_start_date':top_advert_start_date,
                                'top_advert_end_date':top_advert_end_date,
                                'uploaded_pictures':image_count,
                                'uploaded_videos':video_count,
                                'memory_usages':'0',
                                'total_service_cost':total_amount,
                                'total_amount_paid':paid_amount,
                                'saleman_name':'',
                                'saleman_number': ''
                            }
                            final_list.append(advert_data)
                        except Exception:
                            pass
            data = {'success': 'true', 'data': final_list}
        except IntegrityError as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def my_subscribers_list(request):
    try:
        data = {}
        final_list = []
        total_amount = 0
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        from_date = datetime.strptime(from_date, "%m/%d/%Y")
        to_date = datetime.strptime(to_date, "%m/%d/%Y") + timedelta(days=1)
        from_date = from_date.strftime("%Y-%m-%d")
        to_date = to_date.strftime("%Y-%m-%d")
        try:
            supplier_obj = Supplier.objects.filter(date_joined__range=[from_date, to_date])
            print "===========Supplier=================",supplier_obj
            for supplier in supplier_obj:
                if supplier.supplier_status == '1':
                    status = '<a class="btn btn-success">Active<a>'
                else:
                    status = '<a class="btn btn-danger">Inactive<a>'
                business_obj = Business.objects.filter(supplier=str(supplier.supplier_id))
                for business in business_obj:
                    try:
                        payment_obj = PaymentDetail.objects.get(business_id=str(business.business_id))
                        if payment_obj.paid_amount:
                            total_amount = total_amount + int(payment_obj.paid_amount)
                        else:
                            total_amount = total_amount + 0
                    except Exception as e:
                        print e
                        total_amount = 0
                subscriber_data = {
                    'subscriber_id': str(supplier.supplier_id),
                    'business_name': supplier.business_name,
                    'poc_name': supplier.contact_person,
                    'poc_no': supplier.contact_no,
                    'area': '',
                    'city': supplier.city.city_name,
                    'created_date': supplier.date_joined.strftime('%m/%d/%Y'),
                    'total_amount': total_amount,
                    'status': status
                }
                final_list.append(subscriber_data)
            data = {'success': 'true', 'data': final_list}
        except IntegrityError as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def my_subscription_sale(request):
    try:
        data = {}
        final_list = []
        print "----------------------"

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        print from_date,to_date
        from_date = datetime.strptime(from_date, "%m/%d/%Y")
        to_date = datetime.strptime(to_date, "%m/%d/%Y") + timedelta(days=1)
        from_date = from_date.strftime("%Y-%m-%d")
        to_date = to_date.strftime("%Y-%m-%d")

        try:
            supplier_list = Supplier.objects.filter(supplier_status = '1')
            for supplier in supplier_list:
                business_obj = Business.objects.filter(supplier=str(supplier.supplier_id),business_created_date__range=[from_date, to_date])
                for business in business_obj:
                    try:
                        advert_sub_obj = AdvertSubscriptionMap.objects.get(business_id=str(business.business_id))
                        start_date = advert_sub_obj.business_id.start_date
                        end_date = advert_sub_obj.business_id.end_date

                        pre_ser_obj_list = PremiumService.objects.filter(business_id=str(advert_sub_obj.business_id))
                        premium_service, advert_slider, top_advert = 'N/A', 'No', 'No'
                        premium_start_date, slider_start_date, top_advert_start_date = 'N/A', 'N/A', 'N/A'
                        premium_end_date, slider_end_date, top_advert_end_date = 'N/A', 'N/A', 'N/A'

                        for pre_ser_obj in pre_ser_obj_list:
                            if pre_ser_obj.premium_service_name != "Advert Slider" and pre_ser_obj.premium_service_name != "Top Advert":
                                premium_service = pre_ser_obj.premium_service_name
                                premium_start_date = pre_ser_obj.start_date
                                premium_end_date = pre_ser_obj.end_date
                            if pre_ser_obj.premium_service_name == "Advert Slider":
                                advert_slider = 'Yes'
                                slider_start_date = pre_ser_obj.start_date
                                slider_end_date = pre_ser_obj.end_date
                            if pre_ser_obj.premium_service_name == "Top Advert":
                                top_advert = 'No'
                                top_advert_start_date = pre_ser_obj.start_date
                                top_advert_end_date = pre_ser_obj.end_date
                        try:
                            payment_obj = PaymentDetail.objects.get(business_id=str(advert_sub_obj.business_id))
                            total_amount = payment_obj.total_amount 
                            if payment_obj.paid_amount:
                                paid_amount = payment_obj.paid_amount
                            else:
                                paid_amount = 0
                        except Exception as e:
                            total_amount = 0
                            paid_amount = 0

                        advert_data={
                            'advert_title':advert_sub_obj.advert_id.advert_name,
                            'business_name':supplier.business_name,
                            'area':advert_sub_obj.advert_id.area,
                            'city':advert_sub_obj.advert_id.city_place_id.city_id.city_name,
                            'category':advert_sub_obj.advert_id.category_id.category_name,
                            'subs_start_date':start_date,
                            'subs_end_date':end_date,
                            'premium_service':premium_service,
                            'premium_start_date':premium_start_date,
                            'premium_end_date':premium_end_date,
                            'advert_slider':advert_slider,
                            'slider_start_date':slider_start_date,
                            'slider_end_date':slider_end_date,
                            'top_advert':top_advert,
                            'top_advert_start_date':top_advert_start_date,
                            'top_advert_end_date':top_advert_end_date,
                            'total_service_cost':total_amount,
                            'total_amount_paid':paid_amount
                        }
                        final_list.append(advert_data)
                    except Exception as e:
                        print e
                        pass
            data = {'success': 'true', 'data': final_list}
        except IntegrityError as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_advert_databse(request):
    try:
        data = {}
        final_list = []

        try:
            print request.GET.get('city_id')
            category_list = []
            if request.GET.get('city_id') and request.GET.get('city_id') != '0':
                cat_list = CategoryCityMap.objects.filter(city_place_id = request.GET.get('city_id'))
                for category in cat_list:
                    cat_obj = Category.objects.get(category_id=str(category.category_id))
                    category_list.append(cat_obj)
                category_active_list = Category.objects.filter(category_status='1')
                for category in category_active_list:
                    cat_city_obj = CategoryCityMap.objects.filter(category_id=str(category.category_id))
                    if not cat_city_obj:
                        category_list.append(category)

            else:
                category_list = Category.objects.filter(category_status='1')
            for category in category_list:

                category_name = category.category_name
                business_obj = Business.objects.filter(category_id=str(category.category_id))
                count = 0
                for business in business_obj:
                    advert_sub_obj = AdvertSubscriptionMap.objects.get(business_id=str(business.business_id))
                    pre_date = datetime.now().strftime("%m/%d/%Y")
                    pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                    end_date = advert_sub_obj.business_id.end_date
                    end_date = datetime.strptime(end_date, "%m/%d/%Y")
                    date_gap = end_date - pre_date
                    if int(date_gap.days) >= 0:
                        count = count + 1
                    advert_data = {
                        'category': category_name,
                        'count': str(count)
                    }
                    final_list.append(advert_data)

            data = {'success': 'true', 'data': final_list}
        except IntegrityError as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_new_registered_consumer(request):
    try:
        data = {}
        final_list = []
        area = ''
        city = ''
        print "=========================================================="
        try:
            from_date = request.GET.get('from_date')
            to_date = request.GET.get('to_date')
            print from_date,to_date
            from_date = datetime.strptime(from_date, "%m/%d/%Y")
            to_date = datetime.strptime(to_date, "%m/%d/%Y") + timedelta(days=1)
            from_date = from_date.strftime("%Y-%m-%d")
            to_date = to_date.strftime("%Y-%m-%d")

            geolocator = Nominatim()
            #location = geolocator.reverse("18.5204, 73.8567")
            #print '---------location------',location

            consumer_list = ConsumerProfile.objects.filter(date_joined__range=[from_date, to_date])

            n = 0
            for consumer in consumer_list:
                n=n+1
                user_name = consumer.consumer_full_name
                date = consumer.consumer_created_date.strftime('%m/%d/%Y')
                lat = consumer.latitude
                long = consumer.longitude

                if lat:
                    try:
                        geolocator = Nominatim()
                        location = geolocator.reverse((lat, long))
                        print '---------location------',location
                        loc = str(location)
                        city = loc.split(", ")[-4]
                        area = loc.split(", ")[-5]
                        consumer_data={
                            'sr_no':n,
                            'user_name':user_name,
                            'date':date,
                            'area':area,
                            'city':city
                        }
                        final_list.append(consumer_data)

                    except:
                        location = ''
                else:
                    pass

                consumer_data={
                    'sr_no':n,
                    'user_name':user_name,
                    'date':date,
                    'area':'',
                    'city':''
                }
                final_list.append(consumer_data)
            data = {'success': 'true', 'data': final_list}
        except Exception as e:
            print "==============Exception===============================",e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_consumer_activity(request):
    try:
        data = {}
        final_list = []
        try:
            from_date = request.GET.get('from_date')
            to_date = request.GET.get('to_date')
            print from_date,to_date
            from_date = datetime.strptime(from_date, "%m/%d/%Y")
            to_date = datetime.strptime(to_date, "%m/%d/%Y") + timedelta(days=1)
            from_date = from_date.strftime("%Y-%m-%d")
            to_date = to_date.strftime("%Y-%m-%d")

            #consumer_list = ConsumerProfile.objects.all()
            consumer_list = ConsumerProfile.objects.filter(date_joined__range=[from_date, to_date])
            n = 0
            for consumer in consumer_list:
                n=n+1
                user_id = consumer.consumer_id
                date = consumer.consumer_created_date.strftime('%m/%d/%Y')

                lat = consumer.latitude
                long = consumer.longitude

                if lat:
                    try:
                        geolocator = Nominatim()
                        location = geolocator.reverse((lat, long))
                        print '---------location------',location
                        loc = str(location)
                        city = loc.split(", ")[-4]
                        area = loc.split(", ")[-5]
                        consumer_data={
                            'sr_no':n,
                            'user_id':user_id,
                            'date':date,
                            'area':area,
                            'city':city,
                            'app_usage':'',
                        }
                        final_list.append(consumer_data)

                    except:
                        location = ''
                else:
                    pass

                app_usage = ""

                consumer_data={
                    'sr_no':n,
                    'user_id':user_id,
                    'date':date,
                    'area':'',
                    'city':'',
                    'app_usage':'',
                }
                final_list.append(consumer_data)
            data = {'success': 'true', 'data': final_list}
        except Exception as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_consumer_usage(request):
    try:
        data = {}
        final_list = []
        try:
            from_date = request.GET.get('from_date')
            to_date = request.GET.get('to_date')
            print from_date,to_date
            from_date = datetime.strptime(from_date, "%m/%d/%Y")
            to_date = datetime.strptime(to_date, "%m/%d/%Y") + timedelta(days=1)
            from_date = from_date.strftime("%Y-%m-%d")
            to_date = to_date.strftime("%Y-%m-%d")

            #consumer_list = ConsumerProfile.objects.all()
            consumer_list = ConsumerProfile.objects.filter(date_joined__range=[from_date, to_date])
            n = 0
            for consumer in consumer_list:
                n=n+1
                user_id = consumer.consumer_id
                if consumer.no_of_login:
                    login_count = consumer.no_of_login
                else:
                    login_count = 0
            

                consumer_data={
                    'sr_no':n,
                    'user_id':user_id,
                    'login_count':login_count,
                }
                final_list.append(consumer_data)
            data = {'success': 'true', 'data': final_list}
        except Exception as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')