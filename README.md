# Syrup Chat Backend

Backend API для чат-приложения Syrup Chat, построенный на FastAPI с поддержкой WebSocket через Socket.IO.

## 🚀 Возможности

- **REST API** на FastAPI
- **WebSocket чат** через Socket.IO
- **JWT аутентификация** с refresh токенами
- **SQLAlchemy ORM** для работы с базой данных
- **Pydantic** для валидации данных
- **Централизованная конфигурация** через переменные окружения

## 📋 Требования

- Python 3.8+
- SQLite (или другая БД, поддерживаемая SQLAlchemy)

## 🛠 Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd backend
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

5. Настройте переменные окружения в `.env`:
```env
DEBUG=true
JWT_SECRET_KEY="your-super-secret-key"
DATABASE_URL="sqlite:///./database/database.db"
```

## 🚀 Запуск

### Разработка
```bash
python run.py
```

### Продакшн
```bash
uvicorn socket\ io.app.main:asgi_app --host 0.0.0.0 --port 8000
```

## 📚 API Документация

После запуска сервера документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 Аутентификация

API использует JWT токены, хранящиеся в HTTP-only cookies:

- **Access Token**: короткий срок действия (15 минут)
- **Refresh Token**: длительный срок действия (7 дней)

### Эндпоинты аутентификации:

- `POST /auth/register` - Регистрация пользователя
- `POST /auth/login/{id}` - Авторизация по ID
- `POST /auth/login` - Авторизация по логину/паролю
- `POST /auth/refresh` - Обновление access токена

## 💬 WebSocket API

### События:

- `connect` - Подключение к чату
- `disconnect` - Отключение от чата
- `join` - Присоединение к чату с именем пользователя
- `message` - Отправка сообщения
- `typing` - Индикатор печати

### Пример использования:

```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:8000');

// Присоединиться к чату
socket.emit('join', { username: 'John' });

// Отправить сообщение
socket.emit('message', { text: 'Hello, world!' });

// Слушать сообщения
socket.on('message', (data) => {
    console.log(`${data.user}: ${data.text}`);
});

// Слушать количество пользователей
socket.on('user_count', (data) => {
    console.log(`Users online: ${data.count}`);
});
```

## 🗄 База данных

Проект использует SQLAlchemy ORM с автоматическим созданием таблиц при запуске.

### Модели:

- **User** - Пользователи
- **Article** - Статьи/посты
- **Comment** - Комментарии
- **ArticleLike** - Лайки статей

## 📁 Структура проекта

```
backend/
├── api/                    # API роутеры
│   ├── routers/           # Эндпоинты
│   ├── auth_config.py     # Конфигурация аутентификации
│   └── router.py          # Главный роутер
├── auth/                  # Аутентификация
│   ├── dependencies.py    # Зависимости FastAPI
│   └── jwt_auth.py        # JWT функции
├── database/              # База данных
│   ├── config.py          # Конфигурация БД
│   └── managers/          # Менеджеры моделей
├── models/                # SQLAlchemy модели
├── schemas/               # Pydantic схемы
├── socket io/             # WebSocket приложение
│   └── app/
│       ├── main.py        # ASGI приложение
│       └── sockets.py     # Socket.IO обработчики
├── config.py              # Централизованная конфигурация
├── exceptions.py          # Кастомные исключения
├── main.py                # FastAPI приложение
├── run.py                 # Скрипт запуска
└── requirements.txt       # Зависимости
```

## 🔧 Конфигурация

Основные настройки в `config.py`:

- `DEBUG` - Режим отладки
- `JWT_SECRET_KEY` - Секретный ключ для JWT
- `DATABASE_URL` - URL базы данных
- `CORS_ORIGINS` - Разрешенные origins для CORS

## 🧪 Тестирование

```bash
# Запуск тестов (если есть)
pytest

# Проверка здоровья API
curl http://localhost:8000/health
```

## 📝 Логирование

Приложение использует стандартное логирование Python. В режиме DEBUG включено логирование SQL запросов.

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT License 
