from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import PerevalAdded
from .data_manager import PerevalManager


class SubmitDataListAPI(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    manager = PerevalManager()

    @swagger_auto_schema(
        operation_id="submitData_create",
        operation_description="Создание новой записи о перевале",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'beauty_title': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'other_titles': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'connect': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'user': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                        'fam': openapi.Schema(type=openapi.TYPE_STRING),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'otc': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'phone': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    required=['email', 'fam', 'name', 'phone']
                ),
                'coords': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format='float'),
                        'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format='float'),
                        'height': openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                    required=['latitude', 'longitude', 'height']
                ),
                'level': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'winter': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'summer': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'autumn': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'spring': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                    }
                ),
                'images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'data': openapi.Schema(type=openapi.TYPE_STRING, format='binary'),
                            'title': openapi.Schema(type=openapi.TYPE_STRING),
                        },
                        required=['data', 'title']
                    )
                )
            },
            required=['beauty_title', 'title', 'user', 'coords', 'images']
        ),
        responses={
            201: openapi.Response('Created'),
            400: openapi.Response('Bad Request'),
            500: openapi.Response('Server Error')
        }
    )
    def post(self, request):
        result = self.manager.submit_pereval(request.data)
        return Response(result, status=result['status'])

    @swagger_auto_schema(
        operation_id="submitData_listByEmail",
        operation_description="Получение всех перевалов по email пользователя",
        manual_parameters=[
            openapi.Parameter(
                'user__email',
                openapi.IN_QUERY,
                description="Email пользователя",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            500: openapi.Response('Server Error')
        }
    )
    def get(self, request):
        email = request.query_params.get('user__email')
        if email:
            result = self.manager.get_perevals_by_email(email)
            return Response(result, status=result['status'])
        return Response(
            {'status': status.HTTP_400_BAD_REQUEST, 'message': 'Email не указан'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SubmitDataDetailAPI(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    manager = PerevalManager()

    @swagger_auto_schema(
        operation_id="submitData_retrieve",
        operation_description="Получение данных перевала по ID",
        responses={
            200: openapi.Response('OK'),
            404: openapi.Response('Not Found'),
            500: openapi.Response('Server Error')
        }
    )
    def get(self, request, pk):
        result = self.manager.get_pereval_by_id(pk)
        return Response(result, status=result['status'])

    @swagger_auto_schema(
        operation_id="submitData_update",
        operation_description="Обновление данных перевала по ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'beauty_title': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'other_titles': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'connect': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=[choice[0] for choice in PerevalAdded.StatusChoices.choices]
                ),
                'coords': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format='float'),
                        'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format='float'),
                        'height': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                ),
                'level': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'winter': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'summer': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'autumn': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'spring': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                    }
                ),
                'images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'data': openapi.Schema(type=openapi.TYPE_STRING, format='binary'),
                            'title': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    )
                )
            }
        ),
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
            404: openapi.Response('Not Found'),
            500: openapi.Response('Server Error')
        }
    )
    
    def patch(self, request, pk=None):
        manager = PerevalManager()
        result = manager.update_pereval(pk, request.data)
        status_code = 200 if result.get('state', 0) == 1 else 400
        return Response(result, status=status_code)
