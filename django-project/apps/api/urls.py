from django.urls import path
from apps.api.views import ItemListApi

urlpatterns = [
    path('items/', ItemListApi.as_view(), name='item-list'),
]