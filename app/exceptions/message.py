from fastapi import HTTPException, status

class MessageNotFoundError(HTTPException):
    """Исключение для случая, когда сообщение не найдено"""
    def __init__(self, detail: str = "Сообщение не найдено"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class OwnershipMessageError(HTTPException):
    """Исключение для случая, когда пользователь не является автором сообщения"""
    def __init__(self, detail: str = "У вас нет прав на удаление этого сообщения"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
