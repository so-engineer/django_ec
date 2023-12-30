from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import ItemModel
# from django.contrib.sessions.models import Session

from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError

# herokuログ確認
@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)

class ItemList(ListView):
    template_name = 'list.html'
    model = ItemModel
    # メソッドをオーバーライドし商品をid順に取得する
    def get_queryset(self):
        return ItemModel.objects.all().order_by('id')
    
    # メソッドをオーバーライドしURLから取得されるオブジェクトに加えてセッション数を取得する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # セッション数をコンテキストに追加
        # context['session_count'] = Session.objects.count() # 重複が削除されるためNG
        context['session_count'] = get_cart_count(self.request)
        return context

class ItemDetail(DetailView):
    template_name = 'detail.html'
    model = ItemModel

    # メソッドをオーバーライドしURLから取得されるオブジェクトに加えて最新のDBデータを取得する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 最新のDBデータをコンテキストに追加
        context['latest_item'] = ItemModel.objects.latest('id')
        context['session_count'] = get_cart_count(self.request)
        return context
    
def cart_func(request):
    cart = request.session.get('cart', [])
    items = []
    total_price = 0
    # カートの商品数と合計金額を算定
    for cart_pk in cart:
        items.append(get_object_or_404(ItemModel, pk=cart_pk))
        total_price += get_object_or_404(ItemModel, pk=cart_pk).price
    context = {"session_count": len(items), "items": items, "total_price": total_price}

    return render(request, 'checkout.html', context)

def add_to_cart_from_list_func(request, pk):
    # セッションのカートを取得、なければ新しく作成
    cart = request.session.get('cart', [])
    cart.append(pk)
    # カートをセッションに保存
    request.session['cart'] = cart
    return redirect("list")

def add_to_cart_from_detail_func(request, pk):
    # カートへの追加数量を取得
    quantity = int(request.POST.get('quantity', 1))
    # セッションのカートを取得、なければ新しく作成
    cart = request.session.get('cart', [])
    # 商品IDをカートに追加
    for _ in range(quantity):
        cart.append(pk)
    # カートをセッションに保存
    request.session['cart'] = cart
    return redirect("detail", pk) # pk忘れずに

# カート数を返す
def get_cart_count(request):
    cart = request.session.get('cart')
    return len(cart)

def remove_from_cart_func(request, pk):
    cart = request.session.get('cart', [])
    # リストから最初に見つかった特定の要素を削除
    cart.remove(pk)
    # セッションを更新
    request.session['cart'] = cart
    return redirect("checkout_cart")
    