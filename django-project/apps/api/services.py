from apps.api.models import PortfolioAssetWeight
from django.db import transaction
from decimal import Decimal
from django.core.exceptions import ValidationError

@transaction.atomic
def transfer_between_assets(*, 
    portfolio_id: int, 
    from_asset_id: int, 
    to_asset_id: int, 
    amount: Decimal
) -> dict:
    """
    Transfer amount between assets within the same portfolio.
    """
    initial_date = '2022-02-15'

    if from_asset_id == to_asset_id:
        raise ValidationError("No se puede transferir entre el mismo activo.")
    
    # Get current weights
    weights = PortfolioAssetWeight.objects.select_for_update().filter(
        portfolio_id=portfolio_id,
        date=initial_date
    )
    
    from_weight = weights.get(asset_id=from_asset_id)
    to_weight = weights.get(asset_id=to_asset_id)
    
    # Calculate actual amount in dollars
    total_portfolio_value = Decimal('1000000000')
    from_asset_value = total_portfolio_value * from_weight.weight
    
    if from_asset_value < amount:
        raise ValidationError(
            f"Monto insuficiente en activo. Disponible: ${from_asset_value.quantize(Decimal('0.01'))}, Requerido: ${amount}"
        )
    
    # Calculate new weights
    new_from_value = from_asset_value - amount
    new_to_value = (total_portfolio_value * to_weight.weight) + amount
    
    # Update weights
    from_weight.weight = new_from_value / total_portfolio_value
    to_weight.weight = new_to_value / total_portfolio_value
    
    from_weight.save()
    to_weight.save()
    
    return {
        'status': 'success',
        'message': f'Venta de ${amount} de {from_weight.asset.name} y compra de ${amount} de {to_weight.asset.name}',
        'new_weights': {
            'from': float(from_weight.weight),
            'to': float(to_weight.weight)
        }
    }
