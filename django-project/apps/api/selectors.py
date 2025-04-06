from typing import List, Dict, Any
from apps.api.models import Item, PortfolioAssetWeight, AssetPrice, Portfolio
from decimal import Decimal

def item_list() -> List[dict]:
    items = Item.objects.all()
    
    return [{
        'id': item.id,
        'name': item.name,
        'description': item.description
    } for item in items]

def get_initial_quantities(portfolio_id: int) -> List[dict]:
    """
    Get the initial quantities of each asset in the portfolio.
    """
    initial_date = '2022-02-15'
    initial_portfolio_value = Decimal('1000000000')
    
    # Get all weights and prices in a single query each
    weights = (PortfolioAssetWeight.objects
        .filter(
            portfolio_id=portfolio_id, 
            date=initial_date
        )
        .select_related('asset')  # Prefetch asset data
    )
    
    # Get all relevant asset prices at once
    asset_ids = [weight.asset_id for weight in weights]
    prices = {
        price.asset_id: price.price 
        for price in AssetPrice.objects.filter(
            date=initial_date,
            asset_id__in=asset_ids
        )
    }
    
    initial_quantities = []
    for weight in weights:
        price = prices.get(weight.asset_id)
        if price:
            initial_quantity = (
                initial_portfolio_value * weight.weight / price
            ).quantize(Decimal('0.00000001')) # precision necessary to mantain consistency.
            
            initial_quantities.append({
                'quantity': initial_quantity if initial_quantity > 0 else Decimal('0.000'),
                'asset': weight.asset.name,
                'asset_id': weight.asset_id,
            })
    
    return initial_quantities

def get_portfolio_history(initial_date: str, final_date: str, portfolio_id: int) -> Dict[str, Any]:
    """
    Get the weight and portfolio value history of each asset in the portfolio.
    """
    if not initial_date or not final_date:
        return []
    
    # Get initial quantities once
    quantities = {
        q['asset_id']: q 
        for q in get_initial_quantities(portfolio_id) 
        if q['quantity'] > 0
    }
    
    # Fetch all prices at once and organize by date and asset
    prices = (AssetPrice.objects
        .filter(
            date__range=[initial_date, final_date],
            asset_id__in=quantities.keys()
        )
        .select_related('asset')  # Avoid additional queries for asset names
        .order_by('date')
    )
    
    # Pre-organize prices by date and asset_id
    prices_by_date = {}
    for price in prices:
        if price.date not in prices_by_date:
            prices_by_date[price.date] = {}
        prices_by_date[price.date][price.asset_id] = price

    weight_history = {}
    portfolio_history = {}

    # Process all dates
    for date, date_prices in prices_by_date.items():
        portfolio_value = Decimal('0.000')
        amounts = []
        formatted_date = date.strftime('%Y-%m-%d')
        weight_history[formatted_date] = {}

        # Calculate portfolio value
        for asset_id, price in date_prices.items():
            if asset_id in quantities:
                quantity = quantities[asset_id]['quantity']
                amount = price.price * quantity
                portfolio_value += amount
                amounts.append({
                    'asset': quantities[asset_id]['asset'],
                    'amount': amount
                })

        # Store portfolio value
        portfolio_history[formatted_date] = portfolio_value.quantize(Decimal('0.01'), rounding='ROUND_HALF_UP')

        # Calculate weights
        for amount in amounts:
            weight = amount['amount'] / portfolio_value if portfolio_value else Decimal('0.000')
            weight_history[formatted_date][amount['asset']] = (
                weight.quantize(Decimal('0.000001')) # check consistency with graph height.
                if weight > 0 
                else Decimal('0.000')
            )

    return {
        'weights': weight_history,
        'portfolio_value': portfolio_history
    }