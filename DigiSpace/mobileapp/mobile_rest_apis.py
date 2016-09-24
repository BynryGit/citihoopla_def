from django.shortcuts import render
import math
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
import time
from smtplib import SMTPException
# from captcha_form import CaptchaForm
from django.shortcuts import *

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

# for random generation of string and numbers
import string
import random
import urllib  # Python URL functions
import urllib2

# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile

#Push Notifications
from push_notifications.models import APNSDevice, GCMDevice

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    renderer_classes,
    parser_classes,
    )
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import parser_classes
from mobileapp.serializers import *
from mobileapp.helper import UserProfileToJSON

SERVER_URL = "http://192.168.0.151:9090"
#SERVER_URL = "http://52.40.205.128"

# Constants
earth_radius = 6371.0
degrees_to_radians = math.pi / 180.0
radians_to_degrees = 180.0 / math.pi


@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def index(request):
    return Response({"message": "MRBD_App"})


'''
    # REST API to manual_signup and to register device token.
    # Input : email, full name, phone number, sign up source, device token and password of the valid user.
    # Output : Auth token on successful login or error or failure.
'''

@csrf_exempt
@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@csrf_exempt
def consumer_signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        try:
            #json_obj = json.loads(request.body)
            print serializer#.POST
            consumer_obj = ConsumerProfile(
                username=serializer.validated_data['email_id'],
                consumer_full_name=serializer.validated_data['full_name'],
                consumer_contact_no=serializer.validated_data['phone'],
                consumer_email_id=serializer.validated_data['email_id'],
                sign_up_source=serializer.validated_data['sign_up_source'],
                device_token=serializer.validated_data['device_token'],
                consumer_created_date=datetime.now(),
                consumer_status='1',
                consumer_created_by=serializer.validated_data['full_name'],
                consumer_updated_by=serializer.validated_data['full_name'],
                consumer_updated_date=datetime.now(),
                user_verified = 'false'
            );
            consumer_obj.save()
            consumer_obj.set_password(request.POST.get('password'));
            consumer_obj.save()
            device_id = request.POST.get('device_token')
            #device_status = add_update_consumer_device_id(consumer_obj, device_id)
            ret = u''
            ret = ''.join(random.choice('0123456789') for i in range(6))
            OTP = ret
            consumer_obj.consumer_otp = str(OTP)
            consumer_obj.save()
            #request.session["OTP"] = str(OTP)
            #print request.session["OTP"]
            #sms_otp(consumer_obj,OTP)
            try:
                filename = "IMG_%s_%s.png" % (consumer_obj.username, str(datetime.now()).replace('.', '_'))
                resource = urllib.urlopen(serializer.validated_data['user_profile_image'])

                consumer_obj.consumer_profile_pic = ContentFile(resource.read(), filename)  # assign image to model
                consumer_obj.save()
            except:
                pass
            # user = User.objects.get(username = consumer_obj.username)
            # Token.objects.filter(user=user).delete()
            # token = Token.objects.create(user=user)
            # resp = {}
            # resp['authorization'] = "Token " + str(token)
            return Response({
                "result": "success",
                "message": "User Created Successfully.",
                "user_info": get_profile_info(consumer_obj.consumer_id),
                #"authtokendata": resp
            }, status=status.HTTP_200_OK)
        except Exception, e:
            print 'mobile_rest_api.py | consumer_signup | Exception ', e
            return Response({
                "result": "failure",
                "message": "User with same username already exists."
            }, status=status.HTTP_404_NOT_FOUND)
        #return HttpResponse(json.dumps(data), content_type='application/json')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
    # Add or updates device token to GCM
'''

# def add_update_consumer_device_id(consumer_obj, device_id):
#     try:
#         user_obj = User.objects.get(username = consumer_obj.consumer_email_id)
#         check_device = GCMDevice.objects.get(user=user_obj)
#         check_device.registration_id= device_id
#         check_device.save()
#         #send_notification(user_obj)
#         return True
#     except GCMDevice.DoesNotExist as err:
#         print 'app_push_notifications.py | user_obj | Exception ', err
#         user_obj = User.objects.get(username=consumer_obj.consumer_email_id)
#         device = GCMDevice(registration_id = device_id, user = user_obj)
#         device.save()
#         #send_notification(user_obj)
#         return True
#     except Exception as err:
#         print 'app_push_notifications.py | user_obj | Exception ', err
#         return False


'''
    # REST API to LogIn to the App.
    # Input : email and password of the valid user.
    # Output : Auth token on successful login or error or failure.
'''

@csrf_exempt
@api_view(['POST'])
#@parser_classes((MultiPartParser,FormParser)) ''' if wish to support encoded form data, uncomment this decorator '''
@renderer_classes((JSONRenderer,))
def login(request):
    print request.data
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
    	# print serializer.validated_data['email']
        user = authenticate(username=serializer.validated_data['username'],password=serializer.validated_data['password'])
        if user is not None:
            consumer = ConsumerProfile.objects.get(consumer_email_id=user)
            print "First Name " + consumer.consumer_full_name
            if user.is_active:
                #user_info = UserProfileToJSON(user_profile)
                Token.objects.filter(user=user).delete()
                token = Token.objects.create(user=user)
                resp= {}
                resp['authorization'] = "Token "+str(token)
                return Response({
                    "result":"success",
                    "message":"LogIn Successful.",
                    "user_info":get_profile_info(consumer.consumer_id),
                    "authtokendata":resp
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "result":"failure",
                    "message":"Account not activated."
                    }, status = status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                "result":"failure",
                "message":"Login failed. Username Password combination doesn't match."
                }, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_profile_info(user_id):
    print "ID--", user_id

    consumer_object = ConsumerProfile.objects.get(consumer_id=user_id)
    if consumer_object.consumer_profile_pic:
        user_profile_image = consumer_object.consumer_profile_pic.url
    else:
        user_profile_image = ''
    data = {
        'user_id': str(consumer_object.consumer_id),
        'full_name': consumer_object.consumer_full_name,
        'phone': consumer_object.consumer_contact_no,
        'user_profile_image': user_profile_image,
        'email_id': consumer_object.consumer_email_id,
        'active_status': consumer_object.online,
        'created_date': consumer_object.consumer_created_date.strftime('%d/%m/%Y'),
        'user_verified': consumer_object.user_verified,
        'all_notification': consumer_object.notification_status,
        'push_my_reviews': consumer_object.push_review_status,
        'push_my_posts': consumer_object.push_post_status,
        'push_social_notifications': consumer_object.push_social_status,
        'email_my_reviews': consumer_object.email_review_status,
        'email_weekly_newsletter': consumer_object.newsletter_status,
        'email_social_notifications': consumer_object.email_social_status
    }
    return data

'''
    # REST API to get city list.
    # Output : Auth token and city list or error or failure.
'''

@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_city_list(request):
    city_list = []
    city_objs = City_Place.objects.filter(city_status=1)
    for city in city_objs:
        city_id = str(city.city_place_id)
        city_name = str(city.city_id.city_name)
        city_list1 = {'city_id': city_id, 'city_name': city_name}

        city_list.append(city_list1)
    return Response({
        "result": "success",
        "city_list": city_list,
    }, status=status.HTTP_200_OK)

'''
    # REST API to get advert map api.
    # Input : city_id, consumer present latitude and longitude, radius(in kms).
    # Output : Auth token and advert list(with latitude/longitude) or error or failure.
'''

@csrf_exempt
@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_map_advert_list(request):
    user = request.user
    serializer = AdvertMapListSerializer(data=request.data)
    if serializer.is_valid():
        city_id = serializer.validated_data['city_id']
        lon_max, lon_min, lat_max, lat_min = bounding_box(
            float(serializer.validated_data['consumer_latitude']),
            float(serializer.validated_data['consumer_longitude']),
            float(serializer.validated_data['radius'])
        )
        advert_list = []
        try:
            advert_map_obj = Advert.objects.filter(
                city_place_id=city_id,
                latitude__range=[lat_min, lat_max],
                longitude__range=[lon_min, lon_max],
                status = '1'
            )
            for advert_map in advert_map_obj:
                phone_list = []
                email_list = []
                advert_id = str(advert_map.advert_id)
                pre_date = datetime.now().strftime("%m/%d/%Y")
                pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                end_date = advert_sub_obj.business_id.end_date
                end_date = datetime.strptime(end_date, "%m/%d/%Y")
                date_gap = end_date - pre_date
                if int(date_gap.days) >= 0:
                    advert_obj = Advert.objects.get(advert_id=advert_id)
                    advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                    start_date = advert_sub_obj.business_id.start_date
                    end_date = advert_sub_obj.business_id.end_date
                    start_date = datetime.strptime(start_date, "%m/%d/%Y")
                    end_date = datetime.strptime(end_date, "%m/%d/%Y")
                    address = ''
                    if advert_obj.area:
                        address = advert_obj.area
                    if advert_obj.city_place_id:
                        address = address + ' ' + advert_obj.city_place_id.city_id.city_name

                    phone_obj = PhoneNo.objects.filter(advert_id=advert_id)

                    for phone in phone_obj:
                        phone_no = phone.phone_no
                        phone_list.append(phone_no)

                    email_list.append(advert_obj.email_primary)
                    if advert_obj.email_secondary:
                        email_list.append(advert_obj.email_secondary)
                    if advert_obj.display_image:
                        image_url = advert_obj.display_image.url
                    else:
                        image_url = ''

                    try:
                        advert_like_obj = AdvertLike.objects.get(advert_id=advert_id,user_id=str(user.user_id))
                        is_like = "true"
                    except Exception:
                        is_like = "false"

                    try:
                        advert_like_obj = AdvertFavourite.objects.get(advert_id=advert_id, user_id=str(user.user_id))
                        is_favourite = "true"
                    except Exception:
                        is_favourite = "false"

                    if advert_obj.advert_views:
                        views_count = int(advert_obj.advert_views)
                    else:
                        views_count = 0

                    advert_like_obj = AdvertLike.objects.filter(advert_id=advert_id)

                    like_count = 0
                    for advert_like in advert_like_obj:
                        like_count = like_count + 1

                    advert_data = {
                        "advert_id": str(advert_obj.advert_id),
                        "advert_img": image_url,
                        "name": advert_obj.advert_name,
                        "location": address,
                        "offer_start_date": start_date.strftime("%d %b %Y"),
                        "offer_end_date": end_date.strftime("%d %b %Y"),
                        "likes": str(like_count),
                        "is_like": is_like,
                        "is_favorite": is_favourite,
                        "views": str(views_count),
                        "reviews": "0",
                        "phone": phone_list,
                        "email": email_list,
                        "ratings": "3.2",
                        "latitude":str(advert_obj.latitude),
                        "longitude":str(advert_obj.longitude),
                    }
                    advert_list.append(advert_data)
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            resp = {}
            resp['authorization'] = "Token " + str(token)
            return Response({
                "result": "success",
                "message": "",
                "authtokendata": resp,
                "advert_list": advert_list,
            }, status=status.HTTP_200_OK)
        except Exception, ke:
            print ke
            return Response({
                "result": "failure",
                "message": "Something went wrong",
                "advert_list": advert_list,
            }, status=status.HTTP_404_NOT_FOUND)
            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def change_in_latitude(distance):
    "Given a distance north, return the change in latitude."
    return (distance/earth_radius)*radians_to_degrees

def change_in_longitude(latitude, distance):
    "Given a latitude and a distance west, return the change in longitude."
    # Find the radius of a circle around the earth at given latitude.
    r = earth_radius*math.cos(latitude*degrees_to_radians)
    return (distance/r)*radians_to_degrees

def bounding_box(latitude, longitude, distance):
    lat_change = change_in_latitude(distance)
    lat_max = latitude + lat_change
    lat_min = latitude - lat_change
    lon_change = change_in_longitude(latitude, distance)
    lon_max = longitude + lon_change
    lon_min = longitude - lon_change
    return (lon_max, lon_min, lat_max, lat_min)

'''
    # REST API to get advert map api.
    # Input : city_id, consumer present latitude and longitude, radius(in kms).
    # Output : Auth token and advert list(with latitude/longitude) or error or failure.
'''

@csrf_exempt
@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def post_advert_review(request):
    user = request.user
    serializer = PostReviewSerializer(data=request.data)
    if serializer.is_valid():
        try:
            review_obj = AdvertReview()
            review_obj.user_id = ConsumerProfile.objects.get(consumer_email_id=user)
            review_obj.advert_id = Advert.objects.get(advert_id=serializer.validated_data['advert_id'])
            review_obj.ratings = serializer.validated_data['ratings']
            review_obj.review = serializer.validated_data['review']
            review_obj.creation_date = datetime.now()
            review_obj.save()
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            resp = {}
            resp['authorization'] = "Token " + str(token)
            return Response({
                "result": "success",
                "message": "Review published successfully.",
                "authtokendata": resp,
            }, status=status.HTTP_200_OK)
        except Exception, ke:
            print ke
            return Response({
                "result": "failure",
                "message": "Something went wrong",
            }, status=status.HTTP_404_NOT_FOUND)
            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
