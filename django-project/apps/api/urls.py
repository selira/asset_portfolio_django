from django.urls import path
from apps.api.views import ItemListApi
from apps.api.views import PortfolioHistoryApi

urlpatterns = [
    path('items/', ItemListApi.as_view(), name='item-list'),
    path('portfolio/history/', PortfolioHistoryApi.as_view(), name='portfolio-history'),
]