from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from representatives.models import Representative


def index(request):
    context = {}
    if request.GET.get('search'):
        search = request.GET.get('search')
        representative_list = Representative.objects.filter(
            Q(full_name__icontains=search) |
            Q(country__name__icontains=search)
        )
        queries_without_page = request.GET.copy()
        if 'page' in queries_without_page:
            del queries_without_page['page']
        context['queries'] = queries_without_page
    else:
        representative_list = Representative.objects.all()

    paginator = Paginator(representative_list, 15)

    page = request.GET.get('page')
    try:
        representatives = paginator.page(page)
    except PageNotAnInteger:
        representatives = paginator.page(1)
    except EmptyPage:
        representatives = paginator.page(paginator.num_pages)

    context['representatives'] = representatives
    return render(
        request,
        'memopol_representatives/list.html',
        context
    )


def view(request, num):
    representative = get_object_or_404(Representative, pk=num)

    return render(
        request,
        'memopol_representatives/view.html',
        {'representative': representative}
    )
