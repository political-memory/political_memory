# coding: utf-8

from copy import copy

from django import http

import unicodecsv as csv


class ActiveLegislatureMixin(object):
    """
    Mixin for views that can switch between active legislature and all data
    """

    default_active_only = True

    def get(self, *args, **kwargs):
        self.set_active_only()
        return super(ActiveLegislatureMixin, self).get(*args, **kwargs)

    def override_active_only(self):
        """
        Redefine this method to override active legislature selection
        - return None to enable user choice
        - return True or False to disable user choice and set active state
        """
        return None

    def set_active_only(self):
        if 'active_only' in self.request.GET:
            self.request.session['active_only'] = \
                self.request.GET['active_only'] == '1'
        elif 'active_only' not in self.request.session:
            self.request.session['active_only'] = self.default_active_only

    def get_active_only(self):
        overriden = self.override_active_only()
        if overriden is None:
            if 'active_only' in self.request.session:
                return self.request.session['active_only']
            else:
                return self.default_active_only
        else:
            return overriden

    def get_context_data(self, **kwargs):
        c = super(ActiveLegislatureMixin, self).get_context_data(**kwargs)
        if self.override_active_only() is None:
            c['active_only'] = self.get_active_only()
        return c


class SortMixin(object):
    """
    Mixin for views that allow sorting.
    The sort_fields attribute should be defined to a {field: label} dict
    containing all fields usable for sorting.
    The sort_default and sort_default_dir attributes should contain the default
    sorting settings.
    """
    sort_fields = {}
    sort_default_field = None
    sort_default_dir = 'asc'

    def get(self, *args, **kwargs):
        self.set_sorting()
        return super(SortMixin, self).get(*args, **kwargs)

    def set_sorting(self):
        if 'sort_by' in self.request.GET:
            self.request.session['sort_by'] = self.request.GET['sort_by']
        elif 'sort_by' not in self.request.session:
            self.request.session['sort_by'] = self.sort_default_field

        if self.request.session['sort_by'] not in self.sort_fields:
            self.request.session['sort_by'] = self.sort_default_field

        if 'sort_dir' in self.request.GET:
            self.request.session['sort_dir'] = self.request.GET['sort_dir']
        elif 'sort_dir' not in self.request.session:
            self.request.session['sort_dir'] = self.sort_default_dir

    def get_context_data(self, **kwargs):
        c = super(SortMixin, self).get_context_data(**kwargs)

        c['sort_querystring'] = copy(self.request.GET)
        if 'sort_by' in c['sort_querystring']:
            del c['sort_querystring']['sort_by']
        if 'sort_dir' in c['sort_querystring']:
            del c['sort_querystring']['sort_dir']

        c['sort'] = {
            'fields': self.sort_fields,
            'field': self.request.session['sort_by'],
            'dir': self.request.session['sort_dir'],
        }
        return c

    def get_queryset(self):
        qs = super(SortMixin, self).get_queryset()
        if self.request.session['sort_by']:
            qs = qs.order_by('%s%s' % (
                '-' if self.request.session['sort_dir'] == 'desc' else '',
                self.request.session['sort_by']))
        return qs


class PaginationMixin(object):
    pagination_limits = (12, 24, 48, 96)

    def get(self, *args, **kwargs):
        self.set_paginate_by()
        return super(PaginationMixin, self).get(*args, **kwargs)

    def set_paginate_by(self):
        if 'paginate_by' in self.request.GET:
            self.request.session['paginate_by'] = \
                self.request.GET['paginate_by']

        elif 'paginate_by' not in self.request.session:
            self.request.session['paginate_by'] = 12

    def get_paginate_by(self, queryset):
        return self.request.session['paginate_by']

    def get_page_range(self, page):
        pages = []

        if page and page.paginator.num_pages != 1:
            for i in page.paginator.page_range:
                if page.number - 4 < i < page.number + 4:
                    pages.append(i)

        return pages

    def get_context_data(self, **kwargs):
        c = super(PaginationMixin, self).get_context_data(**kwargs)
        c['pagination_limits'] = self.pagination_limits
        c['paginate_by'] = self.request.session['paginate_by']
        c['page_range'] = self.get_page_range(c['page_obj'])
        c['pagination_querystring'] = copy(self.request.GET)
        if 'page' in c['pagination_querystring']:
            del c['pagination_querystring']['page']
        return c


class GridListMixin(object):
    def set_session_display(self):
        if self.request.GET.get('display') in ('grid', 'list'):
            self.request.session['display'] = self.request.GET.get('display')

        if 'display' not in self.request.session:
            self.request.session['display'] = 'grid'

    def get(self, *args, **kwargs):
        self.set_session_display()
        return super(GridListMixin, self).get(*args, **kwargs)

    def get_template_names(self):
        return [t.replace('_list', '_%s' % self.request.session['display'])
                for t in super(GridListMixin, self).get_template_names()]

    def get_context_data(self, **kwargs):
        c = super(GridListMixin, self).get_context_data(**kwargs)
        c['grid_list'] = True
        return c


class CSVDownloadMixin(object):
    def get_context_data(self, **kwargs):
        c = super(CSVDownloadMixin, self).get_context_data(**kwargs)
        c['csv'] = True
        c['csv_querystring'] = copy(self.request.GET)
        return c

    def get_paginate_by(self, queryset):
        if self.request.GET.get('csv', None) is None:
            return super(CSVDownloadMixin, self).get_paginate_by(queryset)
        return None

    def render_to_csv_response(self, context, **kwargs):
        response = http.HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        for result in self.get_csv_results(context, **kwargs):
            writer.writerow(self.get_csv_row(result))

        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (
            self.csv_name)

        return response

    def render_to_response(self, context, **kwargs):
        if self.request.GET.get('csv', None) is None:
            return super(CSVDownloadMixin, self).render_to_response(
                context, **kwargs)

        return self.render_to_csv_response(context, **kwargs)
