# coding: utf-8
from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()
link = '<a class="{network}-link" href="{url}" target="_blank">{user}</a>'


@register.filter
def twitter_link(url):
    return mark_safe(link.format(network='twitter', url=url,
                                 user=re.sub(r'.*/@?([^/]+)', '@\\1', url)))


@register.filter
def facebook_link(url):
    return mark_safe(link.format(network='facebook', url=url,
                                 user=re.sub(r'.*/([^/]+)', '\\1', url)))

