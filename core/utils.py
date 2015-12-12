from __future__ import absolute_import

from pure_pagination import EmptyPage
from pure_pagination import Paginator
from django.shortcuts import render


def create_child_instance_from_parent(child_cls, parent_instance):
    """
    Create a child model instance from a parent instance
    """
    parent_cls = parent_instance.__class__
    field = child_cls._meta.get_ancestor_link(parent_cls).column

    child_instance = child_cls(**{
        field: parent_instance.pk
    })

    child_instance.__dict__.update(parent_instance.__dict__)
    child_instance.save()
    return child_instance


def render_paginate_list(request, object_list, template_name):
    """
    Render a paginated list of representatives
    """
    pagination_limits = (10, 20, 50, 100)
    num_by_page = request.GET.get('limit', 30)
    paginator = Paginator(object_list, num_by_page)
    number = request.GET.get('page', '1')
    number = int(number) if number.isdigit() else 1

    try:
        page = paginator.page(number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {}
    context['paginator'] = paginator
    context['page'] = page
    context['object_list'] = context['page'].object_list
    context['pagination_limits'] = pagination_limits

    return render(
        request,
        template_name,
        context
    )
