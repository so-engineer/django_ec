from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ItemModel, CartModel, CartItemModel, BillModel, BuyDetailModel
# from django.contrib.sessions.models import Session
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail

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
        if self.request.session.get('cart_item_count') is None:
            context['cart_item_count'] = 0
        else:
            context['cart_item_count'] = self.request.session.get('cart_item_count')
        return context

class ItemDetail(DetailView):
    template_name = 'detail.html'
    model = ItemModel

    # メソッドをオーバーライドしURLから取得されるオブジェクトに加えて最新のDBデータを取得する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 最新のDBデータをコンテキストに追加
        context['latest_item'] = ItemModel.objects.latest('id')

        # セッション数をコンテキストに追加 
        if self.request.session.get('cart_item_count') is None:
            context['cart_item_count'] = 0
        else:
            context['cart_item_count'] = self.request.session.get('cart_item_count')
        return context
    
def cart_func(request):
    # カート情報を取得
    cart_object = get_cart_info(request)

    # カートアイテムとカートアイテム数を取得
    cart_items = cart_object.cart_item_all()
    cart_item_count = cart_object.cart_item_count()

    # カートアイテムの数をセッションに保存
    request.session['cart_item_count'] = cart_item_count

    # カートの商品数と合計金額を算定
    total_price = cart_object.cart_item_price()
    context = {"cart_item_count": cart_item_count, "cart_items": cart_items, "total_price": total_price}
    return render(request, 'checkout.html', context)

def add_to_cart_from_list_func(request, pk):
    # カート情報を取得
    cart_object = get_cart_info(request)

    # 商品オブジェクトを作成
    item_object = get_object_or_404(ItemModel, id=pk)

    # 中間オブジェクトを作成
    cart_item_object= CartItemModel.objects.create(cart=cart_object, item=item_object)

    # カートアイテムの数を取得
    cart_item_count = cart_object.cart_item_count()

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
        CartItemModel.objects.create(cart=cart_object, item=item_object)

    # カートアイテムの数を取得
    cart_item_count = cart_object.cart_item_count()

    # カートアイテムの数をセッションに保存
    request.session['cart_item_count'] = cart_item_count
    return redirect("detail", pk) # pk忘れずに

# 各メソッドで共通となるカート情報を返す
def get_cart_info(request):
    cart_id = request.session.get('cart_id')

    if cart_id:
        # cart_object = CartModel.objects.get(id=cart_id)
        cart_object = get_object_or_404(CartModel, id=cart_id)
    else:
        cart_object = CartModel.objects.create()
        # セッションにカートIDを保存
        request.session['cart_id'] = cart_object.id

    return cart_object

def remove_from_cart_func(request, pk):
    # カート情報を取得
    cart_object = get_cart_info(request)

    # カートアイテムからpkに一致する最初のデータを削除
    cart_object.cart_items.filter(item__id=pk).first().delete()

    # セッションを更新
    cart_item_count = cart_object.cart_item_count()
    request.session['cart_item_count'] = cart_item_count
    return redirect("checkout_cart")
    
def bill_flash(request):
    # flashメッセージの設定
    messages.success(request, '購入ありがとうございます')
    # 他にも messages.info, messages.warning, messages.error が利用可能

def create_buy_list(request, pk):
    # カート情報を取得
    cart_object = get_cart_info(request)
    cart_items = cart_object.cart_item_all()

    for cart_item in cart_items:
        BuyDetailModel.objects.create(bill_id = pk, name=cart_item.item.name, content=cart_item.item.content, price=cart_item.item.price)

def send_email(request, email):
    # メール送信
    send_mail(
    'テストメールの件名',
    'テストメールの本文。',
    'xxx@gmail.com',  # 送信元アドレス
    [email],  # 受信者のアドレスリスト
    fail_silently=False, # メール送信時に何か問題が発生した場合にはエラーが発生
    )

def delete_cart(request):
    # カート情報を取得
    cart_object = get_cart_info(request)

    # カート内のアイテムをすべて削除
    cart_object.cart_items.all().delete()

    # カート情報をセッションから削除
    del request.session['cart_id']
    del request.session['cart_item_count']

class BillCreate(CreateView):
    template_name = "checkout.html"
    model = BillModel
    # ブラウザで表示させるフィールド
    fields = ("firstname", "lastname", "username", "email", "address", "address2", "country", "state", \
              "zip", "same_address", "save_info", "cc_name", "cc_number", "cc_expiration", "cc_cvv")
    success_url = reverse_lazy("list")

    # メソッドをオーバーライドしform情報を取得する
    def form_valid(self, form):
        response = super().form_valid(form)
        # flashメッセージの取得
        bill_flash(self.request)
        # 購入明細を作成
        # self.objectは作成されたBillModelオブジェクトを参照
        create_buy_list(self.request, self.object.pk)
        # メール送信
        send_email(self.request, self.object.email)
        # カートを削除
        delete_cart(self.request)

        return response


# 以下管理者用の設定
class AdmItemList(ListView):
    template_name = 'adm/list.html'
    model = ItemModel

    # メソッドをオーバーライドし商品をid順に取得する
    def get_queryset(self):
        return ItemModel.objects.all().order_by('id')
    
    # メソッドをオーバーライドしURLから取得されるオブジェクトに加えてセッション数を取得する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # セッション数をコンテキストに追加
        # context['session_count'] = Session.objects.count() # 重複が削除されるためNG
        if self.request.session.get('cart_item_count') is None:
            context['cart_item_count'] = 0
        else:
            context['cart_item_count'] = self.request.session.get('cart_item_count')
        return context
    
class AdmItemCreate(CreateView):
    template_name = "adm/create.html"
    model = ItemModel
    # ブラウザで表示させるフィールド
    fields = ("name", "price", "item_image", "content")
    success_url = reverse_lazy("adm_list")

class AdmItemUpdate(UpdateView):
    template_name = "adm/update.html"
    model = ItemModel
    # ブラウザで表示させるフィールド
    fields = ("name", "price", "item_image", "content")
    success_url = reverse_lazy("adm_list")

class AdmItemDelete(DeleteView):
    # template_name = "adm/delete.html"
    model = ItemModel
    success_url = reverse_lazy('adm_list')

    # メソッドをオーバーライドしテンプレートに遷移せず直接商品を削除する
    def delete(self, request, *args, **kwargs):
        item_object = self.get_object()
        item_object.delete()
        return redirect(AdmItemDelete.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(self, request, *args, **kwargs)

class AdmBuyList(ListView):
    template_name = 'adm/buy_list.html'
    model = BillModel

    # メソッドをオーバーライドし購入明細をid順に取得する
    def get_queryset(self):
        return BillModel.objects.all().order_by('id')

class AdmBuyDetail(ListView):
    template_name = 'adm/buy_detail.html'
    model = BuyDetailModel

    # メソッドをオーバーライドしbill_idに紐付く購入明細のオブジェクトを取得する
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return BuyDetailModel.objects.filter(bill_id=pk)
