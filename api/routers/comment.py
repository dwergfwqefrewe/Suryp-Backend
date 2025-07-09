from fastapi import APIRouter, Depends, status

from database.managers.comment_manager import CommentManager

from models.user import User
from models.comments import Comment as _Comment

from schemas.comment import CommentCreate, CommentOut, CommentUpdate
from schemas.response import SuccessResponse

from .dependencies import get_current_user, get_comment_or_error


comment_router = APIRouter(prefix="/comments", tags=["Комментарии"])

comment_manager = CommentManager()


@comment_router.post("/",
                     summary='Создать комментарий',
                     status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreate,
                   user: User = Depends(get_current_user)) -> SuccessResponse:
    data = comment.model_dump()
    data.pop("user_id", None)
    comment = _Comment(**data, user_id=user.id)
    comment_manager.create_obj(comment)
    return SuccessResponse(success=True)


@comment_router.get("/{id}",
                    summary='Получить комментарий по ID',
                    status_code=status.HTTP_200_OK) 
def get_comment(id: int, user: User = Depends(get_current_user)) -> CommentOut:
    comment = get_comment_or_error(id, user)
    return CommentOut.model_validate(comment)


@comment_router.put("/{id}",
                    summary='Изменить комментарий по ID',
                    status_code=status.HTTP_200_OK)
def update_comment(id: int,
                   comment_update: CommentUpdate,
                   user: User = Depends(get_current_user)) -> CommentOut:
    get_comment_or_error(id, user)
    updated_comment = comment_manager.update_obj(id=id, updated_obj=comment_update)
    return CommentOut.model_validate(updated_comment)


@comment_router.delete("/{id}",
                       summary='Удалить комментарий по ID',
                       status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, user: User = Depends(get_current_user)) -> None:
    get_comment_or_error(id, user)
    comment_manager.delete_obj(id)
    return None
