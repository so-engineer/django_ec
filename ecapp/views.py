from django.shortcuts import render
from django.views.generic.list import ListView
from .models import ItemModel


class ItemList(ListView):
    template_name = 'list.html'
    model = ItemModel