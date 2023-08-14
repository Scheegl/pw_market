from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Lots, SiteUser, Reply, News
from datetime import datetime


class LotsList(ListView):
    model = Lots
    ordering = "title"
    template_name = "lots.html"
    context_object_name = "lots"
    paginate_by = 10


class LotsDetail(DetailView):
    model = Lots
    template_name = "lot.html"
    context_object_name = "lot"
