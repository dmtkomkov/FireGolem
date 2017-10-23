from django import template

register = template.Library()


@register.simple_tag
def set_url_option(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
