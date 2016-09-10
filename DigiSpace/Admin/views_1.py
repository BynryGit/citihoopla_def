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
from datetime import date, timedelta
from django.views.decorators.cache import cache_control
# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect

SERVER_URL = "http://52.40.205.128"   
#SERVER_URL = "http://127.0.0.1:8000"

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rate_card(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:    
        data = {'username':request.session['login_user']}
        return render(request,'Admin/rate_card.html',data)

def login_open(request):
    if request.user.is_authenticated():
        return redirect('/index/')
    else:
        form = CaptchaForm()
        return render_to_response('Admin/user_login.html', dict(
            form=form
        ), context_instance=RequestContext(request))

def backoffice(request):
    form = CaptchaForm()
##    if request.user.is_authenticated():
##        return redirect('/dashboard/')
    #return render_to_response('index.html')
    return render(request,'Admin/user_login.html', dict(form=form))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:  
        data ={'username':request.session['login_user'] }
        return render(request,'Admin/index.html',data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscriber(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        data={ 'username':request.session['login_user'] }
        return render(request,'Admin/supplier_list.html',data)  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)        
def consumer(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        data ={}
        return render(request,'Admin/consumer.html',data)        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
    	user_role_list = UserRole.objects.filter(role_status='1')
    	data = {'user_role_list':user_role_list}
    	return render(request,'Admin/user_list.html',data)        

def notification(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        return render(request,'Admin/notification.html')   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reference_data(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        data ={'username':request.session['login_user']}
        return render(request,'Admin/rdm.html',data)       

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_supplier(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        data = {'username':request.session['login_user'],'category_list':get_category(request),'currency':get_currency(request),'phone_category':get_phone_category(request),'state_list':get_state(request)}
        return render(request,'Admin/add_supplier.html',data)          

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_city(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        data = {'state_list':get_state(request),'category_list':get_category(request),'username':request.session['login_user']}
        return render(request,'Admin/add_city.html',data)  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        data = {'username':request.session['login_user']}
        return render(request,'Admin/category.html',data)  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_role(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        data ={'username':request.session['login_user']}
        return render(request,'Admin/user_role.html',data)  
       

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_advert(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        user_id = request.GET.get('user_id')
        tax_list = Tax.objects.all()
        
        service_list = ServiceRateCard.objects.filter(service_rate_card_status='1').values('service_name').distinct()    
        advert_service_list, item_ids = [], []
        for item in AdvertRateCard.objects.filter(advert_rate_card_status='1'):
            if item.advert_service_name not in item_ids:
                advert_service_list.append(str(item.advert_rate_card_id))
                item_ids.append(item.advert_service_name)

        advert_service_list = AdvertRateCard.objects.filter(advert_rate_card_id__in=advert_service_list)        

        data = {'tax_list':tax_list,'advert_service_list':advert_service_list,'service_list':service_list,'username':request.session['login_user'],'user_id':user_id,'category_list':get_category(request),'currency':get_currency(request),'phone_category':get_phone_category(request),'state_list':get_state(request)}
        return render(request,'Admin/add_advert.html',data)    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def consumer_detail(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        data ={'username':request.session['login_user']}
        return render(request,'Admin/consumer_detail.html',data) 
        
def deal_detail(request):
    data ={}
    return render(request,'Admin/deal_detail.html',data) 


@csrf_exempt
def signin(request):
        data = {}
        try:
            if request.POST:
                form = CaptchaForm(request.POST)
                print 'logs: login request with: ', request.POST
                username = request.POST['username']
                password = request.POST['password']
        # pdb.set_trace()
                #pdb.set_trace()
                if form.is_valid():
                    try:
                        user_obj = UserProfile.objects.get(username=username)

                        user = authenticate(username=username, password=password)
                        print 'valid form befor----->'
                        if user :
                            if user.is_active:
                                print 'valid form after----->',user
                                user_profile_obj = UserProfile.objects.get(username=user)
                                if user_profile_obj.user_status=="1":
                     
                                    request.session['login_user'] = user_profile_obj.username
                                    request.session['first_name'] = user_profile_obj.user_name 
                                    login(request,user)
                                    print "USERNAME",request.session['login_user']
                                    data= { 'success' : 'true','username':request.session['first_name']}
                                    
                                # else:
                                #     data= { 'success' : 'false', 'message' :'Invalid Password'}
                                #     print "=====PASSWORD===",data
                                #     return HttpResponse(json.dumps(data), content_type='application/json')
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
                    form = CaptchaForm()
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


def signing_out(request):
    logout(request)
    form = CaptchaForm()
    return render_to_response('Admin/user_login.html', dict(
        form=form, message_logout='You have successfully logged out.'
    ), context_instance=RequestContext(request))

@csrf_exempt
def add_user(request):
	try:
		role_id = UserRole.objects.get(role_id=request.POST.get('user_role'))
		user_obj=UserProfile(
			username=request.POST.get('username'),
			user_name=request.POST.get('username'),
			user_contact_no=request.POST.get('contact_no'),
			usre_email_id=request.POST.get('email'),
			user_role=role_id,
            user_created_date = datetime.now(),
			user_status = '1',
			user_created_by = request.session['login_user']
		);
		user_obj.save();
		user_obj.set_password(request.POST.get('password'));
		user_obj.save();

		data={
			'success':'true',
			'message':'User Created Successfully.'
		}
	except Exception, e:
		data={
			'success':'false',
			'message':str(e)
		}
	return HttpResponse(json.dumps(data),content_type='application/json')    


def view_user_list(request):
	try:
		data = {}
		final_list = []
		try:
			user_list = UserProfile.objects.filter(user_status='1')
			for user_obj in user_list:
				if user_obj.user_role:
					role_id = user_obj.user_role.role_name
					user_name = user_obj.user_name
					usre_email_id = user_obj.usre_email_id
					user_contact_no = user_obj.user_contact_no
					edit = '<a class="col-md-offset-2 col-md-1" id="'+str(user_obj)+'" onclick="edit_user_detail(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;" title="Edit" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-pencil"></i></a>'
					delete = '<a class="col-md-1" id="'+str(user_obj)+'" onclick="delete_user_detail(this.id)" style="text-align: center;letter-spacing: 5px;width:15%;" title="Delete"  ><i class="fa fa-trash"></i></a>'
					actions =  edit + delete
					list = {'user_name':user_name,'actions':actions,'role_id':role_id,'usre_email_id':usre_email_id,'user_contact_no':user_contact_no}
					final_list.append(list)
			data = {'success':'true','data':final_list}
		except IntegrityError as e:
			print e
			data = {'success':'false','message':'Error in  loading page. Please try after some time'}
	except MySQLdb.OperationalError, e:
		print e
	except Exception,e:
		print 'Exception ',e
	return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def delete_user(request):
        try:
            user_obj = UserProfile.objects.get(user_id=request.POST.get('user_id'))
            user_obj.user_status = '0'
            user_obj.save()
            data = {'message': 'User Inactivated Successfully', 'success':'true'}

        except IntegrityError as e:
          print e
        except Exception,e:
            print e
        print "Final Data: ",data
        return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def view_user_detail(request):
    try:
        data = {}
        final_list = []
        try:
            if request.method == "GET":
                user_obj = UserProfile.objects.get(user_id=request.GET.get('user_id'))
                role_id = str(user_obj.user_role)
                role_name = user_obj.user_role.role_name
                user_name = user_obj.user_name
                user_email_id = user_obj.usre_email_id
                user_contact_no = user_obj.user_contact_no
                data = {'success':'true','role_name':role_name,'role_id':role_id,'user_name':user_name,'user_email_id':user_email_id,'user_contact_no':user_contact_no}


        except IntegrityError as e:
            print e
            data = {'success':'false','message':'Error in  loading page. Please try after some time'}

    except MySQLdb.OperationalError, e:
        print e

    except Exception,e:
        print 'Exception ',e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def update_user_detail(request):
    
    try:
        #pdb.set_trace()
        data = {}
        #print 'role_id====',request.POST.get('e_user_role')
        role_id = UserRole.objects.get(role_id=request.POST.get('e_user_role'))
        #print '++++++++++++++++++++++hidden id================',request.POST.get('hidden_id')
        user_obj=UserProfile.objects.get(user_id=request.POST.get('hidden_id'))
        #print 'user_obj',user_obj
        #print '=============request.POST.get(user_id)=====',request.POST.get('user_id')

        user_obj.username=str(request.POST.get('e_username'))
        user_obj.user_name=str(request.POST.get('e_username'))
        #print 'Contact No====',request.POST.get('e_contact_no')
        user_obj.user_contact_no=request.POST.get('e_contact_no')
        user_obj.usre_email_id=str(request.POST.get('e_email'))
        user_obj.role_name=role_id
        user_obj.user_created_date = datetime.now()
        user_obj.user_status = '1'
        user_obj.user_created_by = request.session['login_user']
                
        user_obj.save();
        #user_obj.set_password(request.POST.get('e_password'));
        #user_obj.save();

        data={
            'success':'true',
            'message':'User Updated Successfully.'
        }
    except Exception, e:
            data={
                'success':'false',
                'message':str(e)
            }
    return HttpResponse(json.dumps(data),content_type='application/json')      

@csrf_exempt
def view_user_detail(request):
    try:
        data = {}
        final_list = []
        try:
            if request.method == "GET":
                user_obj = UserProfile.objects.get(user_id=request.GET.get('user_id'))
                role_id = str(user_obj.user_role)
                role_name = user_obj.user_role.role_name
                user_name = user_obj.user_name
                user_email_id = user_obj.usre_email_id
                user_contact_no = user_obj.user_contact_no
                data = {'success':'true','role_name':role_name,'role_id':role_id,'user_name':user_name,'user_email_id':user_email_id,'user_contact_no':user_contact_no}


        except IntegrityError as e:
            print e
            data = {'success':'false','message':'Error in  loading page. Please try after some time'}

    except MySQLdb.OperationalError, e:
        print e

    except Exception,e:
        print 'Exception ',e
    return HttpResponse(json.dumps(data), content_type='application/json')  

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

# TO GET THE CATEGOTRY
def get_category(request):
##    pdb.set_trace()
    cat_list = []
    try:
        category = Category.objects.filter(category_status='1',level='0').order_by('category_name')
        for cat in category:
            cat_list.append(
                {'category_id': cat.category_id, 'category': cat.category_name})

    except Exception, e:
        print 'Exception ', e
    return cat_list

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
def get_city(request):
   
   state_id=request.GET.get('state_id')
   city_list=[]
   try:
      city_objs=City.objects.filter(state_id=state_id,city_status='1').order_by('city_name')
      for city in city_objs:
         options_data = '<option value=' + str(
                   city.city_id) + '>' + city.city_name + '</option>'
         city_list.append(options_data)
         print city_list
      data = {'city_list': city_list}

   except Exception, ke:
      print ke
      data={'city_list': 'none','message':'No city available'}
   return HttpResponse(json.dumps(data), content_type='application/json')


# TO GET THE PINCODE
def get_pincode(request):
   #pdb.set_trace()

   pincode_list=[]
   try:
      city_id = request.GET.get('city_id')
      pincode_list1=Pincode.objects.filter(city_id=city_id,pincode_status='1').order_by('pincode')
      pincode_objs = pincode_list1.values('pincode').distinct()
      print pincode_objs
      for pincode in pincode_objs:
         options_data = '<option>' +pincode['pincode']+ '</option>'
         pincode_list.append(options_data)
         print pincode_list
      data = {'pincode_list': pincode_list}

   except Exception, ke:
      print ke
      data={'city_list': 'none','message':'No city available'}
   return HttpResponse(json.dumps(data), content_type='application/json')  
   

# payal
@csrf_exempt
def add_user_role(request):
    try:
        print '=========request============',request
        print '=========post==============',request.POST
        try:
            user_role_obj = UserRole.objects.get(role_name=request.POST.get('user_role'),role_status='1')
            print user_role_obj
            data={
                'success':'false',
                'message':'User role already exist.'
            }
        except:

            user_role_obj=UserRole(
                 role_name=request.POST.get('user_role'),
                role_status="1",
                role_created_date=datetime.now(),
                role_created_by="Admin",
                role_updated_by="Admin",
                role_updated_date = datetime.now(),
                
            );
            user_role_obj.save();
            user_role_add(user_role_obj)
            data={
                'success':'true',
                'message':'User role created successfully.'
            }
    except Exception, e:
        data={
            'success':'false',
            'message':str(e)
        }
    print '===========data================',data    
    return HttpResponse(json.dumps(data),content_type='application/json')   


def user_role_add(user_role_obj):
    gmail_user =  "cityhoopla2016"
    gmail_pwd =  "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    #pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nUser Role " + str(user_role_obj.role_name) + " " +"has been added successfully.\nTo view complete details visit portal and follow - Reference Data -> User Role\n\n Thank You,"+'\n'+"CityHoopla Team"
        SUBJECT = "User Role Added Successfully!"
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
 
def view_user_role_list(request):
    try:
        data = {}
        final_list = []
        try:
            user_role_list = UserRole.objects.all()
            print user_role_list
            for role_obj in user_role_list:
                role_id=role_obj.role_id
                role_name = role_obj.role_name
                role_creation_date = str(role_obj.role_created_date).split(' ')[0]

                if role_obj.role_status == '1':
                    # edit = '<a class="col-md-offset-2 col-md-1" id="'+str(role_id)+'" onclick="edit_user_role(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;" title="Edit" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-pencil"></i></a>'
                    edit = '<a class="col-md-offset-2 col-md-1" id="'+str(role_id)+'" onclick="edit_user_role(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;" title="Edit" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-pencil"></i></a>'
                    delete = '<a id="'+str(role_id)+'" onclick="delete_user_role(this.id)" style="text-align: center;letter-spacing: 5px;width:15%;" title="Delete"  ><i class="fa fa-trash"></i></a>'
                    status = 'Active'
                    actions =  edit + delete
                else:
                    status = 'Inactive'
                    active = '<a class="col-md-2" id="'+str(role_id)+'" onclick="active_service(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;margin-left: 50px !important;" title="Activate" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-repeat"></i></a>'
                    actions =  active
             
                list = {'role_name':role_name,'actions':actions,'role_id':role_id,'role_creation_date':role_creation_date}
                final_list.append(list)
            data = {'success':'true','data':final_list}
        except IntegrityError as e:
            print e
            data = {'success':'false','message':'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception,e:
        print 'Exception ',e
    print data    
    return HttpResponse(json.dumps(data), content_type='application/json')



@csrf_exempt
def edit_user_role(request):
    try:
        data = {}
        final_list = []
        try:
            if request.method == "GET":
                print request
                role_obj = UserRole.objects.get(role_id=request.GET.get('role_id'))
                role_id = str(role_obj.role_id)
                role_name = role_obj.role_name
               
                data = {'success':'true','role_name':role_name,'role_id':role_id}


        except IntegrityError as e:
            print e
            data = {'success':'false','message':'Error in  loading page. Please try after some time'}

    except MySQLdb.OperationalError, e:
        print e

    except Exception,e:
        print 'Exception ',e
    print data    
    return HttpResponse(json.dumps(data),content_type='application/json')      


@csrf_exempt
def update_user_role(request):
    # pdb.set_trace()
    try:
        print request.POST
        data = {}
        role_obj = request.POST.get('edit_role')
        role_id = request.POST.get('role_id')
        try:
            print "==========IN UPDATE ROLE======="
            role_object=UserRole.objects.get(role_name=request.POST.get('edit_role'))
            print "========role_object",role_object
            if(str(role_id)==str(role_object)):
                role_object=UserRole.objects.get(role_name=request.POST.get('edit_role'),role_status=1)
                role_object.role_name = request.POST.get('edit_role')
                role_object.save()
                user_role_edit(role_object)  
                data = {'success':'true'}
            else:
                data = {'success':'false'}
        except:
            role_object=UserRole.objects.get(role_id=role_id)
            role_object.role_name = request.POST.get('edit_role')
            role_object.save() 
            user_role_edit(role_object)  

            data={
                'success':'true',
                }
    except Exception, e:
            data={
                'success':'false',
                'message':str(e)
            }
    print '========data====================',data        
    return HttpResponse(json.dumps(data),content_type='application/json') 


def user_role_edit(role_object):
    gmail_user =  "cityhoopla2016"
    gmail_pwd =  "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    #pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nUser Role " + str(role_object.role_name) + " " +" has been updated successfully.\nTo view complete details visit portal and follow - Reference Data -> User Role\n\n Thank You,"+'\n'+"CityHoopla Team"
        SUBJECT = "User Role Added Successfully!"
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
def delete_user_role(request):
        try:
            role_obj = UserRole.objects.get(role_id=request.POST.get('role_id'))
            role_obj.role_status = '0'
            role_obj.save()
            user_role_delete(role_obj)
            data = {'message': 'User Role De-activeted Successfully', 'success':'true'}

        except IntegrityError as e:
          print e
        except Exception,e:
            print e
        print "Final Data: ",data
        return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def active_user_role(request):
        # pdb.set_trace()
        try:
            role_obj = UserRole.objects.get(role_id=request.POST.get('role_id'))
            role_obj.role_status = '1'
            role_obj.save()
            user_role_active(role_obj)
            data = {'message': 'User Role activated Successfully', 'success':'true'}

        except IntegrityError as e:
          print e
        except Exception,e:
            print e
        print "Final Data: ",data
        return HttpResponse(json.dumps(data), content_type='application/json')

def user_role_active(role_obj):
    gmail_user =  "cityhoopla2016"
    gmail_pwd =  "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    #pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nUser Role " + str(role_obj.role_name) + " " +" has been activated successfully.\nTo view complete details visit portal and follow - Reference Data -> User Role\n\n Thank You,"+'\n'+"CityHoopla Team"
        SUBJECT = "User Role Activated Successfully!"
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

def user_role_delete(role_obj):
    gmail_user =  "cityhoopla2016"
    gmail_pwd =  "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    #pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nUser Role " + str(role_obj.role_name) + " " +" has been updated successfully.\nTo view complete details visit portal and follow - Reference Data -> User Role\n\n Thank You,"+'\n'+"CityHoopla Team"
        SUBJECT = "User Role Added Successfully!"
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
def save_city(request):
    print "IN SAVE CITY", request.POST
    try:
        data = {}
        print request.POST
        print request.FILES
        print '=====type========',type(request.FILES)
        #pdb.set_trace()
        try:
            city_obj=City_Place.objects.get(city_name=request.POST.get('city_name'))
            data={'success':'false','messege':'City Already Exist'}   
        except Exception,e:
            city_obj=City_Place(
         
            city_name=request.POST.get('city_name'),
            state_id =State.objects.get(state_id=request.POST.get('state')),   
            )
            city_obj.save()
            if request.POST.get('about_city'):
                city_obj.about_city=request.POST.get('about_city')

            if request.POST.get('climate'):
                city_obj.climate=request.POST.get('climate')

            if request.POST.get('population'):
                city_obj.population = request.POST.get('population')

            if request.POST.get('timezone'):
                city_obj.time_zone=request.POST.get('timezone')

            if request.POST.get('language'):
                city_obj.language=request.POST.get('language')


            city_obj.save();
            city_place_id = city_obj.city_place_id
            print "city ID",city_place_id

            if request.POST['check_image'] == "1":
                city_obj.city_image = request.FILES['city_image']
                city_obj.save()
   
            data={
                    'success':'true',
                    'message':'City Added Successfully.',
                    "city_place_id":  city_place_id 
                    }


    except Exception, e:
        data={
            'success':'false',
            'message':str(e)
        }
    return HttpResponse(json.dumps(data),content_type='application/json') 



@csrf_exempt
def check_city(request):
    #pdb.set_trace()
    try:
            city_nm = request.POST.get('city');
            city_obj = City_Place.objects.all();
            for cit in city_obj:
                if city_nm == city_obj.city_name:
                    data = {'success':'false'}
                    return HttpResponse(json.dumps(data),content_type='application/json')
            data = {'success':'true'}
            return HttpResponse(json.dumps(data),content_type='application/json')
    except Exception,e:
        pass

@csrf_exempt
def save_city_data(request):
    try:
        city_obj=City_Place.objects.get(city_name=request.POST.get('city_name'))

        poi_range = request.POST.get('poi_range')
        point_of_interest_list = request.POST.get('point_of_interest_list')
        point_of_interest_list = str(point_of_interest_list).split(',')
        point_of_interest_image_list = []
        
        for i in range(int(poi_range)):
            image = "point_of_interest_image" + str(i)
            try:
                point_of_interest_image_list.append(request.FILES[image])                 
            except:
                point_of_interest_image_list.append('')

        zipped_wk = zip(point_of_interest_list,point_of_interest_image_list)
        place_type = 'point_of_interest'
        if(zipped_wk!=[]):
            save_places(zipped_wk,city_obj,place_type)
       
        shop_list = request.POST.get('shop_list')
        shop_list = str(shop_list).split(',')
        shop_range = request.POST.get('shop_range')
        shop_image_list = []
        for i in range(int(shop_range)):
            image = "shop_image" + str(i)
            try:
                shop_image_list.append(request.FILES[image])                 
            except: 
                shop_image_list.append('')

        zipped_wk = zip(shop_list,shop_image_list)
        place_type = 'where_to_shop'

        save_places(zipped_wk,city_obj,place_type)

        hospital_list = request.POST.get('hospital_list')
        hospital_list = str(hospital_list).split(',')

        hospital_range = request.POST.get('hospital_range')
        hospital_image_list = []
        for i in range(int(hospital_range)):
            image = "hospital_image" + str(i)
            try:
                hospital_image_list.append(request.FILES[image])                 
            except:
                hospital_image_list.append('')
        zipped_wk = zip(hospital_list,hospital_image_list)
        place_type = 'reputed_hospitals'

        save_places(zipped_wk,city_obj,place_type)

        college_list = request.POST.get('college_list')
        college_list = str(college_list).split(',')


        college_range = request.POST.get('college_range')
        college_image_list = []
        for i in range(int(college_range)):
            image = "college_image" + str(i)
            try:
                college_image_list.append(request.FILES[image])                 
            except:
                college_image_list.append('')
        zipped_wk = zip(college_list,college_image_list)
        place_type = 'college_and_universities'
        save_places(zipped_wk,city_obj,place_type)
        city_add(city_obj)
        
        data={
            'success':'true',
            'message':'City Added Successfully.'
        }

    except Exception, e:
        data={
            'success':'false',
            'message':str(e)
        }
    return HttpResponse(json.dumps(data),content_type='application/json')    


def update_places(zipped_wk,city_obj,place_type):
    try:

        for interest_id,interest_name,interest_img in zipped_wk:
            try:
                place_obj = Places.objects.get(place_id=interest_id)
                place_obj.place_name = interest_name
                if interest_img != '':
                    place_obj.place_image=interest_img
                else:
                    pass
                place_obj.updated_by="Admin",
                place_obj.updated_date=datetime.now()
                place_obj.save()        
            except:
                if interest_name != '' and interest_img != '' : 
                    interest_name_obj = Places(
                    city_place_id=city_obj,
                    place_name = interest_name,
                    place_image=interest_img,
                    place_type=place_type,
                    created_date=datetime.now(),
                    created_by="Admin",
                    updated_by="Admin",
                    updated_date=datetime.now()
                )
                    interest_name_obj.save()
            data = {'success': 'true'}
            print "RESPONSE",data

    except Exception, e:
        data={
            'success':'false',
            'message':str(e)
        }
    return HttpResponse(json.dumps(data),content_type='application/json') 


def save_places(zipped_wk,city_obj,place_type):
    
    try:
        for interest_name,interest_img in zipped_wk:

            if interest_name != '' and interest_img != '' :
            
                interest_name_obj = Places(
                city_place_id=city_obj,
                place_name = interest_name,
                place_image=interest_img,
                place_type=place_type,
                created_date=datetime.now(),
                created_by="Admin",
                updated_by="Admin",
                updated_date=datetime.now()
            )
                interest_name_obj.save()
            data = {'success': 'true'}

    except Exception, e:
        data={
            'success':'false',
            'message':str(e)
        }
    return 1 




def view_city(request):
    try:
        adv_list = []
        city_obj = City_Place.objects.all()
        for adv in city_obj:
            if adv.city_status == '1':
                status="Active"
                edit = '<a class="col-md-offset-1 col-md-1" style="text-align: center;" href="/edit-city/?city_place_id=' + str(adv.city_place_id) + '" class="edit" data-toggle="modal"><i class="fa fa-pencil"></i></a>'    
                delete = '<a class="col-md-1" id="'+str(adv.city_place_id)+'" onclick="delete_user_detail(this.id)" class="fa  fa-trash-o fa-lg"><i class="fa fa-trash"></a>'    
                action=edit + delete
            else:
                status="Inactive"
                edit = '--'
                delete = '--'
                active = '<a class="col-md-2" id="'+str(adv.city_place_id)+'" onclick="active_service(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;margin-left: 20px !important;" title="Activate" class="edit" data-toggle="modal" ><i class="fa fa-repeat"></i></a>'
                action=active
            temp_obj = {'city_name':adv.city_name,'population':adv.population,'state':adv.state_id.state_name,'status':status,'action':action}
            adv_list.append(temp_obj)
                
        data = {'data':adv_list}

    except Exception, e:
        print 'Exception : ', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')  



@csrf_exempt
def delete_city(request):
        try:
            adv_obj = City_Place.objects.get(city_place_id=request.POST.get('city_place_id'))
            adv_obj.city_status = '0'
            adv_obj.save()
            data = {'message': 'City Inactivated Successfully', 'success':'true'}
            city_delete(adv_obj)
        except IntegrityError as e:
          print e
        except Exception,e:
            print e
        print "Final Data: ",data
        return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def active_city(request):
        # pdb.set_trace()
        try:
            city_obj = City_Place.objects.get(city_place_id=request.POST.get('city_place_id'))
            city_obj.city_status = '1'
            city_obj.save()
            city_activate_mail(city_obj)
            data = {'message': 'City_Place activated Successfully', 'success':'true'}

        except IntegrityError as e:
          print e
        except Exception,e:
            print e
        print "Final Data: ",data
        return HttpResponse(json.dumps(data), content_type='application/json')


def city_activate_mail(city_obj):
    gmail_user =  "cityhoopla2016"
    gmail_pwd =  "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    #pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCity " + str(city_obj.city_name) + " " +"has been activated successfully.\nTo view complete details visit portal and follow - Reference Data -> City\n\n Thank You,"+'\n'+"CityHoopla Team"
        SUBJECT = "City Activated Successfully!"
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
 
      
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_city(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        try:
            city_obj = City_Place.objects.get(city_place_id=request.GET.get('city_place_id'))
            

                
            if city_obj.city_image:
                city_image = SERVER_URL + city_obj.city_image.url
                file_name = city_image[47:]
            else:
                city_image = ""
                file_name  = ""

            city_dict = {
                'success': 'true',
                'city_place_id':city_obj.city_place_id,
                'city_name':city_obj.city_name,
                'state':city_obj.state_id.state_id, 
                'climate': city_obj.climate or '',
                'about_city': city_obj.about_city or '',
                'language': city_obj.language or '',
                'population': city_obj.population or '',
                'timezone':city_obj.time_zone,
                'cityimage':city_image,
                'filename': file_name

            }
             
            intr_list = []      
            point_of_intrest = Places.objects.filter(city_place_id = city_obj,place_type = 'point_of_interest')
            poi_index = 0
            if point_of_intrest:
                    poi_index = len(point_of_intrest)-1
                    i = 0;
                    for place in point_of_intrest:
                        try:
                            place_image = SERVER_URL + place.place_image.url
                            file_name = place_image[47:]
                        except:
                            place_image = ''
                            file_name = ''
                        place_data = {
                            'image_id':i,
                            'place_id':place.place_id,
                            'place_name':place.place_name,
                            'place_image':place_image,
                            'filename':file_name
                        }
                        intr_list.append(place_data)
                        i = i+1 
                    
            shop_list = []      
            shop_name = Places.objects.filter(city_place_id = city_obj,place_type = 'where_to_shop')
            shop_index = 0
            if shop_name:
                    shop_index = len(shop_name)-1
                    i = 0;
                    for shop in shop_name:
                        place_image = SERVER_URL + shop.place_image.url
                        file_name = place_image[47:]
                        place_data = {
                             'place_id':shop.place_id,
                             'image_id':i,
                            'place_name':shop.place_name,
                            'place_image':place_image,
                            'filename':file_name
                        }
                        shop_list.append(place_data) 
                        i = i+1
            hosp_list = []      
            hospital = Places.objects.filter(city_place_id = city_obj,place_type = 'reputed_hospitals')
            hospital_index = 0
            if hospital:
                    hospital_index = len(hospital)-1
                    i = 0;
                    for hosp in hospital:
                        place_image = SERVER_URL + hosp.place_image.url
                        file_name = place_image[47:]
                        place_data = {
                             'place_id':hosp.place_id,
                             'image_id':i,
                            'place_name':hosp.place_name,
                            'place_image':place_image,
                            'filename':file_name
                        }
                        hosp_list.append(place_data) 
                        i = i+1
            clg_list = []      
            college = Places.objects.filter(city_place_id = city_obj,place_type = 'college_and_universities')
            college_index = 0
            if college:
                    college_index = len(hospital)-1
                    i = 0;
                    for clg in college:
                        place_image = SERVER_URL + clg.place_image.url
                        file_name = place_image[32:]
                        place_data = {
                            'image_id':i,
                            'place_id':clg.place_id,
                            'place_name':clg.place_name,
                            'place_image':place_image,
                            'filename':file_name
                        }
                        clg_list.append(place_data) 
                        i = i+1
            data = {'poi_index':poi_index,'shop_index':shop_index,'hospital_index':hospital_index,'college_index':college_index,'city':city_dict,'state_list':get_state(request),'interest':intr_list,'shops':shop_list,'hospitals':hosp_list,'colleges':clg_list,'username':request.session['login_user']}
        except Exception,e:
            print 'Exception:',e
            data = {'data':e}    
        print "Final Data",data
        return render(request,'Admin/edit_city.html',data)  

@csrf_exempt
def update_city(request):
    print 'in update city'
##    pdb.set_trace()
    try:
        if request.method == "POST":
            city_obj = City_Place.objects.get(city_place_id=request.POST.get('city_place_id'))
            city_obj.city_name=request.POST.get('city_name')
            city_obj.state_id =State.objects.get(state_id=request.POST.get('state')) 
            city_obj.save()
            
            if request.POST.get('about_city'):
                city_obj.about_city=request.POST.get('about_city')

            if request.POST.get('climate'):
                city_obj.climate=request.POST.get('climate')

            if request.POST.get('population'):
                city_obj.population = request.POST.get('population')

            if request.POST.get('timezone'):
                city_obj.time_zone=request.POST.get('timezone')

            if request.POST.get('language'):
                city_obj.language=request.POST.get('language')

            city_obj.save();

            if request.POST['check_image'] == "1":
                city_obj.city_image = request.FILES['city_image']
                city_obj.save()

            city_update(city_obj)
            data = {'success': 'true'}
        else:
            data = {'success': 'false'}
    except Exception,e:
        print 'Exception:',e
        data = {'data':'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_city_data(request):
    print 'in update city data'
##    pdb.set_trace()
    try:
        if request.method == "POST":
            
            city_obj = City_Place.objects.get(city_place_id=request.POST.get('city_place_id'))

            poi_range = request.POST.get('poi_range')
            point_of_interest_id_list = request.POST.get('point_of_interest_id_list')
            point_of_interest_id_list = str(point_of_interest_id_list).split(',')
            
            point_of_interest_list = request.POST.get('point_of_interest_list')
            point_of_interest_list = str(point_of_interest_list).split(',')

            point_of_interest_image_list = []
        
            for i in range(int(poi_range)):
                image = "point_of_interest_image" + str(i)
                try:
                    point_of_interest_image_list.append(request.FILES[image])                 
                except:
                    point_of_interest_image_list.append('')

            place_type = 'point_of_interest'

            zipped_wk = zip(point_of_interest_id_list,point_of_interest_list,point_of_interest_image_list)
            update_places(zipped_wk,city_obj,place_type)
                 
            shop_id_list = request.POST.get('shop_id_list')
            shop_id_list = str(shop_id_list).split(',')
            
            shop_list = request.POST.get('shop_list')
            shop_list = str(shop_list).split(',')

            shop_range = request.POST.get('shop_range')
            shop_image_list = []
            for i in range(int(shop_range)):
                image = "shop_image" + str(i)
                try:
                    shop_image_list.append(request.FILES[image])                 
                except: 
                    shop_image_list.append('')

            zipped_wk = zip(shop_id_list,shop_list,shop_image_list)
            place_type = 'where_to_shop'
            update_places(zipped_wk,city_obj,place_type)
            
            hospital_id_list = request.POST.get('hospital_id_list')
            hospital_id_list = str(hospital_id_list).split(',')
            
            hospital_list = request.POST.get('hospital_list')
            hospital_list = str(hospital_list).split(',')

            hospital_range = request.POST.get('hospital_range')
            hospital_image_list = []
            for i in range(int(hospital_range)):
                image = "hospital_image" + str(i)
                try:
                    hospital_image_list.append(request.FILES[image])                 
                except:
                    hospital_image_list.append('')

            zipped_wk = zip(hospital_id_list,hospital_list,hospital_image_list)
            place_type = 'reputed_hospitals'
            update_places(zipped_wk,city_obj,place_type)
            

            college_id_list = request.POST.get('college_id_list')
            college_id_list = str(college_id_list).split(',')

            college_list = request.POST.get('college_list')
            college_list = str(college_list).split(',')


            college_range = request.POST.get('college_range')
            college_image_list = []
            for i in range(int(college_range)):
                image = "college_image" + str(i)
                try:
                    college_image_list.append(request.FILES[image])                 
                except:
                    college_image_list.append('')

            zipped_wk = zip(college_id_list,college_list,college_image_list)
            place_type = 'college_and_universities'
            update_places(zipped_wk,city_obj,place_type)
            
            data = {'success': 'true'}
        else:
            data = {'success': 'false'}
    except Exception,e:
        data = {'data':'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')
 
def city_update(city_obj):
    gmail_user =  "cityhoopla2016"
    gmail_pwd =  "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    #pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCity " + str(city_obj.city_name) + " " +"has been updated successfully.\nTo view complete details visit portal and follow - Reference Data -> City\n\nThank You,"+'\n'+"CityHoopla Team"
        SUBJECT = "City Updated Successfully!"
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
 
def city_delete(adv_obj):
    gmail_user =  "cityhoopla2016"
    gmail_pwd =  "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    #pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCity " + str(adv_obj.city_name) + " " +"has been deactivated successfully.\nTo view complete details visit portal and follow - Reference Data -> City\n\nThank You,"+'\n'+"CityHoopla Team"
        SUBJECT = "City Deactivated Successfully!"
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

def city_add(city_obj):
    gmail_user =  "cityhoopla2016"
    gmail_pwd =  "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    #pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCity " + str(city_obj.city_name) + " " +"has been added successfully.\nTo view complete details visit portal and follow - Reference Data -> City\n\nThank You,"+'\n'+"CityHoopla Team"
        SUBJECT = "City Added Successfully!"
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
