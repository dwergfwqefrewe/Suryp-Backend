from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from exceptions.base import ValidationError, PermissionError, DatabaseError, UnknownDatabaseError
from exceptions.users import UserNotFoundError, UserAlreadyExistsError, InvalidCredentialsError, InvalidUserDataError
from exceptions.comment import CommentNotFoundError, OwnershipCommentError
from exceptions.histories import HistoryNotFoundError, OwnershipHistoryError
from exceptions.like import LikeNotFoundError, OwnershipLikeError
from exceptions.message import MessageNotFoundError, OwnershipMessageError

from core.logger import app_logger  

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except (
            ValidationError, PermissionError, DatabaseError, UnknownDatabaseError,
            UserNotFoundError, UserAlreadyExistsError, InvalidCredentialsError, InvalidUserDataError,
            CommentNotFoundError, OwnershipCommentError,
            HistoryNotFoundError, OwnershipHistoryError,
            LikeNotFoundError, OwnershipLikeError,
            MessageNotFoundError, OwnershipMessageError
        ) as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": exc.detail,
                    "status_code": exc.status_code
                }
            )
        except Exception as exc:
            app_logger.exception(f"Неизвестная ошибка Traceback: {exc.__traceback__}")
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Внутренняя ошибка сервера. Попробуйте позже.",
                    "status_code": HTTP_500_INTERNAL_SERVER_ERROR
                }
            ) 
