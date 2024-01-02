from django.contrib import admin
from .models import ItemModel, CartModel, CartItemModel, BillModel

admin.site.register(ItemModel)
admin.site.register(CartModel)
admin.site.register(CartItemModel)
admin.site.register(BillModel)