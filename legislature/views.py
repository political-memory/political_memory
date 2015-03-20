from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from legislature.models import Representative
from representatives.models import Group


def representatives_index(request):
    representative_list = _filter_by_search(
        request,
        Representative.objects.all()
    )

    return _render_list(request, representative_list)


def representative_by_name(request, name):
    representative = get_object_or_404(
        Representative, full_name=name)
    return render(
        request,
        'legislature/representative_view.html',
        {'representative': representative}
    )


def representative_view(request, num):
    representative = get_object_or_404(Representative, pk=num)

    return render(
        request,
        'legislature/representative_view.html',
        {'representative': representative}
    )


def representatives_by_mandate(request, mandate_kind, mandate_abbr=None,
                               mandate_name=None, search=None):
    if mandate_abbr:
        representative_list = Representative.objects.filter(
            mandate__group__abbreviation=mandate_abbr,
            mandate__group__kind=mandate_kind,
            mandate__active=True
        )

    elif mandate_name:
        representative_list = Representative.objects.filter(
            Q(mandate__group__name__icontains=mandate_name),
            mandate__group__kind=mandate_kind,
            mandate__active=True
        )

    elif search:
        try:
            Group.objects.get(abbreviation=search, kind=mandate_kind)
            representative_list = Representative.objects.filter(
                mandate__group__abbreviation=search,
                mandate__group__kind=mandate_kind,
                mandate__active=True
            )
        except Group.DoesNotExist:
            representative_list = Representative.objects.filter(
                Q(mandate__group__abbreviation__icontains=search) |
                Q(mandate__group__name__icontains=search),
                mandate__group__kind=mandate_kind,
                mandate__active=True
            )

    # Select distinct representatives and filter by search
    representative_list = list(set(
        _filter_by_search(request, representative_list)
    ))

    return _render_list(request, representative_list)


def _filter_by_search(request, representative_list):
    """
    Return a representative_list filtered by
    the representative name provided in search form
    """
    search = request.GET.get('search')
    if search:
        return representative_list.filter(
            Q(full_name__icontains=search)
        )
    else:
        return representative_list


def _render_list(request, representative_list, num_by_page=50):
    """
    Render a paginated list of representatives
    """
    paginator = Paginator(representative_list, num_by_page)
    page = request.GET.get('page')
    try:
        representatives = paginator.page(page)
    except PageNotAnInteger:
        representatives = paginator.page(1)
    except EmptyPage:
        representatives = paginator.page(paginator.num_pages)

    context = {}
    queries_without_page = request.GET.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']
    context['queries'] = queries_without_page

    context['representatives'] = representatives
    context['representative_num'] = paginator.count

    return render(
        request,
        'legislature/representatives_list.html',
        context
    )


def group_by_kind(request, kind):
    groups = Group.objects.filter(
        kind=kind
    )

    return render(
        request,
        'legislature/group_list.html',
        {'groups': groups}
    )
