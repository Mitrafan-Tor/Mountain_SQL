from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .data_manager import PerevalManager
from django.shortcuts import get_object_or_404
from .models import PerevalAdded
from rest_framework import status


class SubmitDataAPI(APIView):
    parser_classes = [JSONParser]

    # POST /submitData/
    def post(self, request):
        manager = PerevalManager()
        result = manager.submit_data(request.data)
        return Response(result, status=result['status'])

    # GET /submitData/<id>/
    def get(self, request, pk=None):
        if pk:
            # Получение одной записи по ID
            manager = PerevalManager()
            result = manager.get_pereval_by_id(pk)
            return Response(result, status=result.get('status', status.HTTP_200_OK))
        else:
            # Фильтрация по email пользователя
            user_email = request.query_params.get('user__email', None)
            if user_email:
                manager = PerevalManager()
                result = manager.get_perevals_by_email(user_email)
                return Response(result, status=result.get('status', status.HTTP_200_OK))
            return Response({'message': 'Не указан email пользователя'}, status=status.HTTP_400_BAD_REQUEST)

    # PATCH /submitData/<id>/
    def patch(self, request, pk=None):
        if not pk:
            return Response({'message': 'Требуется ID перевала'}, status=status.HTTP_400_BAD_REQUEST)

        manager = PerevalManager()
        result = manager.update_pereval(pk, request.data)
        return Response(result, status=result.get('status', status.HTTP_200_OK))