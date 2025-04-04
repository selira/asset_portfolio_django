from typing import List
from apps.api.models import Item

def item_list() -> List[dict]:
    items = Item.objects.all()
    
    return [{
        'id': item.id,
        'name': item.name,
        'description': item.description
    } for item in items]