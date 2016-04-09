# coding: utf-8
from django import http

import unicodecsv as csv


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
