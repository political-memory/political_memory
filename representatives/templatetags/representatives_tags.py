from django import template
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import naturalday

register = template.Library()


@register.filter
def country_flag(country):
    return mark_safe(
        '<span class="flag-icon flag-icon-{code}"></span> {name}'.format(
            name=country.name,
            code=country.code.lower()))


@register.filter
def mandate_date(date, arg=None):
    if date.year == 9999:
        return 'present'
    else:
        return naturalday(date, arg)
