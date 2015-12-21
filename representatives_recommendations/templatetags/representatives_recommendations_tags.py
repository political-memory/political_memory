# coding: utf-8
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


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
