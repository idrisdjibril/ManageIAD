from django import template

register = template.Library()

@register.filter
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif isinstance(value, dict):
        return value.get(arg)
    return