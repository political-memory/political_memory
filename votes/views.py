from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from representatives_votes.models import Dossier

def votes_index(request):
    votes_list = Dossier.objects.all()

    return _render_list(request, votes_list)

def _render_list(request, votes_list, num_by_page=30):
    """
    Render a paginated list of votes
    """
    paginator = Paginator(votes_list, num_by_page)
    page = request.GET.get('page')
    try:
        votes = paginator.page(page)
    except PageNotAnInteger:
        votes = paginator.page(1)
    except EmptyPage:
        votes = paginator.page(paginator.num_pages)

    context = {}
    queries_without_page = request.GET.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']
    context['queries'] = queries_without_page

    context['votes'] = votes
    context['votes_num'] = paginator.count

    return render(
        request,
        'votes/votes_list.html',
        context
    )
