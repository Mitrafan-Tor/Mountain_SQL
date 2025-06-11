from rest_framework.views import APIView
from rest_framework.response import Response
from .data_manager import PerevalManager
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SubmitDataAPI(APIView):
    @swagger_auto_schema(
        operation_description="Добавление нового перевала",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'user', 'coords', 'level'],
            properties={
                'beauty_title': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                # ... остальные поля ...
            },
        ),
        responses={
            200: openapi.Response('Success', examples={
                'application/json': {
                    "status": 200,
                    "message": None,
                    "id": 42
                }
            }),
            400: 'Bad Request',
            500: 'Server Error'
        }
    )
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