from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.selectors import item_list, get_portfolio_history
from apps.api.services import item_create

class ItemListApi(APIView):
    def get(self, request):
        items = item_list()
        return Response(items, status=status.HTTP_200_OK)

    def post(self, request):
        item = item_create(
            name=request.data.get('name'),
            description=request.data.get('description')
        )
        return Response(item, status=status.HTTP_201_CREATED)
    
class PortfolioHistoryApi(APIView):
    def get(self, request):
        initial_date = request.query_params.get('fecha_inicio')
        final_date = request.query_params.get('fecha_fin')
        portfolio_id = request.query_params.get('portfolio_id')
        print(request.query_params)
        print(initial_date, final_date, portfolio_id)
        if not initial_date or not final_date or not portfolio_id:
            return Response({"error": "Initial_date, final_date and portfolio ID are required "}, status=status.HTTP_400_BAD_REQUEST)
        history = get_portfolio_history(initial_date, final_date, portfolio_id)
        if not history:
            return Response({"error": "No data found for the given date range."}, status=status.HTTP_404_NOT_FOUND)
        return Response(history, status=status.HTTP_200_OK)