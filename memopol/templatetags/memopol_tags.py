# coding: utf-8

import re

from django import template
from django.contrib.humanize.templatetags.humanize import naturalday
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()
link = u'<a class="{network}-link" href="{url}" target="_blank">{label}</a>'


def cssify(string):
    return re.sub('[^a-z_-]', '', string.lower())


def fix_url(url):
    # Ensure we have a usable URL
    return re.sub('^(https?://)?', 'https://', url.strip())


@register.filter
def twitter_link(url):
    furl = fix_url(url)
    return mark_safe(link.format(network='twitter', url=furl,
        label=re.sub(r'.*/@?([^/]+)', '@\\1', re.sub(r'/$', '', furl))))


@register.filter
def facebook_link(url):
    furl = fix_url(url)
    clean_url = re.sub(r'/$', '', re.sub(r'\?.*', '', furl))
    m = re.search(r'/pages/([^/]+)', clean_url, re.I)
    return mark_safe(link.format(network='facebook', url=furl,
        label=m.group(1) if m else re.sub(r'.*/([^/]+)', '\\1', clean_url)))


@register.filter
def website_link(url):
    furl = fix_url(url)
    short_url = re.sub(r'^https?://([^/]+).*', '\\1', furl)
    return mark_safe(link.format(network='website', url=furl,
        label=short_url))


@register.filter
def email_link(address):
    return mark_safe(link.format(network='email', url='mailto:%s' % address,
        label=address))


@register.simple_tag
def group_url(group):
    if group.kind == 'chamber' or group.chamber is None:
        return escape(reverse('representative-list', kwargs={
            'group_kind': group.kind,
            'group': group.name
        }))
    else:
        return escape(reverse('representative-list', kwargs={
            'group_kind': group.kind,
            'chamber': group.chamber.name,
            'group': group.name
        }))


@register.simple_tag
def chamber_url(chamber):
    return escape(reverse('representative-list', kwargs={
        'group_kind': 'chamber',
        'group': chamber.name
    }))


@register.simple_tag
def country_url(country):
    return escape(reverse('representative-list', kwargs={
        'group_kind': 'country',
        'group': country.name
    }))


@register.filter
def country_flag(country):
    # Enable using groups instead of countries
    code = country.code if hasattr(country, 'code') else country.abbreviation
    return mark_safe(
        '<span class="flag-icon flag-icon-{code}"></span>'.format(
            code=code.lower()))


@register.filter
def chamber_icon(chamber):
    url = static('images/chamber-%s.png' % cssify(chamber.abbreviation))
    return mark_safe(
        u'<span class="chamber-icon" style="background-image: url({url})">'
        u'</span>'.format(name=chamber.name, url=url))


@register.filter
def chamber_small_icon(chamber):
    url = static('images/chamber-%s.png' % cssify(chamber.abbreviation))
    return mark_safe(
        u'<span class="chamber-icon" style="background-image: url({url})" '
        u'title="{name}"></span>'.format(name=chamber.name, url=url))


@register.simple_tag
def chamber_page_link(site, name):
    icon_url = static('images/chamber-%s.png' % cssify(site.kind))
    site_url = fix_url(site.url)
    return mark_safe(
        u'<span class="chamber-icon" style="background-image: url({icon})" '
        u'></span> <a href="{site}" target="_blank">{name}</a>'
        .format(name=name, site=site_url, icon=icon_url))


@register.filter
def mandate_icon(main_mandate):
    group = main_mandate.group
    url = static('images/group-%s.png' % cssify('%s-%s' % (
        group.chamber.abbreviation, group.abbreviation)))
    return mark_safe(
        u'<span class="group-icon" style="background-image: url({url})">'
        u'</span> {role} of {name}'.format(
            role=main_mandate.role,
            name=main_mandate.group.name,
            url=url))


@register.filter
def group_icon(group):
    url = static('images/group-%s.png' % cssify('%s-%s' % (
        group.chamber.abbreviation, group.abbreviation)))
    return mark_safe(
        u'<span class="group-icon" style="background-image: url({url})">'
        u'</span>'.format(url=url, name=group.abbreviation))


@register.filter
def group_long_icon(group):
    url = static('images/group-%s.png' % cssify('%s-%s' % (
        group.chamber.abbreviation, group.abbreviation)))
    return mark_safe(
        u'<span class="group-icon" style="background-image: url({url})">'
        u'</span> {name}'.format(url=url, name=group.name))


@register.filter
def mandate_date(date, arg=None):
    if date is None or date.year == 9999:
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
def cast_str(val):
    return str(val)
