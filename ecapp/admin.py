from django.contrib import admin
from .models import ItemModel, BillModel

admin.site.register(ItemModel)
admin.site.register(BillModel)