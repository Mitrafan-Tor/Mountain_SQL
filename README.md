# Pereval API

## Документация API
- Интерактивная документация: [/swagger/](http://127.0.0.1:8000/swagger/)
- ReDoc: [/redoc/](http://127.0.0.1:8000/redoc/)

## Запуск проекта
```bash
python manage.py runserver
```

## Основные эндпоинты
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/submitData/` | Добавить новый перевал |
| GET | `/api/submitData/<id>/` | Получить перевал по ID |
| PATCH | `/api/submitData/<id>/` | Редактировать перевал |
| GET | `/api/submitData/?user__email=<email>` | Список перевалов пользователя |

## Переменные окружения
```ini
FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_LOGIN=postgres
FSTR_DB_PASS=your_password
```