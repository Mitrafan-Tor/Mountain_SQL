# API Documentation

## Swagger UI
Документация API доступна через Swagger UI:  
`http://yourdomain.com/swagger/`

## Endpoints

### 1. Добавление нового перевала
`POST /api/submitData/`

**Пример запроса:**
```json
{
  "beauty_title": "пер.",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "user": {
    "email": "user@example.com",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"
  },
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
  },
  "images": [
    {"data": "<картинка1>", "title": "Седловина"},
    {"data": "<картинка>", "title": "Подъём"}
  ]
}
```

**Пример ответа:**
```json
{
  "status": 200,
  "message": null,
  "id": 42
}
```

### 2. Получение данных о перевале
`GET /api/submitData/<id>/`

**Пример ответа:**
```json
{
  "id": 42,
  "beauty_title": "пер.",
  "title": "Пхия",
  "status": "new",
  "user": {
    "email": "user@example.com",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"
  },
  "coords": {
    "latitude": 45.3842,
    "longitude": 7.1525,
    "height": 1200
  },
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": [
    {"title": "Седловина", "data": "..."},
    {"title": "Подъём", "data": "..."}
  ]
}
```

### 3. Редактирование перевала
`PATCH /api/submitData/<id>/`

**Ограничения:**
- Можно редактировать только записи со статусом "new"
- Нельзя изменять персональные данные пользователя

**Пример запроса:**
```json
{
  "title": "Новое название",
  "level": {
    "summer": "2А"
  }
}
```

**Пример ответа:**
```json
{
  "state": 1,
  "message": "Запись успешно обновлена"
}
```

### 4. Получение всех перевалов пользователя
`GET /api/submitData/?user__email=<email>`

**Пример ответа:**
```json
{
  "status": 200,
  "message": null,
  "perevals": [
    {
      "id": 42,
      "beauty_title": "пер.",
      "title": "Пхия",
      "status": "new"
    },
    {
      "id": 43,
      "beauty_title": "пер.",
      "title": "Джантуган",
      "status": "accepted"
    }
  ]
}
```

## Коды ответов
- 200 - Успешный запрос
- 400 - Неверные параметры запроса
- 404 - Запись не найдена
- 500 - Ошибка сервера
