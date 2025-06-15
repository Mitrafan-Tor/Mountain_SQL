from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Coords, Level, PerevalAdded, Image
from .data_manager import PerevalManager
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

    def test_submit_data_success(self):
        """Тест успешного добавления перевала"""
        result = self.manager.submit_data(self.pereval_data)
        self.assertEqual(result['status'], 200)
        self.assertIsNotNone(result['id'])

        # Проверяем, что данные сохранились в БД
        pereval = PerevalAdded.objects.get(id=result['id'])
        self.assertEqual(pereval.title, 'Тестовый перевал')
        self.assertEqual(pereval.user.email, 'test@example.com')

    def test_submit_data_missing_required(self):
        """Тест обработки отсутствия обязательных полей"""
        invalid_data = self.pereval_data.copy()
        del invalid_data['title']

        result = self.manager.submit_data(invalid_data)
        self.assertEqual(result['status'], 400)
        self.assertIn('Отсутствует обязательное поле', result['message'])

    def test_get_pereval_by_id(self):
        """Тест получения перевала по ID"""
        create_result = self.manager.submit_data(self.pereval_data)
        pereval_id = create_result['id']

        result = self.manager.get_pereval_by_id(pereval_id)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['title'], 'Тестовый перевал')

    def test_update_pereval_success(self):
        """Тест успешного обновления перевала"""
        create_result = self.manager.submit_data(self.pereval_data)
        pereval_id = create_result['id']

        update_data = {
            'title': 'Обновленное название',
            'level': {
                'winter': '2A'
            }
        }

        result = self.manager.update_pereval(pereval_id, update_data)
        self.assertEqual(result['state'], 1)

        # Проверяем обновленные данные
        pereval = PerevalAdded.objects.get(id=pereval_id)
        self.assertEqual(pereval.title, 'Обновленное название')
        self.assertEqual(pereval.level.winter, '2A')

    def test_update_pereval_wrong_status(self):
        """Тест попытки редактирования с неправильным статусом"""
        create_result = self.manager.submit_data(self.pereval_data)
        pereval = PerevalAdded.objects.get(id=create_result['id'])
        pereval.status = 'accepted'
        pereval.save()

        result = self.manager.update_pereval(pereval.id, {'title': 'Новое название'})
        self.assertEqual(result['state'], 0)
        self.assertIn('Редактирование запрещено', result['message'])

    def test_get_perevals_by_email(self):
        """Тест поиска перевалов по email пользователя"""
        self.manager.submit_data(self.pereval_data)

        result = self.manager.get_perevals_by_email('test@example.com')
        self.assertEqual(result['status'], 200)
        self.assertEqual(len(result['perevals']), 1)
        self.assertEqual(result['perevals'][0]['title'], 'Тестовый перевал')


class PerevalAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='api_test@example.com',
            fam='Петров',
            name='Иван',
            phone='+79001234567'
        )
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
        self.pereval = PerevalAdded.objects.create(
            beauty_title='пер.',
            title='API Тест',
            user=self.user,
            coords=self.coords,
            level=self.level
        )

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
        """Тест POST /api/submitData/"""
        response = self.client.post(
            reverse('submit-data'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)

    def test_get_pereval(self):
        """Тест GET /api/submitData/<id>/"""
        url = reverse('submit-data-detail', kwargs={'pk': self.pereval.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Тест')

    def test_update_pereval(self):
        """Тест PATCH /api/submitData/<id>/"""
        url = reverse('submit-data-detail', kwargs={'pk': self.pereval.id})
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
        """Тест GET /api/submitData/?user__email=email"""
        url = reverse('submit-data') + '?user__email=api_test@example.com'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['perevals']), 1)
        self.assertEqual(response.data['perevals'][0]['title'], 'API Тест')

    def test_invalid_data(self):
        """Тест обработки невалидных данных"""
        invalid_data = self.valid_payload.copy()
        del invalid_data['title']

        response = self.client.post(
            reverse('submit-data'),
            data=json.dumps(invalid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)