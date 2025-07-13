from fastapi import HTTPException, status

class LikeNotFoundError(HTTPException):
    """Исключение для случая, когда лайк не найден"""
    def __init__(self, detail: str = "Лайк не найден"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class OwnershipLikeError(HTTPException):
    """Исключение для случая, когда пользователь не является автором лайка"""
    def __init__(self, detail: str = "У вас нет прав на удаление этого лайка"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail) 
