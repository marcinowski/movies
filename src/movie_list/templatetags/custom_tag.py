from django import template

register = template.Library()


@register.filter(name='get')
def get(dic, key):
    """Removes all values of arg from the given string"""
    return dic.get(key, '')
