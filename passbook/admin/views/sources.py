"""passbook Source administration"""
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, ListView, UpdateView

from passbook.admin.mixins import AdminRequiredMixin
from passbook.core.models import Source
from passbook.lib.utils.reflection import path_to_class


class SourceListView(AdminRequiredMixin, ListView):
    """Show list of all sources"""

    model = Source
    template_name = 'administration/source/list.html'

    def get_context_data(self, **kwargs):
        kwargs['types'] = {
            x.__name__: x._meta.verbose_name for x in Source.__subclasses__()}
        return super().get_context_data(**kwargs)


class SourceCreateView(SuccessMessageMixin, AdminRequiredMixin, CreateView):
    """Create new Source"""

    template_name = 'generic/create.html'
    success_url = reverse_lazy('passbook_admin:sources')
    success_message = _('Successfully created Source')

    def get_form_class(self):
        source_type = self.request.GET.get('type')
        model = next(x if x.__name__ == source_type else None for x in Source.__subclasses__())
        return path_to_class(model.form)


class SourceUpdateView(SuccessMessageMixin, AdminRequiredMixin, UpdateView):
    """Update source"""

    model = Source
    template_name = 'generic/update.html'
    success_url = reverse_lazy('passbook_admin:sources')
    success_message = _('Successfully updated Source')

    def get_form_class(self):
        form_class_path = self.get_object().form
        form_class = path_to_class(form_class_path)
        return form_class

    def get_object(self, queryset=None):
        obj = Source.objects.get(pk=self.kwargs.get('pk'))
        return obj.cast()
