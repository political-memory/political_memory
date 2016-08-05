from datetime import timedelta
from datetime import date

from django import template

register = template.Library()


@register.filter
def regroup_by_age(positions):
    """
    Returns a list of lists
    """
    timeframes = [[],  # Before
                  [],  # Last year
                  [],  # Last 6 months
                  []]  # This month
    for position in positions:
        index = 0
        if position.datetime +timedelta(30) >= date.today():
            index=3
        elif position.datetime + timedelta(180) >= date.today():
            index=2
        elif position.datetime + timedelta(365) >= date.today():
            index=1

        timeframes[index].append(position)

    return timeframes
