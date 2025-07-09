from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import joinedload

from database.managers.user_manager import UserManager

from models.user import User
from models.history import History
from schemas.user import UserOut, UpdateUser, UpdateMe
from schemas.response import SuccessResponse

from .dependencies import get_current_user
from ..auth_config import JWT_ACCESS_COOKIE_NAME, JWT_REFRESH_COOKIE_NAME

user_manager = UserManager()

user_router = APIRouter(prefix='/user', tags=['Пользователи'])


@user_router.get('/me',
                 summary='Получить данные о себе',
                 status_code=status.HTTP_200_OK)
def get_me(user: User = Depends(get_current_user)) -> UserOut:
    return user_manager.get_obj_by_id(user.id, options=[
        joinedload(User.histories).joinedload(History.author)
    ])


@user_router.patch('/me',
                  summary='Частичное обновление данных о себе',
                  status_code=status.HTTP_200_OK)
def patch_me(updated_user: UpdateMe, user: User = Depends(get_current_user)) -> UserOut:
    update_data = UpdateUser(**updated_user.model_dump())
    user_manager.update_obj(id=user.id, updated_obj=update_data)
    return user_manager.get_obj_by_id(user.id, options=[
        joinedload(User.histories).joinedload(History.author)
    ])


@user_router.delete('/me',
                    summary='Удалить свой аккаунт',
                    status_code=status.HTTP_200_OK)
def delete_user(response: Response, user: User = Depends(get_current_user)) -> SuccessResponse:
    user_manager.delete_obj(id=user.id)
    response.delete_cookie(JWT_ACCESS_COOKIE_NAME)
    response.delete_cookie(JWT_REFRESH_COOKIE_NAME)
    return SuccessResponse(success=True)
