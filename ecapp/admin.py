from django.contrib import admin
from .models import ItemModel, CartModel, CartItemModel, BillModel, BuyItemModel, PromoCodeModel

admin.site.register(ItemModel)
admin.site.register(CartModel)
admin.site.register(CartItemModel)
admin.site.register(BillModel)
admin.site.register(BuyItemModel)
admin.site.register(PromoCodeModel)