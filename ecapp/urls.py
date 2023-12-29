from django.urls import path, include
from .views import ItemList, ItemDetail

urlpatterns = [
    path('', ItemList.as_view(), name='list'),
    path('detail/<int:pk>', ItemDetail.as_view(), name='detail'),
]
