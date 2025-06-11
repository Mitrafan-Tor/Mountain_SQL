from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import User, Coords, Level, PerevalAdded, Image, PerevalImage
import os


class PerevalManager:
    # ... существующие методы ...

    def get_pereval_by_id(self, pereval_id):
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
                'images': [{'title': img.title, 'data': str(img.img)}
                           for img in pereval.images.all()],
                'status': 200,
                'message': None
            }
        except ObjectDoesNotExist:
            return {'status': 404, 'message': 'Перевал не найден', 'id': None}

    def update_pereval(self, pereval_id, data):
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
                    }
                })

            return {'status': 200, 'message': None, 'perevals': result}
        except User.DoesNotExist:
            return {'status': 404, 'message': 'Пользователь с таким email не найден', 'perevals': []}