from fastapi import HTTPException, status


class UserNotFoundError(HTTPException):
    """Исключение для случая, когда пользователь не найден"""
    def __init__(self, detail: str = "Пользователь не найден"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AuthenticationError(HTTPException):
    """Исключение для ошибок аутентификации"""
    def __init__(self, detail: str = "Ошибка аутентификации"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ValidationError(HTTPException):
    """Исключение для ошибок валидации"""
    def __init__(self, detail: str = "Ошибка валидации данных"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class PermissionError(HTTPException):
    """Исключение для ошибок доступа"""
    def __init__(self, detail: str = "Недостаточно прав"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class DatabaseError(HTTPException):
    """Исключение для ошибок базы данных"""
    def __init__(self, detail: str = "Ошибка базы данных"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail) 
