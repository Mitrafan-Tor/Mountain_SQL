from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from .models import User, Coords, Level, PerevalAdded, Image
from .data_manager import PerevalManager
from .views import SubmitDataAPI
import json


class PerevalManagerTest(TestCase):
    def setUp(self):
        self.manager = PerevalManager()
        self.user_data = {
            'email': 'test@example.com',
            'fam': 'Иванов',
            'name': 'Петр',
            'otc': 'Сергеевич',
            'phone': '+79001234567'
        }
        self.pereval_data = {
            'beauty_title': 'пер.',
            'title': 'Тестовый перевал',
            'other_titles': 'Тест',
            'connect': '',
            'user': self.user_data,
            'coords': {
                'latitude': 45.3842,
                'longitude': 7.1525,
                'height': 1200
            },
            'level': {
                'winter': '1A',
                'summer': '1A',
                'autumn': '1A',
                'spring': ''
            },
            'images': [
                {'title': 'Фото 1', 'data': 'base64encodedstring1'},
                {'title': 'Фото 2', 'data': 'base64encodedstring2'}
            ]
        }

    def test_submit_pereval_success(self):
        """Тест успешного добавления перевала"""
        result = self.manager.submit_pereval(self.pereval_data)
        self.assertEqual(result['status'], 200)
        self.assertIsNotNone(result['id'])

        pereval = PerevalAdded.objects.get(id=result['id'])
        self.assertEqual(pereval.title, 'Тестовый перевал')

    def test_get_pereval_by_id(self):
        """Тест получения перевала по ID"""
        # Сначала создаем тестовые данные
        user = User.objects.create(**self.user_data)
        coords = Coords.objects.create(**self.pereval_data['coords'])
        level = Level.objects.create(**self.pereval_data['level'])
        pereval = PerevalAdded.objects.create(
            beauty_title=self.pereval_data['beauty_title'],
            title=self.pereval_data['title'],
            user=user,
            coords=coords,
            level=level
        )

        result = self.manager.get_pereval_by_id(pereval.id)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['title'], 'Тестовый перевал')

    def test_update_pereval_success(self):
        """Тест успешного обновления перевала"""
        # Создаем тестовые данные
        user = User.objects.create(**self.user_data)
        coords = Coords.objects.create(**self.pereval_data['coords'])
        level = Level.objects.create(**self.pereval_data['level'])
        pereval = PerevalAdded.objects.create(
            beauty_title=self.pereval_data['beauty_title'],
            title=self.pereval_data['title'],
            user=user,
            coords=coords,
            level=level
        )

        update_data = {'title': 'Новое название'}
        result = self.manager.update_pereval(pereval.id, update_data)
        self.assertEqual(result['state'], 1)

        updated = PerevalAdded.objects.get(id=pereval.id)
        self.assertEqual(updated.title, 'Новое название')

    def test_get_perevals_by_email(self):
        """Тест поиска перевалов по email"""
        user = User.objects.create(**self.user_data)
        coords = Coords.objects.create(**self.pereval_data['coords'])
        level = Level.objects.create(**self.pereval_data['level'])
        PerevalAdded.objects.create(
            beauty_title=self.pereval_data['beauty_title'],
            title=self.pereval_data['title'],
            user=user,
            coords=coords,
            level=level
        )

        result = self.manager.get_perevals_by_email('test@example.com')
        self.assertEqual(result['status'], 200)
        self.assertEqual(len(result['perevals']), 1)


class PerevalAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

        # Создаем тестового пользователя
        self.user = User.objects.create(
            email='api_test@example.com',
            fam='Петров',
            name='Иван',
            phone='+79001234567'
        )

        # Создаем тестовые координаты и уровень
        self.coords = Coords.objects.create(
            latitude=45.0000,
            longitude=90.0000,
            height=1500
        )
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
            'user': {
                'email': 'new@example.com',
                'fam': 'Сидоров',
                'name': 'Алексей',
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
            }
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