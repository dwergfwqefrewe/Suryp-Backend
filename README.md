# Syrup Chat Backend

## Описание

Syrup Chat — это серверная часть чат-приложения, реализованная на FastAPI с поддержкой WebSocket (Socket.IO), JWT-аутентификацией, хранением истории сообщений, лайков, комментариев и пользователей в базе данных (SQLite через SQLAlchemy).

---

## Структура проекта

```
backend/
  ├── api/                # Основная логика API
  │   ├── router.py       # Главный роутер, объединяющий все маршруты
  │   └── routers/        # Отдельные модули роутеров (auth, user, message, ...)
  ├── config.py           # Конфигурация приложения (настройки, переменные окружения)
  ├── database/           # Работа с базой данных
  │   ├── config.py       # Подключение к БД, создание engine, Base, Session
  │   └── managers/       # CRUD-менеджеры для моделей
  ├── exceptions.py       # Кастомные исключения
  ├── main.py             # Точка входа FastAPI-приложения
  ├── models/             # SQLAlchemy-модели (User, Message, History, ...)
  ├── run.py              # Альтернативный запуск через uvicorn
  ├── schemas/            # Pydantic-схемы для валидации и сериализации
  ├── socket io/          # Реализация Socket.IO (ASGI)
  │   └── app/
  │       ├── main.py     # Точка входа для запуска с сокетами
  │       └── sockets.py  # Логика обработки событий Socket.IO
  └── requirements.txt    # Зависимости проекта
```

---

## Основные компоненты

### 1. FastAPI-приложение (`main.py`)
- Инициализация FastAPI с настройками из `config.py`.
- Подключение CORS.
- Создание таблиц при запуске.
- Подключение главного роутера (`api/router.py`).
- Эндпоинт `/health` для проверки статуса сервера.

### 2. Роутеры (`api/routers/`)
- **auth.py** — регистрация, вход, выход, обновление токенов (JWT, cookies).
- **user.py** — получение/обновление/удаление профиля пользователя.
- **message.py** — получение чатов пользователя.
- **comment.py** — CRUD для комментариев к историям.
- **history.py** — CRUD для историй (постов).
- **like.py** — лайки к историям.

### 3. Модели (`models/`)
- **User** — пользователь (id, login, password_hash, role, avatar_url, about, связи с историями, комментариями, лайками).
- **Message** — сообщение (id, sender_id, receiver_id, text, timestamp).
- **History** — история/пост (id, title, description, likes, created_at, updated_at, author_id, связи с комментариями и лайками).
- **Comment** — комментарий (id, content, created_at, updated_at, user_id, history_id).
- **HistoryLike** — лайк к истории (id, user_id, history_id, created_at).

### 4. Менеджеры (`database/managers/`)
- **BaseManager** — базовые CRUD-операции для моделей.
- **UserManager** — работа с пользователями (поиск по логину, проверка данных).
- **MessageManager** — сохранение сообщений, получение истории переписки, чатов.
- **CommentManager, HistoryManager, LikeManager** — CRUD для соответствующих сущностей.

### 5. Socket.IO (`socket io/app/`)
- **main.py** — точка входа для запуска с поддержкой сокетов.
- **sockets.py** — обработка событий: connect, disconnect, join, message, typing, get_history. Хранение подключённых пользователей, рассылка сообщений, история переписки.

### 6. Исключения (`exceptions.py`)
- Кастомные HTTP-исключения для типовых ошибок (не найдено, аутентификация, права, валидация, БД).

---

## Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/dwergfwqefrewe/Suryp-Backend.git
   cd backend
   ```
2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Запустите сервер:**
   - Через обычный FastAPI:
     ```bash
     uvicorn main:app --reload
     ```
   - С поддержкой Socket.IO:
     ```bash
     python run.py
     ```

---

## Переменные окружения

Все основные настройки можно переопределить через `.env` (см. `config.py`).

- `app_name` — название приложения
- `debug` — режим отладки
- `database_url` — строка подключения к БД
- `jwt_secret_key`, `jwt_algorithm`, `jwt_access_token_expire_minutes`, `jwt_refresh_token_expire_days` — настройки JWT
- `cors_origins` — список разрешённых источников CORS
- `host`, `port` — адрес и порт сервера

---

## Примеры API

- **Регистрация:** `POST /auth/register`
- **Вход:** `POST /auth/login`
- **Обновить токен:** `POST /auth/refresh`
- **Выйти:** `POST /auth/logout`
- **Профиль:** `GET /user/me`, `PATCH /user/me`, `DELETE /user/me`
- **Истории:** `POST /history/`, `GET /history/`, `GET /history/{id}`, `PUT /history/{id}`, `DELETE /history/{id}`
- **Комментарии:** `POST /comments/`, `GET /comments/{id}`, `PUT /comments/{id}`, `DELETE /comments/{id}`
- **Лайки:** `POST /likes/`, `GET /likes/{id}`, `DELETE /likes/{id}`
- **Чаты:** `GET /messages/chats`

---

## Зависимости

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
python-jose[cryptography]>=3.3.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-multipart>=0.0.6
passlib[bcrypt]>=1.7.4
python-socketio>=5.10.0
```

---

## Примечания
- Для production-режима обязательно измените секретные ключи и настройте secure cookies.
- Для работы с фронтендом настройте CORS (`config.py`).
- Для запуска с поддержкой сокетов используйте `run.py` или `socket io/app/main.py`.
- База данных по умолчанию — SQLite, но можно использовать любую, поддерживаемую SQLAlchemy.

---
