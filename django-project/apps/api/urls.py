from django.urls import path
from apps.api.views import PortfolioHistoryApi, AssetTransferApi, InitialAmountsApi

urlpatterns = [
    path('portfolio/history/', PortfolioHistoryApi.as_view(), name='portfolio-history'),
    path('transfer/', AssetTransferApi.as_view(), name='asset-transfer'),
    path('amounts/', InitialAmountsApi.as_view(), name='amounts'),
]