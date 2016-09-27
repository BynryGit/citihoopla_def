
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
#importing exceptions
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
import urllib2

SERVER_URL = "http://52.40.205.128" 
#SERVER_URL = "http://127.0.0.1:8000" 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_subscriber(request):
	if not request.user.is_authenticated():
		return redirect('backoffice')
	else:	
	    state_list = State.objects.filter(state_status='1').order_by('state_name')
	    tax_list = Tax.objects.all()
	    category_list = Category.objects.filter(category_status='1').order_by('category_name')
	    
	    service_list = ServiceRateCard.objects.filter(service_rate_card_status='1').values('service_name').distinct()    
	    advert_service_list, item_ids = [], []
	    for item in AdvertRateCard.objects.filter(advert_rate_card_status='1'):
	        if item.advert_service_name not in item_ids:
	            advert_service_list.append(str(item.advert_rate_card_id))
	            item_ids.append(item.advert_service_name)

	    advert_service_list = AdvertRateCard.objects.filter(advert_rate_card_id__in=advert_service_list,advert_rate_card_status='1')        
	    
	    data = {'country_list':get_country(request),'username':request.session['login_user'],'advert_service_list':advert_service_list,'service_list':service_list,'tax_list':tax_list,'state_list':state_list,'category_list':category_list}
	    return render(request,'Admin/add_supplier.html',data)    


# TO GET THE Country
def get_country(request):
##    pdb.set_trace()
    country_list = []
    try:
        country = Country.objects.filter(country_status='1')
        for sta in country:
            country_list.append(
                {'country_id': sta.country_id, 'country_name': sta.country_name})

    except Exception, e:
        print 'Exception ', e
    return country_list   

@csrf_exempt
def save_supplier(request):
	try:
            # pdb.set_trace()
	    supplier_obj = Supplier(
	    	business_name = request.POST.get('business_name'),
	    	phone_no = request.POST.get('phone_no'),
	    	secondary_phone_no = request.POST.get('sec_phone_no'),
	    	supplier_email = request.POST.get('email'),	
	    	secondary_email = request.POST.get('sec_email'),
	    	address1 = request.POST.get('address1'),
	    	address2 = request.POST.get('address2'),
	    	city_place_id = City_Place.objects.get(city_place_id=request.POST.get('city')),
	    	country_id=Country.objects.get(country_id=request.POST.get('country')),
	    	state = State.objects.get(state_id=request.POST.get('state')),
	    	pincode = Pincode.objects.get(pincode=request.POST.get('pincode')),
	    	business_details = request.POST.get('business'),
	    	contact_person = request.POST.get('user_name'),
	    	contact_email = request.POST.get('user_email'),
	    	contact_no = request.POST.get('user_contact_no'),
	    	username = request.POST.get('user_email'),
            sales_person_name = request.POST.get('sale_person_name'),
            sales_person_email = request.POST.get('sale_person_email'),
            sales_person_contact_number = request.POST.get('sale_person_contact_no'),
	    	supplier_status='1'
	    	)
	    supplier_obj.save()
	    email=str(supplier_obj.contact_email)
	    try:
	    	supplier_add_mail(supplier_obj)
	    except:
	    	pass

	    try:
	    	supplier_obj.logo = request.FILES['logo']
	    	supplier_obj.save()
	    except:
	    	pass
	    data={
			'success':'true',
			'message':"Supplier added successfully",
			'email':email
		}
	except Exception, e:
		data={
			'success':'false',
			'message':str(e)
		}
	return HttpResponse(json.dumps(data),content_type='application/json')   


@csrf_exempt
def save_service(request):
    try:
    	# pdb.set_trace()
        supplier_id = request.POST.get('supplier_id')
        print "supplier_id",supplier_id
        category_id = request.POST.get('sub_category')

        duration = request.POST.get('duration_list')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        premium_service_list = request.POST.getlist('premium_service')
        premium_service_duration_list = request.POST.getlist('premium_ser_duration')
        premium_start_date_list = request.POST.getlist('premium_start_date')
        premium_end_date_list = request.POST.getlist('premium_end_date')
        premium_end_date_list = filter(None, premium_end_date_list)
        #print supplier_id,category_id,duration,start_date,end_date

        zip_premium = zip(premium_service_list,premium_service_duration_list,premium_start_date_list,premium_end_date_list)

        if premium_service_list:
            check_premium_service = check_date(zip_premium,category_id)
            if check_premium_service['success'] == 'false':
                data = {'success': 'false', 'message': check_premium_service['msg']}
                return HttpResponse(json.dumps(data), content_type='application/json')


        chars = string.digits
        pwdSize = 8
        password = ''.join(random.choice(chars) for _ in range(pwdSize))

        supplier_obj = Supplier.objects.get(username = supplier_id)
        category_obj = Category.objects.get(category_id = category_id)
        category_id=str(category_obj.category_id)
        print "category_id",category_id
        service_ratecard_obj = ServiceRateCard.objects.get(duration = duration, service_name = 'Basic Subscription Plan')

        business_obj = Business(
            category = Category.objects.get(category_id =category_id),
            service_rate_card_id=service_ratecard_obj,
            duration=duration,
            start_date=start_date,
            end_date=end_date,
            supplier=supplier_obj,
            transaction_code="TID" + str(password),
            is_active=0,
            business_created_date = datetime.now()
            # business_created_by = supplier_obj.contact_email
        )
        business_obj.save()
        print "business_obj",business_obj

        transaction_code = "TID" + str(password)
        if premium_service_list:
            for premium_service, premium_service_duration, premium_start_date, premium_end_date  in zip_premium:
                premium_service_obj = PremiumService(
                    premium_service_name = premium_service,
                    no_of_days = premium_service_duration,
                    category_id = Category.objects.get(category_id = category_id),
                    start_date=premium_start_date,
                    end_date=premium_end_date,
                    business_id = business_obj,
                    premium_service_status = "1",
                    premium_service_created_date = datetime.now()
                    # premium_service_created_by = supplier_obj.contact_email
                )
                premium_service_obj.save()
        data = {'success': 'true', 'message': 'The subscription is created successfully with transaction ID :'+transaction_code+'. Please proceed with the payment .',
                'business_id':str(business_obj,)
                }
    except Exception as e:
        print e
        data = {'success': 'false', 'message': e}
    return HttpResponse(json.dumps(data), content_type='application/json')

def check_date(zip_premium,category_id):
    flag_1, flag_2, flag_3, flag_4, flag_5 = 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'
    service_list = ''
    for premium_service, premium_service_duration, premium_start_date, premium_end_date  in zip_premium:
        if premium_service == 'No.1 Listing':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                Q(category_id=str(category_id)) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).count()

            if premium_service_obj >= 1:
                flag_1 = 'No'
        if premium_service == 'No.2 Listing':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                Q(category_id=str(category_id)) &
                #Q(start_date__range=(premium_start_date, premium_end_date)) |
                #Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).count()

            print premium_service_obj

            if premium_service_obj >= 1:
                flag_2 = 'No'
        if premium_service == 'No.3 Listing':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                Q(category_id=str(category_id)) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).count()
            if premium_service_obj >= 1:
                flag_3 = 'No'
        if premium_service == 'Advert Slider':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).count()
            if premium_service_obj > 10:
                flag_4 = 'No'
        if premium_service == 'Top Advert':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).count()
            if premium_service_obj >= 1:
                flag_5 = 'No'
    if flag_1 == 'No':
        service_list = 'No.1 Listing,'
    if flag_2 == 'No':
        service_list = service_list + 'No.2 Listing,'
    if flag_3 == 'No':
        service_list = service_list + 'No.3 Listing,'
    if flag_4 == 'No':
        service_list = service_list + 'Advert Slider,'
    if flag_5 == 'No':
        service_list = service_list + 'Top Advert'
    if service_list != '':
        msg = service_list + ' already exist for selected date range'
        data = {'success': 'false','msg':msg}
    else:
        data = {'success': 'true', 'msg': ''}
    return data


def add_subscription_sms(business_obj):
    
    authkey = "118994AIG5vJOpg157989f23"
    # user_obj = Supplier.objects.get(supplier_id=su_id)
 #    contact_no = user_obj.contact_no
 #    print '---------contact_no------',contact_no

    mobiles = "+919403884595"
    message = "New/Renew subscription activity performed on \t"+ str(business_obj.business_id) +"\t"+ str(business_obj.supplier.business_name)+"\t with \t"+str(business_obj.transaction_code)
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
    print output

@csrf_exempt
def edit_service(request):
	try:
		serv_obj = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration'))
		try:
			supplier_obj = Supplier.objects.get(username = request.POST.get('user_email'))
			try:
				business_obj = Business.objects.get(supplier_id=str(supplier_obj))
			except:
				business_obj = ''
			premium_service_list = request.POST.get('premium_service')
			no_of_days_list = request.POST.get('premium_day_list')
			if(premium_service_list):
				final_data = check_subscription(premium_service_list,no_of_days_list)
				if final_data['success']=='true':
					category_obj = Category.objects.get(category_name=request.POST.get('category'))

					date_validation = check_date(premium_service_list,request.POST.get('premium_start_date'),request.POST.get('premium_end_date'),category_obj,business_obj)
					if date_validation['success']=='true':	
						try:		
							business_obj = Business.objects.get(supplier=supplier_obj)
							business_obj.category = Category.objects.get(category_name=request.POST.get('category')) 
							business_obj.service_rate_card_id = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration'))
							business_obj.duration = request.POST.get('selected_duration')
							business_obj.start_date = request.POST.get('duration_start_date')
							business_obj.end_date = request.POST.get('duration_end_date')
							business_obj.save()
						except:
							chars= string.digits
							pwdSize = 8
							password = ''.join(random.choice(chars) for _ in range(pwdSize))
							business_obj = Business(
							category = Category.objects.get(category_name=request.POST.get('category')),
							service_rate_card_id = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration')),
							duration = request.POST.get('selected_duration'),
							start_date = request.POST.get('duration_start_date'),
							end_date = request.POST.get('duration_end_date'),
							supplier= supplier_obj,
							transaction_code = "TID" + str(password),
							is_active = 0
							)
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
						save_working_hours(zipped_wk,business_obj)
						data={
							'success':'true',
							'message':"Supplier profile edited successfully",
							'transaction_code' : str(business_obj.transaction_code),
							'subscriber_id': str(supplier_obj.supplier_id)
						}
						try:
							supplier_edit_service_mail(business_obj)
						except:
							pass	
					else:
					 	data={
					 		'success':'false',
					 		'message':date_validation['message']
					 	}	
				else:
				 	data={
				 		'success':'false',
				 		'message':final_data['message']
				 	}	
			else:
				premium_service_obj = PremiumService.objects.filter(business_id=business_obj).delete()
				try:		
					business_obj = Business.objects.get(supplier=supplier_obj)
					business_obj.category = Category.objects.get(category_name=request.POST.get('category')) 
					business_obj.service_rate_card_id = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration'))
					business_obj.duration = request.POST.get('selected_duration')
					business_obj.start_date = request.POST.get('duration_start_date')
					business_obj.end_date = request.POST.get('duration_end_date')
					business_obj.save()
				except:
					chars= string.digits
					pwdSize = 8
					password = ''.join(random.choice(chars) for _ in range(pwdSize))
					business_obj = Business(
					category = Category.objects.get(category_name=request.POST.get('category')),
					service_rate_card_id = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('selected_duration')),
					duration = request.POST.get('selected_duration'),
					start_date = request.POST.get('duration_start_date'),
					end_date = request.POST.get('duration_end_date'),
					supplier= supplier_obj,
					transaction_code = "TID" + str(password),
					is_active = 0
					)
					business_obj.save()	
				data={
						'success':'true',
						'message':"Supplier profile edited successfully",
						'transaction_code' : str(business_obj.transaction_code),
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
	return HttpResponse(json.dumps(data),content_type='application/json')




def save_working_hours(zipped_wk,business_obj):
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
def register_supplier(request):
	try:
		# pdb.set_trace()
		print "Taxtype",request.POST.get('selected_tax_type')
		business_id = request.POST.get('business_id')
		chars= string.digits
		pwdSize = 8
		password = ''.join(random.choice(chars) for _ in range(pwdSize))
		business_obj =  Business.objects.get(business_id = business_id)	

		payment_obj = PaymentDetail(
			business_id = business_obj,
			note = request.POST.get('note'),
			payment_mode = request.POST.get('payment_mode'),
			bank_name=request.POST.get('bank_name'),
			branch_name=request.POST.get('bank_branch_name'),
			cheque_number=request.POST.get('cheque_number'),
			paid_amount = request.POST.get('paid_amount'),
			payable_amount = request.POST.get('payable_amount'),
			total_amount = request.POST.get('generated_amount'),
			tax_type = Tax.objects.get(tax_type=request.POST.get('selected_tax_type')),
			payment_code = "PMID" + str(password)
			)
		payment_obj.save()
		payment_code=payment_obj.payment_code
		data={
		'success':'true',
		'message':"Supplier added successfully",'business_id':business_id,
		'message': 'Payment done successfully with Payment ID - '+payment_code
			}
		supplier_add_payment_mail(payment_obj)
		payment_sms(payment_obj)

	except Exception, e:
		data={
				'success':'false',
				'message':str(e)
		}
	return HttpResponse(json.dumps(data),content_type='application/json')


def payment_sms(payment_obj):
	# pdb.set_trace()
    business_obj=Business.objects.get(business_id=str(payment_obj.business_id.business_id))

    authkey = "118994AIG5vJOpg157989f23"

    mobiles = "+919403884595"
    message = "Payment made by \t"+ str(business_obj.business_id) +"\t"+ str(business_obj.supplier.business_name)+"\t via \t"+ str(payment_obj.payment_mode) + "\t mode with \t" + str(payment_obj.payment_id) + "\t for the amount \t" +str(payment_obj.payable_amount)
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
    print output


@csrf_exempt
def get_amount(request):
	try:
		premium_service_list = request.POST.get('premium_service_list')
		premium_service_list = str(premium_service_list).split(',')

		premium_day = request.POST.get('premium_day')
		premium_day = str(premium_day).split(',')

		zipped_wk = zip(premium_service_list,premium_day)
		rate_card_obj = ServiceRateCard.objects.get(service_name=request.POST.get('service'),duration=request.POST.get('duration'))
		final_cost = int(rate_card_obj.cost)
		if zipped_wk!=[('', '')]:

			for serv,day in zipped_wk:
				service_rate_card_obj = AdvertRateCard.objects.get(advert_service_name=serv,duration=day)
				final_cost = int(final_cost)+int(service_rate_card_obj.cost)

		data={
				'success':'true',
				'cost': str(final_cost)
		}
	except Exception, e:
		data={
			'success':'false',
			'message':str(e)
		}
	return HttpResponse(json.dumps(data),content_type='application/json')    


@csrf_exempt
def get_basic_subscription_amount(request):
    print "--------------------------------"
    duration = request.POST.get('duration')
    service_obj = ServiceRateCard.objects.get(duration = duration)
    data = {'success': 'true', 'amount': str(service_obj.cost)}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def get_premium_subscription_amount(request):
    # pdb.set_trace()
    print "--------------------------------",request.POST
    duration = request.POST.get('duration')
    service_name = request.POST.get('service_name')
    rate_card_obj = AdvertRateCard.objects.get(advert_service_name=service_name,duration = duration)
    data = {'success': 'true', 'amount': str(rate_card_obj.cost)}
    return HttpResponse(json.dumps(data), content_type='application/json')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_subscriber_list(request):
	try:
		data = {}
		final_list = []
		pre_date = datetime.now().strftime("%m/%d/%Y")
		pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
		date_gap = ''
		advert_count = ''
		try:
			user_list = Supplier.objects.all()
			for user_obj in user_list:
				user_id = str(user_obj.supplier_id)
				business_name = user_obj.business_name
				user_name = user_obj.contact_person
				user_email_id = user_obj.contact_email
				user_contact_no = user_obj.contact_no
				user_city = user_obj.city_place_id.city_id.city_name
				subscription = '---'
				category = '---'
                
				if user_obj.logo:
					logo = SERVER_URL + user_obj.logo.url
				else:
					logo = SERVER_URL + '/static/assets/layouts/layout2/img/City_Hoopla_Logo.png'

				# subscription_start_date = '---'
				subscription_end_date = '---'

				advert_count = Advert.objects.filter(supplier_id=user_obj,status="1").count()

				subscription_obj = Business.objects.filter(supplier=user_obj)
				# for business in subscription_obj:
				#  	start_date=business.start_date
				#  	subscription_start_date = datetime.strptime(start_date, "%m/%d/%Y")
				#  	subscription_start_date=subscription_start_date.strftime("%d %b %y")
				#  	end_date1 = business.end_date
    #       			end_date2 = datetime.strptime(end_date1, "%m/%d/%Y")
    #       			date_gap = (end_date2 - pre_date).days

				print '=========len==========',len(subscription_obj)
				if len(subscription_obj)<=1:
					edit = '<a  id="'+str(user_id)+'" title="Edit" class="edit" style="padding: 8px;" data-toggle="modal;" href="/edit-subscriber/?user_id='+str(user_id)+'"><i class="fa fa-pencil"></i></a>'
				else:
					edit = '<a  id="'+str(user_id)+'" title="Edit" class="edit" style="padding: 8px;" data-toggle="modal;" href="/edit-subscriber-detail/?user_id='+str(user_id)+'"><i class="fa fa-pencil"></i></a>'

				

				# if user_obj.supplier_status == '1':
				# 	status= 'Active'
				# 	advert = '<a  id="'+str(user_id)+'"  style="text-align: center; padding: 8px;" title="Advert" class="edit" data-toggle="modal" onclick="check_advert(this.id)" ><i class="fa fa-shopping-cart"></i></a>'
				# 	#edit = '<a  id="'+str(user_id)+'" title="Edit" class="edit" style="padding: 8px;" data-toggle="modal;" href="/edit-subscriber/?user_id='+str(user_id)+'"><i class="fa fa-pencil"></i></a>'
				# 	delete = '<a  id="'+str(user_id)+'" onclick="delete_user_detail(this.id)" style="padding: 8px;"  title="Delete"  ><i class="fa fa-trash"></i></a>'
				# 	actions =  advert + edit + delete
				# else:
				# 	status = 'Inactive'
				# 	active = '<a  id="'+str(user_id)+'" onclick="active_subscriber(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;" title="Activate" class="edit" data-toggle="modal" ><i class="fa fa-repeat"></i></a>'
				# 	actions =  active
			
				list = {'subscriber_category':category,
						'subscription_end_date':'',
						'subscription_start_date':'',
						'subscriber_subscription':subscription,
						'subscriber_city':user_city,
						'subscriber_id':user_id,
						'business_name':business_name,
						'subscriber_name':user_name,
						'user_email_id':user_email_id,
						'user_contact_no':user_contact_no,
						'logo':logo,
						'advert_count':advert_count,
						'status':user_obj.supplier_status
                        }
				final_list.append(list)
			data = {'username':request.session['login_user'],'success':'true','subscriber_list':final_list}
		except IntegrityError as e:
			data = {'success':'false','message':'Error in  loading page. Please try after some time'}
	except MySQLdb.OperationalError, e:
		print e
	except Exception,e:
		print 'Exception ',e
	return render(request,'Admin/supplier_list.html',data)


@csrf_exempt
def delete_subscriber(request):
        try:
            user_obj = Supplier.objects.get(supplier_id=request.POST.get('user_id'))
            user_obj.supplier_status = '0'
            user_obj.save()
            supplier_inactive_mail(user_obj)
            supplier_inactive_sms(user_obj)
            data = {'message': 'User Inactivated Successfully', 'success':'true'}

        except IntegrityError as e:
          print e
        except Exception,e:
            print e
        print "Final Data: ",data
        return HttpResponse(json.dumps(data), content_type='application/json')


def supplier_inactive_sms(user_obj):
	
    authkey = "118994AIG5vJOpg157989f23"

    contact_no = user_obj.contact_no
    print '---------contact_no------',contact_no

    mobiles = "+919403884595"
    message = "Your profile with CityHoopla has been de-activated, To re-activate, please contact 9028527219 or write us to at info@city-hoopla.com"
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
    print output


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_subscriber(request):
    if not request.user.is_authenticated():      
        return redirect('backoffice')
    else:
        # pdb.set_trace()
         
        business_obj=Business.objects.filter(supplier=request.GET.get('subscriber_id'))
        print 'business_obj',business_obj

        state_list = State.objects.filter(state_status='1').order_by('state_name')
        subscriber_obj = Supplier.objects.get(supplier_id=request.GET.get('subscriber_id'))
        business_name = subscriber_obj.business_name
        phone_no = subscriber_obj.phone_no
        secondary_phone_no = subscriber_obj.secondary_phone_no
        supplier_email = subscriber_obj.supplier_email
        secondary_email = subscriber_obj.secondary_email
        try:
            display_image = SERVER_URL + subscriber_obj.logo.url
            file_name = str(subscriber_obj.logo)[19:]
        except:
            display_image = ''
            file_name = ''

        address1 = subscriber_obj.address1
        address2 = subscriber_obj.address2
        country_list = Country.objects.filter(country_status='1').order_by('country_name')
        country=subscriber_obj.country_id.country_id
        state = subscriber_obj.state.state_id
        city_list = City_Place.objects.filter(state_id=state,city_status='1')
        city = subscriber_obj.city_place_id
        city_name=subscriber_obj.city_place_id.city_id.city_name
        city_id=subscriber_obj.city_place_id.city_id.city_id
        pincode_list = Pincode.objects.filter(city_id=city_id,pincode_status='1')
        pincode = subscriber_obj.pincode
        business_details = subscriber_obj.business_details
        supplier_id=subscriber_obj.supplier_id
        contact_person = subscriber_obj.contact_person
        contact_no = subscriber_obj.contact_no
        contact_email = subscriber_obj.contact_email
        sales_person_name=subscriber_obj.sales_person_name
        sales_person_contact_number=subscriber_obj.sales_person_contact_number
        sales_person_email=subscriber_obj.sales_person_email

        state_list = State.objects.filter(state_status='1').order_by('state_name')
        tax_list = Tax.objects.all()
        category_list = Category.objects.filter(category_status='1').order_by('category_name')
        
        service_list = ServiceRateCard.objects.filter(service_rate_card_status='1').values('service_name').distinct()    
        advert_service_list, item_ids = [], []
        for item in AdvertRateCard.objects.filter(advert_rate_card_status='1'):
            if item.advert_service_name not in item_ids:
                advert_service_list.append(str(item.advert_rate_card_id))
                item_ids.append(item.advert_service_name)

        advert_service_list = AdvertRateCard.objects.filter(advert_rate_card_id__in=advert_service_list,advert_rate_card_status='1')   

        data = {'username':request.session['login_user'],'country_list':country_list,'country':country,'state_list':state_list,'supplier_email':supplier_email,'contact_no':contact_no,'contact_person':contact_person,'secondary_email':secondary_email,
        'city_list':city_list,'state':state,'city':city,'pincode_list':pincode_list,'business_name':business_name,'business_details':business_details,'address2':address2,'address1':address1,
        'file_name':file_name,'display_image':display_image,'phone_no':phone_no,'secondary_phone_no':secondary_phone_no,'contact_email':contact_email,'user_pincode':pincode,'supplier_id':supplier_id,
        'sales_person_name':sales_person_name,'sales_person_contact_number':sales_person_contact_number,'sales_person_email':sales_person_email
            }
        if business_obj:
            return render(request, 'Admin/edit_supplier.html', data)
        else:
            data = {'username':request.session['login_user'],'country_list':country_list,'country':country,'state_list':state_list,'supplier_email':supplier_email,'contact_no':contact_no,'contact_person':contact_person,'secondary_email':secondary_email,
            'city_list':city_list,'state':state,'city':city,'pincode_list':pincode_list,'business_name':business_name,'business_details':business_details,'address2':address2,'address1':address1,
            'file_name':file_name,'display_image':display_image,'phone_no':phone_no,'secondary_phone_no':secondary_phone_no,'contact_email':contact_email,'user_pincode':pincode,'supplier_id':supplier_id,
            'sales_person_name':sales_person_name,'sales_person_contact_number':sales_person_contact_number,'sales_person_email':sales_person_email,
            'country_list':get_country(request),'username':request.session['login_user'],'advert_service_list':advert_service_list,'service_list':service_list,'tax_list':tax_list,'state_list':state_list,'category_list':category_list
            }
            return render(request, 'Admin/edit_supplier_detail.html', data)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_subscriber_detail(request):
	if not request.user.is_authenticated():
		return redirect('backoffice')
	else:	
		status=""
		state_list = State.objects.filter(state_status='1').order_by('state_name')
		country_list = Country.objects.filter(country_status='1').order_by('country_name')
		category_list = Category.objects.filter(category_status='1').order_by('category_name')
		tax_list = Tax.objects.all()
		subscriber_obj = Supplier.objects.get(supplier_id=request.GET.get('user_id'))
		business_name = subscriber_obj.business_name
		phone_no = subscriber_obj.phone_no
		supplier_id=subscriber_obj.supplier_id
		secondary_phone_no = subscriber_obj.secondary_phone_no
		supplier_email = subscriber_obj.supplier_email
		secondary_email = subscriber_obj.secondary_email
		try:
	 		display_image = SERVER_URL + subscriber_obj.logo.url
	 		file_name = str(subscriber_obj.logo)[19:]
	 	except:
	 		display_image = ''
	 		file_name = ''

		address1 = subscriber_obj.address1
		address2 = subscriber_obj.address2
		country=subscriber_obj.country_id.country_id
		state = subscriber_obj.state
		city_list = City_Place.objects.filter(state_id=state,city_status='1') 
		city = subscriber_obj.city_place_id
		city_id=subscriber_obj.city_place_id.city_id.city_id
		print "CITY",city
		pincode_list = Pincode.objects.filter(city_id=city_id,pincode_status='1')
		pincode = subscriber_obj.pincode
		business_details = subscriber_obj.business_details
		contact_person = subscriber_obj.contact_person
		contact_no = subscriber_obj.contact_no
		contact_email = subscriber_obj.contact_email

		subscription_list = Business.objects.filter(supplier_id=str(subscriber_obj))
		final_subscription_details = []
		print subscription_list
		for subscription in subscription_list:
			rate_card_obj = ServiceRateCard.objects.get(service_rate_card_id=str(subscription.service_rate_card_id),duration=subscription.duration)
			final_cost = int(rate_card_obj.cost)
			final_service_list = []
			premium_service_list = PremiumService.objects.filter(business_id=str(subscription))
			if premium_service_list:
				
				for premium_service in premium_service_list:
					
					service_rate_card_obj = AdvertRateCard.objects.get(advert_service_name=premium_service.premium_service_name,duration=premium_service.no_of_days)
					final_cost = int(final_cost)+int(service_rate_card_obj.cost)
					
					service_name = premium_service.premium_service_name
					start_date = premium_service.start_date
					end_date = premium_service.end_date
					service_list = {'service_name':service_name,'start_date':start_date,'end_date':end_date}
					final_service_list.append(service_list)
			else:
				service_list = {'service_name':'---','start_date':'---','end_date':'---'}
				final_service_list.append(service_list)

			print "=================================",str(subscription)
			check_status=datetime.now()
			check_status=check_status.strftime('%m/%d/%Y')
			try:
				advert_obj = AdvertSubscriptionMap.objects.get(business_id=str(subscription))
				business_obj= Business.objects.get(business_id=str(advert_obj.business_id))
				end_date1=business_obj.end_date
				if check_status < end_date1:
					status = "Active"
				else:
					status = "Inactive"
				advert_id = str(advert_obj.advert_id)
				advert_name = advert_obj.advert_id.advert_name
			except Exception as e:
				advert_id = ''
				advert_name = 'N/A'
				status = 'N/A'
			
			subscription_details = {'status':status,'final_cost':final_cost,'final_service_list':final_service_list,'advert_id':advert_id,'advert_name':advert_name}
			final_subscription_details.append(subscription_details)
		data = {'country':country,'state_list':state_list,'country_list':country_list,'supplier_id':supplier_id,'final_subscription_details':final_subscription_details,'username':request.session['login_user'],'user_pincode':pincode,'file_name':file_name,'display_image':display_image,'pincode_list':pincode_list,'city_list':city_list,'state':state,'city':city,'state_list':state_list,'contact_email':contact_email,'contact_no':contact_no,'contact_person':contact_person,'business_details':business_details,'address2':address2,'address1':address1,'secondary_email':secondary_email,'supplier_email':supplier_email,'business_name':business_name,'phone_no':phone_no,'secondary_phone_no':secondary_phone_no}
		return render(request,'Admin/edit-subscriber-detail.html',data)   

@csrf_exempt
def update_subscriber(request):
    try:
        # pdb.set_trace()
        print "USER",request.POST.get('user_email')
        if request.POST.get('user_email'):
            try:
                supplier_obj= Supplier.objects.get(supplier_id=request.POST.get('supplier_id'))
                supplier_obj.username=request.POST.get('user_email')
                supplier_obj.save()
            except IntegrityError, e:
                print "Exception",e
                data={ 'success':'false','message':'User already exist.' }
                return HttpResponse(json.dumps(data),content_type='application/json') 
        print "=======Country",request.POST.get('country')
        supplier_obj = Supplier.objects.get(supplier_id=request.POST.get('supplier_id'))
        supplier_obj.business_name = request.POST.get('business_name')
        supplier_obj.phone_no = request.POST.get('phone_no')
        supplier_obj.secondary_phone_no = request.POST.get('sec_phone_no')
        supplier_obj.country_id=Country.objects.get(country_id=request.POST.get('country'))
        supplier_obj.supplier_email = request.POST.get('email')
        supplier_obj.secondary_email = request.POST.get('sec_email')
        supplier_obj.address1 = request.POST.get('address1')
        supplier_obj.address2 = request.POST.get('address2')
        supplier_obj.city_place_id = City_Place.objects.get(city_place_id=request.POST.get('city'))
        supplier_obj.state = State.objects.get(state_id=request.POST.get('state'))
        supplier_obj.pincode = Pincode.objects.get(pincode=request.POST.get('pincode'))
        supplier_obj.business_details = request.POST.get('business')
        supplier_obj.contact_person = request.POST.get('user_name')
        supplier_obj.contact_no=request.POST.get('user_contact_no')
        supplier_obj.contact_no = request.POST.get('user_contact_no')
        supplier_obj.sales_person_name = request.POST.get('sale_person_name')
        supplier_obj.sales_person_email = request.POST.get('sale_person_email')
        supplier_obj.sales_person_contact_number = request.POST.get('sale_person_contact_no')

        supplier_obj.save()
        if request.POST.get('user_email'):
            supplier_obj.contact_email = request.POST.get('user_email')
            supplier_obj.save()
        try:
            supplier_obj.logo = request.FILES['logo']
        except:
            pass
        supplier_obj.save()
        try:
            supplier_edit_mail(supplier_obj)
        except:
            pass
        data={
            'success':'true',
            'message':"Subscriber edited successfully"
        }
    except Exception, e:
        print e
        data={
            'success':'false',
            'message':str(e)
        }
    return HttpResponse(json.dumps(data),content_type='application/json') 


# TO GET THE CATEGOTRY
def get_category(request):
##    pdb.set_trace()
    cat_list = []
    try:
        category = Category.objects.filter(category_status='1').order_by('category_name')
        for cat in category:
            cat_list.append(
                {'category_id': cat.category_id, 'category': cat.category_name})

    except Exception, e:
        print 'Exception ', e
    return cat_list

    # TO GET THE STATE
def get_states(request):
##    pdb.set_trace()
    state_list = []
    try:
        state = State.objects.filter(state_status='1')
        for sta in state:
            options_data = {
            'state_id':str(sta.state_id),
            'state_name':str(sta.state_name)

            }
            state_list.append(options_data)
        return  state_list
    except Exception, e:
        print 'Exception ', e
        data = {'state_list':'No states available' }
    return HttpResponse(json.dumps(data), content_type='application/json')


def renew_subscription(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        advert_id = request.GET.get('advert_id')
        tax_list = Tax.objects.all()
        advert_obj = Advert.objects.get(advert_id = advert_id)
        supplier_id=advert_obj.supplier_id
        advert_name = advert_obj.advert_name
        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
        business_obj = Business.objects.get(business_id=str(advert_sub_obj.business_id))

        business_data = {
            'business_id': str(business_obj.business_id),
            'category_id': str(business_obj.category.category_id),
        }


        service_list = ServiceRateCard.objects.filter(service_rate_card_status='1').values('service_name').distinct()
        advert_service_list, item_ids = [], []
        for item in AdvertRateCard.objects.filter(advert_rate_card_status='1'):
            if item.advert_service_name not in item_ids:
                advert_service_list.append(str(item.advert_rate_card_id))
                item_ids.append(item.advert_service_name)

        advert_services_list = []
        advert_service_list = AdvertRateCard.objects.filter(advert_rate_card_id__in=advert_service_list)

        try:
            payment_obj = PaymentDetail.objects.get(business_id=str(business_obj.business_id))
            payment_details = {
                'payment_mode': payment_obj.payment_mode,
                'paid_amount': round(float(payment_obj.paid_amount), 2),
                'payable_amount': round(float(payment_obj.payable_amount), 2),
                'total_amount': round(float(payment_obj.total_amount), 2),
                'tax_type': payment_obj.tax_type.tax_rate,
                'note': payment_obj.note,
                'bank_name': payment_obj.bank_name,
                'branch_name': payment_obj.branch_name,
                'cheque_number': payment_obj.cheque_number
            }
            # print payment_details
        except Exception:
            payment_details = {
                'payment_mode': '',
                'paid_amount': '',
                'payable_amount': '',
                'total_amount': '',
                'tax_type': '',
                'note': '',
                'bank_name': '',
                'branch_name': '',
                'cheque_number': ''
            }
            pass

        data = {'tax_list': tax_list, 'advert_service_list': advert_service_list, 'service_list': service_list,
                'username': request.session['login_user'], 'category_list': get_category(request),
                'country_list': get_country(request), 'supplier_id':supplier_id,
                'state_list': get_states(request), 'business_data': business_data, 'advert_name' : advert_name
                }
        return render(request,'Admin/renew_subscription.html',data)


def edit_subscription(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        business_id = request.GET.get('business_id')
        tax_list = Tax.objects.all()

        business_obj = Business.objects.get(business_id=business_id)
        supplier_id=business_obj.supplier_id

        business_data = {
            'business_id': str(business_obj.business_id),
            'category_id': str(business_obj.category.category_id),
            'service_rate_card_duration': int(business_obj.service_rate_card_id.duration),
            'start_date': str(business_obj.start_date),
            'end_date': str(business_obj.end_date)
        }

        basic_amount = int(business_obj.service_rate_card_id.cost)
        amount_1 = 0
        amount_2 = 0
        amount_3 = 0
        amount_4 = 0
        amount_5 = 0

        premium_service_list = []

        premium_service_obj = PremiumService.objects.filter(business_id=str(business_obj.business_id))
        for premium_service in premium_service_obj:
            advert_rate_obj = AdvertRateCard.objects.get(advert_service_name=premium_service.premium_service_name,
                                                         duration=premium_service.no_of_days
                                                         )
            if premium_service.premium_service_name == 'No.1 Listing':
                amount_1 = int(advert_rate_obj.cost)
            if premium_service.premium_service_name == 'No.2 Listing':
                amount_2 = int(advert_rate_obj.cost)
            if premium_service.premium_service_name == 'No.3 Listing':
                amount_3 = int(advert_rate_obj.cost)
            if premium_service.premium_service_name == 'Advert Slider':
                amount_4 = int(advert_rate_obj.cost)
            if premium_service.premium_service_name == 'Top Advert':
                amount_5 = int(advert_rate_obj.cost)

            premium_service_data = {
                'premium_service_name': premium_service.premium_service_name,
                'premium_service_duration': premium_service.no_of_days,
                'premium_service_start_date': premium_service.start_date,
                'premium_service_end_date': premium_service.end_date
            }
            premium_service_list.append(premium_service_data)

        total_amount = basic_amount + amount_1 + amount_2 + amount_3 + amount_4 + amount_5
        service_list = ServiceRateCard.objects.filter(service_rate_card_status='1').values('service_name').distinct()
        advert_service_list, item_ids = [], []
        for item in AdvertRateCard.objects.filter(advert_rate_card_status='1'):
            if item.advert_service_name not in item_ids:
                advert_service_list.append(str(item.advert_rate_card_id))
                item_ids.append(item.advert_service_name)

        advert_services_list = []
        advert_service_list = AdvertRateCard.objects.filter(advert_rate_card_id__in=advert_service_list)
        print advert_service_list
        for advert_service in advert_service_list:
            try:
                premium_obj = PremiumService.objects.get(premium_service_name=advert_service.advert_service_name,
                                                         business_id=str(business_obj.business_id),
                                                         category_id=str(business_obj.category.category_id)
                                                         )
                advert_service_data = {
                    'service_name': advert_service.advert_service_name,
                    'advert_rate_card_id': advert_service.advert_rate_card_id,
                    'checked': 'true',
                    'service_duration': int(premium_obj.no_of_days),
                    'service_start_date': premium_obj.start_date,
                    'service_end_date': premium_obj.end_date
                }
                advert_services_list.append(advert_service_data)
            except Exception as e:
                advert_service_data = {
                    'service_name': advert_service.advert_service_name,
                    'advert_rate_card_id': advert_service.advert_rate_card_id,
                    'checked': 'false',
                    'service_duration': 0,
                    'service_start_date': '',
                    'service_end_date': ''
                }
                advert_services_list.append(advert_service_data)
                pass

        try:
            payment_obj = PaymentDetail.objects.get(business_id=str(business_obj.business_id))
            payment_details = {
                'payment_mode': payment_obj.payment_mode,
                'paid_amount': round(float(payment_obj.paid_amount), 2),
                'payable_amount': round(float(payment_obj.payable_amount), 2),
                'total_amount': round(float(payment_obj.total_amount), 2),
                'tax_type': payment_obj.tax_type.tax_rate,
                'note': payment_obj.note,
                'bank_name': payment_obj.bank_name,
                'branch_name': payment_obj.branch_name,
                'cheque_number': payment_obj.cheque_number
            }
            # print payment_details
        except Exception:
            payment_details = {
                'payment_mode': '',
                'paid_amount': '',
                'payable_amount': '',
                'total_amount': '',
                'tax_type': '',
                'note': '',
                'bank_name': '',
                'branch_name': '',
                'cheque_number': ''
            }
            pass


        data = {'tax_list': tax_list,'supplier_id':supplier_id, 'advert_service_list': advert_services_list, 'service_list': service_list,
                'username': request.session['login_user'], 'category_list': get_category(request), 'business_data': business_data,
                'premium_service_list': premium_service_list,
                'total_amount': float(total_amount), 'basic_amount': basic_amount, 'amount_1': amount_1,
                'amount_2': amount_2, 'amount_3': amount_3, 'amount_4': amount_4, 'amount_5': amount_5,
                'payment_details': payment_details,
                }
        return render(request, 'Admin/edit_subscription.html', data)


@csrf_exempt
def update_subscription_plan(request):
    print "-----------------save---------------",request.POST
    try:
        
        supplier_id = request.POST.get('supplier_id')
        category_id = request.POST.get('sub_category')
        business_id = request.POST.get('business_id')

        duration = request.POST.get('duration_list')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        premium_service_list = request.POST.getlist('premium_service')
        premium_service_duration_list = request.POST.getlist('premium_ser_duration')
        premium_start_date_list = request.POST.getlist('premium_start_date')
        premium_end_date_list = request.POST.getlist('premium_end_date')

        premium_end_date_list = filter(None, premium_end_date_list)
        zip_premium = zip(premium_service_list,premium_service_duration_list,premium_start_date_list,premium_end_date_list)
        if premium_service_list:
            check_premium_service = update_check_date(zip_premium,category_id,business_id)
            if check_premium_service['success'] == 'false':
                data = {'success': 'false', 'message': check_premium_service['msg']}
                return HttpResponse(json.dumps(data), content_type='application/json')

        supplier_obj = Supplier.objects.get(supplier_id = supplier_id)
        category_obj = Category.objects.get(category_id = category_id)
        service_ratecard_obj = ServiceRateCard.objects.get(duration = duration, service_name = 'Basic Subscription Plan')

        business_obj = Business.objects.get(business_id = business_id)
        business_obj.category=category_obj
        business_obj.service_rate_card_id=service_ratecard_obj
        business_obj.duration=duration
        business_obj.start_date=start_date
        business_obj.end_date=end_date
        business_obj.supplier=supplier_obj
        business_obj.business_created_date = datetime.now()
        business_obj.business_created_by = supplier_obj.contact_email

        business_obj.save()
        #
        transaction_code = business_obj.transaction_code
        if premium_service_list:
            PremiumService.objects.filter(business_id = business_id).delete()
            for premium_service, premium_service_duration, premium_start_date, premium_end_date  in zip_premium:
                print "premium_end_date",premium_service,premium_service_duration,premium_start_date,premium_end_date
                premium_service_obj = PremiumService(
                    premium_service_name = premium_service,
                    no_of_days = premium_service_duration,
                    category_id = category_obj,
                    start_date=premium_start_date,
                    end_date=premium_end_date,
                    business_id = business_obj,
                    premium_service_status = "1",
                    premium_service_created_date = datetime.now(),
                    premium_service_created_by = supplier_obj.contact_email
                )
                premium_service_obj.save()
        else:
            PremiumService.objects.filter(business_id=business_id).delete()
        data = {'success': 'true',
                'message': 'The subscription is updated successfully with transaction ID :'+transaction_code+'. Please proceed with the payment .',
                'business_id':str(business_obj)
                }
    except Exception as e:
        print e
        data = {'success': 'false', 'message': e}
    return HttpResponse(json.dumps(data), content_type='application/json')

def update_check_date(zip_premium,category_id,business_id):
    flag_1, flag_2, flag_3, flag_4, flag_5 = 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'
    service_list = ''
    for premium_service, premium_service_duration, premium_start_date, premium_end_date  in zip_premium:
        if premium_service == 'No.1 Listing':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                Q(category_id=str(category_id)) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).exclude(business_id = business_id).count()
            if premium_service_obj >= 1:
                flag_1 = 'No'
        if premium_service == 'No.2 Listing':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                Q(category_id=str(category_id)) &
                #Q(start_date__range=(premium_start_date, premium_end_date)) |
                #Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).exclude(business_id = business_id).count()

            print premium_service_obj

            if premium_service_obj >= 1:
                flag_2 = 'No'
        if premium_service == 'No.3 Listing':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                Q(category_id=str(category_id)) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).exclude(business_id = business_id).count()
            if premium_service_obj >= 1:
                flag_3 = 'No'
        if premium_service == 'Advert Slider':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).exclude(business_id = business_id).count()
            if premium_service_obj > 10:
                flag_4 = 'No'
        if premium_service == 'Top Advert':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).exclude(business_id = business_id).count()
            if premium_service_obj >= 1:
                flag_5 = 'No'
    if flag_1 == 'No':
        service_list = 'No.1 Listing,'
    if flag_2 == 'No':
        service_list = service_list + 'No.2 Listing,'
    if flag_3 == 'No':
        service_list = service_list + 'No.3 Listing,'
    if flag_4 == 'No':
        service_list = service_list + 'Advert Slider,'
    if flag_5 == 'No':
        service_list = service_list + 'Top Advert'
    if service_list != '':
        msg = service_list + ' already exist for selected date range'
        data = {'success': 'false','msg':msg}
    else:
        data = {'success': 'true', 'msg': ''}
    return data


@csrf_exempt
def update_payment_details(request):
    try:
        print "--------------------------------", request.POST

        chars = string.digits
        pwdSize = 8
        password = ''.join(random.choice(chars) for _ in range(pwdSize))

        business_id = request.POST.get('business_id')
        bank_name = request.POST.get('bank_name')
        cheque_number = request.POST.get('cheque_number')
        total_payable_amount = request.POST.get('total_payable_amount')
        bank_branch_name = request.POST.get('bank_branch_name')
        payment_amount = request.POST.get('payment_amount')
        payment_mode = request.POST.get('payment_mode')
        total_paid_amount = request.POST.get('total_paid_amount')
        payment_note = request.POST.get('payment_note')
        tax_type = request.POST.get('tax_type')
        payment_code = "PMID" + str(password)

        business_obj = Business.objects.get(business_id = business_id)
        tax_obj = Tax.objects.get(tax_rate = tax_type)
        try:
            payment_obj = PaymentDetail.objects.get(business_id = business_id)
        except Exception:
            print "=======new payment==========="
            payment_obj = PaymentDetail()
            payment_obj.save()
            payment_obj.payment_code = payment_code
            payment_obj.business_id = business_obj
            payment_obj.save()

        if total_paid_amount:
            payment_obj.paid_amount = total_paid_amount
        if payment_mode == 'cheque':
            payment_obj.bank_name = bank_name
            payment_obj.branch_name = bank_branch_name
            payment_obj.cheque_number = cheque_number

        payment_obj.payment_mode = payment_mode
        payment_obj.payable_amount = total_payable_amount
        payment_obj.total_amount = payment_amount
        payment_obj.note = payment_note
        payment_obj.tax_type = tax_obj
        payment_obj.save()

        data = {'success': 'true', 'message': 'Payment done successfully with Payment ID - '+payment_obj.payment_code}
    except Exception as e:
        print e
        data =  {'success': 'true', 'message': e}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def check_advert(request):
    try:
        print "ID---------",request.POST.get('business_id')
        service_obj = PaymentDetail.objects.filter(business_id=request.POST.get('business_id'))
        if service_obj:
            message = "true"
        else:
            message="false"

        data={
            'success':'true','message':message
        }
    except Exception, e:
        print e
        data={
            'success':'false',
        }
    return HttpResponse(json.dumps(data),content_type='application/json') 



@csrf_exempt
def update_subscriber_detail(request):
	try:
		supplier_obj = Supplier.objects.get(username = request.POST.get('user_email'))
		business_obj = Business.objects.get(supplier_id=supplier_obj)
		try:
			payment_obj = PaymentDetail.objects.get(business_id = business_obj)
			payment_obj.note = request.POST.get('note')
			payment_obj.payment_mode = request.POST.get('payment_mode')
			payment_obj.bank_name=request.POST.get('bank_name')
			payment_obj.branch_name=request.POST.get('bank_branch_name')
			payment_obj.cheque_number=request.POST.get('cheque_number')
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
			business_obj =  Business.objects.get(supplier_id=str(supplier_obj.supplier_id))	

			payment_obj = PaymentDetail(
			business_id = business_obj,
			note = request.POST.get('note'),
			payment_mode = request.POST.get('payment_mode'),
			bank_name=request.POST.get('bank_name'),
			branch_name=request.POST.get('bank_branch_name'),
			cheque_number=request.POST.get('cheque_number'),
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
 		'user_id':str(supplier_obj.supplier_id)
		}
		supplier_edit_payment_mail(payment_obj)
	except Exception, e:
		data={
				'success':'false',
				'message':str(e)
		}

	return HttpResponse(json.dumps(data),content_type='application/json')



def check_subscription(premium_service_list,premium_day):
	print '==in subscruiption function==================='
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
			print '=========in try============'
			service_rate_card_obj = AdvertRateCard.objects.get(advert_service_name=serv,duration=day)

		except Exception,e:
			print '=============in except================='
			print '==========e=============',e
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
			

		


# def check_date(premium_service_list,premium_start_date_list,premium_end_date_list,category_obj,business_obj):
# 	premium_service_list = premium_service_list
# 	premium_service_list = str(premium_service_list).split(',')

# 	premium_start_date_list = str(premium_start_date_list).split(',')
# 	premium_end_date_list = str(premium_end_date_list).split(',')

# 	zipped_wk = zip(premium_service_list,premium_start_date_list,premium_end_date_list)
# 	service_list= []
# 	start_day_list= []
# 	end_day_list= []
# 	false_status = 1	
# 	slider_status = 1
# 	print '===============zipped_wk=============',zipped_wk
# 	for service,start_date,end_date in zipped_wk:
# 		print '===========start date=======',start_date
# 		print '===========end date=======',end_date
		
# 		if service=='Advert Slider':
# 			if business_obj=='':
# 				service_rate_card_obj = PremiumService.objects.filter(Q(premium_service_name=service) & Q(Q(start_date__range = (start_date,end_date)) | Q(end_date__range=(start_date,end_date)) | Q(start_date__lte=start_date,end_date__gte=end_date)))
# 			else:
# 				business_id_list = Business.objects.all().exclude(business_id=str(business_obj))
# 				#service_rate_card_obj = PremiumService.objects.filter(premium_service_name=service,start_date__lte=start_date,end_date__gte=start_date,business_id__in=business_id_list)
# 				service_rate_card_obj = PremiumService.objects.filter(Q(premium_service_name=service) & Q(Q(start_date__range = (start_date,end_date)) | Q(end_date__range=(start_date,end_date)) | Q(start_date__lte=start_date,end_date__gte=end_date)) & Q(business_id__in=business_id_list))

# 			if len(service_rate_card_obj)>=10: 
# 				slider_status = 0
# 			else:
# 				slider_status = 1
				

# 		elif service=='Top Advert':
# 			try:
# 				if business_obj=='':
# 					service_rate_card_obj = PremiumService.objects.get(Q(premium_service_name=service) & Q(Q(start_date__range = (start_date,end_date)) | Q(end_date__range=(start_date,end_date)) | Q(start_date__lte=start_date,end_date__gte=end_date)))
# 					#service_rate_card_obj = PremiumService.objects.get(Q(Q(start_date__range = (start_date,end_date)) | Q(end_date__range=(start_date,end_date)) | Q(start_date__lte=start_date,end_date__gte=end_date)))


# 				else:
# 					business_id_list = Business.objects.all().exclude(business_id=str(business_obj))
# 					service_rate_card_obj = PremiumService.objects.get(Q(premium_service_name=service) & Q(Q(start_date__range = (start_date,end_date)) | Q(end_date__range=(start_date,end_date)) | Q(start_date__lte=start_date,end_date__gte=end_date)) & Q(business_id__in=business_id_list))
		
# 				service_list.append(str(service))
# 				start_day_list.append(service_rate_card_obj.start_date)
# 				end_day_list.append(service_rate_card_obj.end_date)

# 				false_status = 0

# 			except Exception,e:
# 				print '=========e================',e
# 				false_status = 1

# 		else:
# 			try:
# 				business_obj_list = Business.objects.filter(category=category_obj.category_id)

# 				if(business_obj==''):
# 					service_rate_card_obj = PremiumService.objects.get(Q(premium_service_name=service) & Q(Q(start_date__range = (start_date,end_date)) | Q(end_date__range=(start_date,end_date)) | Q(start_date__lte=start_date,end_date__gte=end_date)) & Q(business_id__in=business_obj_list))
# 				else:
# 					business_id_list = Business.objects.filter(category=category_obj.category_id).exclude(business_id=str(business_obj))


# 					service_rate_card_obj = PremiumService.objects.get(Q(premium_service_name=service) & Q(Q(start_date__range = (start_date,end_date)) | Q(end_date__range=(start_date,end_date)) | Q(start_date__lte=start_date,end_date__gte=end_date)) & Q(business_id__in=business_id_list))

# 				service_list.append(str(service))
# 				start_day_list.append(service_rate_card_obj.start_date)
# 				end_day_list.append(service_rate_card_obj.end_date)

# 				false_status = 0

# 			except Exception,e:
# 				false_status = 1


# 	if false_status == 1 and slider_status == 1:
# 		data={
#  				'success':'true',
#  		}
 	
#  	if false_status == 0 and slider_status == 0:
# 		zipped_list = zip(service_list,start_day_list,end_day_list)
# 		message = "Package for Premium Service(s) "
#  		for i,j,k in zipped_list:
#  			message = message + str(i) + " " + "from "+str(j)+" to " + str(k) + ", \n" 
		
# 		message = message[:-3] + " already exists"

# 		if slider_status == 0:
# 			message = message + " and Advert slider for selected date is not available"

# 		data={
#  				'success':'false',
#  				'message':message
#  			}

#  	if false_status == 1 and slider_status == 0:

# 		message = "Package for Premium Service(s) "
 		
# 		if slider_status == 0:
# 			message = message + "\n Advert slider for selected date is not available"

# 		data={
#  				'success':'false',
#  				'message':message
#  			}

#  	if false_status == 0 and slider_status == 1:
# 		zipped_list = zip(service_list,start_day_list,end_day_list)
# 		message = "Package for Premium Service(s) "
#  		for i,j,k in zipped_list:
#  			message = message + str(i) + " " + "from "+str(j)+" to " + str(k) + ", \n" 
		
# 		message = message[:-3] + " already exists"


# 		data={
#  				'success':'false',
#  				'message':message
#  			}		
 			
# 	return data 		

def supplier_add_mail(supplier_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	try:
		TEXT = "Hi Admin,\nSubscriber " + str(supplier_obj.contact_person) + " "+ "with Business " + str(supplier_obj.business_name)+ " " +"has been added successfully.\nTo view complete details visit portal and follow - Customers -> Subscribers"+'\n\n'+ "Thank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Subscriber Added Successfully!"
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

def supplier_add_service_mail(business_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nSubscriber " + str(business_obj.supplier.contact_person) + " "+ "with Business " + str(business_obj.supplier.business_name)+ " " +"has been added successfully.\nTransaction ID "+ str(business_obj.transaction_code) + " for this transaction has been generated successfully.\nTo view complete details visit portal and follow - Customers -> Subscribers"+'\n\n'+ "Thank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Subscriber Added Successfully!"
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


def supplier_add_payment_mail(payment_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	business_obj = Business.objects.get(business_id=str(payment_obj.business_id.business_id))
	supplier_id = Supplier.objects.get(supplier_id=str(business_obj.supplier_id))
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nSubscriber " + str(supplier_id.contact_person) + " "+ "with Business " + str(supplier_id.business_name)+ " " +"has been added successfully.\nPayment ID"+ str(payment_obj.payment_code) + " for this payment has been generated successfully. \nTo view complete details visit portal and follow - Customers -> Subscribers" +'\n\n'+ "Thank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Subscriber Added Successfully!"
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

def supplier_edit_mail(supplier_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	try:
		TEXT = "Hi Admin,\nSubscriber " + str(supplier_obj.contact_person) + " "+ "with Business " + str(supplier_obj.business_name)+ " " +"has been updated successfully.\nTo view complete details visit portal and follow - Customers -> Subscribers"+'\n\n'+ "Thank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Subscriber Updated Successfully!"
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

def supplier_edit_service_mail(business_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nSubscriber " + str(business_obj.supplier.contact_person) + " "+ "with Business " + str(business_obj.supplier.business_name)+ " " +"has been updated successfully. \nTransaction ID "+ str(business_obj.transaction_code) + " for this transaction has been generated successfully.\nTo view complete details visit portal and follow - Customers -> Subscribers"+'\n\n'+ "Thank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Subscriber Updated Successfully!"
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


def supplier_edit_payment_mail(payment_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	business_obj = Business.objects.get(business_id=str(payment_obj.business_id.business_id))
	supplier_id = Supplier.objects.get(supplier_id=str(business_obj.supplier_id))
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nSubscriber " + str(supplier_id.contact_person) + " "+ "with Business " + str(supplier_id.business_name)+ " " +"has been updated successfully.\nPayment ID"+ str(payment_obj.payment_code) + " for this payment has been generated successfully.\nTo view complete details visit portal and follow - Customers -> Subscribers" +'\n\n'+"Thank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Subscriber Updated Successfully!"
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

def supplier_inactive_mail(user_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nSubscriber " + str(user_obj.contact_person) + " "+ "with Business " + str(user_obj.business_name)+ " " +"deactivated successfully.\n\nThank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Subscriber Deactivated Successfully!"
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
def active_subscriber(request):
        try:
            subscriber_obj = Supplier.objects.get(supplier_id=request.POST.get('subscriber_id'))
            subscriber_obj.supplier_status = '1'
            subscriber_obj.save()
            supplier_activate_mail(subscriber_obj)
            data = {'message': 'Subscriber activated Successfully', 'success':'true'}

        except IntegrityError as e:
          print e
        except Exception,e:
            print e
        return HttpResponse(json.dumps(data), content_type='application/json')
       
def supplier_activate_mail(user_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nSubscriber " + str(user_obj.contact_person) + " "+ "with Business " + str(user_obj.business_name)+ " " +"activated successfully.\n\nThank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Subscriber Activated Successfully!"
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
