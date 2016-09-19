import json
import math
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from django.core import serializers
from rest_framework.authtoken.models import Token
from digispaceapp.models import *

def UserProfileToJSON(userprofileObj):
	dict = {}
	attributes = []
	dict1 = {}
	dict1['phone'] = str(userprofileObj.contact_no)
	dict1['user_id'] = str(userprofileObj.id)
	dict1['full_name'] = str(userprofileObj.first_name) + ' ' + str(userprofileObj.last_name)
	# dict1['user_profile_image'] = str(userprofileObj.)
	dict1['email_id'] = str(userprofileObj.email)
	dict1['city'] = str(userprofileObj.city.city)
	attributes.append(dict1)
	dict['user_info'] = attributes
	return dict