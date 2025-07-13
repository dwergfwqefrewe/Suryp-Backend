from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Схема для получения ответа о результате операции"""
    success: bool
