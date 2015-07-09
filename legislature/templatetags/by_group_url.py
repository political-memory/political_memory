from django import template
from django.core.urlresolvers import reverse

from representatives.models import Mandate, Group

register = template.Library()


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
        'legislature:representative_index',
        kwargs=kwargs
    )
