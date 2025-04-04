from django.urls import path
from apps.web import views

app_name = 'web'

urlpatterns = [
    path('items/', views.ItemListView.as_view(), name='item-list'),
]