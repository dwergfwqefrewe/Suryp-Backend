from fastapi import HTTPException, status

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

class UnknownDatabaseError(HTTPException):
    """Исключение для неизвестных ошибок базы данных"""
    def __init__(self, detail: str = "Неизвестная ошибка базы данных"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class ModelNotFoundError(HTTPException):
    """Общее исключение для случая, когда объект модели не найден"""
    def __init__(self, detail: str = "Объект не найден"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
