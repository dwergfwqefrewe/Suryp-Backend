from fastapi import (
    APIRouter,
    Depends,
    status,
    Response
)

from database.managers.like_manager import LikeManager
from database.models.user import User
from database.models.history_like import HistoryLike
from schemas.like import LikeCreate, LikeOut

from api.dependencies.auth import get_current_user
from api.dependencies.ownership import get_like_or_error
from api.docs.like import (
    like_create_responses, 
    like_get_responses, 
    like_delete_responses
)

from core.logger import app_logger

from exceptions.base import DatabaseError
from exceptions.like import LikeNotFoundError, OwnershipLikeError

like_router = APIRouter(prefix="/likes", tags=["Лайки"])

like_manager = LikeManager()

@like_router.post("/",
                  summary='Создать лайк',
                  status_code=status.HTTP_201_CREATED,
                  responses=like_create_responses)
async def create_like(like: LikeCreate,
                user: User = Depends(get_current_user)) -> LikeOut:
    try:
        data = like.model_dump()
        result = HistoryLike(**data, user_id=user.id)
        await like_manager.create_obj(obj=result)
        app_logger.info(f"Лайк {result.id} создан пользователем {user.login}")
        return LikeOut.model_validate(result)
    except (LikeNotFoundError, OwnershipLikeError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при создании лайка: {e}")
        raise DatabaseError("Ошибка при создании лайка")

@like_router.get("/{id}",
                 summary='Получить лайк по ID',
                 status_code=status.HTTP_200_OK,
                 responses=like_get_responses)
async def get_like(id: int, user: User = Depends(get_current_user)) -> LikeOut:
    try:
        result = await get_like_or_error(id=id, user=user)
        app_logger.info(f"Лайк {result.id} получен пользователем {user.login}")
        return LikeOut.model_validate(result)
    except (LikeNotFoundError, OwnershipLikeError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при получении лайка: {e}")
        raise DatabaseError("Ошибка при получении лайка")

@like_router.delete("/{id}",
                    summary='Удалить лайк по ID',
                    status_code=status.HTTP_204_NO_CONTENT,
                    responses=like_delete_responses)
async def delete_like(id: int, user: User = Depends(get_current_user)) -> Response:
    try:
        await get_like_or_error(id=id, user=user)
        await like_manager.delete_obj(id)
        app_logger.info(f"Лайк {id} удален пользователем {user.login}")
        return Response(status_code=204)
    except (LikeNotFoundError, OwnershipLikeError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при удалении лайка: {e}")
        raise DatabaseError("Ошибка при удалении лайка")
