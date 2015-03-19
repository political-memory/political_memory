from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def by_mandate_url(mandate):
    kwargs = {'mandate_kind': mandate.group.kind}

    if mandate.group.abbreviation:
        kwargs['search'] = mandate.group.abbreviation
    else:
        kwargs['search'] = mandate.group.name

    return reverse(
        'legislature:representatives_by_mandate',
        kwargs=kwargs
    )
