from django.urls import path
from apps.api.views import PortfolioHistoryApi, AssetTransferApi

urlpatterns = [
    path('portfolio/history/', PortfolioHistoryApi.as_view(), name='portfolio-history'),
    path('transfer/', AssetTransferApi.as_view(), name='asset-transfer'),
]