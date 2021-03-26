from django import template
import os
register = template.Library()

@register.filter(name = 'rounder')
def rounder(value, arg):
    """Removes all values of arg from the given string"""
    return round(float(value),int(arg))

@register.filter(name = 'getfilename')
def getfilename(value):
    return os.path.basename(value)
