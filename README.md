# 🏔️ Mountain Passes API (ФСТР Перевалы)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-success.svg)](https://swagger.io)

REST API для мобильного приложения туристов. Позволяет добавлять, редактировать и просматривать информацию о горных перевалах с модерацией данных.

## 📌 Оглавление

- [Быстрый старт](#-быстрый-старт)
- [Документация API](#-документация-api)
- [Примеры запросов](#-примеры-запросов)
- [Технологии](#-технологии)
- [Разработчики](#-разработчики)
- [Лицензия](#-лицензия)

## 🚀 Быстрый старт

### Требования
- Python 3.9+
- Django 4.2+
- PostgreSQL 13+
- Pillow 10.3+ (для работы с изображениями)

### 🖼️ Работа с изображениями
API поддерживает загрузку изображений в формате base64. Пример структуры:

```json
{
  "images": [
    {
      "title": "Название фото",
      "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg..."
    }
  ]
}
```
### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/transit_point.git
cd transit_point
Создайте виртуальное окружение:

bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
.\venv\Scripts\activate   # Windows
Установите зависимости:

bash
pip install -r requirements.txt
Настройте базу данных:

sql
CREATE DATABASE pereval 
ENCODING 'UTF8'
LC_COLLATE 'en_US.UTF-8'
LC_CTYPE 'en_US.UTF-8';
Создайте файл .env:

ini
FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_LOGIN=postgres
FSTR_DB_PASS=yourpassword
SECRET_KEY=yoursecretkey
DEBUG=True
Примените миграции:

bash
python manage.py migrate
Запустите сервер:

bash
python manage.py runserver
API будет доступно по адресу: http://localhost:8000/api/
```
### 📚 Документация API
Интерактивная документация:

Swagger UI: /swagger/

```ReDoc: /redoc/

Основные эндпоинты
Метод	Путь	Описание
POST	/api/submitData/	Добавить новый перевал
GET	/api/submitData/<id>/	Получить данные перевала
PATCH	/api/submitData/<id>/	Редактировать перевал (только статус "new")
GET	/api/submitData/?user__email=<email>	Список перевалов пользователя 
```
💡 Примеры запросов
1. Добавление перевала (POST)
```bash
curl -X POST "http://localhost:8000/api/submitData/" \
-H "Content-Type: application/json" \
-d '{
  "beauty_title": "пер.",
  "title": "Пхия",
  "other_titles": "Перевал ветров",
  "connect": "соединяет долины",
  "user": {
    "email": "user@example.com",
    "fam": "Иванов",
    "name": "Иван",
    "otc": "Петрович",
    "phone": "+79001234567"
  },
  "coords": {
    "latitude": 45.3842,
    "longitude": 7.1525,
    "height": 1200
  },
  "level": {
    "winter": "1A",
    "summer": "",
    "autumn": "1B",
    "spring": "2A"
  },
  "images": [
    {
      "title": "Вид с перевала",
      "data": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
    }
  ]
}'
```
2. Получение данных (GET)

```bash
curl "http://localhost:8000/api/submitData/1/"
```
3. Поиск по email (GET)
```bash
curl "http://localhost:8000/api/submitData/?user__email=user@example.com"
```
### 🛠 Технологии
```markdown 
Backend: Django 4.2 + Django REST Framework

База данных: PostgreSQL

Документация: Swagger/OpenAPI 3.0

Аутентификация: [JWT] (планируется)

Кэширование: Redis

Хранение изображений: файловая система (через Django ImageField)

Обработка изображений: Pillow

Валидация: Django Model Validators
```

### 🧪 Тестирование
Для запуска тестов:
```bash
python manage.py test pereval.tests -v 2
```

### 👨‍💻 Разработчик
### [Дмитрий Анатольевич Торжиков] - [dim.ka77@mail.ru]

### 📜 Лицензия
Этот проект распространяется под лицензией MIT.

Примечание: Для production-окружения установите DEBUG=False в .env и настройте WSGI-сервер (Gunicorn + Nginx).

**Примечание для Windows**:
- Используйте PowerShell или Git Bash
- Замените `source venv/bin/activate` на `.\venv\Scripts\activate`