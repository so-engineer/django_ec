from django.urls import path, include
from .views import ItemList

urlpatterns = [
    path('list/', ItemList.as_view()),
]
