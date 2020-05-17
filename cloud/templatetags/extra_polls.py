from django import template

register = template.Library()

@register.filter(name = 'rounder')
def rounder(value, arg):
    """Removes all values of arg from the given string"""
    print(value,arg,round(float(value),int(arg)))
    return round(float(value),int(arg))
