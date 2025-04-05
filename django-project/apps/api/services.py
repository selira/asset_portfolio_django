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

def get_initial_quantities() -> list[dict]:
    """
    Get the initial quantities of each asset in the portfolio.
    """
    initial_date = '2022-02-15'
    initial_portfolio_value = Decimal('1000000000')
    initial_quantities = []
    portfolios = Portfolio.objects.all()
    prices = AssetPrice.objects.filter(date=initial_date)
    
    for portfolio in portfolios:
        weights = PortfolioAssetWeight.objects.filter(portfolio=portfolio, date=initial_date)
        for weight in weights:
            asset = weight.asset
            price = prices.filter(asset_id=asset.id).first()
            if price:
                initial_quantity = (initial_portfolio_value * weight.weight) / price.price
                initial_quantities.append({
                    'quantity': initial_quantity.quantize(Decimal('0.001')) if initial_quantity > 0 else Decimal('0.000'),
                    'portfolio': portfolio.name,
                    'asset': asset.name,
                })
    return initial_quantities