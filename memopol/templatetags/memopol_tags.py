# coding: utf-8

import re

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()
link = '<a class="{network}-link" href="{url}" target="_blank">{label}</a>'


@register.filter
def twitter_link(url):
    return mark_safe(link.format(network='twitter', url=url,
        label=re.sub(r'.*/@?([^/]+)', '@\\1', re.sub(r'/$', '', url.strip()))))


@register.filter
def facebook_link(url):
    return mark_safe(link.format(network='facebook', url=url,
        label=re.sub(r'.*/([^/]+)', '\\1', re.sub(r'/$', '', url.strip()))))


@register.filter
def website_link(url):
    short_url = re.sub(r'^https?://([^/]+).*', '\\1', url)
    return mark_safe(link.format(network='website', url=url,
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
