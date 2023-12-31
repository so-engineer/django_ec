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
    