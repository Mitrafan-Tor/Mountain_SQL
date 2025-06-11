from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .data_manager import PerevalManager


class SubmitDataAPI(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        """Пример обработки GET-запроса"""
        return Response({
            "message": "Используйте POST-запрос для отправки данных",
            "example_request": {
                "beauty_title": "пер.",
                "title": "Название перевала",
                "coords": {
                    "latitude": "45.3842",
                    "longitude": "7.1525",
                    "height": "1200"
                },
                "level": {
                    "winter": "",
                    "summer": "1А",
                    "autumn": "1А",
                    "spring": ""
                }
            }
        }, status=200)

    def post(self, request):
        """Обработка POST-запроса"""
        manager = PerevalManager()
        result = manager.submit_pereval(request.data)
        return Response(result, status=result['status'])