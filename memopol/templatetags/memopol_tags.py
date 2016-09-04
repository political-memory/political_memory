# coding: utf-8

import re

from django import template
from django.contrib.humanize.templatetags.humanize import naturalday
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.safestring import mark_safe


register = template.Library()
link = u'<a class="{network}-link" href="{url}" target="_blank">{label}</a>'


def cssify(string):
    return re.sub('[^a-z_-]', '', string.lower())


@register.filter
def country_flag(country, tplace='bottom'):
    # Enable using groups instead of countries
    code = country.code if hasattr(country, 'code') else country.abbreviation
    return mark_safe(
        u'<span class="flag-icon flag-icon-{code}" title="{name}"'
        u' data-toggle="tooltip" data-placement="{place}"></span>'.format(
            code=code.lower(), place=tplace, name=country.name))


@register.filter
def chamber_icon(chamber, tplace='bottom'):
    url = static('images/chamber-%s.png' % cssify(chamber.abbreviation))
    return mark_safe(
        u'<span class="chamber-icon" style="background-image: url({url})"'
        u' data-toggle="tooltip" data-placement="{place}"'
        u' title="{name}"></span>'.format(
            name=chamber.name,
            url=url,
            place=tplace
        )
    )


@register.filter
def group_icon(group, tplace='bottom'):
    url = static('images/group-%s.png' % cssify('%s-%s' % (
        group.chamber.abbreviation, group.abbreviation)))
    return mark_safe(
        u'<span class="group-icon" style="background-image: url({url})"'
        u' data-toggle="tooltip" data-placement="{place}" title="{name}">'
        u'</span>'.format(url=url, name=group.name, place=tplace))


@register.filter
def mandate_date(date, arg=None):
    if date is None or date.year == 9999:
        return 'present'
    else:
        return naturalday(date, arg)


@register.filter
def position_icon(position, recommendation=None):
    color = 'default'
    if recommendation:
        if position == recommendation:
            color = 'success'
        else:
            color = 'danger'

    if position == 'for':
        icon = "thumbs-up"
    elif position == 'against':
        icon = "thumbs-down"
    else:
        icon = "circle-o"

    pattern = '<i class="fa fa-%s text-%s" title="%s"></i>'
    return mark_safe(pattern % (icon, color, position))


@register.filter
def proposal_status_label(status, recommendation=None):
    color = 'default'
    if recommendation:
        reco = recommendation.recommendation

        if (reco == 'for' and status == 'adopted' or
           reco == 'against' and status == 'rejected'):
            color = 'success'
        elif (reco == 'for' and status == 'rejected' or
              reco == 'against' and status == 'adopted'):
            color = 'danger'

    pattern = '<span class="label label-%s">%s</span>'
    return mark_safe(pattern % (color, status))


@register.filter
def score_badge(score, tooltip=None):
    if score > 0:
        color = 'success'
    elif score < 0:
        color = 'danger'
    else:
        color = 'primary'

    attrs = ''
    if tooltip:
        attrs = 'data-toggle="tooltip" data-placement="%s" title="%s"'
        attrs = attrs % ('left', tooltip)

    pattern = '<span class="badge badge-%s" %s>%s</span>'
    return mark_safe(pattern % (color, attrs, score))


@register.filter
def cast_str(val):
    return str(val)
