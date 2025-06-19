from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Coords, Level, PerevalAdded, Image
from .data_manager import PerevalManager
import json
import base64


class PerevalManagerTest(TestCase):
    def setUp(self):
        self.manager = PerevalManager()

        # Создаем тестового пользователя
        self.user = User.objects.create(
            email='test@example.com',
            fam='Иванов',
            name='Петр',
            otc='Сергеевич',
            phone='+79001234567'
        )

        # Создаем тестовые координаты
        self.coords = Coords.objects.create(
            latitude=45.3842,
            longitude=7.1525,
            height=1200
        )

        # Создаем тестовый уровень сложности
        self.level = Level.objects.create(
            winter='1A',
            summer='1A',
            autumn='1A',
            spring=''
        )

        # Создаем тестовый перевал
        self.pereval = PerevalAdded.objects.create(
            beauty_title='пер.',
            title='Тестовый перевал',
            other_titles='Тест',
            connect='соединяет',
            user=self.user,
            coords=self.coords,
            level=self.level
        )

        # Создаем тестовое изображение
        self.image = Image.objects.create(
            title='Фото 1',
            data='pereval_images/test.jpg'
        )

        # Связываем изображение с перевалом
        self.pereval.images.add(self.image)

        # Данные для создания нового перевала
        self.pereval_data = {
            'beauty_title': 'пер.',
            'title': 'Новый перевал',
            'other_titles': 'Тест',
            'connect': 'соединяет реки',
            'user': {
                'email': 'new@example.com',
                'fam': 'Сидоров',
                'name': 'Алексей',
                'otc': 'Иванович',
                'phone': '+79007654321'
            },
            'coords': {
                'latitude': 46.0000,
                'longitude': 91.0000,
                'height': 1600
            },
            'level': {
                'winter': '',
                'summer': '1A',
                'autumn': '',
                'spring': ''
            },
            'images': [
                {
                    'title': 'Фото 1',
                    'data': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
                }
            ]
        }

    def test_submit_pereval_success(self):
        """Тест успешного добавления перевала"""
        result = self.manager.submit_pereval(self.pereval_data)
        self.assertEqual(result['status'], 200)
        self.assertIsNotNone(result['id'])

    def test_get_pereval_by_id(self):
        """Тест получения перевала по ID"""
        result = self.manager.get_pereval_by_id(self.pereval.id)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['title'], 'Тестовый перевал')

    def test_update_pereval_success(self):
        """Тест успешного обновления перевала"""
        update_data = {'title': 'Обновленный перевал'}
        result = self.manager.update_pereval(self.pereval.id, update_data)
        self.assertEqual(result['state'], 1)
        self.assertEqual(result['message'], 'Запись успешно обновлена')

    def test_update_pereval_not_new_status(self):
        """Тест запрета обновления перевала не в статусе 'new'"""
        self.pereval.status = 'accepted'
        self.pereval.save()

        update_data = {'title': 'Обновленный перевал'}
        result = self.manager.update_pereval(self.pereval.id, update_data)
        self.assertEqual(result['state'], 0)
        self.assertIn('Редактирование запрещено', result['message'])

    def test_get_perevals_by_email(self):
        """Тест поиска перевалов по email"""
        result = self.manager.get_perevals_by_email('test@example.com')
        self.assertEqual(result['status'], 200)
        self.assertEqual(len(result['perevals']), 1)
        self.assertEqual(result['perevals'][0]['title'], 'Тестовый перевал')


class PerevalAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем тестового пользователя
        self.user = User.objects.create(
            email='api_test@example.com',
            fam='Петров',
            name='Иван',
            phone='+79001234567'
        )

        # Создаем тестовые координаты
        self.coords = Coords.objects.create(
            latitude=45.0000,
            longitude=90.0000,
            height=1500
        )

        # Создаем тестовый уровень сложности
        self.level = Level.objects.create(
            winter='1A',
            summer='1B',
            autumn='1A',
            spring=''
        )

        # Создаем тестовый перевал
        self.pereval = PerevalAdded.objects.create(
            beauty_title='пер.',
            title='API Тест',
            user=self.user,
            coords=self.coords,
            level=self.level
        )

        # Данные для POST запроса
        self.valid_payload = {
            'beauty_title': 'пер.',
            'title': 'Новый перевал',
            'other_titles': 'Тест',
            'connect': 'соединяет реки',
            'user': {
                'email': 'new@example.com',
                'fam': 'Сидоров',
                'name': 'Алексей',
                'otc': 'Иванович',
                'phone': '+79007654321'
            },
            'coords': {
                'latitude': 46.0000,
                'longitude': 91.0000,
                'height': 1600
            },
            'level': {
                'winter': '',
                'summer': '1A',
                'autumn': '',
                'spring': ''
            },
            'images': [
                {
                    'title': 'Фото 1',
                    'data': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
                }
            ]
        }

    def test_create_pereval(self):
        """Тест создания нового перевала через API"""
        url = '/api/submitData/'
        response = self.client.post(
            url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)

    def test_get_pereval(self):
        """Тест получения данных о перевале"""
        url = f'/api/submitData/{self.pereval.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Тест')

    def test_update_pereval(self):
        """Тест обновления данных перевала"""
        url = f'/api/submitData/{self.pereval.id}/'
        update_data = {'title': 'Обновленный API Тест'}

        response = self.client.patch(
            url,
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 1)

        # Проверяем обновление в БД
        updated = PerevalAdded.objects.get(id=self.pereval.id)
        self.assertEqual(updated.title, 'Обновленный API Тест')

    def test_search_by_email(self):
        """Тест поиска по email"""
        url = '/api/submitData/?user__email=api_test@example.com'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['perevals']), 1)
        self.assertEqual(response.data['perevals'][0]['title'], 'API Тест')

    def test_invalid_data(self):
        """Тест обработки невалидных данных"""
        url = '/api/submitData/'
        invalid_data = self.valid_payload.copy()
        del invalid_data['title']  # Удаляем обязательное поле

        response = self.client.post(
            url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)