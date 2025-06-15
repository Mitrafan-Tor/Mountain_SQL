import os
import base64
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.files.base import ContentFile
from .models import User, Coords, Level, PerevalAdded, Image, PerevalImage


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

    def submit_pereval(self, data):
        """Основной метод для добавления данных о перевале"""
        try:
            self.validate_data(data)  # Проверяем валидность данных

            # Обработка изображений
            images_data = data.pop('images', [])

            # Создаем пользователя
            user_data = data.pop('user')
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults=user_data
            )

            # Создаем координаты
            coords = Coords.objects.create(**data.pop('coords'))

            # Создаем уровень сложности
            level = Level.objects.create(**data.pop('level'))

            # Создаем перевал
            pereval = PerevalAdded.objects.create(
                user=user,
                coords=coords,
                level=level,
                **data
            )

            # Добавляем изображения
            for img_data in images_data:
                img_format, img_str = img_data['data'].split(';base64,')
                ext = img_format.split('/')[-1]
                img_file = ContentFile(
                    base64.b64decode(img_str),
                    name=f"img_{pereval.id}_{img_data['title']}.{ext}"
                )
                image = Image.objects.create(
                    title=img_data['title'],
                    data=img_file
                )
                PerevalImage.objects.create(pereval=pereval, image=image)

            return {'status': 200, 'message': None, 'id': pereval.id}

        except ValidationError as e:
            return {'status': 400, 'message': str(e), 'id': None}
        except Exception as e:
            return {'status': 500, 'message': str(e), 'id': None}


    def get_pereval_by_id(self, pereval_id):
        """Получение данных о перевале по ID"""
        try:
            pereval = PerevalAdded.objects.get(id=pereval_id)
            return {
                'id': pereval.id,
                'beauty_title': pereval.beauty_title,
                'title': pereval.title,
                'other_titles': pereval.other_titles,
                'connect': pereval.connect,
                'add_time': pereval.add_time,
                'status': pereval.status,
                'user': {
                    'email': pereval.user.email,
                    'fam': pereval.user.fam,
                    'name': pereval.user.name,
                    'otc': pereval.user.otc,
                    'phone': pereval.user.phone
                },
                'coords': {
                    'latitude': pereval.coords.latitude,
                    'longitude': pereval.coords.longitude,
                    'height': pereval.coords.height
                },
                'level': {
                    'winter': pereval.level.winter,
                    'summer': pereval.level.summer,
                    'autumn': pereval.level.autumn,
                    'spring': pereval.level.spring
                },
                'images': [{
                    'title': img.title,
                    'data': img.data.url if img.data else None
                } for img in pereval.images.all()],
                'status': 200,
                'message': None
            }
        except ObjectDoesNotExist:
            return {'status': 404, 'message': 'Перевал не найден', 'id': None}

    def update_pereval(self, pereval_id, data):
        """Обновление данных о перевале"""
        try:
            pereval = PerevalAdded.objects.get(id=pereval_id)

            if pereval.status != 'new':
                return {'state': 0, 'message': 'Редактирование запрещено: запись не в статусе "new"'}

            # Проверяем, что пользователь не меняет свои данные
            user_data = data.get('user', {})
            if any(key in user_data for key in ['email', 'fam', 'name', 'otc', 'phone']):
                return {'state': 0, 'message': 'Редактирование персональных данных запрещено'}

            # Обновляем координаты
            if 'coords' in data:
                coords = pereval.coords
                coords_data = data['coords']
                coords.latitude = coords_data.get('latitude', coords.latitude)
                coords.longitude = coords_data.get('longitude', coords.longitude)
                coords.height = coords_data.get('height', coords.height)
                coords.save()

            # Обновляем уровень сложности
            if 'level' in data:
                level = pereval.level
                level_data = data['level']
                level.winter = level_data.get('winter', level.winter)
                level.summer = level_data.get('summer', level.summer)
                level.autumn = level_data.get('autumn', level.autumn)
                level.spring = level_data.get('spring', level.spring)
                level.save()

            # Обновляем основные данные перевала
            pereval.beauty_title = data.get('beauty_title', pereval.beauty_title)
            pereval.title = data.get('title', pereval.title)
            pereval.other_titles = data.get('other_titles', pereval.other_titles)
            pereval.connect = data.get('connect', pereval.connect)
            pereval.save()

            return {'state': 1, 'message': 'Запись успешно обновлена'}

        except ObjectDoesNotExist:
            return {'state': 0, 'message': 'Перевал не найден'}
        except Exception as e:
            return {'state': 0, 'message': str(e)}

    def get_perevals_by_email(self, email):
        """Получение списка перевалов по email пользователя"""
        try:
            user = User.objects.get(email=email)
            perevals = PerevalAdded.objects.filter(user=user)

            result = []
            for pereval in perevals:
                result.append({
                    'id': pereval.id,
                    'beauty_title': pereval.beauty_title,
                    'title': pereval.title,
                    'other_titles': pereval.other_titles,
                    'connect': pereval.connect,
                    'add_time': pereval.add_time,
                    'status': pereval.status,
                    'coords': {
                        'latitude': pereval.coords.latitude,
                        'longitude': pereval.coords.longitude,
                        'height': pereval.coords.height
                    },
                    'level': {
                        'winter': pereval.level.winter,
                        'summer': pereval.level.summer,
                        'autumn': pereval.level.autumn,
                        'spring': pereval.level.spring
                    },
                    'images': [{
                        'title': img.title,
                        'data': img.data.url if img.data else None
                    } for img in pereval.images.all()]
                })

            return {'status': 200, 'message': None, 'perevals': result}
        except User.DoesNotExist:
            return {'status': 404, 'message': 'Пользователь с таким email не найден', 'perevals': []}