from django.views.generic import ListView
from apps.api.models import Item

class ItemListView(ListView):
    model = Item
    template_name = 'items.html'
    context_object_name = 'items'