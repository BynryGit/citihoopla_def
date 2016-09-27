from django import template
#from django.template import Template

register = template.Library()

@register.filter
def check_list(list, elements):
    elements = elements.split(',')
    flag = 'no'
    for element in elements:
        if element in list:
            flag = 'yes'
    if flag == 'yes':
        return 'true'
    else:
        return 'false'