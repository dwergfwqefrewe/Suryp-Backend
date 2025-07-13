from fastapi import (
    APIRouter,
    Depends,
    status,
    Response
)

from database.managers.comment_manager import CommentManager
from database.models.user import User
from database.models.comments import Comment
from schemas.comment import CommentCreate, CommentOut, CommentUpdate

from api.dependencies.auth import get_current_user
from api.dependencies.ownership import get_comment_or_error

from api.docs.comment import (
    comment_create_responses, 
    comment_get_responses, 
    comment_update_responses, 
    comment_delete_responses
)

from core.logger import app_logger

from exceptions.base import DatabaseError
from exceptions.comment import CommentNotFoundError, OwnershipCommentError


comment_router = APIRouter(prefix="/comments", tags=["Комментарии"])

comment_manager = CommentManager()

@comment_router.post("/",
                     summary='Создать комментарий',
                     status_code=status.HTTP_201_CREATED,
                     responses=comment_create_responses)
async def create_comment(comment: CommentCreate,
                   user: User = Depends(get_current_user)) -> CommentOut:
    try:
        data = comment.model_dump()
        new_comment = Comment(**data, user_id=user.id)
        await comment_manager.create_obj(obj=new_comment)
        app_logger.info(f"Комментарий {new_comment.id} создан пользователем {user.login}")
        return CommentOut.model_validate(new_comment)
    except (CommentNotFoundError, OwnershipCommentError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при создании комментария: {e}")
        raise DatabaseError("Ошибка при создании комментария")

@comment_router.get("/{id}",
                    summary='Получить комментарий по ID',
                    status_code=status.HTTP_200_OK,
                    responses=comment_get_responses)
async def get_comment(id: int, user: User = Depends(get_current_user)) -> CommentOut:
    try:
        comment = await get_comment_or_error(id, user)
        app_logger.info(f"Комментарий {comment.id} получен пользователем {user.login}")
        return CommentOut.model_validate(comment)
    except (CommentNotFoundError, OwnershipCommentError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при получении комментария: {e}")
        raise DatabaseError("Ошибка при получении комментария")

@comment_router.put("/{id}",
                    summary='Изменить комментарий по ID',
                    status_code=status.HTTP_200_OK,
                    responses=comment_update_responses)
async def update_comment(id: int,
                         comment_update: CommentUpdate,
                         user: User = Depends(get_current_user)) -> CommentOut:
    try:
        await get_comment_or_error(id, user)
        updated_comment = await comment_manager.update_obj(id, comment_update)
        app_logger.info(f"Комментарий {updated_comment.id} обновлен пользователем {user.login}")
        return CommentOut.model_validate(updated_comment)
    except (CommentNotFoundError, OwnershipCommentError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при обновлении комментария: {e}")
        raise DatabaseError("Ошибка при обновлении комментария")

@comment_router.delete("/{id}",
                       summary='Удалить комментарий по ID',
                       status_code=status.HTTP_204_NO_CONTENT,
                       responses=comment_delete_responses)
async def delete_comment(id: int, user: User = Depends(get_current_user)) -> Response:
    try:
        await get_comment_or_error(id, user)
        await comment_manager.delete_obj(id)
        app_logger.info(f"Комментарий {id} удален пользователем {user.login}")
        return Response(status_code=204)
    except (CommentNotFoundError, OwnershipCommentError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при удалении комментария: {e}")
        raise DatabaseError("Ошибка при удалении комментария")
