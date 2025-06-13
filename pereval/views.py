from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .data_manager import PerevalManager
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SubmitDataAPI(APIView):
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        operation_description="Добавление нового перевала",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'beauty_title': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'user': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'fam': openapi.Schema(type=openapi.TYPE_STRING),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'phone': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
                'coords': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'latitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'longitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'height': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                ),
                'level': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'winter': openapi.Schema(type=openapi.TYPE_STRING),
                        'summer': openapi.Schema(type=openapi.TYPE_STRING),
                        'autumn': openapi.Schema(type=openapi.TYPE_STRING),
                        'spring': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            },
            required=['title', 'user', 'coords']
        ),
        responses={
            200: openapi.Response('Success'),
            400: openapi.Response('Bad Request'),
            500: openapi.Response('Server Error')
        }
    )
    def post(self, request):
        manager = PerevalManager()
        result = manager.submit_data(request.data)
        return Response(result, status=result['status'])

    @swagger_auto_schema(
        operation_description="Получение данных о перевале по ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID перевала",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response('Success'),
            404: openapi.Response('Not Found')
        }
    )
    def get(self, request, pk=None):
        if pk:
            manager = PerevalManager()
            result = manager.get_pereval_by_id(pk)
            return Response(result, status=result.get('status', 200))