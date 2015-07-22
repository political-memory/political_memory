from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from representatives.models import Mandate, Group

register = template.Library()

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
        return mark_safe('<span class="label label-success">{}</span>'.format(score))
    elif score < 0:
        return mark_safe('<span class="label label-danger">{}</span>'.format(score))
    else:
        return mark_safe('<span class="label label-default">{}</span>'.format(score))


@register.filter
def country_flag(country):
    return mark_safe('{} <span class="flag-icon flag-icon-{}"></span>'.format(
        country.name,
        country.code.lower()
    ))


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
