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
import urllib2

SERVER_URL = "http://52.40.205.128"
#SERVER_URL = "http://192.168.0.151:9090"


# SERVER_URL = "http://52.40.205.128"
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_category(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        city_list = City_Place.objects.filter(city_status='1')
        data = {'city_list': city_list, 'username': request.session['login_user']}
        return render(request, 'Admin/add_category.html', data)

@csrf_exempt
def get_cat_sequence(request):
    city_id = request.POST.get('city_id')
    cat_city_obj = CategoryCityMap.objects.filter(city_place_id = city_id).order_by('sequence')
    i = 0
    sequence_list = []
    for city in cat_city_obj:
        i = i + 1
        sequnce_data = {
            'category_name' : city.category_id.category_name,
            'sequence' : city.sequence,
            'no' : str(i)
        }
        sequence_list.append(sequnce_data)
    print sequence_list
    data = {
        'success': 'true',
        'sequence_list':sequence_list
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_category(request):
    try:
        image = request.FILES['img']
        cat_color = request.POST.get('cat_color')
        x = request.POST.get('list')
        form_data = request.POST.get('form_data')
        cat_name = request.POST.get('cat_name')
        x = ast.literal_eval(x)
        y = [i for n, i in enumerate(x) if i not in x[n + 1:]]
        form_data = form_data.split('&')
        city_list=[]
        sequence_list=[]
        for k in range(len(form_data)):
            city_data = form_data[k].split('=')
            if city_data[0] == 'city':
                city_list.append(str(city_data[1]))
            if city_data[0] == 'sequence':
                sequence_list.append(str(city_data[1]))
        if city_list != ['']:
            print "city_list",city_list
            zipped_list = zip(city_list, sequence_list)
            print cheksamesequence(zipped_list)
            if cheksamesequence(zipped_list):
                print "check sum fail"
                data = {'message': 'Sequence for the selected city already exists, please view current sequence to know sequences used for various cities', 'success': 'false'}
                return HttpResponse(json.dumps(data), content_type='application/json')

        try:
            category_obj = Category.objects.get(category_name=request.POST.get('cat_name'))

            data = {
                'success': 'false',
                'message': "Category already exist"
            }

        except Exception, e:
            print e
            cat_obj = Category(
                category_name=cat_name,
                category_created_date=datetime.now(),
                category_updated_date=datetime.now(),
                category_status='1'
            )
            cat_obj.save()
            cat_obj.category_color = cat_color
            cat_obj.save()
            if image:
                cat_obj.category_image = request.FILES['img']
                cat_obj.save()
            if city_list != ['']:
                cat_map = create_city_map_obj(city_list, sequence_list, cat_obj)
                if cat_map == 'False':
                    data = {
                        'message': e,
                        'success': 'false'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
            for i in y:
                print i
                try:
                    if i['level_1']:
                        try:
                            cat_obj_level_1 = CategoryLevel1.objects.get(parent_category_id=cat_obj,
                                                                         category_name=i['level_1'])
                        except Exception:
                            cat_obj_level_1 = CategoryLevel1(
                                category_name=i['level_1'],
                                category_created_date=datetime.now(),
                                category_updated_date=datetime.now(),
                                category_status='1',
                                parent_category_id=cat_obj
                            )
                            cat_obj_level_1.save()
                    if i['level_2']:
                        for j in i['level_2']:
                            try:
                                cat_obj_level_2 = CategoryLevel2.objects.get(parent_category_id=cat_obj_level_1,
                                                                             category_name=j)
                            except Exception:
                                cat_obj_level_2 = CategoryLevel2(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_1
                                )
                                cat_obj_level_2.save()
                    if i['level_3']:
                        for j in i['level_3']:
                            try:
                                cat_obj_level_3 = CategoryLevel3.objects.get(parent_category_id=cat_obj_level_2,
                                                                             category_name=j)
                            except Exception:
                                cat_obj_level_3 = CategoryLevel3(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_2
                                )
                                cat_obj_level_3.save()
                    if i['level_4']:
                        for j in i['level_4']:
                            try:
                                cat_obj_level_4 = CategoryLevel4.objects.get(parent_category_id=cat_obj_level_3,
                                                                             category_name=j)
                            except Exception:
                                cat_obj_level_4 = CategoryLevel4(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_3
                                )
                                cat_obj_level_4.save()
                    if i['level_5']:
                        for j in i['level_5']:
                            try:
                                cat_obj_level_5 = CategoryLevel5.objects.get(parent_category_id=cat_obj_level_4,
                                                                             category_name=j)
                            except Exception:
                                cat_obj_level_5 = CategoryLevel5(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_4
                                )
                                cat_obj_level_5.save()
                except Exception as e:
                    data = {
                        'success': 'false',
                        'message': e,
                    }
            data = {
                'success': 'true',
                'message': "Category added successfully",
            }
            category_obj = Category.objects.get(category_name=request.POST.get('cat_name'))

            #add_category_sms(category_obj)

    except Exception as e:
        print e
    return HttpResponse(json.dumps(data), content_type='application/json')

def add_category_sms(category_obj):

    authkey = "118994AIG5vJOpg157989f23"
    #mobiles = "7507542642"
    mobiles = "+919403884595"

    category_name= category_obj.category_name
    print '....................category_name.......',category_name
    message = "Hi Admin,"+'\n'+"Category "+category_name+" has been added successfully"
    sender = "DGSPCE"
    route = "4"
    country = "91"

    values = {
              'authkey' : authkey,
              'mobiles' : mobiles,
              'message' : message,
              'sender' : sender,
              'route' : route,
              'country' : country
              }

    url = "http://api.msg91.com/api/sendhttp.php"
    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    output = response.read()



def create_city_map_obj(city_list,sequence_list,cat_obj):
    try:
        zipped_list = zip(city_list, sequence_list)
        if zipped_list:
            for city_id, sequence in zipped_list:
                if city_id != '' and sequence != '':
                    map_obj = CategoryCityMap(
                        city_place_id=City_Place.objects.get(city_place_id=city_id),
                        sequence=sequence,
                        category_id=cat_obj,
                        creation_date=datetime.now(),
                        updation_date=datetime.now()
                    )
                    map_obj.save()
        return 'True'
    except Exception as e:
        print e
        return 'False'

def cheksamesequence(zipped_list):
    for city_id, sequence in zipped_list:
        if city_id != '' and sequence != '':
            try:
                cat_obj = CategoryCityMap.objects.get(city_place_id=City_Place.objects.get(city_place_id=city_id),
                                                      sequence=sequence)
                return True
            except:
                return False


def updatecheksamesequence(zipped_list, cat_id):
    # pdb.set_trace()
    cat_obj = Category.objects.get(category_id=cat_id)
    for city_id, sequence in zipped_list:
        if city_id != '' and sequence != '':
            cat_obj = CategoryCityMap.objects.filter(city_place_id=City_Place.objects.get(city_place_id=city_id),
                                                     sequence=sequence).exclude(category_id=cat_obj.category_id)
            if cat_obj:
                return False
            else:
                return True


def category_list(request):
    try:
        data = {}
        final_list = []
        try:
            category_list = Category.objects.all()
            for cat_obj in category_list:
                category_id = str(cat_obj.category_id)
                active_advert = 'No'
                advert_obj_list = Advert.objects.filter(category_id=category_id)
                obj_count = Advert.objects.filter(category_id=category_id).count()
                inactive_count = Advert.objects.filter(category_id=category_id,status='0').count()
                if advert_obj_list:
                    if obj_count == inactive_count:
                        active_advert = 'No'
                    else:
                        for advert_obj in advert_obj_list:
                            advert_id = str(advert_obj.advert_id)
                            pre_date = datetime.now().strftime("%m/%d/%Y")
                            pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                            end_date = advert_sub_obj.business_id.end_date
                            end_date = datetime.strptime(end_date, "%m/%d/%Y")
                            date_gap = end_date - pre_date
                            if int(date_gap.days) >= 0:
                                active_advert = 'Yes'

                category_name = cat_obj.category_name
                city_name = CategoryCityMap.objects.filter(category_id=cat_obj)
                city_list = ''
                if city_name:
                    for city in city_name:
                        city_list = str(city.city_place_id.city_id.city_name) + ',' + city_list
                    city_list = city_list[:-1]
                if not city_list:
                    city_list = 'All'
                creation_date = str(cat_obj.category_created_date).split()[0]
                updation_date = str(cat_obj.category_updated_date).split()[0]
                if (cat_obj.category_status == '1'):
                    status = 'Active'
                    if active_advert == 'No':
                        delete = '<a id="' + str(
                            category_id) + '" onclick="delete_category(this.id)" style="text-align: center;letter-spacing: 5px;width:15%;" title="Delete"  ><i class="fa fa-trash"></i></a>'
                    else:
                        delete = ''
                    edit = '<a  id="' + str(category_id) + '" href="/edit-category/?category_id=' + str(
                        category_id) + '" style="text-align: center;letter-spacing: 5px;width:15%;" title="Edit" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-pencil"></i></a>'
                    actions = edit + delete
                else:
                    status = 'Inactive'
                    active = '<a class="col-md-2" id="' + str(
                        cat_obj) + '" onclick="active_service(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;margin-left: 36px !important;" title="Activate" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-repeat"></i></a>'
                    actions = active
                list = {'status': status, 'category_name': category_name, 'actions': actions, 'city_name': city_list,
                        'creation_date': creation_date, 'updation_date': updation_date, 'updated_by':cat_obj.category_updated_by}
                final_list.append(list)
            data = {'success': 'true', 'data': final_list}
        except IntegrityError as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    # print '====data============',data
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def delete_category(request):
    try:
        cat_obj = Category.objects.get(category_id=request.POST.get('category_id'))
        cat_obj.category_status = '0'
        cat_obj.save()
        data = {'message': 'User Role De-activeted Successfully', 'success': 'true'}
        inactive_category_mail(cat_obj)
        #delete_category_sms(cat_obj)

    except IntegrityError as e:
        print e
    except Exception, e:
        print e
        print "Final Data: ", data
    return HttpResponse(json.dumps(data), content_type='application/json')


def delete_category_sms(cat_obj):
    print 'sssssssssssssssssssssss'
    
    category_name= cat_obj.category_name
    authkey = "118994AIG5vJOpg157989f23"
    mobiles = "+919403884595"
    message = "Hi Admin,"+'\n'+"Category "+category_name+" has been deactivated successfully "
    sender = "DGSPCE"
    route = "4"
    country = "91"
    values = {
              'authkey' : authkey,
              'mobiles' : mobiles,
              'message' : message,
              'sender' : sender,
              'route' : route,
              'country' : country
              }

    url = "http://api.msg91.com/api/sendhttp.php"
    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    output = response.read()



@csrf_exempt
def delete_sub_category(request):
    try:
        level_name = request.POST.get('sub_cat_level')
        cat_id = request.POST.get('sub_cat_id')
        obj_list = []
        if level_name == 'level_1':
            cat_obj = CategoryLevel1.objects.get(category_id=cat_id)
            cat_obj.delete()
        if level_name == 'level_2':
            cat_obj = CategoryLevel2.objects.get(category_id=cat_id)
            cat_obj.delete()
        if level_name == 'level_3':
            cat_obj = CategoryLevel3.objects.get(category_id=cat_id)
            cat_obj.delete()
        if level_name == 'level_4':
            cat_obj = CategoryLevel4.objects.get(category_id=cat_id)
            cat_obj.delete()
        if level_name == 'level_5':
            cat_obj = CategoryLevel5.objects.get(category_id=cat_id)
            cat_obj.delete()
        data = {'message': 'User Role De-activeted Successfully', 'success': 'true'}

    except IntegrityError as e:
        print e
    except Exception, e:
        print e
        print "Final Data: ", data
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_city(request):
    city_list = []
    try:
        city_objs = City_Place.objects.filter(city_status='1').order_by('city_id__city_name')
        for city in city_objs:
            options_data = '<option value=' + str(
                city.city_place_id) + '>' + city.city_id.city_name + '</option>'
            city_list.append(options_data)
            print city_list
        data = {'city_list': city_list}

    except Exception, ke:
        print ke
        data = {'city_list': 'none', 'message': 'No city available'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_category(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        try:
            data = {}
            final_list = []
            sub_category1_list = []
            sub_category2_list = []
            sub_category3_list = []
            sub_category4_list = []
            sub_category5_list = []
            city_list = City_Place.objects.filter(city_status='1')
            selected_city_list = []
            selected_sequence_list = []

            try:
                category = Category.objects.get(category_id=request.GET.get('category_id'))
                category_id = str(category.category_id)
                category_name = str(category.category_name)
                city_name = CategoryCityMap.objects.filter(category_id=category)
                sequence_list = ['1', '2', '3', '4', '5']

                for city in city_name:
                    selected_city_list.append(str(city.city_place_id.city_id.city_name))
                    selected_sequence_list.append(str(city.sequence))

                city_sequence_list = zip(selected_city_list, selected_sequence_list)

                active_advert = 'No'

                advert_obj_list = Advert.objects.filter(category_id = category_id)
                for advert_obj in advert_obj_list:
                    advert_id = str(advert_obj.advert_id)
                    pre_date = datetime.now().strftime("%m/%d/%Y")
                    pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
                    advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                    end_date = advert_sub_obj.business_id.end_date
                    end_date = datetime.strptime(end_date, "%m/%d/%Y")
                    date_gap = end_date - pre_date
                    if int(date_gap.days) >= 0:
                        active_advert = 'Yes'

                print "=====active_advert=====",active_advert

                print '=====category=======', category
                sub_category1 = CategoryLevel1.objects.filter(parent_category_id=category)
                if sub_category1:
                    for cat in sub_category1:
                        sub_category2 = CategoryLevel2.objects.filter(parent_category_id=cat)
                        if sub_category2:
                            has_subcategory = 'Yes'
                        else:
                            has_subcategory = 'No'
                        category1_list = {
                                            'category_id':str(cat.category_id),
                                            'category_name': cat.category_name,
                                            'parent_category_id':str(cat.parent_category_id),
                                            'has_subcategory':has_subcategory
                                          }

                        sub_category1_list.append(category1_list)
                length1 = len(sub_category1_list)
                print '=====category1=======',sub_category1
                sub_category2 = CategoryLevel2.objects.filter(parent_category_id__in=sub_category1)
                if sub_category2:
                    for cat in sub_category2:
                        sub_category3 = CategoryLevel3.objects.filter(parent_category_id=cat)
                        if sub_category3:
                            has_subcategory = 'Yes'
                        else:
                            has_subcategory = 'No'
                        category2_list = {
                                            'category_id':str(cat.category_id),
                                            'category_name': cat.category_name,
                                            'parent_category_id':str(cat.parent_category_id),
                                            'has_subcategory': has_subcategory
                                          }
                        sub_category2_list.append(category2_list)
                length2 = len(sub_category2_list)
                print '=====category2======='
                sub_category3 = CategoryLevel3.objects.filter(parent_category_id__in=sub_category2)
                if sub_category3:
                    for cat in sub_category3:
                        sub_category4 = CategoryLevel4.objects.filter(parent_category_id=cat)
                        if sub_category4:
                            has_subcategory = 'Yes'
                        else:
                            has_subcategory = 'No'
                        category3_list = {
                                            'category_id':str(cat.category_id),
                                            'category_name': cat.category_name,
                                            'parent_category_id':str(cat.parent_category_id),
                                            'has_subcategory':has_subcategory
                                          }
                        sub_category3_list.append(category3_list)
                length3 = len(sub_category3_list)
                print '=====category3======='
                sub_category4 = CategoryLevel4.objects.filter(parent_category_id__in=sub_category3)
                if sub_category4:
                    for cat in sub_category4:
                        sub_category5 = CategoryLevel5.objects.filter(parent_category_id=cat)
                        if sub_category5:
                            has_subcategory = 'Yes'
                        else:
                            has_subcategory = 'No'
                        category4_list = {
                                            'category_id':str(cat.category_id),
                                            'category_name': cat.category_name,
                                            'parent_category_id':str(cat.parent_category_id),
                                            'has_subcategory':has_subcategory
                                          }
                        sub_category4_list.append(category4_list)
                length4 = len(sub_category4_list)
                print '=====category4======='
                sub_category5 = CategoryLevel5.objects.filter(parent_category_id__in=sub_category4)
                if sub_category5:
                    for cat in sub_category5:
                        category5_list = {
                                            'category_id':str(cat.category_id),
                                            'category_name': cat.category_name,
                                            'parent_category_id':str(cat.parent_category_id)
                                          }
                        sub_category5_list.append(category5_list)
                length5 = len(sub_category5_list)
                print '=====category5======='

                data = {'username': request.session['login_user'], 'sequence_list': sequence_list, 'length5': length5,
                        'length4': length4, 'length3': length3, 'length2': length2, 'length1': length1,
                        'category_id': category_id, 'city_sequence_list': city_sequence_list, 'city_list': city_list,
                        'success': 'true', 'sub_category5_list': sub_category5_list,'cat_img':SERVER_URL + category.category_image.url,
                        'sub_category4_list': sub_category4_list, 'sub_category3_list': sub_category3_list,
                        'sub_category2_list': sub_category2_list, 'category_name': category_name,'active_advert':active_advert,
                        'sub_category1_list': sub_category1_list, 'cat_color':str(category.category_color) or '#000000'}

            except IntegrityError as e:
                print e
                data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
        except MySQLdb.OperationalError, e:
            print e
        except Exception, e:
            print 'Exception ', e
        return render(request, 'Admin/edit_category.html', data)

@csrf_exempt
def update_category(request):
    #print request.POST
    image = request.POST.get('img')
    cat_color = request.POST.get('cat_color')
    print cat_color
    if image:
        image = request.FILES['img']
    x = request.POST.get('list')
    form_data = request.POST.get('form_data')
    cat_name = request.POST.get('cat_name')
    x = ast.literal_eval(x)
    y = [i for n, i in enumerate(x) if i not in x[n + 1:]]
    form_data = form_data.split('&')
    city_list = []
    sequence_list = []
    for k in range(len(form_data)):
        city_data = form_data[k].split('=')
        if city_data[0] == 'category_id':
            category_id = str(city_data[1])
        if city_data[0] == 'city':
            city_list.append(str(city_data[1]))
        if city_data[0] == 'sequence':
            sequence_list.append(str(city_data[1]))
    if city_list != ['']:
        zipped_list = zip(city_list, sequence_list)
        if not (updatecheksamesequence(zipped_list, category_id)):
            data = {
                'message': 'Sequence for the selected city already exists, please view current sequence to know sequences used for various cities',
                'success': 'false'}
            return HttpResponse(json.dumps(data), content_type='application/json')
    try:
        cat_obj = Category.objects.get(category_id=category_id)
        cat_obj.category_name = cat_name
        cat_obj.category_updated_date = datetime.now()
        cat_obj.category_updated_by = request.session['login_user']
        cat_obj.updated_by = cat_color
        cat_obj.save()
        if image:
            cat_obj.category_image = request.FILES['img']
            cat_obj.save()
        CategoryCityMap.objects.filter(category_id=cat_obj).delete()
        if city_list != ['']:
            cat_map = create_city_map_obj(city_list, sequence_list, cat_obj)
            if cat_map == 'False':
                data = {
                    'message': 'Error',
                    'success': 'false'
                }
                return HttpResponse(json.dumps(data), content_type='application/json')
        for i in y:
            try:
                if i['level_1']:
                    try:
                        cat_obj_level_1 = CategoryLevel1.objects.get(parent_category_id=cat_obj,
                                                                     category_id=i['level_id_1'])
                        cat_obj_level_1.category_name = i['level_1']
                        cat_obj_level_1.save()
                    except Exception:
                        cat_obj_level_1 = CategoryLevel1(
                            category_name=i['level_1'],
                            category_created_date=datetime.now(),
                            category_updated_date=datetime.now(),
                            category_status='1',
                            parent_category_id=cat_obj
                        )
                        cat_obj_level_1.save()
                if i['level_2']:
                    for j,k in zip(i['level_2'],i['level_id_2']):
                        if j:
                            try:
                                cat_obj_level_2 = CategoryLevel2.objects.get(parent_category_id=cat_obj_level_1,
                                                                             category_id=k)
                                cat_obj_level_2.category_name = j
                                cat_obj_level_2.save()
                            except Exception:
                                cat_obj_level_2 = CategoryLevel2(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_1
                                )
                                cat_obj_level_2.save()
                if i['level_3']:

                    for j, k in zip(i['level_3'], i['level_id_3']):
                        if j:
                            try:
                                cat_obj_level_3 = CategoryLevel3.objects.get(parent_category_id=cat_obj_level_2,
                                                                             category_id=k)
                                cat_obj_level_3.category_name = j
                                cat_obj_level_3.save()
                            except Exception:
                                cat_obj_level_3 = CategoryLevel3(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_2
                                )
                                cat_obj_level_3.save()
                if i['level_4']:

                    for j, k in zip(i['level_4'], i['level_id_4']):
                        if j:
                            try:
                                cat_obj_level_4 = CategoryLevel4.objects.get(parent_category_id=cat_obj_level_3,
                                                                             category_id=k)
                                cat_obj_level_4.category_name = j
                                cat_obj_level_4.save()
                            except Exception:
                                cat_obj_level_4 = CategoryLevel4(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_3
                                )
                                cat_obj_level_4.save()
                if i['level_5']:
                    #print i['level_id_5']
                    for j, k in zip(i['level_5'], i['level_id_5']):
                        if j:
                            try:
                                cat_obj_level_5 = CategoryLevel5.objects.get(parent_category_id=cat_obj_level_4,
                                                                             category_id=k)
                                cat_obj_level_5.category_name = j
                                cat_obj_level_5.save()
                            except Exception:
                                cat_obj_level_5 = CategoryLevel5(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_4
                                )
                                cat_obj_level_5.save()
            except Exception as e:
                data = {
                    'success': 'false',
                    'message': e,
                }
        data = {
            'success': 'true',
            'message': "Category added successfully",
        }
        #edit_category_mail(cat_obj)
        #edit_category_sms(cat_obj)
    except Exception, e:
        print "==============EXCEPTION+++++++++++++++++++++++++++++++++++++", e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def edit_category_sms(cat_obj):

    authkey = "118994AIG5vJOpg157989f23"
    mobiles = "+919403884595"

    category_name= cat_obj.category_name
    print '....................category_name.......',category_name
    message = "Hi Admin,"+'\n'+"Category "+category_name+" has been updated successfully"
    sender = "DGSPCE"
    route = "4"
    country = "91"
    print 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk'



    values = {
              'authkey' : authkey,
              'mobiles' : mobiles,
              'message' : message,
              'sender' : sender,
              'route' : route,
              'country' : country
              }

    url = "http://api.msg91.com/api/sendhttp.php"
    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    output = response.read()
    print output


def add_category_mail(cat_obj):
    gmail_user = "cityhoopla2016"
    gmail_pwd = "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    # pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCategory " + str(
            cat_obj.category_name) + " " + "has been added successfully." + "\nTo view complete details visit portal and follow - Reference Data -> Category" + "\n\nThank You," + '\n' + "CityHoopla Team"
        SUBJECT = "Category Added Successfully!"
        # server = smtplib.SMTP_SSL()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()

        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException, e:
        print e
    return 1


def edit_category_mail(cat_obj):
    gmail_user = "cityhoopla2016"
    gmail_pwd = "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    # pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCategory " + str(
            cat_obj.category_name) + " " + "has been updated successfully." + "\nTo view complete details visit portal and follow - Reference Data -> Category" + "\n\nThank You," + '\n' + "CityHoopla Team"
        SUBJECT = "Category Updated Successfully!"
        # server = smtplib.SMTP_SSL()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()

        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException, e:
        print e
    return 1


def inactive_category_mail(cat_obj):
    gmail_user = "cityhoopla2016"
    gmail_pwd = "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    # pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCategory " + str(
            cat_obj.category_name) + " " + "has been deactivated successfully." + "\n\nThank You," + '\n' + "CityHoopla Team"
        SUBJECT = "Category Deactivated Successfully!"
        # server = smtplib.SMTP_SSL()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()

        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException, e:
        print e
    return 1


@csrf_exempt
def active_category(request):
    # pdb.set_trace()
    try:
        cat_obj = Category.objects.get(category_id=request.POST.get('category_id'))
        cat_obj.category_status = '1'
        cat_obj.save()
        data = {'message': 'Category activeted Successfully', 'success': 'true'}
        category_active_mail(cat_obj)

    except IntegrityError as e:
        print e
    except Exception, e:
        print e
    print "Final Data: ", data
    return HttpResponse(json.dumps(data), content_type='application/json')


def category_active_mail(cat_obj):
    gmail_user = "cityhoopla2016"
    gmail_pwd = "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    # pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCategory " + str(
            cat_obj.category_name) + " " + " has been activated successfully.\nTo view complete details visit portal and follow - Reference Data -> Category\n\n Thank You," + '\n' + "CityHoopla Team"
        SUBJECT = "Category Activated Successfully!"
        # server = smtplib.SMTP_SSL()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()

        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException, e:
        print e
    return 1


def save_subcategory(level, subcategory_list, category_object):
    i = 0
    subcategory_obj_list = Category.objects.filter(has_category=category_object, level=level)
    for category in subcategory_obj_list:
        category.category_name = subcategory_list[i]
        category.save()
        i = i + 1

    if i < len(subcategory_list):
        for j in range(i, len(subcategory_list)):
            category_obj = Category(
                category_name=subcategory_list[j],
                level=level,
                category_created_date=datetime.now(),
                category_updated_date=datetime.now(),
                category_status='1'
            )
            category_obj.save()
            category_obj.has_category = category_object
            category_obj.save()
            j = j + 1
