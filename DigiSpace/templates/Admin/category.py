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

SERVER_URL = "http://127.0.0.1:8000"   

#SERVER_URL = "http://52.40.205.128"   

def add_category(request):
	city_list = City.objects.filter(city_status='1').order_by('city_name') 
	data = {'city_list':city_list,'username':request.session['login_user']}
	return render(request,'Admin/add_category.html',data)       

@csrf_exempt
def save_category(request):
	#pdb.set_trace()
	city_list = request.POST.getlist('city[]')
	if city_list!=[u'']:	
			sequence_list = request.POST.getlist('sequence[]')
			zipped_list = zip(city_list,sequence_list)
			if(cheksamesequence(zipped_list)):

		
				try:
					print '=============request.POST=======',request.POST
					category_obj = Category.objects.get(category_name=request.POST.get('category_name'))

					data={
						'success':'false',
						'message':"Category already exist"
					}

				except Exception,e:
					print e
					cat_obj = Category(
						category_name=request.POST.get('category_name'),
						level = '0',
						category_created_date = datetime.now(),
						category_updated_date = datetime.now(),
						category_status = '1'
					)
					cat_obj.save()
					cat_obj.has_category = cat_obj
					cat_obj.save()
					city_list = request.POST.getlist('city[]')
					print "---------city_list",city_list
					if city_list!=[u'']:	
						sequence_list = request.POST.getlist('sequence[]')
						zipped_list = zip(city_list,sequence_list)
						if zipped_list:
							for city_id,sequence in zipped_list:
								if city_id!='' and sequence!='':
									map_obj=CategoryCityMap(
										city_id=City.objects.get(city_id=city_id),
										sequence=sequence,
										category_id=cat_obj,
										creation_date=datetime.now(),
										updation_date=datetime.now()
									)
									map_obj.save()

					subcategory_list1 = request.POST.getlist('subcategory1[]')
					if subcategory_list1!=[u'']:
						for category in subcategory_list1:
							category_obj = Category(
								category_name = category,
								level = '1',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj.save()
							category_obj.has_category = cat_obj
							category_obj.save()	        
					subcategory_list2 = request.POST.getlist('subcategory2[]')

					if subcategory_list2!=[u'']:
						for category in subcategory_list2:
							category_obj = Category(
								category_name = category,
								level = '2',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj.save()
							category_obj.has_category = cat_obj
							category_obj.save()	        
					subcategory_list3 = request.POST.getlist('subcategory3[]')

					if subcategory_list3!=[u'']:
						for category in subcategory_list3:
							category_obj = Category(
								category_name = category,
								level = '3',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj.save()
							category_obj.has_category = cat_obj
							category_obj.save()
					subcategory_list4 = request.POST.getlist('subcategory4[]')			        
					if subcategory_list4!=[u'']:
						for category in subcategory_list4:
							category_obj = Category(
								category_name = category,
								level = '4',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj.save()
							category_obj.has_category = cat_obj
							category_obj.save()
					subcategory_list5 = request.POST.getlist('subcategory5[]')			        
					if subcategory_list5!=[u'']:
						for category in subcategory_list5:
							category_obj = Category(
								category_name = category,
								level = '5',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj.save()
							category_obj.has_category = cat_obj
							category_obj.save()	        
					data={
						'success':'true',
						'message':"Category added successfully",
					}
					add_category_mail(cat_obj)
			else:
				data = {'message':'Sequence for the selected city already exists','success':'false'}
			print '===========data============',data
	
	else:
		try:
			category_obj = Category.objects.get(category_name=request.POST.get('category_name'))

			data={
						'success':'false',
						'message':"Category already exist"
			}

		except Exception,e:
			print e
			cat_obj = Category(
				category_name=request.POST.get('category_name'),
				level = '0',
				category_created_date = datetime.now(),
				category_updated_date = datetime.now(),
				category_status = '1'
			)
			cat_obj.save()
			cat_obj.has_category = cat_obj
			cat_obj.save()

			subcategory_list1 = request.POST.getlist('subcategory1[]')
			if subcategory_list1!=[u'']:
				for category in subcategory_list1:
					category_obj = Category(
						category_name = category,
						level = '1',
						category_created_date = datetime.now(),
						category_updated_date = datetime.now(),
						category_status = '1'
					)
					category_obj.save()
					category_obj.has_category = cat_obj
					category_obj.save()	        
			subcategory_list2 = request.POST.getlist('subcategory2[]')

			if subcategory_list2!=[u'']:
				for category in subcategory_list2:
					category_obj = Category(
						category_name = category,
						level = '2',
						category_created_date = datetime.now(),
						category_updated_date = datetime.now(),
						category_status = '1'
					)
					category_obj.save()
					category_obj.has_category = cat_obj
					category_obj.save()	        
			subcategory_list3 = request.POST.getlist('subcategory3[]')

			if subcategory_list3!=[u'']:
				for category in subcategory_list3:
					category_obj = Category(
						category_name = category,
						level = '3',
						category_created_date = datetime.now(),
						category_updated_date = datetime.now(),
						category_status = '1'
					)
					category_obj.save()
					category_obj.has_category = cat_obj
					category_obj.save()
			subcategory_list4 = request.POST.getlist('subcategory4[]')			        
			if subcategory_list4!=[u'']:
				for category in subcategory_list4:
					category_obj = Category(
						category_name = category,
						level = '4',
						category_created_date = datetime.now(),
						category_updated_date = datetime.now(),
						category_status = '1'
					)
					category_obj.save()
					category_obj.has_category = cat_obj
					category_obj.save()
			subcategory_list5 = request.POST.getlist('subcategory5[]')			        
			if subcategory_list5!=[u'']:
				for category in subcategory_list5:
					category_obj = Category(
						category_name = category,
						level = '5',
						category_created_date = datetime.now(),
						category_updated_date = datetime.now(),
						category_status = '1'
					)
					category_obj.save()
					category_obj.has_category = cat_obj
					category_obj.save()	        
			data={
				'success':'true',
				'message':"Category added successfully",
			}
			add_category_mail(cat_obj)		

	return HttpResponse(json.dumps(data),content_type='application/json')


def cheksamesequence(zipped_list):
	for city_id,sequence in zipped_list:
		if city_id!='' and sequence!='':

			try:
				cat_obj = CategoryCityMap.objects.get(city_id=City.objects.get(city_id=city_id),sequence=sequence)
			except:
				return True	



def updatecheksamesequence(zipped_list,cat_id):
	#pdb.set_trace()
	cat_obj = Category.objects.get(category_id=cat_id)
	for city_id,sequence in zipped_list:
		if city_id!='' and sequence!='':
			cat_obj = CategoryCityMap.objects.filter(city_id=City.objects.get(city_id=city_id),sequence=sequence).exclude(category_id=cat_obj.category_id)
			if cat_obj:
				return False
			else:
				return True	

def category_list(request):
	try:
		data = {}
		final_list = []
		try:
			category_list = Category.objects.filter(level='0')
			for cat_obj in category_list:
				category_id = str(cat_obj.category_id)
				category_name = cat_obj.category_name
				city_name = CategoryCityMap.objects.filter(category_id=cat_obj)
				city_list = ''
				if city_name:
					for city in city_name:
						city_list = str(city.city_id.city_name)+ ',' + city_list
					city_list = city_list[:-1]	
				creation_date = str(cat_obj.category_created_date).split( )[0]
				updation_date = str(cat_obj.category_updated_date).split( )[0]
				if(cat_obj.category_status=='1'):
					status= 'Active'
					delete = '<a id="'+str(category_id)+'" onclick="delete_category(this.id)" style="text-align: center;letter-spacing: 5px;width:15%;" title="Delete"  ><i class="fa fa-trash"></i></a>'
					edit = '<a  id="'+str(category_id)+'" href="/edit-category/?category_id='+str(category_id)+'" style="text-align: center;letter-spacing: 5px;width:15%;" title="Edit" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-pencil"></i></a>'
					actions =  edit + delete
				else:
					status = 'Inactive'	
					active = '<a class="col-md-2" id="'+str(cat_obj)+'" onclick="active_service(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;margin-left: 36px !important;" title="Activate" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-repeat"></i></a>'	
					actions =  active
				list = {'status':status,'category_name':category_name,'actions':actions,'city_name':city_list,'creation_date':creation_date,'updation_date':updation_date}
				final_list.append(list)
			data = {'success':'true','data':final_list}
		except IntegrityError as e:
			print e
			data = {'success':'false','message':'Error in  loading page. Please try after some time'}
	except MySQLdb.OperationalError, e:
		print e
	except Exception,e:
		print 'Exception ',e
	#print '====data============',data	
	return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def delete_category(request):
	try:
		cat_obj = Category.objects.get(category_id=request.POST.get('category_id'))
		cat_obj.category_status = '0'
		cat_obj.save()
		data = {'message': 'User Role De-activeted Successfully', 'success':'true'}
		inactive_category_mail(cat_obj)
	except IntegrityError as e:
		print e
	except Exception,e:
		print e
		print "Final Data: ",data
	return HttpResponse(json.dumps(data), content_type='application/json')
   
def get_city(request):
   
   city_list=[]
   try:
      city_objs=City.objects.filter(city_status='1').order_by('city_name')
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

def edit_category(request):
	try:
		data = {}
		final_list = []
		sub_category1_list = []
		sub_category2_list = []
		sub_category3_list = []
		sub_category4_list = []
		sub_category5_list = []
		city_list = City.objects.filter(city_status='1')
		selected_city_list = []
		selected_sequence_list = []

		try:
			category = Category.objects.get(category_id=request.GET.get('category_id'))
			category_id = str(category.category_id)
			category_name = str(category.category_name)
			city_name = CategoryCityMap.objects.filter(category_id=category)
			sequence_list = ['1','2','3','4','5']
			for city in city_name:
				selected_city_list.append(str(city.city_id.city_name))
				selected_sequence_list.append(str(city.sequence))

			city_sequence_list = zip(selected_city_list,selected_sequence_list)
			print '=====category=======',category 
			sub_category1 = Category.objects.filter(has_category=category,level='1')
			if sub_category1:
				for cat in sub_category1:
					category1_list = {'category_name':cat.category_name}

					sub_category1_list.append(category1_list)		
			length1 = len(sub_category1_list)
			sub_category2 = Category.objects.filter(has_category=category,level='2')
			if sub_category2:
				for cat in sub_category2:
					category2_list = {'category_name':cat.category_name}	
					sub_category2_list.append(category2_list)		
			length2 = len(sub_category2_list)	


			sub_category3 = Category.objects.filter(has_category=category,level='3')
			if sub_category3:
				for cat in sub_category3:
					category3_list = {'category_name':cat.category_name}	
					sub_category3_list.append(category3_list)		
			length3 = len(sub_category3_list)	


			sub_category4 = Category.objects.filter(has_category=category,level='4')
			if sub_category4:
				for cat in sub_category4:
					category4_list = {'category_name':cat.category_name}	
					sub_category4_list.append(category4_list)		
			length4 = len(sub_category4_list)


			sub_category5 = Category.objects.filter(has_category=category,level='5')
			if sub_category5:
				for cat in sub_category5:
					category5_list = {'category_name':cat.category_name}	
					sub_category5_list.append(category5_list)		
			length5 = len(sub_category5_list)


			data = {'username':request.session['login_user'],'sequence_list':sequence_list,'length5':length5,'length4':length4,'length3':length3,'length2':length2,'length1':length1,'category_id':category_id,'city_sequence_list':city_sequence_list,'city_list':city_list,'success':'true','sub_category5_list':sub_category5_list,'sub_category4_list':sub_category4_list,'sub_category3_list':sub_category3_list,'sub_category2_list':sub_category2_list,'category_name':category_name,'sub_category1_list':sub_category1_list}
			
		except IntegrityError as e:
			print e
			data = {'success':'false','message':'Error in  loading page. Please try after some time'}
	except MySQLdb.OperationalError, e:
		print e
	except Exception,e:
		print 'Exception ',e
	return render(request,'Admin/edit_category.html',data)       



@csrf_exempt
def update_category(request):
	#try:
	print '================request=======',request.POST
	#pdb.set_trace()
	data = {}
	category_obj = request.POST.get('category_name')
	category_id = request.POST.get('category_id')
	#pdb.set_trace()
	try:
		city_list = request.POST.getlist('city[]')
		if city_list!=[u'']:	
			sequence_list = request.POST.getlist('sequence[]')
			zipped_list = zip(city_list,sequence_list)
			if(updatecheksamesequence(zipped_list,category_id)):
				category_object=Category.objects.get(category_name=request.POST.get('category_name'),level='0')
				if(str(category_id)==str(category_object)):
					category_object=Category.objects.get(category_name=request.POST.get('category_name'),level='0')
					category_object.category_name = request.POST.get('category_name')
					category_object.save()
					city_list = request.POST.getlist('city[]')
					if city_list!=[u'']:	
						sequence_list = request.POST.getlist('sequence[]')
						zipped_list = zip(city_list,sequence_list)
						cat_obj = CategoryCityMap.objects.filter(category_id=category_object).delete()
						if city_list:
							for city_id,sequence in zipped_list:
								map_obj=CategoryCityMap(
									city_id=City.objects.get(city_id=city_id),
									sequence=sequence,
									category_id=category_object,
									creation_date=datetime.now(),
									updation_date=datetime.now()
									)
								map_obj.save()
					cat_id = category_object.category_id
					subcategory_obj = Category.objects.filter(has_category=category_object).exclude(level='0').delete()
					subcategory_list1 = request.POST.getlist('subcategory1[]')
					if subcategory_list1!=[u'']:
						for category in subcategory_list1:
							category_obj1 = Category(
								category_name = category,
								level = '1',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
					 		)
					 		category_obj1.save()
					 		category_obj1.has_category = category_object
					 		category_obj1.save()
					subcategory_list2 = request.POST.getlist('subcategory2[]')
					if subcategory_list2!=[u'']:
						for category in subcategory_list2:
							category_obj2 = Category(
								category_name = category,
								level = '2',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj2.save()
							category_obj2.has_category = category_object
							category_obj2.save()
					subcategory_list3 = request.POST.getlist('subcategory3[]')
					if subcategory_list3!=[u'']:
						for category in subcategory_list3:
							category_obj3 = Category(
								category_name = category,
								level = '3',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj3.save()
							category_obj3.has_category = category_object
							category_obj3.save()
					subcategory_list4 = request.POST.getlist('subcategory4[]')
					if subcategory_list4!=[u'']:
						for category in subcategory_list4:
							category_obj4 = Category(
								category_name = category,
								level = '4',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj4.save()
							category_obj4.has_category = category_object
							category_obj4.save()

					subcategory_list5 = request.POST.getlist('subcategory5[]')
					if subcategory_list5!=[u'']:
						for category in subcategory_list5:
							category_obj5 = Category(
								category_name = category,
								level = '5',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj5.save()
							category_obj5.has_category = category_object
							category_obj5.save()
					edit_category_mail(category_object)		
					data = {'success':'true'}
					return HttpResponse(json.dumps(data),content_type='application/json')
				else:
					data = {'success':'false123'}
			else:
				data = {'message':'Sequence for the selected city already exists','success':'false'}
		# code if city not selected
		else:
				category_object=Category.objects.get(category_name=request.POST.get('category_name'),level='0')
				if(str(category_id)==str(category_object)):
					category_object=Category.objects.get(category_name=request.POST.get('category_name'),level='0')
					category_object.category_name = request.POST.get('category_name')
					category_object.save()
					cat_id = category_object.category_id
					subcategory_obj = Category.objects.filter(has_category=category_object).exclude(level='0').delete()
					subcategory_list1 = request.POST.getlist('subcategory1[]')
					if subcategory_list1!=[u'']:
						for category in subcategory_list1:
							category_obj1 = Category(
								category_name = category,
								level = '1',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
					 		)
					 		category_obj1.save()
					 		category_obj1.has_category = category_object
					 		category_obj1.save()
					subcategory_list2 = request.POST.getlist('subcategory2[]')
					if subcategory_list2!=[u'']:
						for category in subcategory_list2:
							category_obj2 = Category(
								category_name = category,
								level = '2',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj2.save()
							category_obj2.has_category = category_object
							category_obj2.save()
					subcategory_list3 = request.POST.getlist('subcategory3[]')
					if subcategory_list3!=[u'']:
						for category in subcategory_list3:
							category_obj3 = Category(
								category_name = category,
								level = '3',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj3.save()
							category_obj3.has_category = category_object
							category_obj3.save()
					subcategory_list4 = request.POST.getlist('subcategory4[]')
					if subcategory_list4!=[u'']:
						for category in subcategory_list4:
							category_obj4 = Category(
								category_name = category,
								level = '4',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj4.save()
							category_obj4.has_category = category_object
							category_obj4.save()

					subcategory_list5 = request.POST.getlist('subcategory5[]')
					if subcategory_list5!=[u'']:
						for category in subcategory_list5:
							category_obj5 = Category(
								category_name = category,
								level = '5',
								category_created_date = datetime.now(),
								category_updated_date = datetime.now(),
								category_status = '1'
							)
							category_obj5.save()
							category_obj5.has_category = category_object
							category_obj5.save()
					edit_category_mail(category_object)		
					data = {'success':'true'}
					return HttpResponse(json.dumps(data),content_type='application/json')
				else:
					data = {'success':'false123'}

	except Exception,e:
		print '=======e================',e
		#pdb.set_trace()
		city_list = request.POST.getlist('city[]')
		if city_list!=[u'']:	
			sequence_list = request.POST.getlist('sequence[]')
			zipped_list = zip(city_list,sequence_list)
			if(updatecheksamesequence(zipped_list,category_id)):
				category_obj=Category.objects.get(category_id=str(category_id))
				category_obj.category_name = request.POST.get('category_name')
				category_obj.save()
				city_list = request.POST.getlist('city[]')
				if city_list!=[u'']:	
					sequence_list = request.POST.getlist('sequence[]')
					zipped_list = zip(city_list,sequence_list)
					cat_obj = CategoryCityMap.objects.filter(category_id=category_obj).delete()
					for city_id,sequence in zipped_list:
						map_obj=CategoryCityMap(
							city_id=City.objects.get(city_id=city_id),
							sequence=sequence,
							category_id=category_obj,
							creation_date=datetime.now(),
							updation_date=datetime.now()
							)
						map_obj.save()
				subcategory_obj = Category.objects.filter(has_category=str(category_obj.category_id)).exclude(level='0').delete()
				subcategory_list1 = request.POST.getlist('subcategory1[]')
				if subcategory_list1!=[u'']:
					for category in subcategory_list1:
						category_obj1 = Category(
							category_name = category,
							level = '1',
							category_created_date = datetime.now(),
							category_updated_date = datetime.now(),
							category_status = '1'
						)
						category_obj1.save()
						category_obj1.has_category = category_obj
						category_obj1.save()
				subcategory_list2 = request.POST.getlist('subcategory2[]')
				if subcategory_list2!=[u'']:
					for category in subcategory_list2:
						category_obj2 = Category(
							category_name = category,
							level = '2',
				 			category_created_date = datetime.now(),
				 			category_updated_date = datetime.now(),
				 			category_status = '1'
				 		)
				 		category_obj2.save()
				 		category_obj2.has_category = category_obj
				 		category_obj2.save()

				subcategory_list3 = request.POST.getlist('subcategory3[]')

				if subcategory_list3!=[u'']:
				 	for category in subcategory_list3:
				 		category_obj3 = Category(
				 			category_name = category,
				 			level = '3',
				 			category_created_date = datetime.now(),
				 			category_updated_date = datetime.now(),
				 			category_status = '1'
				 		)
				 		category_obj3.save()
				 		category_obj3.has_category = category_obj
				 		category_obj3.save()

				subcategory_list4 = request.POST.getlist('subcategory4[]')

				if subcategory_list4!=[u'']:
				 	for category in subcategory_list3:
				 		category_obj4 = Category(
				 			category_name = category,
				 			level = '4',
				 			category_created_date = datetime.now(),
				 			category_updated_date = datetime.now(),
				 			category_status = '1'
				 		)
				 		category_obj4.save()
				 		category_obj4.has_category = category_obj
				 		category_obj4.save()

				subcategory_list5 = request.POST.getlist('subcategory5[]')

				if subcategory_list5!=[u'']:
					for category in subcategory_list5:
					 	category_obj5 = Category(
					 			category_name = category,
					 			level = '5',
					 			category_created_date = datetime.now(),
					 			category_updated_date = datetime.now(),
					 			category_status = '1'
					 	)
					 	category_obj5.save()
					 	category_obj5.has_category = category_obj
					 	category_obj5.save()
				edit_category_mail(category_obj)
				data={
				    'success':'true',
				    }
			else:
				data = {'message':'Sequence for the selected city already exists','success':'false'}

		
		# code if city not selected
		else:
				category_object=Category.objects.get(category_id=str(category_id))
				category_object.category_name = request.POST.get('category_name')
				category_object.save()
				cat_id = category_object.category_id
				subcategory_obj = Category.objects.filter(has_category=category_object).exclude(level='0').delete()
				subcategory_list1 = request.POST.getlist('subcategory1[]')
				if subcategory_list1!=[u'']:
					for category in subcategory_list1:
						category_obj1 = Category(
							category_name = category,
							level = '1',
							category_created_date = datetime.now(),
							category_updated_date = datetime.now(),
							category_status = '1'
				 		)
				 		category_obj1.save()
				 		category_obj1.has_category = category_object
				 		category_obj1.save()
				subcategory_list2 = request.POST.getlist('subcategory2[]')
				if subcategory_list2!=[u'']:
					for category in subcategory_list2:
						category_obj2 = Category(
							category_name = category,
							level = '2',
							category_created_date = datetime.now(),
							category_updated_date = datetime.now(),
							category_status = '1'
						)
						category_obj2.save()
						category_obj2.has_category = category_object
						category_obj2.save()
				subcategory_list3 = request.POST.getlist('subcategory3[]')
				if subcategory_list3!=[u'']:
					for category in subcategory_list3:
						category_obj3 = Category(
							category_name = category,
							level = '3',
							category_created_date = datetime.now(),
							category_updated_date = datetime.now(),
							category_status = '1'
						)
						category_obj3.save()
						category_obj3.has_category = category_object
						category_obj3.save()
				subcategory_list4 = request.POST.getlist('subcategory4[]')
				if subcategory_list4!=[u'']:
					for category in subcategory_list4:
						category_obj4 = Category(
							category_name = category,
							level = '4',
							category_created_date = datetime.now(),
							category_updated_date = datetime.now(),
							category_status = '1'
						)
						category_obj4.save()
						category_obj4.has_category = category_object
						category_obj4.save()

				subcategory_list5 = request.POST.getlist('subcategory5[]')
				if subcategory_list5!=[u'']:
					for category in subcategory_list5:
						category_obj5 = Category(
							category_name = category,
							level = '5',
							category_created_date = datetime.now(),
							category_updated_date = datetime.now(),
							category_status = '1'
						)
						category_obj5.save()
						category_obj5.has_category = category_object
						category_obj5.save()
				edit_category_mail(category_object)		
				data = {'success':'true'}
				return HttpResponse(json.dumps(data),content_type='application/json')
		

	return HttpResponse(json.dumps(data),content_type='application/json')      


def add_category_mail(cat_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nCategory " + str(cat_obj.category_name) + " "+ "has been added successfully." + "\nTo view complete details visit portal and follow - Reference Data -> Category"+ "\n\nThank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Category Added Successfully!"
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

def edit_category_mail(cat_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nCategory " + str(cat_obj.category_name) + " "+ "has been updated successfully." + "\nTo view complete details visit portal and follow - Reference Data -> Category"+ "\n\nThank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Category Updated Successfully!"
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

def inactive_category_mail(cat_obj):
	gmail_user =  "cityhoopla2016"
	gmail_pwd =  "cityhoopla@2016"
	FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
	TO = ['cityhoopla2016@gmail.com']
	#pdb.set_trace()
	try:
		TEXT = "Hi Admin,\nCategory " + str(cat_obj.category_name) + " "+ "has been deactivated successfully." +  "\n\nThank You,"+'\n'+"CityHoopla Team"
		SUBJECT = "Category Deactivated Successfully!"
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
def active_category(request):
        # pdb.set_trace()
        try:
			cat_obj = Category.objects.get(category_id=request.POST.get('category_id'))
			cat_obj.category_status ='1'
			cat_obj.save()
			data = {'message': 'Category activeted Successfully', 'success':'true'}
			category_active_mail(cat_obj)

        except IntegrityError as e:
          print e
        except Exception,e:
            print e
        print "Final Data: ",data
        return HttpResponse(json.dumps(data), content_type='application/json')

def category_active_mail(cat_obj):
    gmail_user =  "cityhoopla2016"
    gmail_pwd =  "cityhoopla@2016"
    FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
    TO = ['cityhoopla2016@gmail.com']
    #pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCategory " + str(cat_obj.category_name) + " " +" has been activated successfully.\nTo view complete details visit portal and follow - Reference Data -> Category\n\n Thank You,"+'\n'+"CityHoopla Team"
        SUBJECT = "Category Activated Successfully!"
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
