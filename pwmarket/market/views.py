from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Lots, SiteUser, Reply, News
from datetime import datetime
from .filters import LotsFilter
from .forms import LotsForm


class LotsList(ListView):
    model = Lots
    ordering = "title"
    template_name = "lots.html"
    context_object_name = "lots"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = LotsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class LotsDetail(DetailView):
    model = Lots
    template_name = "lot.html"
    context_object_name = "lot"


def create_lots(request):
    form = LotsForm()
    if request.method == 'POST':
        form = LotsForm(request.LOTS)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lots/')
    return render(request, 'lots_edit.html', {'form': form})


class LotsCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = LotsForm
    model = Lots
    template_name = 'lots_edit.html'


class LotsUpdate(UpdateView):
    form_class = LotsForm
    model = Lots
    template_name = 'lots_edit.html'


class LotsDelete(DeleteView):
    model = Lots
    template_name = 'lots_delete.html'
    success_url = reverse_lazy('lots_list')
