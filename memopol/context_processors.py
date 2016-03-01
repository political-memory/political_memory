from representatives.models import Group


def search_form_options(request):
    d = {}
    # Note: Those queries needs to be eval in the template so that we can cache it efficiently

    d['countries'] = Group.objects.filter(kind='country')
    d['parties'] = Group.objects.filter(kind='group')
    d['delegations'] = Group.objects.filter(kind='delegation')
    d['committees'] = Group.objects.filter(kind='committee')

    return d
