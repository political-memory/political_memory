from django import template
from django.utils.safestring import mark_safe

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
