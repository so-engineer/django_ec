from django.contrib import admin

from .models import (
    BillModel,
    BuyItemModel,
    CartItemModel,
    CartModel,
    ItemModel,
    PromoCodeModel,
)

admin.site.register(ItemModel)
admin.site.register(CartModel)
admin.site.register(CartItemModel)
admin.site.register(BillModel)
admin.site.register(BuyItemModel)
admin.site.register(PromoCodeModel)
