from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.selectors import item_list
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