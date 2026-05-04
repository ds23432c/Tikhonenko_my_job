from django import template

register = template.Library()


@register.filter(name='split')
def split(value, delimiter='|'):
    if value is None:
        return []
    items = str(value).split(delimiter)
    parsed = []
    for item in items:
        parts = [part.strip() for part in item.split(',')]
        parsed.append(tuple(parts))
    return parsed


@register.filter(name='get_item')
def get_item(value, key):
    try:
        return value[key]
    except (TypeError, KeyError, IndexError):
        return []
