# coding: utf-8
from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()
link = '<a class="{network}-link" href="{url}" target="_blank">{label}</a>'


@register.filter
def twitter_link(url):
    return mark_safe(link.format(network='twitter', url=url,
                                 label=re.sub(r'.*/@?([^/]+)', '@\\1', url)))


@register.filter
def facebook_link(url):
    return mark_safe(link.format(network='facebook', url=url,
                                 label=re.sub(r'.*/([^/]+)', '\\1', url)))


@register.filter
def website_link(url):
    short_url = re.sub(r'^https?://([^/]+).*', '\\1', url)
    return mark_safe(link.format(network='website', url=url,
                                 label=short_url))
