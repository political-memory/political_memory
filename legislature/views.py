from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from legislature.models import MRepresentative, MGroup


def representatives_index(request):
    representative_list = _filter_by_search(
        request,
        MRepresentative.objects.all()
    )

    return _render_list(request, representative_list)


def representative_by_name(request, name):
    representative = get_object_or_404(
        MRepresentative, full_name=name)
    return render(
        request,
        'legislature/representative_view.html',
        {'representative': representative}
    )


def representative_view(request, num):
    representative = get_object_or_404(MRepresentative, pk=num)

    return render(
        request,
        'legislature/representative_view.html',
        {'representative': representative}
    )


def representatives_by_group(request, group_kind, group_abbr=None,
                             group_name=None, search=None):
    if group_abbr:
        representative_list = MRepresentative.objects.filter(
            mmandate__mgroup__abbreviation=group_abbr,
            mmandate__mgroup__kind=group_kind,
            mmandate__active=True
        )

    elif group_name:
        representative_list = MRepresentative.objects.filter(
            Q(mmandate__mgroup__name__icontains=group_name),
            mmandate__mgroup__kind=group_kind,
            mmandate__active=True
        )

    elif search:
        try:
            MGroup.objects.get(abbreviation=search, kind=group_kind)
            representative_list = MRepresentative.objects.filter(
                mmandate__mgroup__abbreviation=search,
                mmandate__mgroup__kind=group_kind,
                mmandate__active=True
            )
        except MGroup.DoesNotExist:
            representative_list = MRepresentative.objects.filter(
                Q(mmandate__mgroup__abbreviation__icontains=search) |
                Q(mmandate__mgroup__name__icontains=search),
                mmandate__mgroup__kind=group_kind,
                mmandate__active=True
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


def _render_list(request, representative_list, num_by_page=30):
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


def groups_by_kind(request, kind):
    groups = MGroup.objects.filter(
        kind=kind,
        active=True
    )

    return render(
        request,
        'legislature/groups_list.html',
        {'groups': groups}
    )
