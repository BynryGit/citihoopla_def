from django import template
#from django.template import Template

register = template.Library()

@register.filter
def check_list(list, elements):
    print list
    elements = elements.split(',')
    print elements
    flag = 'no'
    for element in elements:
        if element in list:
            flag = 'yes'
    if flag == 'yes':
        return 'true'
    else:
        return 'false'