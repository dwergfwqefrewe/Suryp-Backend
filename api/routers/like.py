from fastapi import (
    APIRouter,
    Depends,
    status,
    Response
)

from database.managers.like_manager import LikeManager

from models.user import User
from models.history_like import HistoryLike as _HistoryLike

from schemas.like import LikeCreate, LikeOut

from .dependencies import get_current_user, get_like_or_error


like_router = APIRouter(prefix="/likes", tags=["Лайки"])

like_manager = LikeManager()


@like_router.post("/",
                  summary='Создать лайк',
                  status_code=status.HTTP_201_CREATED)
async def create_like(like: LikeCreate,
                user: User = Depends(get_current_user)) -> LikeOut:
    like_obj = _HistoryLike(**like.model_dump(exclude={"user_id"}), user_id=user.id)
    return await like_manager.create_obj(like_obj)


@like_router.get("/{id}",
                 summary='Получить лайк по ID',
                 status_code=status.HTTP_200_OK)
async def get_like(id: int, user: User = Depends(get_current_user)) -> LikeOut:
    like = await get_like_or_error(id=id, user=user)
    return LikeOut.model_validate(like)


@like_router.delete("/{id}",
                    summary='Удалить лайк по ID',
                    status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(id: int, user: User = Depends(get_current_user)) -> Response:
    await get_like_or_error(id=id, user=user)
    await like_manager.delete_obj(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
