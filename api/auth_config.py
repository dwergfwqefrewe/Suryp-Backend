from main_config import settings

# Импортируем настройки из централизованной конфигурации
JWT_SECRET_KEY = settings.jwt_secret_key
JWT_ACCESS_COOKIE_NAME = settings.jwt_access_cookie_name
JWT_REFRESH_COOKIE_NAME = settings.jwt_refresh_cookie_name
