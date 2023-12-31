from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import ItemModel, CartModel, CartItemModel
# from django.contrib.sessions.models import Session

# herokuログ確認
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError

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
        context['session_count'] = self.request.session.get('cart_item_count')
        return context

class ItemDetail(DetailView):
    template_name = 'detail.html'
    model = ItemModel

    # メソッドをオーバーライドしURLから取得されるオブジェクトに加えて最新のDBデータを取得する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 最新のDBデータをコンテキストに追加
        context['latest_item'] = ItemModel.objects.latest('id')
        context['session_count'] = self.request.session.get('cart_item_count')
        return context
    
def cart_func(request):
    # カート情報を取得
    cart_object = get_cart_info(request)

    # カートアイテムとカートアイテム数を取得
    cart_items = cart_object.cart_items.all()
    cart_item_count = cart_object.cart_items.all().count()

    # カートアイテムの数をセッションに保存
    request.session['cart_item_count'] = cart_item_count

    total_price = 0
    # カートの商品数と合計金額を算定
    for cart_item in cart_items:
        total_price += cart_item.item.price
    context = {"session_count": cart_item_count, "cart_items": cart_items, "total_price": total_price}
    return render(request, 'checkout.html', context)

def add_to_cart_from_list_func(request, pk):
    # カート情報を取得
    cart_object = get_cart_info(request)

    # 商品オブジェクトを作成
    item_object = get_object_or_404(ItemModel, id=pk)

    # 中間オブジェクトを作成
    cart_item_object= CartItemModel.objects.create(cart=cart_object, item=item_object)
    cart_item_object.save()

    # カートアイテムの数を取得
    cart_item_count = cart_object.cart_items.all().count()

    # カートアイテムの数をセッションに保存
    request.session['cart_item_count'] = cart_item_count
    return redirect("list")

def add_to_cart_from_detail_func(request, pk):
    # カート情報を取得
    cart_object = get_cart_info(request)

    # 商品オブジェクトを作成
    item_object = get_object_or_404(ItemModel, id=pk)

    # カートへの追加数量を取得
    quantity = int(request.POST.get('quantity', 1))

    # カートへの追加数量分だけ中間オブジェクトを作成
    for _ in range(quantity):
        cart_item_object= CartItemModel.objects.create(cart=cart_object, item=item_object)
        cart_item_object.save()

    # カートアイテムの数を取得
    cart_item_count = cart_object.cart_items.all().count()

    # カートアイテムの数をセッションに保存
    request.session['cart_item_count'] = cart_item_count
    return redirect("detail", pk) # pk忘れずに

# 各メソッドで共通となるカート情報を返す
def get_cart_info(request):
    cart_id = request.session.get('cart_id')

    if cart_id:
        cart_object = CartModel.objects.get(id=cart_id)
    else:
        cart_object = CartModel.objects.create()
        cart_object.save()
        # セッションにカートIDを保存
        request.session['cart_id'] = cart_object.id

    return cart_object

def remove_from_cart_func(request, pk):
    # カート情報を取得
    cart_object = get_cart_info(request)

    # カートアイテムからpkに一致する最初のデータを削除
    cart_object.cart_items.filter(item__id=pk).first().delete()

    # セッションを更新
    cart_item_count = cart_object.cart_items.all().count()
    request.session['cart_item_count'] = cart_item_count
    return redirect("checkout_cart")
    