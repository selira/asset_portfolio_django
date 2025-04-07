from django.urls import path
from apps.web import views

app_name = 'web'

urlpatterns = [
    path('', views.PortfolioView.as_view(), name='root'),
    path('history/', views.PortfolioHistoryView.as_view(), name='portfolio-history'),
    path('trade/', views.AssetTradeView.as_view(), name='asset-trade'),
]