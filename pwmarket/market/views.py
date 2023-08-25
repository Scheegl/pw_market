from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Lots, SiteUser, Reply, News
from datetime import datetime
from .filters import LotsFilter
from .forms import LotsForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reply_form'] = ReplyForm()
        return context

    def post(self, request, *args, **kwargs):
        lot = self.get_object()
        reply_form = ReplyForm(request.POST)

        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.reply_user = self.request.user
            reply.reply_lots = lot
            reply.save()


            return HttpResponseRedirect(self.request.path_info)

        context = self.get_context_data(object=lot, reply_form=reply_form)
        return self.render_to_response(context)

@login_required
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

def lot_detail(request, lot_id):
    lot = get_object_or_404(Lots, pk=lot_id)
    replies = Reply.objects.filter(reply_lots=lot)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.reply_user = request.user
            reply.reply_lots = lot
            reply.save()
            return redirect('lot_detail', lot_id=lot_id)
    else:
        form = ReplyForm()

    return render(request, 'lot.html', {'lot': lot, 'replies': replies, 'form': form})