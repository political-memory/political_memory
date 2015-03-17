from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def by_mandate_url(mandate):
    kwargs = {'mandate_kind': mandate.group.kind}

    if mandate.group.abbreviation:
        kwargs['mandate_abbr'] = mandate.group.abbreviation
    else:
        kwargs['mandate_name'] = mandate.group.name

    return reverse(
        'representatives:listby',
        kwargs=kwargs
    )
