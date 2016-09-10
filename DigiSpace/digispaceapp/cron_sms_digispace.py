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
from erozgarapp.models import *
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction
import pdb
import csv
import json
# importing exceptions
from smtplib import SMTPException
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from erozgarapp import models
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.cache import cache_control
# Create your views here.
import smtplib
import re
import string
import random
import urllib
from datetime import date, timedelta
# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect

#pip install django-crontab

# ('*/5 * * * *', 'myapp.cron.my_scheduled_job')

#python manage.py crontab add

#python manage.py crontab show

#python manage.py crontab remove

#Add this in settings - CRONJOBS = [
#    ('0 0 * * *', 'digispaceapp.cron_sms_digispace .my_scheduled_job'),
#]

#INSTALLED_APPS = (
#    'django_crontab',
#    'django.contrib.contenttypes',
#    'django.contrib.sessions',
#)

def my_scheduled_job():
    MAILTO=""
    today_date = str(datetime.now())
    next_week_date = str(datetime.now() + timedelta(days=7))
    list = []
    consumer_obj_list = Business.objects.filter(end_date__range=[today_date,next_week_date])
	
    if consumer_obj_list:
        for consumer_obj in consumer_obj_list:
            email_id = consumer_obj.supplier.supplier_email 
            list.append(str(email_id))
        email_list = set(list)

        for email in email_list:
            gmail_user =  "cityhoopla2016"
            gmail_pwd =  "cityhoopla@2016"
            FROM = 'CityHoopla Admin: <cityhoopla2016@gmail.com>'
            TO = [email]

            try:
            	TEXT = 'Your advert is going to expire'
                SUBJECT = 'Welcome to City Hoopla'
            	server = smtplib.SMTP_SSL()
            	server = smtplib.SMTP("smtp.gmail.com", 587) 
            	server.ehlo()
            	server.starttls()

            	server.login(gmail_user, gmail_pwd)
            	message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            	server.sendmail(FROM, TO, message)
            	server.quit()
            except SMTPException,e:
            	print e
        

