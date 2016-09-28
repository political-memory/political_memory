from django.views import generic

from .forms import PositionForm


class PositionFormMixin(generic.View):
    """
    Mixin for class views that handle a position form (should be all full-page
    views, ie. all template views that use a templates that extends base.html).

    We don't use a FormView here to allow usage of this mixin in views that
    have their own form.
    """

    position_form = None
    position_created = False

    def post(self, request, *args, **kwargs):
        if 'position-representative' in request.POST:
            self.position_form = PositionForm(request.POST, prefix='position')
            if self.position_form.is_valid():
                self.position_form.save()
                self.position_form = None
                self.position_created = True

        return self.get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        c = super(PositionFormMixin, self).get_context_data(**kwargs)

        c['position_form'] = \
            self.position_form or PositionForm(prefix='position')
        c['position_created'] = self.position_created

        return c
