from django.urls import path, include
from .views import ItemList

urlpatterns = [
    path('', ItemList.as_view()),
]
