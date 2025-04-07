from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.api.selectors import get_portfolio_history, get_initial_amounts
from apps.api.services import transfer_between_assets
    
class PortfolioHistoryApi(APIView):
    def get(self, request):
        initial_date = request.query_params.get('fecha_inicio')
        final_date = request.query_params.get('fecha_fin')
        portfolio_id = request.query_params.get('portfolio_id')
        if not initial_date or not final_date or not portfolio_id:
            return Response({"error": "Initial_date, final_date and portfolio ID are required "}, status=status.HTTP_400_BAD_REQUEST)
        history = get_portfolio_history(initial_date, final_date, portfolio_id)
        if not history:
            return Response({"error": "No data found for the given date range."}, status=status.HTTP_404_NOT_FOUND)
        return Response(history, status=status.HTTP_200_OK)

class AssetTransferApi(APIView):
    def post(self, request):
        try:
            result = transfer_between_assets(
                portfolio_id=int(request.data.get('portfolio')),
                from_asset_id=int(request.data.get('venta')),
                to_asset_id=int(request.data.get('compra')),
                amount=Decimal(str(request.data.get('monto')))
            )
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response(
                {'error': 'An unexpected error occurred'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class InitialAmountsApi(APIView):
    def get(self, request):
        assets, portfolios, portfolio_amounts = get_initial_amounts()
        return Response({
            'assets': [asset.name for asset in assets],
            'portfolios': [portfolio.name for portfolio in portfolios],
            'portfolio_amounts': portfolio_amounts
        }, status=status.HTTP_200_OK)