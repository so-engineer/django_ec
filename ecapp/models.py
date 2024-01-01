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
    