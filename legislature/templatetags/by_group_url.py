from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def by_group_url(group):
    kwargs = {'group_kind': group.kind}

    if group.abbreviation:
        kwargs['search'] = group.abbreviation
    else:
        kwargs['search'] = group.name

    return reverse(
        'legislature:representatives_by_group',
        kwargs=kwargs
    )


@register.filter
def by_mandate_url(mandate):
    return by_group_url(mandate.group)
