
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import HttpResponse
from Admin.captcha_form import CaptchaForm
import json,random


def reload_captcha(request):
    form = CaptchaForm()
    print "==================check======================"
    to_json_response = dict()
    to_json_response['status'] = 1
    to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
    to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])
    return HttpResponse(json.dumps(to_json_response), content_type='application/json')


def random_digit_challenge():
    ret = u''
    ret=''.join(random.choice('0123456789ABCDEF') for i in range(5))
    #for i in range(6):
    #    ret += str(random.randint(0,9))
    return ret, ret
