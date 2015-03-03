from django import template

register = template.Library()

@register.inclusion_tag("blocks/navigation.html")
def build_menu():
    return {
        'menus': [{
            'id': 'countries_menu',
            'name': 'Country',
            'content': ({
                "url": "country:%s is_active:1" % country.code,
                "display": country.name,
                "sprite": "sprite-country_small-%s" % country.code} for country in Country.objects.all().order_by("name")),
            'flyout_class': 'four',
        },
        {
            'id': 'groups_menu',
            'name': 'Political group',
            'content': ({
                "url": "group:%s is_active:1" % group.abbreviation,
                "display": group.name,
                "sprite": "sprite-eu_group-%s" % group.abbreviation.replace("/", "")} for group in Group.ordered_by_meps_count()),
            'flyout_class': 'twelve',
        },
        {
            'id': 'committees_menu',
            'name': 'Committees',
            'content': ({
                "url": "committees:%s is_active:1" % committee.abbreviation,
                "code": committee.abbreviation,
                "display": committee.name} for committee in Committee.ordered_by_meps_count()),
            'flyout_class': 'twelve',
        },
        ]
    }
