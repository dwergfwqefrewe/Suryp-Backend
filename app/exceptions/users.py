from fastapi import HTTPException, status

class UserAlreadyExistsError(HTTPException):
    """Исключение для случая, когда пользователь с таким логином уже существует"""
    def __init__(self, detail: str = "Пользователь с таким логином уже существует"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class UserNotFoundError(HTTPException):
    """Исключение для случая, когда пользователь не найден"""
    def __init__(self, detail: str = "Пользователь не найден"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class InvalidCredentialsError(HTTPException):
    """Исключение для случая, когда неверные логин или пароль"""
    def __init__(self, detail: str = "Неверный логин или пароль"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class InvalidUserDataError(HTTPException):
    """Исключение для случая, когда неверные данные пользователя"""
    def __init__(self, detail: str = "Неверные данные пользователя"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
