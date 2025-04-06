from django.urls import path
from apps.web import views

app_name = 'web'

urlpatterns = [
    path('items/', views.ItemListView.as_view(), name='item-list'),
    path('portfolio/history/', views.PortfolioHistoryView.as_view(), name='portfolio-history'),
]