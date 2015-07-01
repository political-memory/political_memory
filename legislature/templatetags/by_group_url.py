from django import template
from django.core.urlresolvers import reverse

from representatives.models import Mandate

register = template.Library()


@register.filter
def by_group_url(group):
    if isinstance(group, Mandate):
        group = group.group
        
    kwargs = {'group_kind': group.kind}

    if group.abbreviation:
        kwargs['search'] = group.abbreviation
    else:
        kwargs['search'] = group.name

    kwargs['group_id'] = group.id
    
    return reverse(
        'legislature:representatives_by_group',
        kwargs=kwargs
    )
