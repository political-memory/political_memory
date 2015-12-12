# coding: utf-8

# This file is part of memopol.
#
# memopol is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# memopol is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

"""
This file contains all templatetags used by the representative app
"""

from django import template
from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from representatives.models import Group, Mandate

register = template.Library()


@register.filter
def mandate_date(date, arg=None):
    if date.year == 9999:
        return 'present'
    else:
        return naturalday(date, arg)


@register.filter
def position_icon(position):
    if position == 'for':
        return mark_safe(
            '<i \
            aria-label="for" \
            class="fa fa-thumbs-up vote_positive" \
            title="for" \
            ></i>')
    elif position == 'against':
        return mark_safe(
            '<i \
            aria-label="against" \
            class="fa fa-thumbs-down vote_negative" \
            title="against" \
            ></i>')
    else:
        return mark_safe(
            '<i \
            aria-label="abstain" \
            class="fa fa-circle-o vote_abstain" \
            title="abstain" \
            ></i>')


@register.filter
def score_label(score):
    if score > 0:
        return mark_safe(
            '<span class="label label-success">{}</span>'.format(score))
    elif score < 0:
        return mark_safe(
            '<span class="label label-danger">{}</span>'.format(score))
    else:
        return mark_safe(
            '<span class="label label-default">{}</span>'.format(score))


@register.filter
def country_flag(country):
    return mark_safe(
        '<span class="flag-icon flag-icon-{code}"></span> {name}'.format(
            name=country.name,
            code=country.code.lower()))


@register.filter
def by_group_url(group):
    if isinstance(group, Mandate):
        group = group.group

    if not isinstance(group, Group):
        return ''

    kwargs = {'group_kind': group.kind}

    if group.abbreviation:
        kwargs['group'] = group.abbreviation
    else:
        kwargs['group'] = group.name

    # kwargs['group_id'] = group.id

    return reverse(
        'legislature:representative-index',
        kwargs=kwargs
    )
