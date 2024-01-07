from django.urls import path
from .views import ItemList, ItemDetail, BillCreate, \
     cart_func, add_to_cart_from_list_func, add_to_cart_from_detail_func, remove_from_cart_func, \
     AdmItemList, AdmItemCreate, AdmItemUpdate, AdmItemDelete, AdmBuyList, AdmBuyDetail
# ベーシック認証用
from basicauth.decorators import basic_auth_required

urlpatterns = [
    path('', ItemList.as_view(), name='list'),
    path('detail/<int:pk>', ItemDetail.as_view(), name='detail'),
    path('checkout/cart/', cart_func, name='checkout_cart'),
    path('checkout/add_list/<int:pk>', add_to_cart_from_list_func, name='checkout_add_list'),
    path('checkout/add_detail/<int:pk>', add_to_cart_from_detail_func, name='checkout_add_detail'),
    path('checkout/remove/<int:pk>', remove_from_cart_func, name='checkout_remove'),
    path('checkout/bill/', BillCreate.as_view(), name="checkout_bill"),

    path('adm/items/', basic_auth_required(AdmItemList.as_view()), name="adm_list"),
    path('adm/items/create/', basic_auth_required(AdmItemCreate.as_view()), name="adm_create"),
    path('adm/items/update/<int:pk>', basic_auth_required(AdmItemUpdate.as_view()), name="adm_update"),
    path('adm/items/delete/<int:pk>', basic_auth_required(AdmItemDelete.as_view()), name="adm_delete"),
    path('adm/bills/', basic_auth_required(AdmBuyList.as_view()), name="adm_buy_list"),
    path('adm/bills/<int:pk>/items/', basic_auth_required(AdmBuyDetail.as_view()), name="adm_buy_detail"),

]
