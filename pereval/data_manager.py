import os
from django.core.exceptions import ValidationError
from .models import *


class PerevalManager:
    @staticmethod
    def get_db_config():
        """Получение конфигурации БД из переменных окружения"""
        return {
            'host': os.getenv('FSTR_DB_HOST', 'localhost'),
            'port': os.getenv('FSTR_DB_PORT', '5432'),
            'login': os.getenv('FSTR_DB_LOGIN', 'postgres'),
            'password': os.getenv('FSTR_DB_PASS', 'postgres'),
        }

    @staticmethod
    def validate_data(data):
        """Валидация входящих данных"""
        required_fields = [
            'beauty_title', 'title', 'other_titles', 'connect',
            'user', 'coords', 'level', 'images'
        ]

        for field in required_fields:
            if field not in data:
                raise ValidationError(f'Отсутствует обязательное поле: {field}')

        user_fields = ['email', 'fam', 'name', 'otc', 'phone']
        for field in user_fields:
            if field not in data['user']:
                raise ValidationError(f'Отсутствует обязательное поле пользователя: {field}')

        coord_fields = ['latitude', 'longitude', 'height']
        for field in coord_fields:
            if field not in data['coords']:
                raise ValidationError(f'Отсутствует обязательное поле координат: {field}')

        level_fields = ['winter', 'summer', 'autumn', 'spring']
        for field in level_fields:
            if field not in data['level']:
                raise ValidationError(f'Отсутствует обязательное поле уровня сложности: {field}')

        if not isinstance(data['images'], list) or len(data['images']) == 0:
            raise ValidationError('Должна быть хотя бы одна фотография')

    def submit_data(self, data):
        """Основной метод для добавления данных о перевале"""
        try:
            # Валидация данных
            self.validate_data(data)

            # Получаем или создаем пользователя
            user, created = User.objects.get_or_create(
                email=data['user']['email'],
                defaults={
                    'fam': data['user']['fam'],
                    'name': data['user']['name'],
                    'otc': data['user']['otc'],
                    'phone': data['user']['phone'],
                }
            )

            # Создаем координаты
            coords = Coords.objects.create(
                latitude=data['coords']['latitude'],
                longitude=data['coords']['longitude'],
                height=data['coords']['height'],
            )

            # Создаем уровень сложности
            level = Level.objects.create(
                winter=data['level']['winter'],
                summer=data['level']['summer'],
                autumn=data['level']['autumn'],
                spring=data['level']['spring'],
            )

            # Создаем перевал
            pereval = PerevalAdded.objects.create(
                beauty_title=data['beauty_title'],
                title=data['title'],
                other_titles=data.get('other_titles', ''),
                connect=data.get('connect', ''),
                user=user,
                coords=coords,
                level=level,
            )

            # Добавляем изображения
            for img_data in data['images']:
                image = Image.objects.create(
                    data=img_data['data'].encode(),
                    title=img_data['title'],
                )
                PerevalImage.objects.create(pereval=pereval, image=image)

            return {
                'status': 200,
                'message': None,
                'id': pereval.id,
            }

        except ValidationError as e:
            return {
                'status': 400,
                'message': str(e),
                'id': None,
            }
        except Exception as e:
            return {
                'status': 500,
                'message': f'Ошибка при сохранении данных: {str(e)}',
                'id': None,
            }