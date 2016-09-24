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

from helper import dd2dms

# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile

# Push Notifications
from push_notifications.models import APNSDevice, GCMDevice

# SERVER_URL = "http://192.168.0.151:9090"
SERVER_URL = "http://52.40.205.128"

# Constants
earth_radius = 6371.0
degrees_to_radians = math.pi / 180.0
radians_to_degrees = 180.0 / math.pi

#from geopy.geocoders import Nominatim
import geocoder

@csrf_exempt
def consumer_signup(request):
    try:
        json_obj = json.loads(request.body)
        consumer_obj = ConsumerProfile(
            username=json_obj['email_id'],
            consumer_full_name=json_obj['full_name'],
            consumer_contact_no=json_obj['phone'],
            consumer_email_id=json_obj['email_id'],
            sign_up_source=json_obj['sign_up_source'],
            device_token=json_obj['device_token'],
            consumer_created_date=datetime.now(),
            consumer_status='1',
            consumer_created_by=json_obj['full_name'],
            consumer_updated_by=json_obj['full_name'],
            consumer_updated_date=datetime.now(),
            user_verified='false'
        );
        consumer_obj.save()
        consumer_obj.set_password(json_obj['password']);
        consumer_obj.save()
        device_id = json_obj['device_token']
        device_status = add_update_consumer_device_id(consumer_obj, device_id)
        print "=======device_status=======", device_status
        ret = u''
        ret = ''.join(random.choice('0123456789') for i in range(6))
        OTP = ret
        consumer_obj.consumer_otp = str(OTP)
        consumer_obj.save()
        # request.session["OTP"] = str(OTP)
        # print request.session["OTP"]
        sms_otp(consumer_obj, OTP)
        try:
            filename = "IMG_%s_%s.png" % (consumer_obj.username, str(datetime.now()).replace('.', '_'))
            resource = urllib.urlopen(json_obj['user_profile_image'])

            consumer_obj.consumer_profile_pic = ContentFile(resource.read(), filename)  # assign image to model
            consumer_obj.save()
        except:
            pass

        data = {
            'success': 'true',
            'message': 'User Created Successfully',
            'user_info': get_profile_info(consumer_obj.consumer_id)
        }
    except Exception, e:
        print '=e===========', e
        data = {
            'success': 'false',
            'message': 'User with same username already exists'
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


def add_update_consumer_device_id(consumer_obj, device_id):
    try:
        user_obj = User.objects.get(username=consumer_obj.consumer_email_id)
        check_device = GCMDevice.objects.get(user=user_obj)
        check_device.registration_id = device_id
        check_device.save()
        send_notification(user_obj)
        return True
    except GCMDevice.DoesNotExist as err:
        print 'app_push_notifications.py | user_obj | Exception ', err
        user_obj = User.objects.get(username=consumer_obj.consumer_email_id)
        device = GCMDevice(registration_id=device_id, user=user_obj)
        device.save()
        send_notification(user_obj)
        return True
    except Exception as err:
        print 'app_push_notifications.py | user_obj | Exception ', err
        return False


@csrf_exempt
def send_notification(user_obj):
    try:
        devices = GCMDevice.objects.get(user=user_obj)
        status = devices.send_message(None,
                                      extra={"message": "Hello from City Hoopla", "badge": "1", "sound": "default",
                                             "title": "City Hoopla"})
        print 'Status : ', status
        return True
    except Exception, e:
        print e
        return False


def sms_otp(consumer_obj, OTP):
    authkey = "118994AIG5vJOpg157989f23"
    mobiles = str(consumer_obj.consumer_contact_no)

    message = "Dear User,\n"
    message = message + str(OTP) + " is your One Time Password(OTP) for CityHoopla"
    print message
    sender = "DGSPCE"
    route = "4"
    country = "91"

    values = {
        'authkey': authkey,
        'mobiles': mobiles,
        'message': message,
        'sender': sender,
        'route': route,
        'country': country
    }

    url = "http://api.msg91.com/api/sendhttp.php"
    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    output = response.read()
    print output


@csrf_exempt
def resend_otp(request):
    json_obj = json.loads(request.body)
    user_id = json_obj['user_id']
    contact_no = json_obj['contact_no']
    ret = u''
    ret = ''.join(random.choice('0123456789') for i in range(6))
    OTP = ret
    # request.session["OTP"] = str(OTP)
    consumer_obj = ConsumerProfile.objects.get(consumer_id=str(user_id))
    consumer_obj.consumer_contact_no = str(contact_no)
    consumer_obj.consumer_otp = str(OTP)
    consumer_obj.save()
    sms_otp(consumer_obj, OTP)
    data = {'success': 'true', 'message': 'OPT send to user'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def check_otp(request):
    json_obj = json.loads(request.body)
    # print request.session["OTP"]
    # session_otp = request.session['OTP']
    user_id = json_obj['user_id']
    contact_no = json_obj['contact_no']
    msg_otp = json_obj['OTP']
    consumer_obj = ConsumerProfile.objects.get(consumer_id=str(user_id))
    session_otp = str(consumer_obj.consumer_otp)
    if session_otp == msg_otp:
        consumer_obj.user_verified = 'true'
        consumer_obj.consumer_contact_no = str(contact_no)
        consumer_obj.save()
        data = {'success': 'true', 'message': 'OPT match'}
    else:
        data = {'success': 'false', 'message': "OPT doesn't match"}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Sign Up via Gmail and Facebook
@csrf_exempt
def social_signup(request):
    try:
        # pdb.set_trace()
        json_obj = json.loads(request.body)
        print 'JSON OBJECT : ', json_obj
        consumer_obj = ConsumerProfile(
            username=json_obj['email_id'],
            consumer_full_name=json_obj['full_name'],
            consumer_email_id=json_obj['email_id'],
            device_token=json_obj['device_token'],
            sign_up_source=json_obj['sign_up_source'],
            consumer_profile_pic=json_obj['user_profile_image'],
            consumer_contact_no=json_obj['phone'],
            consumer_created_date=datetime.now(),
            consumer_status='1',
            consumer_created_by=json_obj['full_name'],
            consumer_updated_by=json_obj['full_name'],
            consumer_updated_date=datetime.now()
        )
        consumer_obj.save()

        filename = "IMG_%s_%s.jpg" % (
            consumer_obj.username, str(datetime.now()).replace('.', '_'))  # For giving filename to Image
        resource = urllib.urlopen(json_obj['user_profile_image'])

        consumer_obj.consumer_profile_pic = ContentFile(resource.read(), filename)  # assign image to model
        consumer_obj.save()

        if consumer_obj:
            data = {'success': 'true', 'message': 'Successful Sign Up',
                    'user_info': get_profile_info(consumer_obj.consumer_id)}
            email = consumer_obj.username
        else:
            data = {'success': 'false', 'message': 'Sign Up not Successful'}
    except ConsumerProfile.DoesNotExist, e:
        data = {'success': 'false', 'message': str(e)}
    except IntegrityError as err:
        json_obj = json.loads(request.body)
        consumer_obj = ConsumerProfile.objects.get(username=json_obj['email_id'])
        data = {'success': 'true', 'message': 'Login Successful',
                'user_info': get_profile_info(consumer_obj.consumer_id)}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        json_obj = json.loads(request.body)
        email_id = json_obj['email_id']
        data = {'success': 'false', 'message': 'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def set_notification_settings(request):
    try:
        json_obj = json.loads(request.body)
        print json_obj

        customer_object = ConsumerProfile.objects.get(consumer_id=json_obj['user_id'])
        customer_object.notification_status = json_obj['all_notification_status']
        customer_object.push_review_status = json_obj['push_my_reviews_status']
        customer_object.push_post_status = json_obj['push_my_posts_status']
        customer_object.push_social_status = json_obj['push_social_notifications_status']
        customer_object.email_review_status = json_obj['email_my_reviews_status']
        customer_object.newsletter_status = json_obj['email_weekly_newsletter_status']
        customer_object.email_social_status = json_obj['email_social_notifications_status']
        customer_object.save()

        data = {'success': 'true', 'message': 'Notification setting updated successfully',
                'user_info': get_profile_info(customer_object.consumer_id)}
    except Exception, e:
        print e
        data = {'success': 'false', 'message': "Server Error, Please try again!"}
    return HttpResponse(json.dumps(data), content_type='application/json')


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


@csrf_exempt
def consumer_login(request):
    try:
        print request.body
        if request.method == 'POST':
            json_obj = json.loads(request.body)
            try:
                consumer_obj = ConsumerProfile.objects.get(username=json_obj['username'])
                user = authenticate(username=json_obj['username'], password=json_obj['password'])

                print "info", user
                if user:
                    consumer = ConsumerProfile.objects.get(consumer_email_id=user)
                    if user.is_active:
                        if consumer.no_of_login:
                            count = int(consumer.no_of_login) + 1
                        else:
                            count = 1
                        consumer.no_of_login = count
                        consumer.save()

                        data = {'success': 'true', 'message': 'Login Successful',
                                'user_info': get_profile_info(consumer.consumer_id)}

                    else:
                        data = {'success': 'false', 'message': 'User Is Not Active'}
                else:
                    data = {'success': 'false', 'message': 'Please enter valid Password'}
            except:
                data = {'success': 'false', 'message': 'Invalid Username'}
        else:
            data = {'success': 'false', 'message': 'Invalid Request'}
    except User.DoesNotExist as err:
        print 'usr NOt Exist'
        data = {'success': 'false', 'message': 'User Not Exists'}
    except Exception, e:
        print e
        data = {'success': 'false', 'message': 'Internal Server Error '}
    return HttpResponse(json.dumps(data), content_type='application/json')


# API for forgot password
@csrf_exempt
def forgot_password(request):
    gmail_user = "cityhoopla2016@gmail.com"
    gmail_pwd = "cityhoopla@2016"
    FROM = 'Cityhoopla Admin: <cityhoopla2016@gmail.com>'
    TO = []
    chars = string.ascii_uppercase + string.digits
    pwdSize = 8

    password = ''.join((random.choice(chars)) for x in range(pwdSize))
    print "PASSWORD", password
    try:
        if request.method == 'POST':
            json_obj = json.loads(request.body)
            user_name = json_obj['email_id']
            TO.append(user_name)
            customer_obj = ConsumerProfile.objects.get(username=user_name)
            sign_up_source = customer_obj.sign_up_source
            if sign_up_source == 'FACEBOOK_ANDROID':
                data = {'success': 'false', 'message': "Email ID registered with Facebook. Cannot generate password"}
            elif sign_up_source == 'GOOGLE_ANDROID':
                data = {'success': 'false', 'message': "Email ID registered with Google+. Cannot generate password"}
            else:
                customer_obj.set_password(password)
                customer_obj.save()
                TEXT = "Dear Customer,"
                TEXT = TEXT + "\n\nYour account information is :"
                TEXT = TEXT + "\nEmail Address: " + str(user_name)
                TEXT = TEXT + "\nPassword: " + str(password)
                TEXT = TEXT + "\n\nThank You,"
                TEXT = TEXT + "\nCityHoopla Team"

                SUBJECT = "New Password"
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()

                server.login(gmail_user, gmail_pwd)
                message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
                server.sendmail(FROM, TO, message)
                server.quit()
                data = {'success': 'true', 'message': " Password Sent Successfully"}

    except User.DoesNotExist, e:
        data = {'success': 'false', 'message': "Email ID does not exists"}
        print "failed to send mail", e
    except Exception, e:
        print e
        data = {'success': 'false', 'message': "Server Error, Please try again!"}
    print '=====data=============', data
    return HttpResponse(json.dumps(data), content_type='application/json')


# @csrf_exempt
# @api_view(['GET'])
# @renderer_classes((JSONRenderer,))
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_city_list(request):
    city_list = []
    try:
        city_objs = City_Place.objects.filter(city_status=1)
        for city in city_objs:
            city_id = str(city.city_place_id)
            city_name = str(city.city_id.city_name)
            city_list1 = {'city_id': city_id, 'city_name': city_name}

            city_list.append(city_list1)
        data = {'city_list': city_list, 'success': 'true'}
    except Exception, ke:
        print ke
        data = {'city_list': city_list, 'success': 'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_about_city(request):
    json_obj = json.loads(request.body)
    city_id = json_obj['city_id']
    try:
        advert_list = []
        # where_to_shop
        # reputed_hospitals
        # college_and_universities
        # point_of_interest

        city_obj = City_Place.objects.get(city_place_id=city_id)
        city_name = city_obj.city_id.city_name
        state_county_name = city_obj.city_id.state_id.state_name + ', ' + city_obj.city_id.state_id.country_id.country_name
        city_image = city_obj.city_image.url
        about_city = city_obj.about_city
        city_add = city_name +', '+ state_county_name
        location = geocoder.google(city_add)
        latitude = location.lat
        longitude = location.lng
        long_degrees, lat_degrees = dd2dms(longitude, latitude)

        point_of_interest_list = []
        colleges_list = []
        shopping_hub_list = []
        hospital_list = []

        point_of_interest_obj = Places.objects.filter(city_place_id = city_id, place_type = 'point_of_interest')
        for point_of_interest in point_of_interest_obj:
            poi_data = {
                'place_details':point_of_interest.place_name,
                'place_image':point_of_interest.place_image.url
            }
            point_of_interest_list.append(poi_data)

        college_obj = Places.objects.filter(city_place_id=city_id, place_type='college_and_universities')
        for college in college_obj:
            college_data = {
                'place_details':college.place_name,
                'place_image':college.place_image.url
            }
            colleges_list.append(college_data)

        shopping_obj = Places.objects.filter(city_place_id=city_id, place_type='where_to_shop')
        for shopping in shopping_obj:
            shopping_data = {
                'place_details':shopping.place_name,
                'place_image':shopping.place_image.url
            }
            shopping_hub_list.append(shopping_data)

        hospital_obj = Places.objects.filter(city_place_id=city_id, place_type='reputed_hospitals')
        for hospital in hospital_obj:
            hospital_data = {
                'place_details':hospital.place_name,
                'place_image':hospital.place_image.url
            }
            hospital_list.append(hospital_data)

        data = {
            'success': 'true', 'message': '',
            'city_name': city_name,
            'state_county_name': state_county_name,
            'city_image': city_image,
            'about_city': about_city,
            'longitude': long_degrees,
            'latitude': lat_degrees,
            'point_of_interest': point_of_interest_list,
            'colleges': colleges_list,
            'shopping_hub': shopping_hub_list,
            'hospitals': hospital_list
        }
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Something went wrong', 'advert_list': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_bottom_advert_list(request):
    json_obj = json.loads(request.body)
    city_id = json_obj['city_id']
    user_id = json_obj['user_id']
    try:
        advert_list = []
        advert_obj_list = Advert.objects.filter(city_place_id=city_id)
        for advert_obj in advert_obj_list:
            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=str(advert_obj.advert_id))
            pre_ser_obj_list = PremiumService.objects.filter(business_id=str(advert_sub_obj.business_id))
            for pre_ser_obj in pre_ser_obj_list:
                if pre_ser_obj.premium_service_name == "Advert Slider":
                    advert_data = {
                        "advert_id": str(advert_obj.advert_id),
                        "advert_image": advert_obj.display_image.url,
                        "user_id": str(user_id),
                        "category_id": "0",
                        "level": "0"
                    }
                    advert_list.append(advert_data)
        data = {'success': 'true', 'message': '', 'advert_list': advert_list}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Something went wrong', 'advert_list': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_top_advert(request):
    json_obj = json.loads(request.body)
    city_id = json_obj['city_id']
    user_id = json_obj['user_id']
    try:
        advert_list = []
        advert_data = ''
        advert_obj_list = Advert.objects.filter(city_place_id=city_id)
        if advert_obj_list:
            for advert_obj in advert_obj_list:
                advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=str(advert_obj.advert_id))
                pre_ser_obj_list = PremiumService.objects.filter(business_id=str(advert_sub_obj.business_id))
                for pre_ser_obj in pre_ser_obj_list:
                    if pre_ser_obj.premium_service_name == "Top Advert":
                        advert_data = {
                            "advert_id": str(advert_obj.advert_id),
                            "advert_image": advert_obj.display_image.url,
                            "user_id": str(user_id),
                            "category_id": "0",
                            "level": "0"
                        }
        else:
            advert_data = ''
        data = {'success': 'true', 'message': '', 'advert_data': advert_data}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Something went wrong', 'advert_data': ''}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_category_subcategory_list(request):
    ##    pdb.set_trace()
    json_obj = json.loads(request.body)
    city_id = json_obj['city_id']
    level = json_obj['level']
    category_list = []
    category_id_list = []
    color = ''
    try:
        cat_objs = Category.objects.filter(category_status='1')
        x = 0
        for cat in cat_objs:
            cat_city_obj = CategoryCityMap.objects.filter(category_id=str(cat.category_id))
            if cat_city_obj:
                for cat_city in cat_city_obj:
                    if int(cat_city.city_place_id.city_place_id) == int(city_id):
                        category_id_list.append(str(cat.category_id))
            else:
                category_id_list.append(str(cat.category_id))
        print category_id_list
        for cat_city in category_id_list:
            category_id = str(cat_city)
            cat_objs = Category.objects.filter(category_id=category_id, category_status='1')
            for cat_obj in cat_objs:
                cat_id = str(cat_obj.category_id)
                advert_count, like_count, subcat_list = get_cat_data(cat_id, city_id)
                cat_obj_data = {
                    "category_id": str(cat_id),
                    "category_name": cat_obj.category_name,
                    "category_img": cat_obj.category_image.url,
                    "total_adverts_count": str(advert_count),
                    "total_likes": str(like_count),
                    "favorite": "0",
                    "category": subcat_list,
                    "category_color": str(cat_obj.category_color) or '#000000'
                }
                category_list.append(cat_obj_data)

        data = {'success': 'true', 'message': '', 'category_list': category_list, 'level': level}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Something went wrong', 'category_list': [], 'level': ''}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_cat_data(cat_id, city_id):
    advert_count = 0
    like_count = 0
    sub_cat_obj = CategoryLevel1.objects.filter(parent_category_id=cat_id, category_status='1')
    subcat_list = []
    for sub_cat in sub_cat_obj:
        i = 0
        advert_obj = Advert.objects.filter(category_level_1=str(sub_cat.category_id))
        for adverts in advert_obj:
            advert_id = adverts.advert_id
            if adverts.city_place_id:
                if int(adverts.city_place_id.city_place_id) == int(city_id):
                    print "Match"
                    try:
                        pre_date = datetime.now().strftime("%m/%d/%Y")
                        pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                        end_date = advert_sub_obj.business_id.end_date
                        end_date = datetime.strptime(end_date, "%m/%d/%Y")
                        date_gap = end_date - pre_date
                        if int(date_gap.days) < 0:
                            i = i + 1
                    except Exception:
                        print ""

                    advert_like_obj = AdvertLike.objects.filter(advert_id=advert_id)
                    for advert_like in advert_like_obj:
                        like_count = like_count + 1

                else:
                    i = i + 1
        cat_id = str(sub_cat.category_id)
        subcat2_list = get_cat2_data(cat_id, city_id)

        sub_cat_data = {
            "category_id": str(sub_cat.category_id),
            "category_name": sub_cat.category_name,
            "total_adverts_count": str(int(advert_obj.count()) - i),
            "level": "1",
            "category": subcat2_list,
        }
        advert_count = advert_count + int(advert_obj.count()) - i
        subcat_list.append(sub_cat_data)
    return advert_count, like_count, subcat_list


def get_cat2_data(cat_id, city_id):
    advert_count = 0
    like_count = 0
    sub_cat_obj = CategoryLevel2.objects.filter(parent_category_id=cat_id, category_status='1')
    subcat_list = []
    for sub_cat in sub_cat_obj:
        i = 0
        advert_obj = Advert.objects.filter(category_level_2=str(sub_cat.category_id))
        for adverts in advert_obj:
            advert_id = adverts.advert_id
            if adverts.city_place_id:
                if int(adverts.city_place_id.city_place_id) == int(city_id):
                    print "Match"
                    try:
                        pre_date = datetime.now().strftime("%m/%d/%Y")
                        pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                        end_date = advert_sub_obj.business_id.end_date
                        end_date = datetime.strptime(end_date, "%m/%d/%Y")
                        date_gap = end_date - pre_date
                        if int(date_gap.days) < 0:
                            i = i + 1
                    except Exception:
                        print ""

                        # advert_like_obj = AdvertLike.objects.filter(advert_id=advert_id)
                        # for advert_like in advert_like_obj:
                        #     like_count = like_count + 1

                else:
                    i = i + 1
        cat_id = str(sub_cat.category_id)
        subcat3_list = get_cat3_data(cat_id, city_id)

        sub_cat_data = {
            "category_id": str(sub_cat.category_id),
            "category_name": sub_cat.category_name,
            "total_adverts_count": str(int(advert_obj.count()) - i),
            "level": "2",
            "category": subcat3_list
        }
        # advert_count = advert_count + int(advert_obj.count()) - i
        subcat_list.append(sub_cat_data)
    return subcat_list


def get_cat3_data(cat_id, city_id):
    advert_count = 0
    like_count = 0
    sub_cat_obj = CategoryLevel3.objects.filter(parent_category_id=cat_id, category_status='1')
    subcat_list = []
    for sub_cat in sub_cat_obj:
        i = 0
        advert_obj = Advert.objects.filter(category_level_3=str(sub_cat.category_id))
        for adverts in advert_obj:
            advert_id = adverts.advert_id
            if adverts.city_place_id:
                if int(adverts.city_place_id.city_place_id) == int(city_id):
                    print "Match"
                    try:
                        pre_date = datetime.now().strftime("%m/%d/%Y")
                        pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                        end_date = advert_sub_obj.business_id.end_date
                        end_date = datetime.strptime(end_date, "%m/%d/%Y")
                        date_gap = end_date - pre_date
                        if int(date_gap.days) < 0:
                            i = i + 1
                    except Exception:
                        print ""

                        # advert_like_obj = AdvertLike.objects.filter(advert_id=advert_id)
                        # for advert_like in advert_like_obj:
                        #     like_count = like_count + 1

                else:
                    i = i + 1
        cat_id = str(sub_cat.category_id)
        subcat4_list = get_cat4_data(cat_id, city_id)

        sub_cat_data = {
            "category_id": str(sub_cat.category_id),
            "category_name": sub_cat.category_name,
            "total_adverts_count": str(int(advert_obj.count()) - i),
            "level": "3",
            "category": subcat4_list
        }
        # advert_count = advert_count + int(advert_obj.count()) - i
        subcat_list.append(sub_cat_data)
    return subcat_list


def get_cat4_data(cat_id, city_id):
    advert_count = 0
    like_count = 0
    sub_cat_obj = CategoryLevel4.objects.filter(parent_category_id=cat_id, category_status='1')
    subcat_list = []
    for sub_cat in sub_cat_obj:
        i = 0
        advert_obj = Advert.objects.filter(category_level_4=str(sub_cat.category_id))
        for adverts in advert_obj:
            advert_id = adverts.advert_id
            if adverts.city_place_id:
                if int(adverts.city_place_id.city_place_id) == int(city_id):
                    print "Match"
                    try:
                        pre_date = datetime.now().strftime("%m/%d/%Y")
                        pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                        end_date = advert_sub_obj.business_id.end_date
                        end_date = datetime.strptime(end_date, "%m/%d/%Y")
                        date_gap = end_date - pre_date
                        if int(date_gap.days) < 0:
                            i = i + 1
                    except Exception:
                        print ""

                        # advert_like_obj = AdvertLike.objects.filter(advert_id=advert_id)
                        # for advert_like in advert_like_obj:
                        #     like_count = like_count + 1

                else:
                    i = i + 1
        cat_id = str(sub_cat.category_id)
        subcat5_list = get_cat5_data(cat_id, city_id)

        sub_cat_data = {
            "category_id": str(sub_cat.category_id),
            "category_name": sub_cat.category_name,
            "total_adverts_count": str(int(advert_obj.count()) - i),
            "level": "4",
            "category": subcat5_list
        }
        # advert_count = advert_count + int(advert_obj.count()) - i
        subcat_list.append(sub_cat_data)
    return subcat_list


def get_cat5_data(cat_id, city_id):
    advert_count = 0
    like_count = 0
    sub_cat_obj = CategoryLevel5.objects.filter(parent_category_id=cat_id, category_status='1')
    subcat_list = []
    for sub_cat in sub_cat_obj:
        i = 0
        advert_obj = Advert.objects.filter(category_level_5=str(sub_cat.category_id))
        for adverts in advert_obj:
            advert_id = adverts.advert_id
            if adverts.city_place_id:
                if int(adverts.city_place_id.city_place_id) == int(city_id):
                    print "Match"
                    try:
                        pre_date = datetime.now().strftime("%m/%d/%Y")
                        pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                        end_date = advert_sub_obj.business_id.end_date
                        end_date = datetime.strptime(end_date, "%m/%d/%Y")
                        date_gap = end_date - pre_date
                        if int(date_gap.days) < 0:
                            i = i + 1
                    except Exception:
                        print ""

                        # advert_like_obj = AdvertLike.objects.filter(advert_id=advert_id)
                        # for advert_like in advert_like_obj:
                        #     like_count = like_count + 1

                else:
                    i = i + 1
        sub_cat_data = {
            "category_id": str(sub_cat.category_id),
            "category_name": sub_cat.category_name,
            "total_adverts_count": str(int(advert_obj.count()) - i),
            "level": "5"
        }
        # advert_count = advert_count + int(advert_obj.count()) - i
        subcat_list.append(sub_cat_data)
    return subcat_list


@csrf_exempt
def get_category_list(request):
    ##    pdb.set_trace()
    json_obj = json.loads(request.body)
    city_id = json_obj['city_id']
    level = json_obj['level']
    category_list = []
    category_id_list = []
    color = ''
    try:
        if json_obj['category_id'] == "0":
            cat_objs = Category.objects.filter(category_status='1')
            x = 0
            for cat in cat_objs:
                cat_city_obj = CategoryCityMap.objects.filter(category_id=str(cat.category_id))
                if cat_city_obj:
                    for cat_city in cat_city_obj:
                        if int(cat_city.city_place_id.city_place_id) == int(city_id):
                            category_id_list.append(str(cat.category_id))
                else:
                    category_id_list.append(str(cat.category_id))
            print category_id_list
            for cat_city in category_id_list:
                category_id = str(cat_city)
                # print category_id
                cat_objs = Category.objects.filter(category_id=category_id, category_status='1')
                for cat_obj in cat_objs:
                    cat_id = str(cat_obj.category_id)
                    advert_count = 0
                    like_count = 0
                    sub_cat_obj = CategoryLevel1.objects.filter(parent_category_id=cat_id, category_status='1')
                    subcat_list = []
                    for sub_cat in sub_cat_obj:
                        i = 0
                        advert_obj = Advert.objects.filter(category_level_1=str(sub_cat.category_id))
                        for adverts in advert_obj:
                            advert_id = adverts.advert_id
                            if adverts.city_place_id:
                                if int(adverts.city_place_id.city_place_id) == int(city_id):
                                    print "Match"
                                    try:
                                        pre_date = datetime.now().strftime("%m/%d/%Y")
                                        pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                                        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                                        end_date = advert_sub_obj.business_id.end_date
                                        end_date = datetime.strptime(end_date, "%m/%d/%Y")
                                        date_gap = end_date - pre_date
                                        if int(date_gap.days) < 0:
                                            i = i + 1
                                    except Exception:
                                        print ""

                                    advert_like_obj = AdvertLike.objects.filter(advert_id=advert_id)
                                    for advert_like in advert_like_obj:
                                        like_count = like_count + 1

                                else:
                                    i = i + 1
                        sub_cat_data = {
                            "id": sub_cat.category_id,
                            "name": sub_cat.category_name,
                            "count": int(advert_obj.count()) - i,
                        }
                        advert_count = advert_count + int(advert_obj.count()) - i
                        subcat_list.append(sub_cat_data)
                    cat_obj_data = {
                        "category_id": cat_id,
                        "category_name": cat_obj.category_name,
                        "category_img": cat_obj.category_image.url,
                        "total_adverts_count": advert_count,
                        "total_likes": like_count,
                        "favorite": "0",
                        "subcategories": subcat_list,
                        "category_color": str(cat_obj.category_color) or '#000000'
                    }
                    category_list.append(cat_obj_data)
        else:
            if level == '1':
                cat_objs = CategoryLevel1.objects.filter(category_id=json_obj['category_id'],
                                                         category_status='1')
            if level == '2':
                cat_objs = CategoryLevel2.objects.filter(category_id=json_obj['category_id'],
                                                         category_status='1')
            if level == '3':
                cat_objs = CategoryLevel3.objects.filter(category_id=json_obj['category_id'],
                                                         category_status='1')
            if level == '4':
                cat_objs = CategoryLevel4.objects.filter(category_id=json_obj['category_id'],
                                                         category_status='1')
            if level == '5':
                cat_objs = CategoryLevel5.objects.filter(category_id=json_obj['category_id'],
                                                         category_status='1')
            print cat_objs
            for cat_obj in cat_objs:
                cat_id = str(cat_obj.category_id)
                advert_count = 0
                like_count = 0
                if level == '1':
                    sub_cat_obj = CategoryLevel2.objects.filter(parent_category_id=cat_id, category_status='1')
                if level == '2':
                    sub_cat_obj = CategoryLevel3.objects.filter(parent_category_id=cat_id, category_status='1')
                if level == '3':
                    sub_cat_obj = CategoryLevel4.objects.filter(parent_category_id=cat_id, category_status='1')
                if level == '4':
                    sub_cat_obj = CategoryLevel5.objects.filter(parent_category_id=cat_id, category_status='1')
                subcat_list = []
                for sub_cat in sub_cat_obj:
                    i = 0
                    if level == '1':
                        advert_obj = Advert.objects.filter(category_level_2=str(sub_cat.category_id))
                    if level == '2':
                        advert_obj = Advert.objects.filter(category_level_3=str(sub_cat.category_id))
                    if level == '3':
                        advert_obj = Advert.objects.filter(category_level_4=str(sub_cat.category_id))
                    if level == '4':
                        advert_obj = Advert.objects.filter(category_level_5=str(sub_cat.category_id))
                    for adverts in advert_obj:
                        advert_id = adverts.advert_id
                        if adverts.city_place_id:
                            if int(adverts.city_place_id.city_place_id) == int(city_id):
                                print "Match"
                                try:
                                    pre_date = datetime.now().strftime("%m/%d/%Y")
                                    pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                                    advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                                    end_date = advert_sub_obj.business_id.end_date
                                    end_date = datetime.strptime(end_date, "%m/%d/%Y")
                                    date_gap = end_date - pre_date
                                    if int(date_gap.days) < 0:
                                        i = i + 1
                                except Exception:
                                    print ""

                                advert_like_obj = AdvertLike.objects.filter(advert_id=advert_id)

                                for advert_like in advert_like_obj:
                                    like_count = like_count + 1

                            else:
                                i = i + 1
                    sub_cat_data = {
                        "id": sub_cat.category_id,
                        "name": sub_cat.category_name,
                        "count": int(advert_obj.count()) - i,
                    }
                    advert_count = advert_count + int(advert_obj.count()) - i
                    subcat_list.append(sub_cat_data)
                cat_obj_data = {
                    "category_id": str(cat_obj.category_id),
                    "category_name": cat_obj.category_name,
                    "category_img": "",
                    "total_adverts_count": advert_count,
                    "total_likes": like_count,
                    "favorite": "0",
                    "subcategories": subcat_list,
                    "category_color": color
                }
                category_list.append(cat_obj_data)
        data = {'success': 'true', 'message': '', 'category_list': category_list, 'level': level}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Something went wrong', 'category_list': [], 'level': ''}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_advert_list(request):
    json_obj = json.loads(request.body)
    category_id = json_obj['category_id']
    city_id = json_obj['city_id']
    user_id = json_obj['user_id']
    level = json_obj['level']
    advert_list = []
    try:
        print level
        if level == '1':
            advert_map_obj = Advert.objects.filter(category_level_1=category_id)
        if level == '2':
            advert_map_obj = Advert.objects.filter(category_level_2=CategoryLevel2.objects.get(category_id=category_id))

        if level == '3':
            advert_map_obj = Advert.objects.filter(category_level_3=category_id)
        if level == '4':
            advert_map_obj = Advert.objects.filter(category_level_4=category_id)
        if level == '5':
            advert_map_obj = Advert.objects.filter(category_level_5=category_id)
        if level == '0':
            advert_map_obj = Advert.objects.filter(category_id=category_id)
        print advert_map_obj
        for advert_map in advert_map_obj:
            if advert_map.city_place_id:
                if int(advert_map.city_place_id.city_place_id) == int(city_id):
                    phone_list = []
                    email_list = []
                    advert_id = str(advert_map.advert_id)
                    pre_date = datetime.now().strftime("%m/%d/%Y")
                    pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                    advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                    end_date = advert_sub_obj.business_id.end_date
                    end_date = datetime.strptime(end_date, "%m/%d/%Y")
                    date_gap = end_date - pre_date
                    print date_gap
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
                            advert_like_obj = AdvertLike.objects.get(advert_id=advert_id, user_id=str(user_id))
                            is_like = "true"
                        except Exception:
                            is_like = "false"

                        try:
                            advert_like_obj = AdvertFavourite.objects.get(advert_id=advert_id, user_id=str(user_id))
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
                            "is_favourite": is_favourite,
                            "views": str(views_count),
                            "reviews": "0",
                            "phone": phone_list,
                            "email": email_list,
                            "ratings": "3.2",
                            "level": level
                        }
                        advert_list.append(advert_data)
        data = {'success': 'true', 'message': '', 'advert_list': advert_list, 'category_id': category_id}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Something went wrong', 'advert_list': [], 'category_id': category_id}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_advert_details(request):
    json_obj = json.loads(request.body)
    advert_id = json_obj['advert_id']
    user_id = json_obj['user_id']
    category_id = json_obj['category_id']
    level = json_obj['level']
    advert_list = []
    try:
        mobile_list = []
        landline_list = []
        email_list = []
        image_list = []
        video_list = []
        time_list = []
        advert_id = str(advert_id)
        advert_obj = Advert.objects.get(advert_id=advert_id)
        if advert_obj.advert_views:
            views_count = int(advert_obj.advert_views) + 1
        else:
            views_count = 1
        advert_obj.advert_views = views_count
        advert_obj.save()

        try:
            coupon_obj = CouponCode.objects.get(advert_id=advert_id, user_id=json_obj['user_id'])
            coupon_flag = 'true'
        except Exception, ke:
            coupon_flag = 'false'

        try:
            advert_like_obj = AdvertLike.objects.get(advert_id=advert_id, user_id=str(user_id))
            is_like = "true"
        except Exception:
            is_like = "false"

        try:
            advert_like_obj = AdvertFavourite.objects.get(advert_id=advert_id, user_id=str(user_id))
            is_favourite = "true"
        except Exception:
            is_favourite = "false"

        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
        start_date = advert_sub_obj.business_id.start_date
        end_date = advert_sub_obj.business_id.end_date
        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")
        landmark = ''
        address = advert_obj.address_line_1
        if advert_obj.address_line_2:
            address = address + ', ' + advert_obj.address_line_2
        if advert_obj.area:
            address = address + ', ' + advert_obj.area
            landmark = advert_obj.area
        if advert_obj.city_place_id:
            address = address + ', ' + advert_obj.city_place_id.city_id.city_name
            landmark = landmark + ' ' + advert_obj.city_place_id.city_id.city_name
        if advert_obj.state_id:
            address = address + ', ' + advert_obj.state_id.state_name
        if advert_obj.pincode_id:
            address = address + '-' + advert_obj.pincode_id.pincode

        phone_obj = PhoneNo.objects.filter(advert_id=advert_id)
        advert_img_obj = AdvertImage.objects.filter(advert_id=advert_id)
        advert_video_obj = Advert_Video.objects.filter(advert_id=advert_id)

        for advert_img in advert_img_obj:
            image_url = advert_img.advert_image.url
            image_list.append(image_url)

        for advert_video in advert_video_obj:
            video_url = advert_video.advert_video_name.url
            video_list.append(video_url)

        for phone in phone_obj:
            phone_no = phone.phone_no
            phone_name = phone.phone_category_id.phone_category_name
            if phone_name == 'Mobile':
                mobile_list.append(phone_no)
            else:
                landline_list.append(phone_no)

        email_list.append(advert_obj.email_primary)
        if advert_obj.email_secondary:
            email_list.append(advert_obj.email_secondary)

        if advert_obj.display_image:
            image_url = advert_obj.display_image.url
        else:
            image_url = ''

        if advert_obj.any_other_details:
            other_details = advert_obj.any_other_details
        else:
            other_details = ''

        if advert_obj.product_description:
            product_description = advert_obj.product_description
        else:
            product_description = ''

        if advert_obj.discount_description:
            discount_description = advert_obj.discount_description
        else:
            discount_description = ''

        hours_obj = WorkingHours.objects.filter(advert_id=advert_id)
        for hours in hours_obj:
            timing = hours.day + ', ' + hours.start_time.lower() + ' to ' + hours.end_time.lower()
            time_list.append(timing)

        time_list = ["Monday, 9:30 am to 1:30 pm, 4:30 am to 11:30 pm",
                     "Tuesday, 9:30 am to 1:30 pm, 4:30 am to 11:30 pm"]

        advert_like_obj = AdvertLike.objects.filter(advert_id=advert_id)

        like_count = 0
        for advert_like in advert_like_obj:
            like_count = like_count + 1

        if advert_obj.speciality:
            speciality = advert_obj.speciality
        else:
            speciality = ''

        if advert_obj.short_description:
            short_description = advert_obj.short_description
        else:
            short_description = ''

        review_list = []
        review_data_1 = {
            "reviewer_name": "Alisha Menon",
            "reviewer_image": "/static/assets/layouts/layout2/img/City_Hoopla_Logo.png",
            "review_date": "28 August 2016",
            "review": "A new restaurant in busy area of Chinchwad, this one is gaining popularity because of its affordable barbecue and tasty food. Table booking is recommended. They have the option of ala carte as well as buffet meals. Buffet includes the barbecue snacks. The options in barbecue are less. Food is tasty. Service is good if you turn up early. Service quality diminishes at peak time. Overall it's a must visit once.",
            "review_rating": "4.2"
        }
        review_list.append(review_data_1)
        review_data_2 = {
            "reviewer_name": "John Marks",
            "reviewer_image": "/static/assets/layouts/layout2/img/City_Hoopla_Logo.png",
            "review_date": "24 August 2016",
            "review": "Ambiance is good for a rooftop restaurant but you have to wait as it is very crowded and then the staff and captain are not in a mood to serve maybe they are tensed. Food is OK nothing great soups not up to the mark, panner tika was good, they must improve on quality as it is crowded so if the quality and service improves they have made it . ",
            "review_rating": "3.8"
        }
        review_list.append(review_data_2)
        review_data_3 = {
            "reviewer_name": "Alisha Menon",
            "reviewer_image": "/static/assets/layouts/layout2/img/City_Hoopla_Logo.png",
            "review_date": "21 August 2016",
            "review": "Everything was good in veg buffet excep pineapple macroni. I don't know due to rush or anything else but management is too lazy or what. They can remove same or limited serves if they are not able to fetch orders in time. After ordering one macroni taking 1 hour to serve. We went on weekend and thought it was due to rush but in next week thursday same situation. Please remove macroni and do less pricing else serve properly and dont make customers to feel like they have asked for diamond after ordering same. ",
            "review_rating": "4.0"
        }
        review_list.append(review_data_3)

        if advert_obj.advert_views:
            advert_views = str(advert_obj.advert_views)
        else:
            advert_views = "0"

        advert_data = {
            "advert_id": str(advert_obj.advert_id),
            "advert_img": image_url,
            "name": advert_obj.advert_name,
            "location": address,
            "offer_start_date": start_date.strftime("%d %b %Y"),
            "offer_end_date": end_date.strftime("%d %b %Y"),
            "likes": str(like_count),
            "is_like": is_like,
            "is_favourite": is_favourite,
            "views": advert_views,
            "reviews": "3",
            "ratings": "3.2",
            "email": email_list,
            "discount_description": discount_description,
            "product_description": product_description,
            "other_details": other_details,
            "short_description": short_description,
            "latitude": advert_obj.latitude,
            "longitude": advert_obj.longitude,
            "opening_closing_time": time_list,
            "landline_no": landline_list,
            "phone_no": mobile_list,
            "image_list": image_list,
            "video_list": video_list,
            "landmark": landmark,
            "coupon_flag": coupon_flag,
            "review_list": review_list,
            "advert_speciality": speciality,
            "level": level
        }
        advert_list.append(advert_data)
        data = {'success': 'true', 'message': '', 'advert_list': advert_list, 'category_id': category_id,
                'level': level}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Something went wrong', 'advert_list': [], 'category_id': category_id,
                'level': level}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_coupon_code(request):
    json_obj = json.loads(request.body)
    advert_id = json_obj['advert_id']
    user_id = json_obj['user_id']
    try:
        advert_id = str(advert_id)
        advert_obj = Advert.objects.get(advert_id=advert_id)
        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
        category_name = advert_sub_obj.business_id.category.category_name
        city_name = advert_obj.city_place_id.city_id.city_name
        random_no = u''
        random_no = random_no.join(random.choice('0123456789') for i in range(4))
        coupon_code = 'CH' + city_name[:3].upper() + category_name[:2].upper() + str(random_no)

        coupon_obj = CouponCode.objects.create()
        coupon_obj.coupon_code = coupon_code
        coupon_obj.user_id = ConsumerProfile.objects.get(consumer_id=json_obj['user_id'])
        coupon_obj.advert_id = advert_obj
        coupon_obj.creation_date = datetime.now()
        coupon_obj.save()

        data = {'success': 'true', 'message': '', 'coupon_code': coupon_code}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': '', 'coupon_code': ''}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def like_advert(request):
    json_obj = json.loads(request.body)
    try:
        if json_obj['like_status'] == 'true':
            advert_like_obj = AdvertLike.objects.create()
            advert_like_obj.user_id = ConsumerProfile.objects.get(consumer_id=json_obj['user_id'])
            advert_like_obj.advert_id = Advert.objects.get(advert_id=json_obj['advert_id'])
            advert_like_obj.creation_date = datetime.now()
            advert_like_obj.save()
        else:
            advert_like_obj = AdvertLike.objects.get(advert_id=json_obj['advert_id'], user_id=json_obj['user_id'])
            advert_like_obj.delete()
        data = {'success': 'true', 'message': ''}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Oops! Something went wrong'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def favourite_advert(request):
    json_obj = json.loads(request.body)
    try:
        if json_obj['favourite_status'] == 'true':
            advert_fav_obj = AdvertFavourite.objects.create()
            advert_fav_obj.user_id = ConsumerProfile.objects.get(consumer_id=json_obj['user_id'])
            advert_fav_obj.advert_id = Advert.objects.get(advert_id=json_obj['advert_id'])
            advert_fav_obj.creation_date = datetime.now()
            advert_fav_obj.save()
        else:
            advert_fav_obj = AdvertFavourite.objects.get(advert_id=json_obj['advert_id'], user_id=json_obj['user_id'])
            advert_fav_obj.delete()
        data = {'success': 'true', 'message': ''}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Oops! Something went wrong'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_discount_details(request):
    json_obj = json.loads(request.body)
    user_id = json_obj['user_id']
    discount_detail = []
    try:
        coupon_obj = CouponCode.objects.filter(user_id=user_id)
        for coupons in coupon_obj:
            advert_obj = Advert.objects.get(advert_id=str(coupons.advert_id))
            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=str(coupons.advert_id))
            start_date = advert_sub_obj.business_id.start_date
            end_date = advert_sub_obj.business_id.end_date
            start_date = datetime.strptime(start_date, "%m/%d/%Y")
            end_date = datetime.strptime(end_date, "%m/%d/%Y")
            pre_date = datetime.now().strftime("%m/%d/%Y")
            pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
            date_gap = end_date - pre_date
            if int(date_gap.days) >= 0:
                status = 'Active'
            else:
                status = 'Inactive'
            address = ''
            if advert_obj.area:
                address = advert_obj.area
            if advert_obj.city_place_id:
                address = address + ' ' + advert_obj.city_place_id.city_id.city_name

            try:
                advert_like_obj = AdvertFavourite.objects.get(advert_id=str(coupons.advert_id), user_id=str(user_id))
                is_favourite = "true"
            except Exception:
                is_favourite = "false"

            try:
                advert_like_obj = AdvertLike.objects.get(advert_id=str(coupons.advert_id), user_id=str(user_id))
                is_like = "true"
            except Exception:
                is_like = "false"

            advert_like_obj = AdvertLike.objects.filter(advert_id=str(coupons.advert_id))

            like_count = 0
            for advert_like in advert_like_obj:
                like_count = like_count + 1

            if advert_obj.advert_views:
                advert_views = str(advert_obj.advert_views)
            else:
                advert_views = '0'

            advert_data = {
                "advert_id": str(advert_obj.advert_id),
                "name": advert_obj.advert_name,
                "location": address,
                "offer_start_date": start_date.strftime("%d %b %Y"),
                "offer_end_date": end_date.strftime("%d %b %Y"),
                "likes": str(like_count),
                "views": advert_views,
                "reviews": "0",
                "ratings": "3.2",
                "is_favourite": is_favourite,
                "is_like": is_like,
                "coupon_avail_date": coupons.creation_date.strftime("%d %b %Y"),
                "status": status
            }
            discount_detail.append(advert_data)
        data = {'success': 'true', 'message': '', 'count': len(discount_detail), 'discount_detail': discount_detail}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Something went wrong', 'count': '', 'discount_detail': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_favourite_details(request):
    json_obj = json.loads(request.body)
    user_id = json_obj['user_id']
    discount_detail = []
    try:
        advert_fav_obj = AdvertFavourite.objects.filter(user_id=user_id)
        for advert_fav in advert_fav_obj:
            advert_obj = Advert.objects.get(advert_id=str(advert_fav.advert_id))
            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=str(advert_fav.advert_id))
            start_date = advert_sub_obj.business_id.start_date
            end_date = advert_sub_obj.business_id.end_date
            start_date = datetime.strptime(start_date, "%m/%d/%Y")
            end_date = datetime.strptime(end_date, "%m/%d/%Y")
            pre_date = datetime.now().strftime("%m/%d/%Y")
            pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
            date_gap = end_date - pre_date
            if int(date_gap.days) >= 0:
                status = 'Active'
            else:
                status = 'Inactive'
            address = ''
            if advert_obj.area:
                address = advert_obj.area
            if advert_obj.city_place_id:
                address = address + ' ' + advert_obj.city_place_id.city_id.city_name

            try:
                advert_like_obj = AdvertLike.objects.get(advert_id=str(advert_fav.advert_id), user_id=str(user_id))
                is_like = "true"
            except Exception:
                is_like = "false"

            advert_like_obj = AdvertLike.objects.filter(advert_id=str(advert_fav.advert_id))

            like_count = 0
            for advert_like in advert_like_obj:
                like_count = like_count + 1
            if advert_obj.display_image:
                image_path = advert_obj.display_image.url
            else:
                image_path = ''
            if advert_obj.advert_views:
                views = advert_obj.advert_views
            else:
                views = 0
            advert_data = {
                "advert_id": str(advert_obj.advert_id),
                "name": advert_obj.advert_name,
                "category_id": str(advert_obj.category_id.category_id),
                "category_name": advert_obj.category_id.category_name,
                "advert_image": image_path,
                "location": address,
                "offer_start_date": start_date.strftime("%d %b %Y"),
                "offer_end_date": end_date.strftime("%d %b %Y"),
                "likes": str(like_count),
                "views": str(views),
                "reviews": "0",
                "ratings": "3.2",
                "is_favourite": "true",
                "is_like": is_like
            }
            discount_detail.append(advert_data)
        data = {'success': 'true', 'message': '', 'count': len(discount_detail), 'favourite_detail': discount_detail}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'count': '', 'message': 'Something went wrong', 'favourite_detail': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_active_discount_details(request):
    json_obj = json.loads(request.body)
    user_id = json_obj['user_id']
    discount_detail = []
    try:
        coupon_obj = CouponCode.objects.filter(user_id=user_id)
        for coupons in coupon_obj:
            advert_obj = Advert.objects.get(advert_id=str(coupons.advert_id))
            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=str(coupons.advert_id))
            start_date = advert_sub_obj.business_id.start_date
            end_date = advert_sub_obj.business_id.end_date
            start_date = datetime.strptime(start_date, "%m/%d/%Y")
            end_date = datetime.strptime(end_date, "%m/%d/%Y")
            pre_date = datetime.now().strftime("%m/%d/%Y")
            pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
            date_gap = end_date - pre_date
            if int(date_gap.days) >= 0:
                status = 'Active'
                address = ''
                if advert_obj.area:
                    address = advert_obj.area
                if advert_obj.city_place_id:
                    address = address + ' ' + advert_obj.city_place_id.city_id.city_name

                try:
                    advert_like_obj = AdvertFavourite.objects.get(advert_id=str(coupons.advert_id),
                                                                  user_id=str(user_id))
                    is_favourite = "true"
                except Exception:
                    is_favourite = "false"

                try:
                    advert_like_obj = AdvertLike.objects.get(advert_id=str(coupons.advert_id), user_id=str(user_id))
                    is_like = "true"
                except Exception:
                    is_like = "false"

                advert_like_obj = AdvertLike.objects.filter(advert_id=str(coupons.advert_id))

                like_count = 0
                for advert_like in advert_like_obj:
                    like_count = like_count + 1

                if advert_obj.advert_views:
                    advert_views = str(advert_obj.advert_views)
                else:
                    advert_views = '0'
                advert_data = {
                    "advert_id": str(advert_obj.advert_id),
                    "name": advert_obj.advert_name,
                    "location": address,
                    "offer_start_date": start_date.strftime("%d %b %Y"),
                    "offer_end_date": end_date.strftime("%d %b %Y"),
                    "likes": str(like_count),
                    "views": advert_views,
                    "reviews": "0",
                    "ratings": "3.2",
                    "is_like": is_like,
                    "is_favourite": is_favourite,
                    "coupon_avail_date": coupons.creation_date.strftime("%d %b %Y"),
                    "status": status
                }
                discount_detail.append(advert_data)
        data = {'success': 'true', 'message': '', 'count': len(discount_detail), 'discount_detail': discount_detail}
    except Exception, ke:
        print ke
        data = {'success': 'false', 'message': 'Something went wrong', 'count': '', 'discount_detail': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def edit_customer_profile(request):
    print "REQUEST", request.body
    try:
        json_obj = json.loads(request.body)
        print 'JSON OBJECT : ', json_obj
        if request.method == 'POST':
            customer_object = ConsumerProfile.objects.get(consumer_id=json_obj['user_id'])
            customer_object.consumer_full_name = json_obj['full_name']
            customer_object.consumer_contact_no = json_obj['phone']
            customer_object.consumer_updated_by = json_obj['full_name']
            # customer_object.consumer_email_id = json_obj['email_id']
            customer_object.device_token = json_obj['device_token']
            customer_object.consumer_area = json_obj['consumer_area']
            customer_object.consumer_updated_date = datetime.now()
            customer_object.save()

            # try:
            #    filename = "IMG_%s_%s.png" % (customer_object.username, str(datetime.now()).replace('.', '_'))
            #    resource = urllib.urlopen(json_obj['user_profile_image'])

            #    customer_object.consumer_profile_pic = ContentFile(resource.read(), filename)  # assign image to model
            #    customer_object.save()
            # except:
            #    pass

            data = {'success': 'true', 'message': 'Profile Updated Successfully',
                    'user_info': get_profile_info(customer_object.consumer_id)}
        else:
            data = {'success': 'false', 'message': 'Profile Update Failed'}
    except ConsumerProfile.DoesNotExist, e:
        print e
        data = {'success': 'false', 'message': 'User does not exists'}
    except Exception, e:
        print e
        data = {'success': 'false', 'message': 'Invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# save consumer feedback
@csrf_exempt
def consumer_feedback(request):
    try:
        json_obj = json.loads(request.body)
        print 'JSON OBJECT : ', json_obj
        if request.method == 'POST':
            user_id = json_obj['user_id']
            consumer_feedback = Consumer_Feedback(
                consumer_id=ConsumerProfile.objects.get(consumer_id=user_id),
                consumer_feedback=json_obj['feedback']
            );
            consumer_feedback.save()
            data = {'success': 'true', 'message': "Feedback Sent Successfully"}

    except Consumer_Feedback.DoesNotExist, e:
        data = {'success': 'false', 'message': "Feedback not Send"}
        print "failed to send mail", e
    except Exception, e:
        print e
        data = {'success': 'false', 'message': "Server Error, Please try again!"}
    return HttpResponse(json.dumps(data), content_type='application/json')


# update device_token
@csrf_exempt
def update_device_token(request):
    print "REQUEST", request.body
    try:
        ##        pdb.set_trace()
        json_obj = json.loads(request.body)

        if request.method == 'POST':
            customer_object = ConsumerProfile.objects.get(consumer_id=json_obj['user_id'])
            customer_object.device_token = json_obj['device_token']
            customer_object.save()
            data = {'success': 'true', 'message': 'Device Token Updated Successfully'}
    except ConsumerProfile.DoesNotExist, e:
        data = {'success': 'false', 'message': "Device token is not update"}
        print "Exception in Update Token", e
    except Exception, e:
        print e
        data = {'success': 'false', 'message': "Server Error, Please try again!"}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_profile_photo(request):
    try:
        json_obj = json.loads(request.body)
        if request.method == 'POST':
            try:
                customer_object = ConsumerProfile.objects.get(consumer_id=json_obj['user_id'])
                customer_object.consumer_profile_pic = save_image(
                    json_obj['user_profile_image'])
                customer_object.save()
            except:
                pass
            data = {'success': 'true', 'message': 'Profile Picture Updated Successfully',
                    'user_info': get_profile_info(customer_object.consumer_id)}
    except ConsumerProfile.DoesNotExist, e:
        data = {'success': 'false', 'message': "Profile Picture is not update"}
        print "Exception in Update Token", e
    except Exception, e:
        print e
        data = {'success': 'false', 'message': "Server Error, Please try again!"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_image(imgdata):
    import os
    print "save_image"
    # pdb.set_trace()
    try:
        filename = "uploaded_image%s.png" % str(datetime.now()).replace('.', '_')
        decoded_image = imgdata.decode('base64')
        return ContentFile(decoded_image, filename)
    except Exception, e:
        print e
        data = {'data': None}
        return False


@csrf_exempt
def search_advert(request):
    print "REQUEST", request.body
    try:
        ##      pdb.set_trace()
        json_obj = json.loads(request.body)
        flag = json_obj['flag']
        list = []
        advert_list = []
        advert_obj = Advert_Category_Map.objects.filter(
            category_id=Category.objects.get(category_id=json_obj['category_id']))
        for advert in advert_obj:
            list.append(str(advert.advert_id))
            if list:
                advert_obj_list = Advert.objects.filter(advert_id__in=list)

                if (flag == '1'):
                    consumer_latitude = json_obj['latitude']
                    consumer_longitude = json_obj['longitude']
                    distance = json_obj['distance']
                    lon_max, lon_min, lat_max, lat_min = bounding_box(float(consumer_latitude),
                                                                      float(consumer_longitude), float(distance))
                    advert_obj_list = Advert.objects.filter(latitude__range=[lat_min, lat_max],
                                                            longitude__range=[lon_min, lon_max],
                                                            advert_id__in=advert_obj_list)

                if (flag == '2'):
                    advert_obj_list = Advert.objects.filter(
                        product_price__range=[json_obj['min_price'], json_obj['max_price']],
                        advert_id__in=advert_obj_list)

                if (flag == '3'):
                    consumer_latitude = json_obj['latitude']
                    consumer_longitude = json_obj['longitude']
                    distance = json_obj['distance']
                    lon_max, lon_min, lat_max, lat_min = bounding_box(float(consumer_latitude),
                                                                      float(consumer_longitude), float(distance))
                    advert_obj_list = Advert.objects.filter(latitude__range=[lat_min, lat_max],
                                                            longitude__range=[lon_min, lon_max],
                                                            advert_id__in=advert_obj_list,
                                                            product_price__range=[json_obj['min_price'],
                                                                                  json_obj['max_price']])

                if advert_obj_list:
                    for advert in advert_obj_list:
                        advert_id = str(advert.advert_id)
                        advert_name = advert.advert_name
                        try:
                            advert_image = advert.display_image.url
                        except:
                            advert_image = ''
                        try:
                            advert_city = advert.city_place_id.city_name
                        except:
                            advert_city = ''
                        advert_area = advert.area
                        advert_discount = advert.discount_description
                        advert_obj = AdvertLike.objects.filter(advert_id=advert)
                        advert_like_count = len(advert_obj)
                        advert_view_count = 0
                        advert_review_count = 0
                        advert_email = advert.email_primary
                        try:
                            advert_contact = PhoneNo.objects.get(advert_id=advert).phone_no
                        except:
                            advert_contact = ''
                        advert_validity = ''
                        advert_price = ''
                        advert_rating = ''

                        advert_list = {'advert_rating': advert_rating, 'advert_price': advert_price,
                                       'advert_validity': advert_validity, 'advert_contact': advert_contact,
                                       'advert_email': advert_email, 'advert_review_count': advert_review_count,
                                       'advert_view_count': advert_view_count, 'advert_like_count': advert_like_count,
                                       'advert_discount': advert_discount, 'advert_area': advert_area,
                                       'advert_city': advert_city, 'advert_id': advert_id, 'advert_name': advert_name,
                                       'advert_image': advert_image}
        data = {'success': 'true', 'advert_list': advert_list}

    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def bounding_box(latitude, longitude, distance):
    lat_change = change_in_latitude(distance)
    lat_max = latitude + lat_change
    lat_min = latitude - lat_change
    lon_change = change_in_longitude(latitude, distance)
    lon_max = longitude + lon_change
    lon_min = longitude - lon_change
    return (lon_max, lon_min, lat_max, lat_min)


def change_in_latitude(distance):
    "Given a distance north, return the change in latitude."
    return (distance / earth_radius) * radians_to_degrees


def change_in_longitude(latitude, distance):
    r = earth_radius * math.cos(latitude * degrees_to_radians)
    return (distance / r) * radians_to_degrees


@csrf_exempt
def get_category(request):
    print "REQUEST", request.body
    try:
        cat_id_list = []
        json_obj = json.loads(request.body)
        cat_obj_list = CategoryCityMap.objects.filter(city_id=City.objects.get(city_id=json_obj['city_id']))
        for cat in cat_obj_list:
            cat_id_list.append(str(cat.category_id))
        if cat_id_list:
            category_obj_list = Category.objects.filter(category_id__in=cat_id_list)
            if category_obj_list:
                for category in category_obj_list:
                    category_id = str(category.category_id)
                    category_name = category.category_name
                    category_image = ''
                    category_advert = Advert.objects.filter(category_id=category)
                    category_advert_count = len(category_advert)
                    category_like = ''
                    category_favourite = ''
                    sub_category = Category.objects.filter(has_category=category)
                    if sub_category:
                        sub_category_list = []
                        for sub_cat in sub_category:
                            id = str(sub_cat.category_id)
                            name = sub_cat.category_name
                            count = ''
                            sub_category_list = {'id': id, 'name': name, 'count': count}

                    list = {'sub_category_list': sub_category_list, 'category_favourite': category_favourite,
                            'category_like': category_like, 'category_advert_count': category_advert_count,
                            'category_image': category_image, 'category_id': category_id,
                            'category_name': category_name}

        data = {'success': 'true', 'list': list}

    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def user_logout(request):
    json_obj = json.loads(request.body)
    user_obj = ConsumerProfile.objects.get(consumer_id=json_obj['user_id'])
    user_obj.online = '0'
    user_obj.save()
    data = {'success': 'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Save Sell Ticket
@csrf_exempt
def save_sellticket(request):
    try:
        # pdb.set_trace()
        json_obj = json.loads(request.body)
        print 'JSON OBJECT : ', json_obj
        user_id = json_obj['user_id']
        sellticket_obj = SellTicket(
            user_id=ConsumerProfile.objects.get(consumer_id=user_id),
            event_name=json_obj['event_name'],
            event_venue=json_obj['event_venue'],
            start_date=json_obj['start_date'],
            start_time=json_obj['start_time'],
            select_activation_date=json_obj['select_activation_date'],
            other_comments=json_obj['other_comments'],
            ticket_class=json_obj['ticket_class'],
            no_of_tickets=json_obj['no_of_tickets'],
            original_price=json_obj['original_price'],
            asking_price=json_obj['asking_price'],
            contact_number=json_obj['contact_number']

        )
        sellticket_obj.save()

        if json_obj['image_one']:
            sellticket_obj.image_one = save_image(json_obj['image_one'])
            sellticket_obj.save()

        if json_obj['image_two']:
            sellticket_obj.image_two = save_image(json_obj['image_two'])
            sellticket_obj.save()

        if json_obj['image_three']:
            sellticket_obj.image_three = save_image(json_obj['image_three'])
            sellticket_obj.save()

        data = {'success': 'true', 'message': 'Sell Ticket Saved Successfully'}

    except Exception, e:
        print "Exception", e
        data = {'success': 'false', 'message': 'Sell Ticket not Save'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Sell Ticket List
@csrf_exempt
def view_list_sellticket(request):
    try:
        # pdb.set_trace()
        sell_ticket_list = []
        sell_ticket_obj = SellTicket.objects.filter()
        if sell_ticket_obj:
            for ticket in sell_ticket_obj:
                user_id = str(ticket.user_id)
                consumer_object = ConsumerProfile.objects.get(consumer_id=user_id)
                phone_no = consumer_object.consumer_contact_no
                email = consumer_object.consumer_email_id
                if ticket.image_one:
                    image_one = ticket.image_one.url
                else:
                    image_one = ''

                tkt_data = {
                    "sellticket_id": str(ticket.sellticket_id),
                    "event_name": ticket.event_name,
                    "event_venue": ticket.event_venue,
                    "start_date": ticket.start_date.strftime('%d/%m/%Y'),
                    "start_time": ticket.start_time,
                    "image_one": image_one,
                    "phone_no": phone_no,
                    "email": email
                }
                sell_ticket_list.append(tkt_data)
            data = {"success": "true", "sell_ticket_list": sell_ticket_list}
        else:
            tkt_data = {
                "": ""
            }
            sell_ticket_list.append(tkt_data)
            data = {"success": "false", 'message': "Sell Ticket not Availabel"}

    except Exception, e:
        print "Exception", e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Sell Ticket Detail
@csrf_exempt
def view_sellticket_detail(request):
    try:
        # pdb.set_trace()
        sell_ticket_detail = []
        if request.method == 'POST':
            json_obj = json.loads(request.body)
            sellticket_id = json_obj['sellticket_id']
            ticket_object_list = SellTicket.objects.filter(sellticket_id=sellticket_id)
            for ticket_object in ticket_object_list:
                user_id = str(ticket_object.user_id)
                consumer_object = ConsumerProfile.objects.get(consumer_id=user_id)
                phone_no = consumer_object.consumer_contact_no
                email = consumer_object.consumer_email_id

                if ticket_object.image_one:
                    image_one = ticket_object.image_one.url
                else:
                    image_one = ''
                if ticket_object.image_two:
                    image_two = ticket_object.image_two.url
                else:
                    image_two = ''
                if ticket_object.image_three:
                    image_three = ticket_object.image_three.url
                else:
                    image_three = ''
                if ticket_object.image_four:
                    image_four = ticket_object.image_four.url
                else:
                    image_four = ''

                ticket_data = {
                    'image_one': image_one,
                    'image_two': image_two,
                    'image_three': image_three,
                    'image_four': image_four,
                    'event_name': ticket_object.event_name,
                    'event_venue': ticket_object.event_venue,
                    'start_date': ticket_object.start_date.strftime('%d/%m/%Y'),
                    'start_time': ticket_object.start_time,
                    'original_price': ticket_object.original_price,
                    'no_of_tickets': ticket_object.no_of_tickets,
                    'phone_no': phone_no,
                    'email': email,
                    'ticket_class': ticket_object.ticket_class,
                    'asking_price': ticket_object.asking_price
                }
                sell_ticket_detail.append(ticket_data)

        data = {"success": "true", "sell_ticket_detail": sell_ticket_detail}

    except Exception, e:
        print "Exception", e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_map_advert_list(request):
    json_obj = json.loads(request.body)
    user_id = json_obj['user_id']
    city_id = json_obj['city_id']
    lon_max, lon_min, lat_max, lat_min = bounding_box(
        float(json_obj['consumer_latitude']),
        float(json_obj['consumer_longitude']),
        float(json_obj['radius'])
    )
    advert_list = []
    try:
        advert_map_obj = Advert.objects.filter(
            city_place_id=city_id,
            latitude__range=[lat_min, lat_max],
            longitude__range=[lon_min, lon_max],
            status='1'
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
                    advert_like_obj = AdvertLike.objects.get(advert_id=advert_id, user_id=str(user_id))
                    is_like = "true"
                except Exception:
                    is_like = "false"

                try:
                    advert_like_obj = AdvertFavourite.objects.get(advert_id=advert_id, user_id=str(user_id))
                    is_favourite = "true"
                except Exception:
                    is_favourite = "false"

                views_count = AdvertView.objects.filter(advert_id=advert_id).count()
                like_count = AdvertLike.objects.filter(advert_id=advert_id).count()

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
                    "latitude": str(advert_obj.latitude),
                    "longitude": str(advert_obj.longitude),
                }
                advert_list.append(advert_data)
        # Token.objects.filter(user=user).delete()
        # token = Token.objects.create(user=user)
        # resp = {}
        # resp['authorization'] = "Token " + str(token)
        data = {"success": "true", "message": "", "advert_list": advert_list}

    except Exception, e:
        print "Exception", e
        data = {"success": "false", "message": "Something went wrong", "advert_list": advert_list}
    return HttpResponse(json.dumps(data), content_type='application/json')


def change_in_latitude(distance):
    "Given a distance north, return the change in latitude."
    return (distance / earth_radius) * radians_to_degrees


def change_in_longitude(latitude, distance):
    "Given a latitude and a distance west, return the change in longitude."
    # Find the radius of a circle around the earth at given latitude.
    r = earth_radius * math.cos(latitude * degrees_to_radians)
    return (distance / r) * radians_to_degrees


def bounding_box(latitude, longitude, distance):
    lat_change = change_in_latitude(distance)
    lat_max = latitude + lat_change
    lat_min = latitude - lat_change
    lon_change = change_in_longitude(latitude, distance)
    lon_max = longitude + lon_change
    lon_min = longitude - lon_change
    return (lon_max, lon_min, lat_max, lat_min)


@csrf_exempt
def post_advert_review(request):
    json_obj = json.loads(request.body)
    user_id = json_obj['user_id']
    advert_id = json_obj['advert_id']
    ratings = json_obj['ratings']
    review = json_obj['review']
    try:
        review_obj = AdvertReview()
        review_obj.user_id = ConsumerProfile.objects.get(consumer_id=user_id)
        review_obj.advert_id = Advert.objects.get(advert_id=advert_id)
        review_obj.ratings = ratings
        review_obj.review = review
        review_obj.creation_date = datetime.now()
        review_obj.save()
        data = {"success": "true", "message": "Review published successfully."}

    except Exception, e:
        print "Exception", e
        data = {"success": "false", "message": "Something went wrong"}
    return HttpResponse(json.dumps(data), content_type='application/json')
