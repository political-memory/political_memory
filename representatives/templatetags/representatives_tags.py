import re
from django import template
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import naturalday

register = template.Library()


def cssify(string):
    return re.sub('[^a-z_-]', '', string.lower())


@register.filter
def country_flag(country):
    return mark_safe(
        '<span class="flag-icon flag-icon-{code}"></span> {name}'.format(
            name=country.name,
            code=country.code.lower()))


@register.filter
def chamber_icon(chamber):
    return mark_safe(
        u'<span class="chamber-icon ' +
        u'chamber-icon-{abbr}"></span> {name}'.format(
            name=chamber.name,
            abbr=cssify(chamber.abbreviation)))


@register.filter
def mandate_icon(main_mandate):
    return mark_safe(
        u'<span class="group-icon ' +
        u'group-icon-{abbr}"></span> {role} of {name}'.format(
            role=main_mandate.role,
            name=main_mandate.group.name,
            abbr=cssify(main_mandate.group.abbreviation)))


@register.filter
def group_icon(group):
    return mark_safe(
        u'<span class="group-icon ' +
        u'group-icon-{abbr}"></span> {name}'.format(
            abbr=cssify(group.abbreviation),
            name=group.abbreviation))


@register.filter
def group_long_icon(group):
    return mark_safe(
        u'<span class="group-icon ' +
        u'group-icon-{abbr}"></span> {name}'.format(
            abbr=cssify(group.abbreviation),
            name=group.name))


@register.filter
def mandate_date(date, arg=None):
    if date is None or date.year == 9999:
        return 'present'
    else:
        return naturalday(date, arg)
