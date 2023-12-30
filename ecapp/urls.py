from django.urls import path
from .views import ItemList, ItemDetail, cart_func, add_to_cart_from_list_func, add_to_cart_from_detail_func, remove_from_cart_func

urlpatterns = [
    path('', ItemList.as_view(), name='list'),
    path('detail/<int:pk>', ItemDetail.as_view(), name='detail'),
    path('checkout/cart/', cart_func, name='checkout_cart'),
    path('checkout/add_list/<int:pk>', add_to_cart_from_list_func, name='checkout_add_list'),
    path('checkout/add_detail/<int:pk>', add_to_cart_from_detail_func, name='checkout_add_detail'),
    path('checkout/remove/<int:pk>', remove_from_cart_func, name='checkout_remove'),
    # path('checkout/bill/', bill_func, name='checkout_bill'),
]
