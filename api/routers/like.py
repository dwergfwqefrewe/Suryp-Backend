from fastapi import (
    APIRouter,
    Depends,
    status
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
def create_like(like: LikeCreate,
                user: User = Depends(get_current_user)) -> LikeOut:
    new_like = _HistoryLike(**like.model_dump(), user_id=user.id)  
    created_like = like_manager.create_obj(new_like)   
    return LikeOut.model_validate(created_like)


@like_router.get("/{id}",
                 summary='Получить лайк по ID',
                 status_code=status.HTTP_200_OK)
def get_like(id: int, user: User = Depends(get_current_user)) -> LikeOut:
    like = get_like_or_error(id=id, user=user)
    return LikeOut.model_validate(like)


@like_router.delete("/{id}",
                    summary='Удалить лайк по ID',
                    status_code=status.HTTP_204_NO_CONTENT)
def delete_like(id: int, user: User = Depends(get_current_user)) -> None:
    get_like_or_error(id=id, user=user)
    like_manager.delete_obj(id)
    return None
