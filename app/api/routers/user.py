from typing import List

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Query,
    Body
)

from exceptions.base import DatabaseError
from exceptions.users import UserNotFoundError

from database.managers.user_manager import UserManager
from database.managers.history_manager import HistoryManager
from database.models.user import User

from schemas.user import UserOut, UpdateUser, UpdateMe
from schemas.history import HistoryOutShort

from api.dependencies.auth import get_current_user

from core.cookie import clear_auth_cookies
from core.logger import app_logger

from api.docs.user import (
    user_get_responses, 
    user_update_responses, 
    user_histories_responses, 
    user_delete_responses
)

user_manager = UserManager()
history_manager = HistoryManager()

user_router = APIRouter(prefix='/user', tags=['Пользователи'])

@user_router.get('/histories/{id}',
                 summary='Получить все истории пользователя по ID',
                 status_code=status.HTTP_200_OK,
                 responses=user_histories_responses)
async def get_histories_by_id(id: int) -> List[HistoryOutShort]:
    try:
        app_logger.info(f"Получены истории пользователя {id}")
        return await history_manager.get_histories_by_author_id(author_id=id)
    except UserNotFoundError as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при получении историй пользователя: {e}")
        raise DatabaseError("Ошибка при получении историй пользователя")

@user_router.get('/me',
                 summary='Получить данные о себе',
                 status_code=status.HTTP_200_OK,
                 responses=user_get_responses)
async def get_me(user: User = Depends(get_current_user)) -> UserOut:
    try:
        app_logger.info(f"Получены данные о себе для пользователя {user.login}")
        db_user = await user_manager.get_obj_by_id(getattr(user, 'id', 0))
        if not db_user:
            app_logger.error(f"Пользователь {user.login} не найден")
            raise UserNotFoundError()
        return UserOut.model_validate(db_user, from_attributes=True)
    except UserNotFoundError as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при получении данных о себе: {e}")
        raise DatabaseError("Ошибка при получении данных о себе")

@user_router.get('/me/histories',
                 summary="Получить свои истории",
                 status_code=status.HTTP_200_OK,
                 responses=user_histories_responses)
async def get_histories(user: User = Depends(get_current_user),
                        skip: int = Query(0, ge=0),
                        limit: int = Query(100, ge=1, le=100)) -> List[HistoryOutShort]:
    try:
        app_logger.info(f"Получены истории пользователя {user.login}")
        return await history_manager.get_histories_by_author_id(author_id=getattr(user, 'id', 0), skip=skip, limit=limit)
    except UserNotFoundError as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при получении своих историй: {e}")
        raise DatabaseError("Ошибка при получении своих историй")

@user_router.get('/{login}/avatar', summary='Получить аватар пользователя по логину', status_code=status.HTTP_200_OK)
async def get_avatar_by_login(login: str):
    try:
        user = await user_manager.get_user_by_login(login)
        if not user or not user.avatar_url:
            return {"avatar_url": None}
        return {"avatar_url": user.avatar_url}
    except UserNotFoundError as e:
        return {"avatar_url": None}
    except Exception as e:
        app_logger.error(f"Ошибка при получении аватара: {e}")
        raise DatabaseError("Ошибка при получении аватара")

@user_router.patch('/me',
                  summary='Частичное обновление данных о себе',
                  status_code=status.HTTP_200_OK,
                  responses=user_update_responses)
async def patch_me(updated_user: UpdateMe,
                   user: User = Depends(get_current_user)) -> UserOut:
    try:
        update_data = UpdateUser(**updated_user.model_dump())
        result = await user_manager.update_obj(id=getattr(user, 'id', 0), updated_obj=update_data)
        app_logger.info(f"Данные о себе для пользователя {user.login} обновлены")
        return UserOut.model_validate(result, from_attributes=True)
    except UserNotFoundError as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при обновлении данных о себе: {e}")
        raise DatabaseError("Ошибка при обновлении данных о себе")

@user_router.patch('/me/avatar', summary='Обновить аватар (base64-строка)', status_code=status.HTTP_200_OK)
async def update_avatar(avatar_base64: str = Body(..., embed=True), user: User = Depends(get_current_user)):
    try:
        update_data = UpdateUser(avatar_url=avatar_base64)
        result = await user_manager.update_obj(id=getattr(user, 'id', 0), updated_obj=update_data)
        app_logger.info(f"Аватар пользователя {user.login} обновлён")
        return {"avatar_url": result.avatar_url}
    except UserNotFoundError as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при обновлении аватара: {e}")
        raise DatabaseError("Ошибка при обновлении аватара")

@user_router.delete('/me',
                    summary='Удалить свой аккаунт',
                    status_code=status.HTTP_204_NO_CONTENT,
                    responses=user_delete_responses)
async def delete_user(response: Response, user: User = Depends(get_current_user)) -> Response:
    try:
        await user_manager.delete_obj(id=getattr(user, 'id', 0))
        clear_auth_cookies(response)
        app_logger.info(f"Аккаунт пользователя {user.login} удален")
        return response
    except UserNotFoundError as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при удалении аккаунта: {e}")
        raise DatabaseError("Ошибка при удалении аккаунта")
