# coding: utf-8

from copy import copy

from django import http

import unicodecsv as csv


class ThemeSelectionMixin(object):
    """
    Mixin for views that allow selecting a theme
    """

    def get(self, *args, **kwargs):
        self.set_selected_theme()
        return super(ThemeSelectionMixin, self).get(*args, **kwargs)

    def set_selected_theme(self):
        if 'selected_theme' in self.request.GET:
            theme = self.request.GET['selected_theme']
            self.request.session['selected_theme'] = \
                theme if len(theme) else None
        elif 'selected_theme' not in self.request.session:
            self.request.session['selected_theme'] = None

    def get_selected_theme(self):
        if 'selected_theme' in self.request.session:
            return self.request.session['selected_theme']
        else:
            return None

    def get_context_data(self, **kwargs):
        c = super(ThemeSelectionMixin, self).get_context_data(**kwargs)
        c['selected_theme'] = self.get_selected_theme()
        c['theme_querystring'] = copy(self.request.GET)
        if 'selected_theme' in c['theme_querystring']:
            del c['theme_querystring']['selected_theme']
        return c


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
    The sort_modes attribute should be defined to a dict as such:
    {
        'mode1': {
            'order': 42,
            'label': 'mode label',
            'fields': ['-field1', 'field2', ...]
        },
        ...
    }

    The sort_default attribute should contain the default sorting mode.
    """
    sort_modes = {}
    sort_default = None
    sort_session_prefix = ''

    def get(self, *args, **kwargs):
        self.set_sorting()
        return super(SortMixin, self).get(*args, **kwargs)

    def _session_get_sort(self):
        k = '%s_sort' % self.sort_session_prefix
        return self.request.session[k]

    def _session_set_sort(self, value):
        k = '%s_sort' % self.sort_session_prefix
        self.request.session[k] = value

    def _session_sort_exists(self):
        k = '%s_sort' % self.sort_session_prefix
        return k in self.request.session

    def set_sorting(self):
        if 'sort' in self.request.GET:
            self._session_set_sort(self.request.GET['sort'])
        elif not self._session_sort_exists():
            self._session_set_sort(self.sort_default)

        if self._session_get_sort() not in self.sort_modes:
            self._session_set_sort(self.sort_default)

    def get_context_data(self, **kwargs):
        c = super(SortMixin, self).get_context_data(**kwargs)

        c['sort_querystring'] = copy(self.request.GET)
        if 'sort' in c['sort_querystring']:
            del c['sort_querystring']['sort']

        c['sort'] = {
            'modes': [{'id': k, 'label': v['label'], 'order': v['order']}
                      for k, v in self.sort_modes.iteritems()],
            'mode': self._session_get_sort()
        }
        return c

    def get_queryset(self):
        qs = super(SortMixin, self).get_queryset()
        if self._session_get_sort() in self.sort_modes:
            mode = self.sort_modes[self._session_get_sort()]
            qs = qs.order_by(*mode['fields'])
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
