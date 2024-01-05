from django.db import models


class ItemModel(models.Model):
    name = models.CharField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    item_image = models.ImageField(upload_to="", null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class CartModel(models.Model):
    def __str__(self):
        return self.id
    
    # カートの商品を全て取得
    def cart_item_all(self):
        return self.cart_items.all()
    
    # カートの商品数を算定
    def cart_item_count(self):
        return self.cart_items.count()
    
    # カートの合計金額を算定
    def cart_item_price(self):
        total_price = 0
        for cart_item in self.cart_item_all():
            total_price += cart_item.item.price
        return total_price
    
class CartItemModel(models.Model):
    # 中間テーブルの作成
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE, related_name='item_carts')

    def __str__(self):
        return f"{self.cart}_{self.item}"
    
class BillModel(models.Model):
    firstname = models.CharField(null=True, blank=True)
    lastname = models.CharField(null=True, blank=True)
    username = models.CharField(null=True, blank=True)
    email = models.CharField(null=True, blank=True)
    address = models.CharField(null=True, blank=True)
    address2 = models.CharField(null=True, blank=True)
    country = models.CharField(null=True, blank=True)
    state = models.CharField(null=True, blank=True)
    zip = models.CharField(null=True, blank=True)
    same_address = models.CharField(null=True, blank=True)
    save_info = models.CharField(null=True, blank=True)
    cc_name = models.CharField(null=True, blank=True)
    cc_number = models.CharField(null=True, blank=True)
    cc_expiration = models.CharField(null=True, blank=True)
    cc_cvv = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.firstname
    
class BuyItemModel(models.Model):
    bill = models.ForeignKey(BillModel, on_delete=models.CASCADE, null=True, blank=True, related_name='bill_buys')

    name = models.CharField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    # item_image = models.ImageField(upload_to="", null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.bill_id
    
class PromoCodeModel(models.Model):
    code = models.CharField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.code