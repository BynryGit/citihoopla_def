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
from digispaceapp.models import UserProfile

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
from captcha_form import CaptchaForm
import operator
from django.db.models import Q
import datetime
from datetime import datetime
from datetime import date, timedelta
from django.views.decorators.cache import cache_control
# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect

SERVER_URL = "http://52.40.205.128"   
#SERVER_URL = "http://127.0.0.1:8000"

#CTI CRM APIs=============================================================================

def crm_login_form(request):
    form = CaptchaForm()
    return render(request,'CTI_CRM/operator_login.html', dict(form=form))

def crm_home(request):
    return render(request,'CTI_CRM/crm_home.html')

@csrf_exempt
def demo_function(request):
    print 'in demo'
    data = {}
    try:
        if request.method == "POST":
            print 'list: ', request.POST.getlist('a')

    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def get_consumer_detail(request):
    data = {}
    try:
        if request.method == "POST":
            print 'number: ', request.POST.get('number')
            user_obj = CallerDetails.objects.get(IncomingTelNo=request.POST.get('number'))
            print '--------user_obj-----',user_obj
            if user_obj :
                phone_number = user_obj.IncomingTelNo
                data= { 'success' : 'true','phone_number':str(phone_number),'caller_id':str(user_obj)}
            else:
                print '---------record not found---------'
                data= { 'success' : 'false'}

    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def crm_login(request):
        data = {}
        try:
            if request.POST:
                print 'logs: login request with: ', request.POST
                username = request.POST['username']
                password = request.POST['password']
                try:
                        user_obj = Operator.objects.get(username=username)
                        user = authenticate(username=username, password=password)
                        print 'valid form befor----->'
                        if user :
                            if user.is_active:
                                print 'valid form after----->',user
                                user_profile_obj = Operator.objects.get(username=user)
                                print '---user_profile_obj----',user_profile_obj
                                if user_profile_obj.operator_status=="1":
                                    print '--------in if ---------'
                                    request.session['login_user'] = user_profile_obj.username
                                    print "USERNAME",request.session['login_user']
                                    login(request,user)
                                    print "USERNAME",request.session['login_user']
                                    data= { 'success' : 'true','username':request.session['login_user']}
                            else:
                                data= { 'success' : 'false', 'message':'User Is Not Active'}
                                return HttpResponse(json.dumps(data), content_type='application/json')
                        else:
                                data= { 'success' : 'Invalid Password', 'message' :'Invalid Password'}
                                print "====Password",data
                                return HttpResponse(json.dumps(data), content_type='application/json')
                except:
                        data= { 'success' : 'false', 'message' :'Invalid Username'}
                        return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                    data= { 'success' : 'Invalid Captcha', 'message' :'Invalid Captcha'}
                    print "INVALID CAPTCHA"
                    return HttpResponse(json.dumps(data), content_type='application/json')
        except MySQLdb.OperationalError, e:
            print e
            data= {'success' : 'false', 'message':'Internal server'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception, e:
            print 'Exception ', e
            data= { 'success' : 'false', 'message':'Invalid Username or Password'}
        return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def caller_details_api(request):
    try:
        json_obj = json.loads(request.body)
        print '----------json obj--------',json_obj
        call_obj = CallInfo(
            UCID=json_obj['UCID'],
            CallerID=json_obj['CallerID'],
            CalledNo=json_obj['CalledNo'],
            CallStartTime=json_obj['CallStartTime'],
            DialStartTime=json_obj['DialStartTime'],
            DialEndTime=json_obj['DialEndTime'],
            DisconnectType=json_obj['DisconnectType'],
            CallStatus=json_obj['CallStatus'],
            CallDuration=json_obj['CallDuration'],
            CallType=json_obj['CallType'],
            AudioRecordingURL=json_obj['Audio Recording URL'],
            DialedNumber=json_obj['DialedNumber'],
            Department=json_obj['Department'],
            Extn=json_obj['Extn']
        );
        call_obj.save()
        data= { 'success' : 'true'}

    except Exception, e:
        print 'Exception ', e
        data= { 'success' : 'false', 'message':'Invalid data'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def crm_details(request):
    user_obj = CallerDetails.objects.get(CallerID=request.GET.get('callerid'))
    enquiry=''
    address=''
    e_date=''
    action=''
    caller_id=''
    detail_list=[]
    caller_id = user_obj.CallerID
    phone_number = user_obj.IncomingTelNo
    first_name = user_obj.first_name
    last_name = user_obj.last_name
    CallerArea = user_obj.CallerArea
    CallerCity = user_obj.CallerCity
    CallerPincode = user_obj.CallerPincode

    enquiry_obj = EnquiryDetails.objects.filter(CallerID=user_obj)
    print '--------enquiry obj-----',enquiry_obj
    sr_no=0
    for e in enquiry_obj:
        sr_no=sr_no+1
        enquiry = e.enquiryFor
        print '-----enquiry-----',enquiry
        address = str(e.SelectedArea) +','+str(e.SelectedCity)+'-'+str(e.SelectedPincode)
        e_date = e.created_date

        data_list={'sr_no':sr_no,'enquiry':enquiry,'address':address,'e_date':e_date}
        detail_list.append(data_list)

    data = {'detail_list':detail_list,'caller_id':caller_id,'phone_number':phone_number,'first_name':first_name,'last_name':last_name,'area':CallerArea,'city':CallerCity,'pincode':CallerPincode,
            'enquiry':enquiry,'address':address,'e_date':e_date}
    return render(request,'CTI_CRM/crm_details.html',data)

def new_consumer(request):
    data={}
    city_list = City.objects.all()
    data = {'city_list':city_list}
    return render(request,'CTI_CRM/new_consumer.html',data)

@csrf_exempt
def save_consumer_details(request):
    print "IN SAVE consumer"
    id = Pincode.objects.get(pincode=request.POST.get('pincode'))
    city = City.objects.get(city_id=request.POST.get('city'))
    mobile = CallerDetails.objects.get(IncomingTelNo=request.POST.get('mobile'))
    print '---------mobile--------',mobile
    try:
        if request.method == "POST":
            if CallerDetails.objects.get(IncomingTelNo=request.POST.get('mobile')):
                data = {'success': 'exists','caller_id':str(mobile)}
            else:
                caller_obj = CallerDetails(
                    first_name=request.POST.get('fname'),
                    last_name=request.POST.get('lname'),
                    IncomingTelNo=request.POST.get('mobile'),
                    email=request.POST.get('email'),
                    CallerArea=request.POST.get('area'),
                    CallerPincode=id,
                    CallerCity=city,
                    caller_created_date=datetime.now()
                )
                caller_obj.save()
                print '--------caller id------',caller_obj
                data = {'success': 'true','caller_id':str(caller_obj)}

    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_pincode_list(request):
    data={}
    pincode_list = []
    try:
        city_id = request.GET.get('city_id')
        city_id1 = City_Place.objects.get(city_id=str(city_id))
        city_id2 = City.objects.get(city_id=str(city_id1.city_id.city_id))
        pincode_list1 = Pincode.objects.filter(city_id=city_id2.city_id).order_by('pincode')
        pincode_objs = pincode_list1.values('pincode').distinct()
        for pincode in pincode_objs:
            options_data = '<option>' + pincode['pincode'] + '</option>'
            pincode_list.append(options_data)
            #print pincode_list
        data = {'pincode_list': pincode_list}
    except Exception, ke:
        print ke
        data = {'city_list': 'none', 'message': 'No city available'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def enquiry_form(request):
    user_obj = CallerDetails.objects.get(CallerID=request.GET.get('callerid'))
    phone_number = user_obj.IncomingTelNo
    first_name = user_obj.first_name
    last_name = user_obj.last_name
    CallerArea = user_obj.CallerArea
    CallerCity = user_obj.CallerCity
    CallerPincode = user_obj.CallerPincode
    email = user_obj.email
    cid = request.GET.get('callerid')

    #category_list = Category.objects.all()
    #business_list = Business.objects.all()
    #subcategory_list1 = CategoryLevel1.objects.all()
    #subcategory_list2 = CategoryLevel2.objects.all()
    #city_list = City.objects.all()

    #data = {'city_list':city_list,'category_list':category_list,'subcategory_list1':subcategory_list1,'subcategory_list2':subcategory_list2,'first_name':first_name,'phone_number':phone_number,'last_name':last_name,'CallerArea':CallerArea,'CallerCity':CallerCity,'CallerPincode':CallerPincode}

    data = {'cid':cid,'email':email,'first_name':first_name,'phone_number':phone_number,'last_name':last_name,'CallerArea':CallerArea,'CallerCity':CallerCity,'CallerPincode':CallerPincode}

    print data
    return render(request,'CTI_CRM/equiry_form.html',data)

def enquiry_search_results(request):
    return render(request,'CTI_CRM/enquiry_search_results.html')
#
# def crm_logout(request):
#     logout(request)
#     form = CaptchaForm()
#     return render_to_response('Admin/user_login.html', dict(
#         form=form, message_logout='You have successfully logged out.'
#     ), context_instance=RequestContext(request))


@csrf_exempt
def save_enquiry_details(request):
    i=0
    print '------------in save----------',request.POST.get('alist')
    try:
        cid = CallerDetails.objects.get(CallerID=request.POST.get('cid'))
        list = request.POST.get('alist')
        ele = list.split(',')
        for i in range(len(ele)):
            print ele[i]
            supplier_obj = Supplier.objects.get(supplier_id=ele[i])
            business_name = supplier_obj.business_name
            cat_obj = Business.objects.get(supplier=supplier_obj)
            cat_id = cat_obj.category
            enq_obj = EnquiryDetails(
                CallerID = cid,
                enquiryFor=request.POST.get('keyword'),
                SelectedArea = supplier_obj.area,
                SelectedPincode = supplier_obj.pincode,
                SelectedCity = supplier_obj.city,
                category_id = cat_id,
                created_date = datetime.now()
            );
            enq_obj.save()
            data = {'success':'true'}
    except Exception as e:
        print e
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def enquiry_search_details(request):
    print '------------in search----------',request.POST.get('keyword')
    data = {}
    result_list=[]
    category_obj=[]
    n=0
    try:
        if request.method == "POST":
            if request.POST.get('keyword'):
                text = request.POST.get('keyword')
                area = request.POST.get('area')
                try :
                    if Supplier.objects.filter(business_name__icontains=text):
                        category_obj = business_search(text,area)
                        if category_obj:
                            print '---------len-----',len(category_obj)
                            data = {'result_list':category_obj,'success':'true'}
                        else :
                            data = {'success':'false'}

                    elif Category.objects.filter(category_name__icontains=text):
                        category_obj = category_search(text,area)
                        if category_obj:
                            print '---------len-----',len(category_obj)
                            data = {'result_list':category_obj,'success':'true'}
                        else :
                            data = {'success':'false'}

                    elif CategoryLevel1.objects.filter(category_name__icontains=text):
                        if area=='':
                            area = ''
                            category_obj = category_search1(text,area)
                        else:
                            category_obj = category_search1(text,area)
                        #category_obj = category_search1(text)
                        if category_obj:
                            print '---------len-----',len(category_obj)
                            data = {'result_list':category_obj,'success':'true'}
                        else :
                            data = {'success':'false'}

                    elif CategoryLevel2.objects.filter(category_name__icontains=text):
                        if area=='':
                            area = ''
                            category_obj = category_search2(text,area)
                        else:
                            category_obj = category_search2(text,area)
                        #category_obj = category_search2(text)
                        if category_obj:
                            print '---------len-----',len(category_obj)
                            data = {'result_list':category_obj,'success':'true'}
                        else :
                            data = {'success':'false'}

                    elif CategoryLevel3.objects.filter(category_name__icontains=text):
                        if area=='':
                            area = ''
                            category_obj = category_search3(text,area)
                        else:
                            category_obj = category_search3(text,area)
                        #category_obj = category_search3(text)
                        if category_obj:
                            print '---------len-----',len(category_obj)
                            data = {'result_list':category_obj,'success':'true'}
                        else :
                            data = {'success':'false'}

                    elif CategoryLevel4.objects.filter(category_name__icontains=text):
                        if area=='':
                            area = ''
                            category_obj = category_search4(text,area)
                        else:
                            category_obj = category_search4(text,area)
                        #category_obj = category_search4(text)
                        if category_obj:
                            print '---------len-----',len(category_obj)
                            data = {'result_list':category_obj,'success':'true'}
                        else :
                            data = {'success':'false'}

                    elif CategoryLevel5.objects.filter(category_name__icontains=text):
                        if area=='':
                            area = ''
                            category_obj = category_search5(text,area)
                        else:
                            category_obj = category_search5(text,area)
                        #category_obj = category_search5(text)
                        if category_obj:
                            print '---------len-----',len(category_obj)
                            data = {'result_list':category_obj,'success':'true'}
                        else :
                            data = {'success':'false'}

                    # elif City.objects.filter(city_name__icontains=text):
                    #     city_obj = city_search(text)
                    #     category_obj = city_obj
                    #     if category_obj:
                    #         data = {'result_list':category_obj,'success':'true'}
                    #     else :
                    #         data = {'success':'false'}

                    elif Advert.objects.filter(keywords__icontains=text):
                        for c in Advert.objects.filter(keywords__icontains=text):
                            print '----------- 7 ---------'
                            if area:
                                supplier_id = str(c.supplier_id)
                                supplier_obj = Supplier.objects.filter(supplier_id=supplier_id,area__icontains=area)
                                for s in supplier_obj:
                                    supplier_id = s.supplier_id
                                    business_name = str(s.business_name)
                                    address = str(b.address1)+' '+str(b.address2)+','+str(b.city)+'-'+str(b.pincode)
                                    business_obj = Business.objects.filter(supplier=s)
                                    for b in business_obj:
                                        cat = str(b.category)
                                        cat_obj = Category.objects.filter(category_id=cat)
                                        for cat in cat_obj:
                                            cat_name = cat.category_name
                                            subcat1_obj = CategoryLevel1.objects.filter(parent_category_id=cat)
                                            for s1 in subcat1_obj:
                                                subcat1_name = s1.category_name
                                                subcat2_obj = CategoryLevel2.objects.filter(parent_category_id=s1)
                                                for s2 in subcat2_obj:
                                                    subcat2_name = s2.category_name
                                            advert_obj = {'supplier_id':supplier_id,'business_name':business_name,'category_name':cat_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                                            category_obj.append(advert_obj)
                                        category_obj = category_obj[:10]
                            else:
                                supplier_id = str(c.supplier_id)
                                supplier_obj = Supplier.objects.filter(supplier_id=supplier_id)
                                for s in supplier_obj:
                                    supplier_id = s.supplier_id
                                    business_name = str(s.business_name)
                                    address = str(b.address1)+' '+str(b.address2)+','+str(b.city)+'-'+str(b.pincode)
                                    business_obj = Business.objects.filter(supplier=s)
                                    for b in business_obj:
                                        cat = str(b.category)
                                        cat_obj = Category.objects.filter(category_id=cat)
                                        for cat in cat_obj:
                                            cat_name = cat.category_name
                                            subcat1_obj = CategoryLevel1.objects.filter(parent_category_id=cat)
                                            for s1 in subcat1_obj:
                                                subcat1_name = s1.category_name
                                                subcat2_obj = CategoryLevel2.objects.filter(parent_category_id=s1)
                                                for s2 in subcat2_obj:
                                                    subcat2_name = s2.category_name
                                            advert_obj = {'supplier_id':supplier_id,'business_name':business_name,'category_name':cat_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                                            category_obj.append(advert_obj)
                                        category_obj = category_obj[:10]
                        if category_obj:
                            print '---------len-----',len(category_obj)
                            data = {'result_list':category_obj,'success':'true'}
                        else :
                            data = {'success':'false'}

                    print '-------data-------',data
                except Exception,e:
                    print e
                    data = {'success':'false'}
            else:
                data = {'message': "No Result Found", 'success':'false'}

    except Exception as e:
        print e
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def business_search(text,area):
    print '----------- 1 ---------',area
    category_obj1=[]
    category_obj=[]
    subcat2_name = ''
    if area:
        b_obj = Supplier.objects.filter(business_name__icontains=text,area__icontains=area)
        for b in b_obj:
            print '--------b_obj------',b
            supplier_id = b
            name = b.business_name
            address = str(b.address1)+' '+str(b.address2)+','+str(b.city)+'-'+str(b.pincode)
            category_obj = Business.objects.filter(supplier=b)
            print '-----------category obj-------',category_obj
            for c in category_obj:
                cat_obj = str(c.category)
                cat_name = Category.objects.get(category_id=str(cat_obj))
                cname = str(cat_name.category_name)
                subcat1_obj = CategoryLevel1.objects.filter(parent_category_id=cat_name)
                for s1 in subcat1_obj:
                    subcat1_name = str(s1.category_name)
                    subcat2_obj = CategoryLevel2.objects.filter(parent_category_id=s1)
                    for s2 in subcat2_obj:
                        subcat2_name = str(s2.category_name)
                        cat_obj = {'supplier_id':str(supplier_id),'business_name':name,'category_name':cname,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                category_obj1.append(cat_obj)
            category_obj1 = category_obj1[:10]
        return category_obj1

    else:
        print '-------in else---------'
        business_obj = Supplier.objects.filter(business_name__icontains=text)
        for b in business_obj:
            supplier_id = b
            name = b.business_name
            address = str(b.address1)+' '+str(b.address2)+','+str(b.city)+'-'+str(b.pincode)
            category_obj = Business.objects.filter(supplier__icontains=business_obj)
            for c in category_obj:
                cat_obj = str(c.category)
                cat_name = Category.objects.get(category_id=str(cat_obj))
                cname = str(cat_name.category_name)
                subcat1_obj = CategoryLevel1.objects.filter(parent_category_id=cat_name)
                for s1 in subcat1_obj:
                    subcat1_name = str(s1.category_name)
                    subcat2_obj = CategoryLevel2.objects.filter(parent_category_id=s1)
                    for s2 in subcat2_obj:
                        subcat2_name = str(s2.category_name)
                        cat_obj = {'supplier_id':str(supplier_id),'business_name':name,'category_name':cname,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                category_obj1.append(cat_obj)
            category_obj1 = category_obj1[:10]
        return category_obj1

def category_search(text,area):
    print '----------- 2 ---------',area
    subcat2_name = ''
    category_obj=[]
    if area:
        category_obj1 = Category.objects.filter(category_name__icontains=text)
        for c in category_obj1:
            cname1 = c.category_name
            subcat1_obj = CategoryLevel1.objects.filter(parent_category_id=c)
            for s1 in subcat1_obj:
                subcat1_name = s1.category_name
                subcat2_obj = CategoryLevel2.objects.filter(parent_category_id=s1)
                for s2 in subcat2_obj:
                    subcat2_name = s2.category_name
        business_obj1 = Business.objects.filter(category__icontains=category_obj1)
        for b in business_obj1:
            b_obj = Supplier.objects.filter(supplier_id__icontains=b.supplier,area__icontains=area)
            print '------------b obj----2------------',b_obj
            for c in b_obj:
                supplier_obj = c.supplier.business_name
                supplier_id = c.supplier.supplier_id
                address = str(c.supplier.address1)+' '+str(c.supplier.address2)+','+str(c.supplier.city)+'-'+str(c.supplier.pincode)
                cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':cname1,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                category_obj.append(cat_obj)
            category_obj = category_obj[:10]
            return category_obj

    else:
        category_obj1 = Category.objects.filter(category_name__icontains=text)
        for c in category_obj1:
            cname1 = c.category_name
            subcat1_obj = CategoryLevel1.objects.filter(parent_category_id=c)
            for s1 in subcat1_obj:
                subcat1_name = s1.category_name
                subcat2_obj = CategoryLevel2.objects.filter(parent_category_id=s1)
                for s2 in subcat2_obj:
                    subcat2_name = s2.category_name
        business_obj1 = Business.objects.filter(category__icontains=category_obj1)
        for b in business_obj1:
            supplier_obj = b.supplier.business_name
            supplier_id = b.supplier.supplier_id
            address = str(b.supplier.address1)+' '+str(b.supplier.address2)+','+str(b.supplier.city)+'-'+str(b.supplier.pincode)
            cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':cname1,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
            category_obj.append(cat_obj)
        category_obj = category_obj[:10]
        return category_obj

def category_search1(text,area):
    print '----------- 3 ---------',area
    subcat2_name = ''
    category_obj=[]
    if area:
        category_obj2 = CategoryLevel1.objects.filter(category_name__icontains=text)
        for c in category_obj2:
            cname = c.parent_category_id
            subcat1_name = c.category_name
            subcat2_obj = CategoryLevel2.objects.filter(parent_category_id=c)
            for s2 in subcat2_obj:
                subcat2_name = s2.category_name
            category_name = c.parent_category_id.category_name
            business_obj = Business.objects.filter(category=cname)
            for b in business_obj:
                print '-------b---------',b
                b_obj = Supplier.objects.filter(supplier_id__icontains=b.supplier,area__icontains=area)
                print '------------b obj----2------------',b_obj
                for c in b_obj:
                    supplier_obj = c.supplier.business_name
                    supplier_id = c.supplier.supplier_id
                    address = str(c.supplier.address1)+' '+str(c.supplier.address2)+','+str(c.supplier.city)+'-'+str(c.supplier.pincode)
                    cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':category_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                    category_obj.append(cat_obj)
                category_obj = category_obj[:10]
            return category_obj

    else:
        category_obj2 = CategoryLevel1.objects.filter(category_name__icontains=text)
        for c in category_obj2:
            cname = c.parent_category_id
            subcat1_name = c.category_name
            subcat2_obj = CategoryLevel2.objects.filter(parent_category_id=c)
            for s2 in subcat2_obj:
                subcat2_name = s2.category_name
            category_name = c.parent_category_id.category_name
            business_obj = Business.objects.filter(category=cname)
            for b in business_obj:
                supplier_obj = b.supplier.business_name
                supplier_id = b.supplier.supplier_id
                address = str(b.supplier.address1)+' '+str(b.supplier.address2)+','+str(b.supplier.city)+'-'+str(b.supplier.pincode)
                cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':category_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                category_obj.append(cat_obj)
            category_obj = category_obj[:10]
        return category_obj

def category_search2(text,area):
    print '----------- 4 ---------',area
    category_obj=[]
    if area:
        category_obj2 = CategoryLevel2.objects.filter(category_name__icontains=text)
        for c in category_obj2:
            subcat2_name = c.category_name
            subcat1_name = c.parent_category_id.category_name
            cname = c.parent_category_id.parent_category_id
            category_name = c.parent_category_id.parent_category_id.category_name
            business_obj = Business.objects.filter(category=cname)
            for b in business_obj:
                print '-------b---------',b
                b_obj = Supplier.objects.filter(supplier_id__icontains=b.supplier,area__icontains=area)
                print '------------b obj----2------------',b_obj
                for c in b_obj:
                    supplier_obj = c.supplier.business_name
                    supplier_id = c.supplier.supplier_id
                    address = str(c.supplier.address1)+' '+str(c.supplier.address2)+','+str(c.supplier.city)+'-'+str(c.supplier.pincode)
                    cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':category_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                    category_obj.append(cat_obj)
                category_obj = category_obj[:10]
            return category_obj

    else:
        category_obj2 = CategoryLevel2.objects.filter(category_name__icontains=text)
        for c in category_obj2:
            subcat2_name = c.category_name
            subcat1_name = c.parent_category_id.category_name
            cname = c.parent_category_id.parent_category_id
            category_name = c.parent_category_id.parent_category_id.category_name
            business_obj = Business.objects.filter(category=cname)
            for b in business_obj:
                supplier_obj = b.supplier.business_name
                supplier_id = b.supplier.supplier_id
                address = str(b.supplier.address1)+' '+str(b.supplier.address2)+','+str(b.supplier.city)+'-'+str(b.supplier.pincode)
                cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':category_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                category_obj.append(cat_obj)
            category_obj = category_obj[:10]
        return category_obj

def category_search3(text,area):
    print '----------- 5 ---------',area
    category_obj=[]
    if area:
        category_obj2 = CategoryLevel3.objects.filter(category_name__icontains=text)
        for c in category_obj2:
            cname = c.parent_category_id.parent_category_id.parent_category_id
            subcat2_name = c.parent_category_id.category_name
            subcat1_name = c.parent_category_id.parent_category_id.category_name
            category_name = c.parent_category_id.parent_category_id.parent_category_id.category_name
            business_obj = Business.objects.filter(category=cname)
            for b in business_obj:
                print '-------b---------',b
                b_obj = Supplier.objects.filter(supplier_id__icontains=b.supplier,area__icontains=area)
                print '------------b obj----2------------',b_obj
                for c in b_obj:
                    supplier_obj = c.supplier.business_name
                    supplier_id = c.supplier.supplier_id
                    address = str(c.supplier.address1)+' '+str(c.supplier.address2)+','+str(c.supplier.city)+'-'+str(c.supplier.pincode)
                    cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':category_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                    category_obj.append(cat_obj)
                category_obj = category_obj[:10]
            return category_obj

    else:
        category_obj2 = CategoryLevel3.objects.filter(category_name__icontains=text)
        for c in category_obj2:
            cname = c.parent_category_id.parent_category_id.parent_category_id
            subcat2_name = c.parent_category_id.category_name
            subcat1_name = c.parent_category_id.parent_category_id.category_name
            category_name = c.parent_category_id.parent_category_id.parent_category_id.category_name
            business_obj = Business.objects.filter(category=cname)
            for b in business_obj:
                supplier_obj = b.supplier.business_name
                supplier_id = b.supplier.supplier_id
                address = str(b.supplier.address1)+' '+str(b.supplier.address2)+','+str(b.supplier.city)+'-'+str(b.supplier.pincode)
                cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':category_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                category_obj.append(cat_obj)
            category_obj = category_obj[:10]
        return category_obj

def category_search4(text,area):
    print '----------- 51 ---------',area
    category_obj=[]
    if area:
        category_obj2 = CategoryLevel4.objects.filter(category_name__icontains=text)
        for c in category_obj2:
            cname = c.parent_category_id.parent_category_id.parent_category_id.parent_category_id
            subcat2_name = c.parent_category_id.parent_category_id.category_name
            subcat1_name = c.parent_category_id.parent_category_id.parent_category_id.category_name
            category_name = c.parent_category_id.parent_category_id.parent_category_id.parent_category_id.category_name
            business_obj = Business.objects.filter(category=cname)
            for b in business_obj:
                print '-------b---------',b
                b_obj = Supplier.objects.filter(supplier_id__icontains=b.supplier,area__icontains=area)
                print '------------b obj----2------------',b_obj
                for c in b_obj:
                    supplier_obj = c.supplier.business_name
                    supplier_id = c.supplier.supplier_id
                    address = str(c.supplier.address1)+' '+str(c.supplier.address2)+','+str(c.supplier.city)+'-'+str(c.supplier.pincode)
                    cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':category_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                    category_obj.append(cat_obj)
                category_obj = category_obj[:10]
            return category_obj

    else:
        category_obj2 = CategoryLevel4.objects.filter(category_name__icontains=text)
        for c in category_obj2:
            cname = c.parent_category_id.parent_category_id.parent_category_id.parent_category_id
            subcat2_name = c.parent_category_id.parent_category_id.category_name
            subcat1_name = c.parent_category_id.parent_category_id.parent_category_id.category_name
            category_name = c.parent_category_id.parent_category_id.parent_category_id.parent_category_id.category_name
            business_obj = Business.objects.filter(category=cname)
            for b in business_obj:
                supplier_obj = b.supplier.business_name
                supplier_id = b.supplier.supplier_id
                address = str(b.supplier.address1)+' '+str(b.supplier.address2)+','+str(b.supplier.city)+'-'+str(b.supplier.pincode)
                cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':category_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                category_obj.append(cat_obj)
            category_obj = category_obj[:10]
        return category_obj


def category_search5(text,area):
    print '----------- 6 ---------'
    category_obj=[]
    if area:
        category_obj2 = CategoryLevel5.objects.filter(category_name__icontains=text)
        for c in category_obj2:
            cname = c.parent_category_id.parent_category_id.parent_category_id.parent_category_id.parent_category_id
            subcat2_name = c.parent_category_id.parent_category_id.parent_category_id.category_name
            subcat1_name = c.parent_category_id.parent_category_id.parent_category_id.parent_category_id.category_name
            category_name = c.parent_category_id.parent_category_id.parent_category_id.parent_category_id.parent_category_id.category_name
            business_obj = Business.objects.filter(category=cname)
            for b in business_obj:
                print '-------b---------',b
                b_obj = Supplier.objects.filter(supplier_id__icontains=b.supplier,area__icontains=area)
                print '------------b obj----2------------',b_obj
                for c in b_obj:
                    supplier_obj = c.supplier.business_name
                    supplier_id = c.supplier.supplier_id
                    address = str(c.supplier.address1)+' '+str(c.supplier.address2)+','+str(c.supplier.city)+'-'+str(c.supplier.pincode)
                    cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':category_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                    category_obj.append(cat_obj)
                category_obj = category_obj[:10]
            return category_obj

    else:
        category_obj2 = CategoryLevel5.objects.filter(category_name__icontains=text)
        for c in category_obj2:
            cname = c.parent_category_id.parent_category_id.parent_category_id.parent_category_id.parent_category_id
            subcat2_name = c.parent_category_id.parent_category_id.parent_category_id.category_name
            subcat1_name = c.parent_category_id.parent_category_id.parent_category_id.parent_category_id.category_name
            category_name = c.parent_category_id.parent_category_id.parent_category_id.parent_category_id.parent_category_id.category_name
            business_obj = Business.objects.filter(category=cname)
            for b in business_obj:
                supplier_obj = b.supplier.business_name
                supplier_id = b.supplier.supplier_id
                address = str(b.supplier.address1)+' '+str(b.supplier.address2)+','+str(b.supplier.city)+'-'+str(b.supplier.pincode)
                cat_obj = {'supplier_id':supplier_id,'business_name':supplier_obj,'category_name':category_name,'subcategory1':subcat1_name,'subcategory2':subcat2_name,'address':address}
                category_obj.append(cat_obj)
            category_obj = category_obj[:10]
        return category_obj

# def city_search(text):
#     data=[]
#     city_obj = City.objects.filter(city_name__icontains=text)
#     for c in city_obj:
#         supplier_obj = Supplier.objects.filter(city=c)
#         for s in supplier_obj:
#             business_name = str(s.business_name)
#             business_obj = Business.objects.filter(supplier=s)
#             for b in business_obj:
#                 cat = str(b.category)
#                 cat_obj = Category.objects.filter(category_id=cat)
#                 for cat in cat_obj:
#                     cat_name = cat.category_name
#                     city_obj = {'business_name':business_name,'category_name':cat_name}
#                     data.append(city_obj)
#         city_obj = data
#         return city_obj



#========================================================================================================================


