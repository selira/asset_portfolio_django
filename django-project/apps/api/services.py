from apps.api.models import Item, PortfolioAssetWeight, AssetPrice, Portfolio
from decimal import Decimal

def item_create(*, name: str, description: str = '') -> dict:
    item = Item.objects.create(
        name=name,
        description=description
    )
    
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description
    }
