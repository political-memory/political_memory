# coding: utf-8
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def score_arrow(score):
    if score > 0:
        return mark_safe(
            '<span class="glyphicon glyphicon-upload text-success"></span>')
    elif score < 0:
        return mark_safe(
            '<span class="glyphicon glyphicon-upload text-danger"></span>')
    else:
        return ''


@register.filter
def vote_glyphicon(position):
    if position == 'for':
        return 'glyphicon-ok'
    elif position == 'against':
        return 'glyphicon-remove'
    else:
        return ''

@register.filter
def vote_icon_color(position, recommendation):
    if recommendation:
        if position == recommendation:
            return 'text-success'
        else:
            return 'text-danger'
    else:
        return ''

