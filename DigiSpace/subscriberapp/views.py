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
from django.shortcuts import *
from digispaceapp.models import UserProfile
import dateutil.relativedelta
# import Admin
from captcha_form import CaptchaForm

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
from django.views.decorators.cache import cache_control
# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import dateutil.relativedelta
from django.db.models import Count
from datetime import date
import calendar
import urllib2

import string
import random

# SERVER_URL = "http://52.40.205.128"
SERVER_URL = "http://192.168.0.151:9090"


# SERVER_URL = "http://127.0.0.1:8000"

def signing_out(request):
    logout(request)
    form = CaptchaForm()
    return render_to_response('Subscriber/user_login.html', dict(
        form=form, message_logout='You have successfully logged out.'
    ), context_instance=RequestContext(request))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_advert(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        user_id = request.session['supplier_id']
        business_id = request.GET.get('business_id')
        tax_list = Tax.objects.all()

        service_list = ServiceRateCard.objects.filter(service_rate_card_status='1').values('service_name').distinct()
        advert_service_list, item_ids = [], []
        for item in AdvertRateCard.objects.filter(advert_rate_card_status='1'):
            if item.advert_service_name not in item_ids:
                advert_service_list.append(str(item.advert_rate_card_id))
                item_ids.append(item.advert_service_name)

        advert_service_list = AdvertRateCard.objects.filter(advert_rate_card_id__in=advert_service_list)

        data = {'tax_list': tax_list, 'advert_service_list': advert_service_list, 'service_list': service_list,
                'username': request.session['login_user'], 'user_id': user_id, 'category_list': get_category(request),
                'country_list': get_country(request), 'phone_category': get_phone_category(request), 'business_id':business_id,
                'state_list': get_states(request)}
        if business_id:
            business_obj = Business.objects.get(business_id = business_id)
            data = {'tax_list': tax_list, 'advert_service_list': advert_service_list, 'service_list': service_list,
                    'username': request.session['login_user'], 'user_id': user_id,
                    'category_list': get_category(request), 'category_id':str(business_obj.category.category_id),
                    'country_list': get_country(request), 'phone_category': get_phone_category(request),
                    'business_id': business_id,
                    'state_list': get_states(request)}
            return render(request, 'Subscriber/add_advert_form.html', data)
        else:
            return render(request, 'Subscriber/add_advert.html', data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_advert_form(request):
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

        data = {'tax_list': tax_list, 'advert_service_list': advert_service_list, 'service_list': service_list,
                'username': request.session['login_user'], 'user_id': user_id, 'category_list': get_category(request),
                'country_list': get_country(request), 'phone_category': get_phone_category(request),
                'state_list': get_states(request)}
        return render(request, 'Subscriber/add_advert_form.html', data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def advert_bookings(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        advert_id = request.GET.get('advert_id')
        advert_obj = Advert.objects.get(advert_id=advert_id)
        coupon_user = CouponCode.objects.filter(advert_id=advert_id)
        coupon_list = []
        for coupons in coupon_user:
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
            print status
            coupon_obj = {
                'coupon_code': coupons.coupon_code,
                'avail_date': coupons.creation_date.strftime("%d/%m/%Y"),
                'user_id': str(coupons.user_id),
                'mobile_no': coupons.user_id.consumer_contact_no,
                'user_img': SERVER_URL + coupons.user_id.consumer_profile_pic.url,
                'user_name': coupons.user_id.consumer_full_name,
                'user_area': coupons.user_id.consumer_area,
                'user_email_id': coupons.user_id.consumer_email_id,
                'coupon_expiry_date': end_date.strftime("%d/%m/%Y"),
                'days_remaining': int(date_gap.days),
                'status': status
            }
            coupon_list.append(coupon_obj)
        data = {'coupon_list': coupon_list, 'advert_name': advert_obj.advert_name, 'booking_count': len(coupon_list),
                'username': request.session['login_user']}
        return render(request, 'Subscriber/advert_bookings.html', data)


def get_country(request):
    ##    pdb.set_trace()
    country_list = []
    try:
        country_obj = Country.objects.filter(country_status='1')
        for country in country_obj:
            country_list.append(
                {'country_id': country.country_id, 'country_name': country.country_name})

    except Exception, e:
        print 'Exception ', e
    return country_list


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


# TO GET THE STATE
def get_states(request):
    ##    pdb.set_trace()
    state_list = []
    try:
        state = State.objects.filter(state_status='1')
        for sta in state:
            options_data = {
                'state_id': str(sta.state_id),
                'state_name': str(sta.state_name)

            }
            state_list.append(options_data)
        return state_list
    except Exception, e:
        print 'Exception ', e
        data = {'state_list': 'No states available'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_basic_subscription_amount(request):
    print "--------------------------------"
    duration = request.POST.get('duration')
    service_obj = ServiceRateCard.objects.get(duration=duration)
    data = {'success': 'true', 'amount': str(service_obj.cost)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_premium_subscription_amount(request):
    print "--------------------------------", request.POST
    duration = request.POST.get('duration')
    service_name = request.POST.get('service_name')
    rate_card_obj = AdvertRateCard.objects.get(advert_service_name=service_name, duration=duration)
    data = {'success': 'true', 'amount': str(rate_card_obj.cost)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_subscription_plan(request):
    print "-----------------save---------------", request.POST
    try:
        supplier_id = request.session['supplier_id']
        category_id = request.POST.get('sub_category')

        duration = request.POST.get('duration_list')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        premium_service_list = request.POST.getlist('premium_service')
        premium_service_duration_list = request.POST.getlist('premium_ser_duration')
        premium_start_date_list = request.POST.getlist('premium_start_date')
        premium_end_date_list = request.POST.getlist('premium_end_date')
        premium_end_date_list = filter(None, premium_end_date_list)
        # print supplier_id,category_id,duration,start_date,end_date

        zip_premium = zip(premium_service_list, premium_service_duration_list, premium_start_date_list,
                          premium_end_date_list)

        if premium_service_list:
            check_premium_service = check_date(zip_premium, category_id)
            if check_premium_service['success'] == 'false':
                data = {'success': 'false', 'message': check_premium_service['msg']}
                return HttpResponse(json.dumps(data), content_type='application/json')

        chars = string.digits
        pwdSize = 8
        password = ''.join(random.choice(chars) for _ in range(pwdSize))

        supplier_obj = Supplier.objects.get(supplier_id=supplier_id)
        category_obj = Category.objects.get(category_id=category_id)
        service_ratecard_obj = ServiceRateCard.objects.get(duration=duration, service_name='Basic Subscription Plan')

        business_obj = Business(
            category=category_obj,
            service_rate_card_id=service_ratecard_obj,
            duration=duration,
            start_date=start_date,
            end_date=end_date,
            supplier=supplier_obj,
            transaction_code="TID" + str(password),
            is_active=0,
            business_created_date=datetime.now(),
            business_created_by=supplier_obj.contact_email
        )
        business_obj.save()

        transaction_code = "TID" + str(password)
        if premium_service_list:
            for premium_service, premium_service_duration, premium_start_date, premium_end_date in zip_premium:
                premium_service_obj = PremiumService(
                    premium_service_name=premium_service,
                    no_of_days=premium_service_duration,
                    category_id=category_obj,
                    start_date=premium_start_date,
                    end_date=premium_end_date,
                    business_id=business_obj,
                    premium_service_status="1",
                    premium_service_created_date=datetime.now(),
                    premium_service_created_by=supplier_obj.contact_email
                )
                premium_service_obj.save()
        data = {'success': 'true',
                'message': 'The subscription is created successfully with transaction ID :' + transaction_code + '. Please proceed with the payment .',
                'business_id': str(business_obj)
                }
    except Exception as e:
        print e
        data = {'success': 'false', 'message': e}
    return HttpResponse(json.dumps(data), content_type='application/json')


def check_date(zip_premium, category_id):
    flag_1, flag_2, flag_3, flag_4, flag_5 = 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'
    service_list = ''
    for premium_service, premium_service_duration, premium_start_date, premium_end_date in zip_premium:
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
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
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
        data = {'success': 'false', 'msg': msg}
    else:
        data = {'success': 'true', 'msg': ''}
    return data


@csrf_exempt
def save_payment_details(request):
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

        business_obj = Business.objects.get(business_id=business_id)
        tax_obj = Tax.objects.get(tax_rate=tax_type)
        payment_obj = PaymentDetail(
            payment_code=payment_code,
            payment_mode=payment_mode,
            payable_amount=total_payable_amount,
            total_amount=payment_amount,
            note=payment_note,
            tax_type=tax_obj,
            business_id=business_obj
        )
        payment_obj.save()

        if total_paid_amount:
            payment_obj.paid_amount = total_paid_amount
        if payment_mode == 'cheque':
            payment_obj.bank_name = bank_name
            payment_obj.branch_name = bank_branch_name
            payment_obj.cheque_number = cheque_number

        payment_obj.save()

        data = {'success': 'true', 'message': 'Payment done successfully with Payment ID - ' + payment_code}
    except Exception as e:
        print e
        data = {'success': 'true', 'message': e}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_state(request):
    country_id = request.GET.get('country_id')
    state_list = []
    try:
        state = State.objects.filter(state_status='1', country_id=country_id)
        currency = Currency.objects.get(country_id=country_id)
        for sta in state:
            options_data = '<option value=' + str(
                sta.state_id) + '>' + sta.state_name + '</option>'
            state_list.append(options_data)
            print state_list
        data = {'state_list': state_list, 'currency': currency.currency}
    except Exception, e:
        print 'Exception ', e
        data = {'state_list': 'No states available'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_advert(request):
    ##    pdb.set_trace()
    print "IN SAVE ADVERT METHOD", request.POST
    try:
        if request.method == "POST":
            print '===request========', request.POST.get('advert_keywords')
            advert_obj = Advert(
                supplier_id=Supplier.objects.get(supplier_id=request.session['supplier_id']),
                category_id=Category.objects.get(category_id=request.POST.get('categ')),
                advert_name=request.POST.get('advert_title'),
                contact_name=request.POST.get('contact_name'),
                contact_no=request.POST.get('phone_no'),
                website=request.POST.get('website'),
                latitude=request.POST.get('lat'),
                longitude=request.POST.get('lng'),
                short_description=request.POST.get('short_discription'),
                product_description=request.POST.get('product_discription'),
                currency=request.POST.get('currency'),
                country_id=Country.objects.get(country_id=request.POST.get('country')) if request.POST.get(
                    'country') else None,
                # product_price=request.POST.get('product_price'),
                discount_description=request.POST.get('discount_discription'),
                email_primary=request.POST.get('email_primary'),
                email_secondary=request.POST.get('email_secondary'),
                address_line_1=request.POST.get('address_line1'),
                address_line_2=request.POST.get('address_line2'),
                area=request.POST.get('area'),
                landmark=request.POST.get('landmark'),
                state_id=State.objects.get(state_id=request.POST.get('statec')) if request.POST.get('statec') else None,
                city_place_id=City_Place.objects.get(city_place_id=request.POST.get('city')) if request.POST.get(
                    'city') else None,
                pincode_id=Pincode.objects.get(pincode=request.POST.get('pincode')) if request.POST.get(
                    'pincode') else None,
                property_market_rate=request.POST.get('pro_mark_rate'),
                possesion_status=request.POST.get('possesion_status'),
                date_of_delivery=request.POST.get('date_of_delivery'),
                other_projects=request.POST.get('other_projects'),
                distance_frm_railway_station=request.POST.get('dis_rail_stat'),
                distance_frm_railway_airport=request.POST.get('dis_airport'),
                speciality=request.POST.get('speciality'),
                affilated_to=request.POST.get('affilated'),
                course_duration=request.POST.get('course_duration'),
                happy_hour_offer=request.POST.get('happy_hour_offer'),
                facility=request.POST.get('facility'),
                keywords=request.POST.get('advert_keywords'),
                image_video_space_used=request.POST.get('image_and_video_space')
            );
            advert_obj.save()
            if request.POST.get('any_other_details'):
                advert_obj.any_other_details = request.POST.get('any_other_details')
                advert_obj.save()
            if request.POST.get('subscription_id'):
                map_subscription(request.POST.get('subscription_id'), advert_obj)

            subcat_list = request.POST.get('subcat_list')
            print subcat_list
            subcat_lvl = 1
            # String to list
            if subcat_list != '':
                sc_list = subcat_list.split(',')
                for subcat in sc_list[0:5]:
                    if subcat:
                        print 'Subcat: ', subcat, subcat_lvl
                        if subcat_lvl == 1:
                            advert_obj.category_level_1 = CategoryLevel1.objects.get(category_id=subcat)
                            advert_obj.save()
                        if subcat_lvl == 2:
                            advert_obj.category_level_2 = CategoryLevel2.objects.get(category_id=subcat)
                            advert_obj.save()
                        if subcat_lvl == 3:
                            advert_obj.category_level_3 = CategoryLevel3.objects.get(category_id=subcat)
                            advert_obj.save()
                        if subcat_lvl == 4:
                            advert_obj.category_level_4 = CategoryLevel4.objects.get(category_id=subcat)
                            advert_obj.save()
                        if subcat_lvl == 5:
                            advert_obj.category_level_5 = CategoryLevel5.objects.get(category_id=subcat)
                            advert_obj.save()
                        print 'Advert Subcat Mapping saved'
                        subcat_lvl += 1
            if request.POST['check_image'] == "1":
                advert_obj.display_image = request.FILES['display_image']
                advert_obj.save()

            attachment_list = []
            attachment_list = request.POST.get('attachments')
            save_attachments(attachment_list, advert_obj)

            video_list = []
            video_list = request.POST.get('ac_attachment')
            save_video(video_list, advert_obj)

            # phone_category_list = request.POST.get('phone_category_list')
            # phone_category_list = phone_category_list.split(',')
            # phone_number_list = request.POST.get('phone_number_list')
            # phone_number_list = phone_number_list.split(',')
            # zipped = zip(phone_category_list, phone_number_list)
            # save_phone_number(zipped, advert_obj)

            product_name_list = request.POST.get('product_name_list')
            product_name_list = product_name_list.split(',')
            product_price_list = request.POST.get('product_price_list')
            product_price_list = product_price_list.split(',')
            zipped_product = zip(product_name_list, product_price_list)
            save_product(zipped_product, advert_obj)

            opening_day_list = request.POST.get('opening_day_list')
            opening_day_list = opening_day_list.split(',')

            start_time_list = request.POST.get('start_time_list')
            start_time_list = start_time_list.split(',')

            end_time_list = request.POST.get('end_time_list')
            end_time_list = end_time_list.split(',')

            zipped_wk = zip(opening_day_list, start_time_list, end_time_list)
            save_working_hours(zipped_wk, advert_obj)

            amenity_list = request.POST.get('amenity_list')
            amenity_list = amenity_list.split(',')
            save_amenity(amenity_list, advert_obj)

            exe_amenity_list = request.POST.get('additional_amenity')
            exe_amenity_list = exe_amenity_list.split(',')
            save_exe_amenity(exe_amenity_list, advert_obj)

            near_attr_list = request.POST.get('near_attraction')
            near_attr_list = near_attr_list.split(',')
            save_near_attr(near_attr_list, advert_obj)

            near_shopnmal = request.POST.get('near_shopnmal')
            near_shopnmal = near_shopnmal.split(',')

            near_shonmald = request.POST.get('near_shonmald')
            near_shonmald = near_shonmald.split(',')

            zipped_shopmal = zip(near_shopnmal, near_shonmald)
            save_shpnmal(zipped_shopmal, advert_obj)

            cat = advert_obj.category_id.category_name
            if cat == 'Real Estate':
                print "SCHOOL", request.POST.get('near_schol')
                near_schol = request.POST.get('near_schol')
                near_schol = near_schol.split(',')

                print "SCHOOL DI SORTING", request.POST.get('near_schold')
                near_schold = request.POST.get('near_schold')
                near_schold = near_schold.split(',')

                print "AFTER SCHOOL"

                zipped_school = zip(near_schol, near_schold)
                save_school(zipped_school, advert_obj)

                near_hosp = request.POST.get('near_hosp')
                near_hosp = near_hosp.split(',')

                near_hospd = request.POST.get('near_hospd')
                near_hospd = near_hospd.split(',')

                zipped_hospital = zip(near_hosp, near_hospd)
                save_hospital(zipped_hospital, advert_obj)
            # advert_add_sms(advert_obj)
            # advert_add_mail(advert_obj)
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def map_subscription(subscription_id, advert_obj):
    business_obj = Business.objects.get(business_id=str(subscription_id))
    business_obj.is_active = 1
    business_obj.save()
    sub_obj = AdvertSubscriptionMap(
        business_id=Business.objects.get(business_id=str(subscription_id)),
        advert_id=advert_obj
    )
    sub_obj.save()


def save_attachments(attachment_list, advert_id):
    try:
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        print attachment_list
        for attached_id in attachment_list:
            attachment_obj = AdvertImage.objects.get(advert_image_id=attached_id)
            attachment_obj.advert_id = advert_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_video(video_list, advert_id):
    try:
        video_list = video_list.split(',')
        video_list = filter(None, video_list)
        print video_list
        for attached_id in video_list:
            attachment_obj = Advert_Video.objects.get(advert_video_id=attached_id)
            attachment_obj.advert_id = advert_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_phone_number(zipped, advert_id):
    ##    pdb.set_trace()
    print "IN SAVE PHONE NUMBER"
    try:
        for phone_no_id, phone_no in zipped:
            if phone_no_id != '' and phone_no != '':
                print 'Phone number ID: ', phone_no_id
                phoneno_obj = PhoneNo(
                    advert_id=advert_id,
                    phone_category_id=PhoneCategory.objects.get(phone_category_id=phone_no_id),
                    phone_no=phone_no
                )
                phoneno_obj.save()
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_product(zipped_product, advert_id):
    ##    pdb.set_trace()
    print "IN SAVE PRODUCT"
    try:
        for product_name, product_price in zipped_product:
            if product_name != '' and product_price != '':
                product_obj = Product(
                    advert_id=advert_id,
                    product_name=product_name,
                    product_price=product_price
                )
                product_obj.save()
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_working_hours(zipped_wk, advert_id):
    ##    pdb.set_trace()
    print "IN SAVE WORKING HOURS"
    try:
        for wk_day, strt_tm, end_tm in zipped_wk:
            if wk_day != '' and strt_tm != '' and end_tm != '':
                wk_obj = WorkingHours(
                    advert_id=advert_id,
                    day=wk_day,
                    start_time=strt_tm,
                    end_time=end_tm
                )
                wk_obj.save()
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_amenity(amenity_list, advert_id):
    ##    pdb.set_trace()
    print "IN SAVE AMENITY"
    try:
        print "Advert Id", advert_id
        for amenity in amenity_list:
            if amenity == 'car':
                ame = 'Car Parking'
            elif amenity == 'club':
                ame = "Club House"
            elif amenity == 'swim':
                ame = "Swimming Pool"
            elif amenity == 'power':
                ame = "24 Hours Power Backup"
            elif amenity == 'gym':
                ame = "Gymanasium"

            elif amenity == 'kids':
                ame = "Kids Play Area"
            elif amenity == 'rain_water':
                ame = "Rain Water Harvesting"
            else:
                ame = "Garden"
            ame_obj = Amenities(
                advert_id=advert_id,
                amenity=ame
            )
            ame_obj.save()
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_exe_amenity(exe_amenity_list, advert_id):
    ##    pdb.set_trace()
    print "IN SAVE EXTRA AMENITY"
    try:
        for exe_am in exe_amenity_list:
            if exe_am != '':
                ame_obj = AdditionalAmenities(
                    advert_id=advert_id,
                    extra_amenity=exe_am
                )
                ame_obj.save()
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_near_attr(near_attr_list, advert_id):
    ##    pdb.set_trace()
    print "IN SAVE NEAR ATTRACTION"
    try:
        for ner_attr in near_attr_list:
            if ner_attr != '':
                ner_attr_obj = NearByAttraction(
                    advert_id=advert_id,
                    attraction=ner_attr
                )
                ner_attr_obj.save()
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_shpnmal(zipped_shopmal, advert_id):
    ##    pdb.set_trace()
    print "IN SAVE SHOP N MAL"
    try:
        for shpnml, shpnmld in zipped_shopmal:
            if shpnml != '' and shpnmld != '':
                shopnmal_obj = NearestShopping(
                    advert_id=advert_id,
                    shop_name=shpnml,
                    distance_frm_property=shpnmld
                )
                shopnmal_obj.save()
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_school(zipped_school, advert_id):
    ##    pdb.set_trace()
    print "IN SAVE SCHOOL"
    try:
        for school, schoold in zipped_school:
            if school != '' and schoold != '':
                school_obj = NearestSchool(
                    advert_id=advert_id,
                    school_name=school,
                    distance_frm_property=schoold
                )
                school_obj.save()
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_hospital(zipped_hospital, advert_id):
    ##    pdb.set_trace()
    print "IN SAVE HOSPITAL"
    try:
        for hospital, hospitald in zipped_hospital:
            if hospital != '' and hospitald != '':
                hospital_obj = NearestHospital(
                    advert_id=advert_id,
                    hospital_name=hospital,
                    distance_frm_property=hospitald
                )
                hospital_obj.save()
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')

#edit_subscription

def edit_subscription(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        business_id = request.GET.get('business_id')
        tax_list = Tax.objects.all()

        business_obj = Business.objects.get(business_id=business_id)

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


        data = {'tax_list': tax_list, 'advert_service_list': advert_services_list, 'service_list': service_list,
                'username': request.session['login_user'], 'category_list': get_category(request), 'business_data': business_data,
                'premium_service_list': premium_service_list,
                'total_amount': float(total_amount), 'basic_amount': basic_amount, 'amount_1': amount_1,
                'amount_2': amount_2, 'amount_3': amount_3, 'amount_4': amount_4, 'amount_5': amount_5,
                'payment_details': payment_details,
                }
        return render(request, 'Subscriber/edit_subscription.html', data)

def edit_advert(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        advert_id = request.GET.get('advert_id')
        tax_list = Tax.objects.all()

        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
        business_obj = Business.objects.get(business_id=str(advert_sub_obj.business_id))

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

        advert_obj = Advert.objects.get(advert_id=advert_id)

        if advert_obj.category_level_1:
            category_l1_list = CategoryLevel1.objects.filter(parent_category_id=str(advert_obj.category_id.category_id))
        else:
            category_l1_list = []

        if advert_obj.category_level_2:
            category_l2_list = CategoryLevel2.objects.filter(
                parent_category_id=str(advert_obj.category_level_1.category_id))
        else:
            category_l2_list = []

        if advert_obj.category_level_3:
            category_l3_list = CategoryLevel3.objects.filter(
                parent_category_id=str(advert_obj.category_level_2.category_id))
        else:
            category_l3_list = []

        if advert_obj.category_level_4:
            category_l4_list = CategoryLevel4.objects.filter(
                parent_category_id=str(advert_obj.category_level_3.category_id))
        else:
            category_l4_list = []

        if advert_obj.category_level_5:
            category_l5_list = CategoryLevel5.objects.filter(
                parent_category_id=str(advert_obj.category_level_4.category_id))
        else:
            category_l5_list = []

        advert_data = {
            'category_id': advert_obj.category_id.category_id,
            'category_level_1': advert_obj.category_level_1.category_id if advert_obj.category_level_1 else '',
            'category_level_2': advert_obj.category_level_2.category_id if advert_obj.category_level_2 else '',
            'category_level_3': advert_obj.category_level_3.category_id if advert_obj.category_level_3 else '',
            'category_level_4': advert_obj.category_level_4.category_id if advert_obj.category_level_4 else '',
            'category_level_5': advert_obj.category_level_5.category_id if advert_obj.category_level_5 else '',
            'advert_name': advert_obj.advert_name,
            'contact_name': advert_obj.contact_name,
            'contact_no': advert_obj.contact_no,
            'latitude': advert_obj.latitude,
            'longitude': advert_obj.longitude,
            'short_description': advert_obj.short_description,
            'product_description': advert_obj.product_description,
            'discount_description': advert_obj.discount_description,
            'currency': advert_obj.currency,
            'display_image': SERVER_URL + advert_obj.display_image.url if advert_obj.display_image else '',
            'address_line_1': advert_obj.address_line_1,
            'address_line_2': advert_obj.address_line_2,
            'country_id': advert_obj.country_id.country_id,
            'currency': advert_obj.currency,
            'state_id': advert_obj.state_id.state_id,
            'city_place_id': advert_obj.city_place_id.city_place_id,
            'pincode_id': advert_obj.pincode_id.pincode_id,
            'area': advert_obj.area,
            'landmark': advert_obj.landmark,
            'email_primary': advert_obj.email_primary,
            'property_market_rate': advert_obj.property_market_rate,
            'possesion_status': advert_obj.possesion_status,
            'other_projects': advert_obj.other_projects,
            'date_of_delivery': advert_obj.date_of_delivery,
            'any_other_details': advert_obj.any_other_details,
            'speciality': advert_obj.speciality,
            'happy_hour_offer': advert_obj.happy_hour_offer,
            'course_duration': advert_obj.course_duration,
            'affilated_to': advert_obj.affilated_to,
            'image_video_space_used': advert_obj.image_video_space_used,
            'facility': advert_obj.facility,
            'keywords': advert_obj.keywords,
            'distance_frm_railway_station': advert_obj.distance_frm_railway_station,
            'distance_frm_airport': advert_obj.distance_frm_railway_airport,
        }

        product_obj = Product.objects.filter(advert_id=advert_id)
        product_list = []
        if product_obj:
            for products in product_obj:
                product_data = {
                    "product_name": products.product_name,
                    "product_price": products.product_price
                }
                product_list.append(product_data)

        time_list = []
        time_obj = WorkingHours.objects.filter(advert_id=advert_id)
        if time_obj:
            for time in time_obj:
                time_data = {
                    "day": time.day,
                    "start_time": time.start_time,
                    "end_time": time.end_time,
                }
                time_list.append(time_data)

        amenities_obj = Amenities.objects.filter(advert_id=advert_id)
        amenities_list = []
        if amenities_obj:
            for amenities in amenities_obj:
                amenities_data = {
                    "amenity": amenities.amenity
                }
                amenities_list.append(amenities.amenity)

        add_amenities_obj = AdditionalAmenities.objects.filter(advert_id=advert_id)
        add_amenities_list = []
        if amenities_obj:
            for add_amenities in add_amenities_obj:
                add_amenities_data = {
                    "extra_amenity": add_amenities.extra_amenity
                }
                add_amenities_list.append(add_amenities_data)

        nr_attr_obj = NearByAttraction.objects.filter(advert_id=advert_id)
        nr_attr_list = []
        if nr_attr_obj:
            for nr_attr in nr_attr_obj:
                nr_attr_data = {
                    "attraction": nr_attr.attraction
                }
                nr_attr_list.append(nr_attr_data)

        nr_shop_obj = NearestShopping.objects.filter(advert_id=advert_id)
        nr_shop_list = []
        if nr_shop_obj:
            for nr_shop in nr_shop_obj:
                nr_shop_data = {
                    "shop_name": nr_shop.shop_name,
                    "distance_frm_property": nr_shop.distance_frm_property
                }
                nr_shop_list.append(nr_shop_data)

        nr_shcl_obj = NearestSchool.objects.filter(advert_id=advert_id)
        nr_shcl_list = []
        if nr_shcl_obj:
            for schools in nr_shcl_obj:
                schools_data = {
                    "school_name": schools.school_name,
                    "distance_frm_property": schools.distance_frm_property
                }
                nr_shcl_list.append(schools_data)

        nr_hosp_obj = NearestHospital.objects.filter(advert_id=advert_id)
        nr_hosp_list = []
        if nr_hosp_obj:
            for hospitals in nr_hosp_obj:
                hospital_data = {
                    "hospital_name": hospitals.hospital_name,
                    "distance_frm_property": hospitals.distance_frm_property
                }
                nr_hosp_list.append(hospital_data)

        data = {'tax_list': tax_list, 'advert_service_list': advert_services_list, 'service_list': service_list,
                'username': request.session['login_user'], 'category_list': get_category(request),
                'country_list': get_country(request), 'phone_category': get_phone_category(request),
                'state_list': get_states(request), 'business_data': business_data,
                'premium_service_list': premium_service_list, 'product_list': product_list, 'time_list': time_list,
                'total_amount': float(total_amount), 'basic_amount': basic_amount, 'amount_1': amount_1,
                'amount_2': amount_2, 'advert_data': advert_data, 'advert_id': advert_id,
                'amount_3': amount_3, 'amount_4': amount_4, 'amount_5': amount_5, 'payment_details': payment_details,
                'amenities_list': amenities_list, 'add_amenities_list': add_amenities_list,
                'nr_attr_list': nr_attr_list,
                'nr_shop_list': nr_shop_list, 'nr_shcl_list': nr_shcl_list, 'nr_hosp_list': nr_hosp_list,
                'category_l1_list': category_l1_list, 'category_l2_list': category_l2_list,
                'category_l3_list': category_l3_list,
                'category_l4_list': category_l4_list, 'category_l5_list': category_l5_list
                }
        return render(request, 'Subscriber/edit_advert.html', data)


def renew_subscription(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        advert_id = request.GET.get('advert_id')
        tax_list = Tax.objects.all()
        advert_obj = Advert.objects.get(advert_id = advert_id)
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
                'country_list': get_country(request), 'phone_category': get_phone_category(request),
                'state_list': get_states(request), 'business_data': business_data, 'advert_name' : advert_name
                }
        return render(request, 'Subscriber/renew_subscription.html', data)


@csrf_exempt
def update_subscription_plan(request):
    print "-----------------save---------------", request.POST
    try:
        supplier_id = request.session['supplier_id']
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
        zip_premium = zip(premium_service_list, premium_service_duration_list, premium_start_date_list,
                          premium_end_date_list)
        if premium_service_list:
            check_premium_service = update_check_date(zip_premium, category_id, business_id)
            if check_premium_service['success'] == 'false':
                data = {'success': 'false', 'message': check_premium_service['msg']}
                return HttpResponse(json.dumps(data), content_type='application/json')

        supplier_obj = Supplier.objects.get(supplier_id=supplier_id)
        category_obj = Category.objects.get(category_id=category_id)
        service_ratecard_obj = ServiceRateCard.objects.get(duration=duration, service_name='Basic Subscription Plan')

        business_obj = Business.objects.get(business_id=business_id)
        business_obj.category = category_obj
        business_obj.service_rate_card_id = service_ratecard_obj
        business_obj.duration = duration
        business_obj.start_date = start_date
        business_obj.end_date = end_date
        business_obj.supplier = supplier_obj
        business_obj.business_created_date = datetime.now()
        business_obj.business_created_by = supplier_obj.contact_email

        business_obj.save()
        #
        transaction_code = business_obj.transaction_code
        if premium_service_list:
            PremiumService.objects.filter(business_id=business_id).delete()
            for premium_service, premium_service_duration, premium_start_date, premium_end_date in zip_premium:
                print "premium_end_date", premium_service, premium_service_duration, premium_start_date, premium_end_date
                premium_service_obj = PremiumService(
                    premium_service_name=premium_service,
                    no_of_days=premium_service_duration,
                    category_id=category_obj,
                    start_date=premium_start_date,
                    end_date=premium_end_date,
                    business_id=business_obj,
                    premium_service_status="1",
                    premium_service_created_date=datetime.now(),
                    premium_service_created_by=supplier_obj.contact_email
                )
                premium_service_obj.save()
        else:
            PremiumService.objects.filter(business_id=business_id).delete()
        data = {'success': 'true',
                'message': 'The subscription is created successfully with transaction ID :' + transaction_code + '. Please proceed with the payment .',
                'business_id': str(business_obj)
                }
    except Exception as e:
        print e
        data = {'success': 'false', 'message': e}
    return HttpResponse(json.dumps(data), content_type='application/json')


def update_check_date(zip_premium, category_id, business_id):
    flag_1, flag_2, flag_3, flag_4, flag_5 = 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'
    service_list = ''
    for premium_service, premium_service_duration, premium_start_date, premium_end_date in zip_premium:
        if premium_service == 'No.1 Listing':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                Q(category_id=str(category_id)) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).exclude(business_id=business_id).count()
            if premium_service_obj >= 1:
                flag_1 = 'No'
        if premium_service == 'No.2 Listing':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                Q(category_id=str(category_id)) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).exclude(business_id=business_id).count()

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
            ).exclude(business_id=business_id).count()
            if premium_service_obj >= 1:
                flag_3 = 'No'
        if premium_service == 'Advert Slider':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).exclude(business_id=business_id).count()
            if premium_service_obj > 10:
                flag_4 = 'No'
        if premium_service == 'Top Advert':
            premium_service_obj = PremiumService.objects.filter(
                Q(premium_service_name=premium_service) &
                # Q(start_date__range=(premium_start_date, premium_end_date)) |
                # Q(end_date__range=(premium_start_date, premium_end_date)) |
                Q(start_date__lte=premium_start_date, end_date__gte=premium_end_date) &
                Q(premium_service_status='1')
            ).exclude(business_id=business_id).count()
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
        data = {'success': 'false', 'msg': msg}
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

        business_obj = Business.objects.get(business_id=business_id)
        tax_obj = Tax.objects.get(tax_rate=tax_type)
        try:
            payment_obj = PaymentDetail.objects.get(business_id=business_id)
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

        data = {'success': 'true', 'message': 'Payment done successfully with Payment ID - ' + payment_obj.payment_code}
    except Exception as e:
        print e
        data = {'success': 'true', 'message': e}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_advert(request):
    ##    pdb.set_trace()
    print "IN SAVE ADVERT METHOD",  # request.POST
    try:
        if request.method == "POST":
            print '===request========', request.POST.get('pincode')
            advert_id = request.POST.get('advert_id')
            advert_obj = Advert.objects.get(advert_id=request.POST.get('advert_id'))

            advert_obj.supplier_id = Supplier.objects.get(supplier_id=request.session['supplier_id'])
            advert_obj.category_id = Category.objects.get(category_id=request.POST.get('categ'))
            advert_obj.advert_name = request.POST.get('advert_title')
            advert_obj.contact_name = request.POST.get('contact_name')
            advert_obj.contact_no = request.POST.get('phone_no')
            advert_obj.website = request.POST.get('website')
            advert_obj.latitude = request.POST.get('lat')
            advert_obj.longitude = request.POST.get('lng')
            advert_obj.short_description = request.POST.get('short_discription')
            advert_obj.product_description = request.POST.get('product_discription')
            advert_obj.currency = request.POST.get('currency')
            advert_obj.country_id = Country.objects.get(country_id=request.POST.get('country')) if request.POST.get(
                'country') else None
            # product_price=request.POST.get('product_price'),
            advert_obj.discount_description = request.POST.get('discount_discription')
            advert_obj.email_primary = request.POST.get('email_primary')
            advert_obj.email_secondary = request.POST.get('email_secondary')
            advert_obj.address_line_1 = request.POST.get('address_line1')
            advert_obj.address_line_2 = request.POST.get('address_line2')
            advert_obj.area = request.POST.get('area')
            advert_obj.landmark = request.POST.get('landmark')
            advert_obj.state_id = State.objects.get(state_id=request.POST.get('statec')) if request.POST.get(
                'statec') else None
            advert_obj.city_place_id = City_Place.objects.get(
                city_place_id=request.POST.get('city')) if request.POST.get(
                'city') else None
            advert_obj.pincode_id = Pincode.objects.get(pincode_id=request.POST.get('pincode')) if request.POST.get(
                'pincode') else None
            advert_obj.property_market_rate = request.POST.get('pro_mark_rate')
            advert_obj.possesion_status = request.POST.get('possesion_status')
            advert_obj.date_of_delivery = request.POST.get('date_of_delivery')
            advert_obj.other_projects = request.POST.get('other_projects')
            advert_obj.distance_frm_railway_station = request.POST.get('dis_rail_stat')
            advert_obj.distance_frm_railway_airport = request.POST.get('dis_airport')
            advert_obj.speciality = request.POST.get('speciality')
            advert_obj.affilated_to = request.POST.get('affilated')
            advert_obj.course_duration = request.POST.get('course_duration')
            advert_obj.happy_hour_offer = request.POST.get('happy_hour_offer')
            advert_obj.facility = request.POST.get('facility')
            advert_obj.keywords = request.POST.get('advert_keywords')
            advert_obj.image_video_space_used = request.POST.get('image_and_video_space')
            advert_obj.save()
            print "advert updated"

            if request.POST.get('any_other_details'):
                advert_obj.any_other_details = request.POST.get('any_other_details')
                advert_obj.save()

            print "advert updated"

            subcat_list = request.POST.get('subcat_list')
            print subcat_list
            subcat_lvl = 1
            # String to list
            if subcat_list != '':
                sc_list = subcat_list.split(',')
                for subcat in sc_list[0:5]:
                    if subcat:
                        print 'Subcat: ', subcat, subcat_lvl
                        if subcat_lvl == 1:
                            advert_obj.category_level_1 = CategoryLevel1.objects.get(category_id=subcat)
                            advert_obj.save()
                        if subcat_lvl == 2:
                            advert_obj.category_level_2 = CategoryLevel2.objects.get(category_id=subcat)
                            advert_obj.save()
                        if subcat_lvl == 3:
                            advert_obj.category_level_3 = CategoryLevel3.objects.get(category_id=subcat)
                            advert_obj.save()
                        if subcat_lvl == 4:
                            advert_obj.category_level_4 = CategoryLevel4.objects.get(category_id=subcat)
                            advert_obj.save()
                        if subcat_lvl == 5:
                            advert_obj.category_level_5 = CategoryLevel5.objects.get(category_id=subcat)
                            advert_obj.save()
                        print 'Advert Subcat Mapping saved'
                        subcat_lvl += 1
            if request.POST['check_image'] == "1":
                advert_obj.display_image = request.FILES['display_image']
                advert_obj.save()

            attachment_list = []
            attachment_list = request.POST.get('attachments')
            save_attachments(attachment_list, advert_obj)

            video_list = []
            video_list = request.POST.get('ac_attachment')
            save_video(video_list, advert_obj)

            print "advert uodated"

            # phone_category_list = request.POST.get('phone_category_list')
            # phone_category_list = phone_category_list.split(',')
            # phone_number_list = request.POST.get('phone_number_list')
            # phone_number_list = phone_number_list.split(',')
            # zipped = zip(phone_category_list, phone_number_list)
            # save_phone_number(zipped, advert_obj)

            if request.POST.get('product_name_list'):
                Product.objects.filter(advert_id=advert_id).delete()
            if request.POST.get('opening_day_list'):
                WorkingHours.objects.filter(advert_id=advert_id).delete()
            if request.POST.get('amenity_list'):
                Amenities.objects.filter(advert_id=advert_id).delete()
            if request.POST.get('additional_amenity'):
                AdditionalAmenities.objects.filter(advert_id=advert_id).delete()
            if request.POST.get('near_attraction'):
                NearByAttraction.objects.filter(advert_id=advert_id).delete()
            if request.POST.get('near_shopnmal'):
                NearestShopping.objects.filter(advert_id=advert_id).delete()

            product_name_list = request.POST.get('product_name_list')
            product_name_list = product_name_list.split(',')
            product_price_list = request.POST.get('product_price_list')
            product_price_list = product_price_list.split(',')
            zipped_product = zip(product_name_list, product_price_list)
            save_product(zipped_product, advert_obj)

            opening_day_list = request.POST.get('opening_day_list')
            opening_day_list = opening_day_list.split(',')

            start_time_list = request.POST.get('start_time_list')
            start_time_list = start_time_list.split(',')

            end_time_list = request.POST.get('end_time_list')
            end_time_list = end_time_list.split(',')

            zipped_wk = zip(opening_day_list, start_time_list, end_time_list)
            save_working_hours(zipped_wk, advert_obj)

            amenity_list = request.POST.get('amenity_list')
            amenity_list = amenity_list.split(',')
            save_amenity(amenity_list, advert_obj)

            exe_amenity_list = request.POST.get('additional_amenity')
            exe_amenity_list = exe_amenity_list.split(',')
            save_exe_amenity(exe_amenity_list, advert_obj)

            near_attr_list = request.POST.get('near_attraction')
            near_attr_list = near_attr_list.split(',')
            save_near_attr(near_attr_list, advert_obj)

            near_shopnmal = request.POST.get('near_shopnmal')
            near_shopnmal = near_shopnmal.split(',')

            near_shonmald = request.POST.get('near_shonmald')
            near_shonmald = near_shonmald.split(',')

            zipped_shopmal = zip(near_shopnmal, near_shonmald)
            save_shpnmal(zipped_shopmal, advert_obj)

            cat = advert_obj.category_id.category_name
            if cat == 'Real Estate':
                print "SCHOOL", request.POST.get('near_schol')
                if request.POST.get('near_schol'):
                    NearestSchool.objects.filter(advert_id=advert_id).delete()

                near_schol = request.POST.get('near_schol')
                near_schol = near_schol.split(',')

                print "SCHOOL DI SORTING", request.POST.get('near_schold')
                near_schold = request.POST.get('near_schold')
                near_schold = near_schold.split(',')

                print "AFTER SCHOOL"

                zipped_school = zip(near_schol, near_schold)
                save_school(zipped_school, advert_obj)

                if request.POST.get('near_hosp'):
                    NearestHospital.objects.filter(advert_id=advert_id).delete()

                near_hosp = request.POST.get('near_hosp')
                near_hosp = near_hosp.split(',')

                near_hospd = request.POST.get('near_hospd')
                near_hospd = near_hospd.split(',')

                zipped_hospital = zip(near_hosp, near_hospd)
                save_hospital(zipped_hospital, advert_obj)
            # advert_add_sms(advert_obj)
            # advert_add_mail(advert_obj)
            data = {'success': 'true'}

    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def uploaded_images(request):
    try:
        advert_id = request.GET.get('advert_id')
        image_list = []
        advert_image = AdvertImage.objects.filter(advert_id=advert_id)
        for images in advert_image:
            image_path = images.advert_image.url
            image_path = image_path.split('/')
            advert_image_data = {
                "image_path": SERVER_URL + images.advert_image.url,
                "image_size": "12345",
                "image_name": image_path[-1]
            }
            image_list.append(advert_image_data)
        data = {'image_list': image_list}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def uploaded_videos(request):
    try:
        advert_id = request.GET.get('advert_id')
        video_list = []
        advert_video = Advert_Video.objects.filter(advert_id=advert_id)
        for videos in advert_video:
            video_path = videos.advert_video_name.url
            video_path = video_path.split('/')
            advert_video_data = {
                "video_path": SERVER_URL + videos.advert_video_name.url,
                "video_size": "12345",
                "video_name": video_path[-1]
            }
            video_list.append(advert_video_data)
        data = {'video_list': video_list}
    except Exception, e:
        print 'Exception :', e
        data = {'data': 'none'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# -------------------------------------------------------------------------------------------#

def login_open(request):
    form = CaptchaForm()
    return render_to_response('Subscriber/user_login.html', dict(
        form=form
    ), context_instance=RequestContext(request))


@csrf_exempt
def signin(request):
    data = {}
    try:
        if request.POST:
            form = CaptchaForm(request.POST)
            print 'logs: login request with: ', request.POST
            username = request.POST['username']
            password = request.POST['password']

            if form.is_valid():
                try:
                    user_obj = Supplier.objects.get(username=username)

                    user = authenticate(username=username, password=password)
                    print 'valid form befor----->'
                    if user:
                        if user.is_active:
                            print 'valid form after----->', user
                            user_Supplier_obj = Supplier.objects.get(username=username)
                            if user_Supplier_obj.supplier_status == "1":
                                print "-----------------active----------------------"
                                request.session['login_user'] = user_Supplier_obj.username
                                request.session['first_name'] = user_Supplier_obj.contact_person
                                request.session['supplier_id'] = user_Supplier_obj.supplier_id
                                if user_Supplier_obj.logo:
                                    request.session['user_image'] = SERVER_URL + user_Supplier_obj.logo.url
                                else:
                                    request.session['user_image'] = ''
                                login(request, user)
                                print "USERNAME", request.session['login_user']
                                data = {'success': 'true', 'username': request.session['first_name'],
                                        'supplier_id': user_Supplier_obj.supplier_id}

                        else:
                            data = {'success': 'false', 'message': 'User Is Not Active'}
                            return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        data = {'success': 'Invalid Password', 'message': 'Invalid Password'}
                        print "====USERNAME", data
                        return HttpResponse(json.dumps(data), content_type='application/json')
                except Exception as e:
                    print e
                    data = {'success': 'false', 'message': 'Invalid Username'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                form = CaptchaForm()
                data = {'success': 'Invalid Captcha', 'message': 'Invalid Captcha'}
                print "INVALID CAPTCHA"
                return HttpResponse(json.dumps(data), content_type='application/json')
    except MySQLdb.OperationalError, e:
        print e
        data = {'success': 'false', 'message': 'Internal server'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false', 'message': 'Invalid Username or Password'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_city(request):
    state_id = request.GET.get('state_id')
    city_list = []
    try:
        city_objs = City_Place.objects.filter(state_id=state_id, city_status='1')  # .order_by('city_name')
        for city in city_objs:
            options_data = '<option value="' + str(
                city.city_place_id) + '">' + str(city.city_id) + '</option>'
            city_list.append(options_data)
            print city_list
        data = {'city_list': city_list}

    except Exception, ke:
        print ke
        data = {'city_list': 'none', 'message': 'No city available'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def subscriber_profile(request):
    try:
        data = {}
        final_list = []
        final_list1 = []
        try:
            supplier_id = request.GET.get('supplier_id')
            # print '=======request======first===', supplier_id
            Supplier_obj = Supplier.objects.get(supplier_id=request.GET.get('supplier_id'))
            # print "..................Supplier_obj.........", Supplier_obj

            advert_list = Advert.objects.filter(supplier_id=request.GET.get('supplier_id'))
            # print "..................advert_list.........", advert_list
            for advert_obj in advert_list:
                advert_id = advert_obj.advert_id
                advert_name = advert_obj.advert_name
                address_line_1 = advert_obj.address_line_1
                area = advert_obj.area
                category_name = advert_obj.category_id.category_name
                if advert_obj.display_image:
                    display_image = SERVER_URL + advert_obj.display_image.url
                else:
                    display_image = ''
                # display_image = SERVER_URL + advert_obj.display_image.url
                count_total = CouponCode.objects.filter(advert_id=advert_id).count()

                pre_date = datetime.now().strftime("%Y-%m-%d")
                # print '..............pre_date......pre_date........', pre_date
                pre_date = datetime.strptime(pre_date, "%Y-%m-%d")
                # print '..............pre_date...222...pre_date........', pre_date
                advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)

                start_date = advert_sub_obj.business_id.start_date

                end_date = advert_sub_obj.business_id.end_date
                end_date = datetime.strptime(end_date, "%m/%d/%Y")

                date_gap = (end_date - pre_date).days

                if date_gap > 0:
                    date_gap = date_gap
                else:
                    date_gap = 0

                business_id = advert_sub_obj.business_id
                print business_id
                premium_ser_list = PremiumService.objects.filter(business_id=business_id)
                for obj in premium_ser_list:

                    start_date1 = obj.start_date
                    end_date1 = obj.end_date
                    end_date1 = datetime.strptime(end_date1, "%m/%d/%Y")
                    date_gap1 = (end_date1 - pre_date).days

                    if date_gap1 > 0:
                        date_gap1 = date_gap1
                    else:
                        date_gap1 = 0

                    list1 = {'start_date1': start_date1, 'date_gap1': date_gap1}
                    final_list1.append(list1)

                list = {'advert_id': advert_id, 'advert_name': advert_name, 'address_line_1': address_line_1,
                        'area': area, 'category_name': category_name, 'display_image': display_image,
                        'count_total': count_total, 'start_date': start_date, 'date_gap': date_gap}
                final_list.append(list)
            if Supplier_obj.logo:
                logo = SERVER_URL + Supplier_obj.logo.url
            else:
                logo = ''
            business_name = Supplier_obj.business_name

            business_details = Supplier_obj.business_details
            business_details_count = Supplier_obj.business_details
            business_details_length = len(business_details_count);
            phone_no = Supplier_obj.phone_no
            secondary_phone_no = Supplier_obj.secondary_phone_no
            supplier_email = Supplier_obj.supplier_email
            secondary_email = Supplier_obj.secondary_email
            address1 = Supplier_obj.address1
            address2 = Supplier_obj.address2
            country_id = Supplier_obj.country_id.country_id
            state_id = Supplier_obj.state.state_id
            print '...............country_nm...............', country_id
            city_id = Supplier_obj.city_place_id.city_place_id
            pincode_id = Supplier_obj.pincode.pincode_id

            city = Supplier_obj.city_place_id.city_id.city_name
            pincode = Supplier_obj.pincode
            contact_person = Supplier_obj.contact_person
            contact_no = Supplier_obj.contact_no
            contact_email = Supplier_obj.contact_email
            state_list = State.objects.filter(state_status='1').order_by('state_name')
            city_list = City_Place.objects.filter(city_status='1')  # .order_by('city_name')
            pincode_list = Pincode.objects.filter(pincode_status='1')
            country_list = Country.objects.filter(country_status='1').order_by('country_name')
            notification_status = Supplier_obj.notification_status
            reminders_status = Supplier_obj.reminders_status
            discounts_status = Supplier_obj.discounts_status
            request_call_back_status = Supplier_obj.request_call_back_status
            no_call_status = Supplier_obj.no_call_status

            data = {'country_list': country_list, 'country_id': country_id, 'state_id': state_id, 'city_id': city_id,
                    'pincode_id': pincode_id,
                    'business_details_length': business_details_length, 'pincode_list': pincode_list,
                    'city_list': city_list, 'state_list': state_list, 'address2': address2, 'pincode': pincode,
                    'notification_status': notification_status, 'reminders_status': reminders_status,
                    'discounts_status': discounts_status, 'request_call_back_status': request_call_back_status,
                    'no_call_status': no_call_status, 'supplier_id': supplier_id, 'final_list1': final_list1,
                    'final_list': final_list, 'success': 'true', 'logo': logo, 'business_name': business_name,
                    'city': city, 'business_details': business_details, 'phone_no': phone_no,
                    'secondary_phone_no': secondary_phone_no, 'supplier_email': supplier_email,
                    'secondary_email': secondary_email, 'address1': address1, 'contact_person': contact_person,
                    'contact_no': contact_no, 'contact_email': contact_email}

        except IntegrityError as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time',
                    'username': request.session['login_user']}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    print data
    return render(request, 'Subscriber/subscriber-profile.html', data)


@csrf_exempt
def subscriber_advert(request):
    try:
        data = {}

        advert_list = []
        category_list = []
        pre_date = datetime.now().strftime("%m/%d/%Y")
        pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
        # print "------------------------------", request.GET
        try:
            supplier_id = request.GET.get('supplier_id')
            start_date_var = request.GET.get('start_date_var')
            end_date_var = request.GET.get('end_date_var')
            category_var = request.GET.get('category_var')
            status_var = request.GET.get('status_var')

            if start_date_var and end_date_var and status_var and category_var:
                Advert_list1 = Advert.objects.filter(category_id=request.GET.get('category_var'),
                                                     supplier_id=request.GET.get('supplier_id'),
                                                     creation_date__range=[start_date_var, end_date_var],
                                                     status=request.GET.get('status_var'))

            elif start_date_var and end_date_var and category_var:
                Advert_list1 = Advert.objects.filter(category_id=request.GET.get('category_var'),
                                                     supplier_id=request.GET.get('supplier_id'),
                                                     creation_date__range=[start_date_var, end_date_var])

            elif start_date_var and end_date_var and status_var:
                Advert_list1 = Advert.objects.filter(supplier_id=request.GET.get('supplier_id'),
                                                     creation_date__range=[start_date_var, end_date_var],
                                                     status=request.GET.get('status_var'))

            elif status_var:
                Advert_list1 = Advert.objects.filter(
                    status=request.GET.get('status_var'))

            elif start_date_var and end_date_var:
                Advert_list1 = Advert.objects.filter(supplier_id=request.GET.get('supplier_id'),
                                                     creation_date__range=[start_date_var, end_date_var])

            elif category_var:
                Advert_list1 = Advert.objects.filter(supplier_id=request.GET.get('supplier_id'),
                                                     category_id=request.GET.get('category_var'))

            else:
                Advert_list1 = Advert.objects.filter(supplier_id=request.GET.get('supplier_id'))

            category_objs = Category.objects.all()
            for category_obj in category_objs:
                category_id = category_obj.category_id
                category_name = category_obj.category_name
                cat_data = {'category_name': category_name, 'category_id': category_id}
                category_list.append(cat_data)

            business_obj = Business.objects.filter(supplier_id=request.GET.get('supplier_id'))
            for business in business_obj:
                try:
                    advert_sub_obj = AdvertSubscriptionMap.objects.get(business_id=business.business_id)
                except:
                    print business
                    start_date = business.start_date
                    start_date = datetime.strptime(start_date, "%m/%d/%Y")
                    end_date = business.end_date
                    end_date = datetime.strptime(end_date, "%m/%d/%Y")

                    date_gap = (end_date - pre_date).days

                    if date_gap > 0:
                        date_gap = date_gap
                    else:
                        date_gap = 0

                    if date_gap <= 10 and date_gap >= 1:
                        advert_status = 1
                        subscription_days = "( " + str(date_gap) + " days Remaining )"
                        subscription_text = "Starts on " + start_date.strftime("%d %b %y")
                        subscriber_color = "orange"
                        advert_color = "orange"
                    elif date_gap == 0:
                        advert_status = 0
                        subscription_days = ""
                        subscription_text = "Expired on " + start_date.strftime("%d %b %y")
                        subscriber_color = "red"
                        advert_color = "red"
                    else:
                        advert_status = 2
                        subscription_days = "( " + str(date_gap) + " days Remaining )"
                        subscription_text = "Starts on " + start_date.strftime("%d %b %y")
                        subscriber_color = "#333"
                        advert_color = "green"

                    premium_serv_list = premium_list(business.business_id)

                    advert_data = {
                        'advert_id': '',
                        'business_id': business.business_id,
                        'advert_status': advert_status,
                        'advert_name': 'No Advert is added for this subscription.',
                        'advert_area': '',
                        'advert_city': '',
                        'category_name': '',
                        'display_image': SERVER_URL + '/static/assets/layouts/layout2/img/City_Hoopla_Logo.jpg',
                        'advert_views': '',
                        'advert_likes': '',
                        'advert_shares': '',
                        'subscription_days': subscription_days,
                        'subscription_text': subscription_text,
                        'subscriber_color': subscriber_color,
                        'premium_service_list': premium_serv_list,
                        'advert_bookings': '',
                        'advert_color': advert_color,
                    }
                    advert_list.append(advert_data)

            for advert_obj in Advert_list1:
                premium_service_list = []
                advert_id = advert_obj.advert_id

                advert_views = AdvertView.objects.filter(advert_id=advert_id).count()
                advert_likes = AdvertLike.objects.filter(advert_id=advert_id).count()
                advert_shares = AdvertShares.objects.filter(advert_id=advert_id).count()
                advert_bookings = CouponCode.objects.filter(advert_id=advert_id).count()

                advert_name = advert_obj.advert_name
                advert_area = advert_obj.area
                advert_city = advert_obj.city_place_id.city_id.city_name
                category_name = advert_obj.category_id.category_name

                if advert_obj.display_image:
                    display_image = SERVER_URL + advert_obj.display_image.url
                else:
                    display_image = SERVER_URL + '/static/assets/layouts/layout2/img/City_Hoopla_Logo.jpg'

                advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)

                start_date = advert_sub_obj.business_id.start_date
                start_date = datetime.strptime(start_date, "%m/%d/%Y")
                end_date = advert_sub_obj.business_id.end_date
                end_date = datetime.strptime(end_date, "%m/%d/%Y")

                date_gap = (end_date - pre_date).days

                if date_gap > 0:
                    date_gap = date_gap
                else:
                    date_gap = 0

                if date_gap <= 10 and date_gap >= 1:
                    advert_status = 1
                    subscription_days = "( "+ str(date_gap) +" days Remaining )"
                    subscription_text = "Starts on " + start_date.strftime("%d %b %y")
                    subscriber_color = "orange"
                    advert_color = "orange"
                elif date_gap == 0:
                    advert_status = 0
                    subscription_days = ""
                    subscription_text = "Expired on " + start_date.strftime("%d %b %y")
                    subscriber_color = "red"
                    advert_color = "red"
                else:
                    advert_status = 2
                    subscription_days = "( " + str(date_gap) + " days Remaining )"
                    subscription_text = "Starts on " + start_date.strftime("%d %b %y")
                    subscriber_color = "#333"
                    advert_color = "green"

                business_id = advert_sub_obj.business_id
                premium_service_list = premium_list(business_id)
                advert_data = {
                    'advert_id': advert_id,
                    'advert_status': advert_status,
                    'advert_name': advert_name,
                    'advert_area': advert_area,
                    'advert_city': advert_city,
                    'category_name': category_name,
                    'display_image' : display_image,
                    'advert_views': advert_views,
                    'advert_likes': advert_likes,
                    'advert_shares': advert_shares,
                    'subscription_days': subscription_days,
                    'subscription_text': subscription_text,
                    'subscriber_color': subscriber_color,
                    'premium_service_list': premium_service_list,
                    'advert_bookings': advert_bookings,
                    'advert_color': advert_color,
                }
                advert_list.append(advert_data)
            data = {
                'advert_list': advert_list,
                'category_list': category_list,
                'start_date_var': start_date_var,
                'end_date_var': end_date_var,
                'category_var': category_var,
                'status_var': status_var,
                'supplier_id': supplier_id,
                'success': 'true',
            }

        except IntegrityError as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time',
                    'username': request.session['login_user']}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return render(request, 'Subscriber/subscriber-advert.html', data)


def premium_list(business_id):
    premium_ser_list = PremiumService.objects.filter(business_id=business_id)
    premium_service_list = []
    pre_date = datetime.now().strftime("%m/%d/%Y")
    pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
    for premium_obj in premium_ser_list:
        status_advert = ''
        date_gap = ''
        premium_service_name = premium_obj.premium_service_name
        start_date = premium_obj.start_date
        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = premium_obj.end_date
        end_date = datetime.strptime(end_date, "%m/%d/%Y")
        date_gap = (end_date - pre_date).days

        if date_gap > 0:
            date_gap = date_gap
        else:
            date_gap = 0

        if date_gap <= 10 and date_gap >= 1:
            status_advert = 1
            premium_days = "( " + str(date_gap) + " days Remaining )"
            premium_text = "Starts on " + start_date.strftime("%d %b %y")
            premium_color = "orange"
        elif date_gap == 0:
            status_advert = 0
            premium_days = ""
            premium_text = "Expired on " + start_date.strftime("%d %b %y")
            premium_color = "red"
        else:
            status_advert = 2
            premium_days = "( " + str(date_gap) + " days Remaining )"
            premium_text = "Starts on " + start_date.strftime("%d %b %y")
            premium_color = "#333"

        premium_data = {
            'premium_service_name': premium_service_name,
            'premium_days': premium_days,
            'premium_text': premium_text,
            'premium_color': premium_color
        }
        premium_service_list.append(premium_data)
    return premium_service_list

def subscriber_booking(request):
    try:
        data = {}
        final_list = []
        final_list1 = []
        final_list2 = []

        try:
            supplier_id = request.session['supplier_id']
            print '=======......supplier_id........======', supplier_id

            start_date_var = request.GET.get('start_date_var')
            print start_date_var
            end_date_var = request.GET.get('end_date_var')
            print end_date_var
            category_var = request.GET.get('category_var')
            print category_var
            status_var = request.GET.get('status_var')
            print status_var

            if start_date_var and end_date_var and status_var and category_var:
                Advert_list1 = Advert.objects.filter(category_id=request.GET.get('category_var'),
                                                     creation_date__range=[start_date_var, end_date_var],
                                                     status=request.GET.get('status_var'))

                print '...................All..........................', Advert_list1

            elif start_date_var and end_date_var and category_var:
                Advert_list1 = Advert.objects.filter(category_id=request.GET.get('category_var'),
                                                     creation_date__range=[start_date_var, end_date_var])

                print '...........start_date_var and end_date_var  and category_var............', Advert_list1


            elif start_date_var and end_date_var and status_var:
                Advert_list1 = Advert.objects.filter(
                    creation_date__range=[start_date_var, end_date_var], status=request.GET.get('status_var'))

                print '...................start_date_var and end_date_var  and status_var..........................', Advert_list1

            elif status_var:
                Advert_list1 = Advert.objects.filter(
                    status=request.GET.get('status_var'))

                print '...................status_var  and category_var..........................', Advert_list1

            elif start_date_var and end_date_var:
                Advert_list1 = Advert.objects.filter(
                    creation_date__range=[start_date_var, end_date_var])

                print '...................start_date_var and end_date_var..........................', Advert_list1

            elif category_var:
                Advert_list1 = Advert.objects.filter(
                    category_id=request.GET.get('category_var'))

                print '...................category_var..........................', Advert_list1

            else:
                Advert_list1 = Advert.objects.filter(supplier_id=supplier_id)
                print "..................ELSE.........", Advert_list1

            category_list = Category.objects.all()
            for category_obj in category_list:
                category_id = category_obj.category_id
                category_name = category_obj.category_name
                list2 = {'category_name': category_name, 'category_id': category_id}
                final_list2.append(list2)

            for advert_obj in Advert_list1:

                # # To find out coupon code
                advert_id = advert_obj.advert_id
                if advert_obj.display_image:
                    display_image = SERVER_URL + advert_obj.display_image.url
                else:
                    display_image = ''
                advert_sub_list = CouponCode.objects.filter(advert_id=advert_id)

                for advert_sub_obj in advert_sub_list:
                    coupon_code = advert_sub_obj.coupon_code
                    # Availed date
                    creation_date = (advert_sub_obj.creation_date).strftime('%b %d,%Y')
                    print '............creation_date..............', creation_date

                    # consumer personal data
                    user_id = advert_sub_obj.user_id

                    consumer_obj = ConsumerProfile.objects.get(consumer_id=str(user_id))
                    consumer_full_name = str(consumer_obj.consumer_full_name)

                    consumer_contact_no = consumer_obj.consumer_contact_no
                    consumer_email_id = consumer_obj.consumer_email_id
                    consumer_area = consumer_obj.consumer_area
                    consumer_profile_pic = SERVER_URL + consumer_obj.consumer_profile_pic.url

                    # Expiry Date
                    pre_date = datetime.now().strftime("%Y-%m-%d")
                    pre_date = datetime.strptime(pre_date, "%Y-%m-%d")

                    expiry_data_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                    business_id = expiry_data_obj.business_id
                    end_date = expiry_data_obj.business_id.end_date
                    end_date = datetime.strptime(end_date, "%m/%d/%Y")

                    date_gap = (end_date - pre_date).days

                    if date_gap > 0:
                        date_gap = date_gap
                        status_advert = 1
                    else:
                        date_gap = 0
                        status_advert = 0

                    end_date = end_date.strftime('%b %d,%Y')
                    # logo

                    list = {'display_image': display_image, 'consumer_full_name': consumer_full_name,
                            'consumer_contact_no': consumer_contact_no, 'consumer_email_id': consumer_email_id,
                            'consumer_area': consumer_area, 'consumer_profile_pic': consumer_profile_pic,
                            'end_date': end_date, 'coupon_code': coupon_code, 'creation_date': creation_date,
                            'date_gap': date_gap, 'status_advert': status_advert}
                    final_list.append(list)

            Supplier_obj = Supplier.objects.get(supplier_id=supplier_id)
            logo = SERVER_URL + Supplier_obj.logo.url

            data = {'logo': logo, 'final_list': final_list, 'success': 'true', 'final_list2': final_list2}

        except IntegrityError as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time',
                    'username': request.session['login_user']}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    print data
    return render(request, 'Subscriber/subscriber-booking.html', data)

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def advert_bookings(request):
#     if not request.user.is_authenticated():
#         return redirect('backoffice')
#     else:
#         advert_id = request.GET.get('advert_id')
#         advert_obj = Advert.objects.get(advert_id=advert_id)
#         coupon_user = CouponCode.objects.filter(advert_id=advert_id)
#         coupon_list = []
#         for coupons in coupon_user:
#             advert_obj = Advert.objects.get(advert_id=str(coupons.advert_id))
#             advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=str(coupons.advert_id))
#             start_date = advert_sub_obj.business_id.start_date
#             end_date = advert_sub_obj.business_id.end_date
#             start_date = datetime.strptime(start_date, "%m/%d/%Y")
#             end_date = datetime.strptime(end_date, "%m/%d/%Y")
#             pre_date = datetime.now().strftime("%m/%d/%Y")
#             pre_date = datetime.strptime(pre_date, "%m/%d/%Y")
#             date_gap = end_date - pre_date
#             if int(date_gap.days) >= 0:
#                 status = 'Active'
#             else:
#                 status = 'Inactive'
#             print status
#             coupon_obj = {
#                 'coupon_code': coupons.coupon_code,
#                 'avail_date': coupons.creation_date.strftime("%d/%m/%Y"),
#                 'user_id': str(coupons.user_id),
#                 'mobile_no': coupons.user_id.consumer_contact_no,
#                 'user_img': SERVER_URL + coupons.user_id.consumer_profile_pic.url,
#                 'user_name': coupons.user_id.consumer_full_name,
#                 'user_area': coupons.user_id.consumer_area,
#                 'user_email_id': coupons.user_id.consumer_email_id,
#                 'coupon_expiry_date': end_date.strftime("%d/%m/%Y"),
#                 'days_remaining': int(date_gap.days),
#                 'status': status
#             }
#             coupon_list.append(coupon_obj)
#         data = {'coupon_list': coupon_list, 'advert_name': advert_obj.advert_name, 'booking_count': len(coupon_list),
#                 'username': request.session['login_user']}
#         return render(request, 'Subscriber/advert_bookings.html', data)

def get_pincode(request):
    # pdb.set_trace()

    pincode_list = []
    try:
        city_id = request.GET.get('city_id')
        city_place_obj = City_Place.objects.get(city_place_id=city_id)
        pincode_list1 = Pincode.objects.filter(city_id=str(city_place_obj.city_id.city_id)).order_by('pincode')
        # pincode_objs = pincode_list1.values('pincode').distinct()
        # print pincode_objs
        for pincode in pincode_list1:
            options_data = '<option value=' + str(pincode.pincode_id) + '>' + str(pincode.pincode) + '</option>'
            pincode_list.append(options_data)
            # print pincode_list
        data = {'pincode_list': pincode_list}

    except Exception, ke:
        print ke
        data = {'city_list': 'none', 'message': 'No city available'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_profile(request):
    try:
        if request.POST:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            supplier_id = request.POST.get('supplier_id')
            print '............supplier_id............', supplier_id
            supplier_obj = Supplier.objects.get(supplier_id=request.POST.get('supplier_id'))
            supplier_obj.business_name = request.POST.get('business_name')
            supplier_obj.phone_no = request.POST.get('phone_no')
            supplier_obj.secondary_phone_no = request.POST.get('sec_phone_no')
            supplier_obj.supplier_email = request.POST.get('email')
            supplier_obj.secondary_email = request.POST.get('sec_email')
            supplier_obj.address1 = request.POST.get('address1')
            supplier_obj.address2 = request.POST.get('address2')
            print supplier_obj.address2
            supplier_obj.city_place_id = City_Place.objects.get(city_place_id=request.POST.get('city'))
            print supplier_obj.city_place_id
            supplier_obj.country_id = Country.objects.get(country_id=request.POST.get('country'))
            supplier_obj.state = State.objects.get(state_id=request.POST.get('state'))
            supplier_obj.pincode = Pincode.objects.get(pincode_id=request.POST.get('pincode'))
            supplier_obj.business_details = request.POST.get('business')
            supplier_obj.contact_person = request.POST.get('user_name')
            supplier_obj.contact_email = request.POST.get('user_email')
            supplier_obj.contact_no = request.POST.get('user_contact_no')

            supplier_obj.notification_status = request.POST.get('state1')
            supplier_obj.reminders_status = request.POST.get('state2')
            supplier_obj.discounts_status = request.POST.get('state3')
            supplier_obj.request_call_back_status = request.POST.get('state4')
            supplier_obj.no_call_status = request.POST.get('state5')

            supplier_obj.save()
            try:
                supplier_obj.logo = request.FILES['logo']
            except:
                pass

            supplier_obj.save()

            data = {
                'success': 'true',
                'message': "Subscriber edited successfully"
            }
    except Exception, e:
        print e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')
