from django import template

register = template.Library()


@register.simple_tag
def set_url_option(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.filter
def tail(value, key):
    if value is not None:
        return str(value).split(key)[-1]
    return value
