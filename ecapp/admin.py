from django.contrib import admin
from .models import ItemModel, CartModel, CartItemModel

admin.site.register(ItemModel)
admin.site.register(CartModel)
admin.site.register(CartItemModel)