from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ItemModel


class ItemList(ListView):
    template_name = 'list.html'
    model = ItemModel
    # メソッドをオーバーライドし商品をid順に取得する
    def get_queryset(self):
        return ItemModel.objects.all().order_by('id')

class ItemDetail(DetailView):
    template_name = 'detail.html'
    model = ItemModel

    # メソッドをオーバーライドしURLから取得されるオブジェクトに加えて最新のDBデータを取得する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_item'] = ItemModel.objects.latest('id')
        return context