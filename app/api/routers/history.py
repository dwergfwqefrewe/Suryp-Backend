from typing import Sequence

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response
)

from database.managers.history_manager import HistoryManager
from database.models.user import User
from database.models.history import History
from schemas.history import HistoryCreate, HistoryUpdate, HistoryOut

from api.dependencies.auth import get_current_user
from api.dependencies.ownership import get_history_or_error
from api.docs.history import (
    history_create_responses, 
    history_get_all_responses, 
    history_get_responses, 
    history_update_responses,
    history_delete_responses
)

from core.logger import app_logger

from exceptions.base import DatabaseError
from exceptions.histories import HistoryNotFoundError, OwnershipHistoryError

history_manager = HistoryManager()

history_router = APIRouter(prefix='/history', tags=['Истории'])

@history_router.post('/',
                     summary='Создать историю',
                     status_code=status.HTTP_201_CREATED,
                     responses=history_create_responses)
async def create_history(new_history: HistoryCreate,
                         user: User = Depends(get_current_user)) -> HistoryOut:
    try:
        data = new_history.model_dump(exclude={"author_id"})
        result = History(**data, author_id=user.id)
        history_out = await history_manager.create_history_with_response(result)
        app_logger.info(f"История {result.id} создана пользователем {user.login}")
        return history_out
    except (HistoryNotFoundError, OwnershipHistoryError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при создании истории: {e}")
        raise DatabaseError("Ошибка при создании истории")

@history_router.get('/',
                    summary='Получить все истории',
                    status_code=status.HTTP_200_OK,
                    responses=history_get_all_responses)
async def get_histories() -> Sequence[HistoryOut]:
    try:
        return await history_manager.get_histories_with_authors()
    except (HistoryNotFoundError, OwnershipHistoryError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при получении всех историй: {e}")
        raise DatabaseError("Ошибка при получении всех историй")

@history_router.get('/{id}',
                    summary='Получить историю по ID',
                    status_code=status.HTTP_200_OK,
                    responses=history_get_responses)
async def get_history(id: int, user: User = Depends(get_current_user)) -> HistoryOut:
    try:
        history_out = await history_manager.get_history_by_id_with_author(id)
        if history_out is None:
            raise HistoryNotFoundError()
        app_logger.info(f"История {id} получена пользователем {user.login}")
        return history_out
    except (HistoryNotFoundError, OwnershipHistoryError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при получении истории: {e}")
        raise DatabaseError("Ошибка при получении истории")

@history_router.put('/{id}',
                    summary='Изменить историю по ID',
                    status_code=status.HTTP_200_OK,
                    responses=history_update_responses)
async def update_history(id: int,
                         history_update: HistoryUpdate,
                         user: User = Depends(get_current_user)) -> HistoryOut:
    try:
        await get_history_or_error(id=id, user=user)
        await history_manager.update_obj(id=id, updated_obj=history_update)
        history_out = await history_manager.get_history_by_id_with_author(id)
        if history_out is None:
            raise HistoryNotFoundError()
        app_logger.info(f"История {id} обновлена пользователем {user.login}")
        return history_out
    except (HistoryNotFoundError, OwnershipHistoryError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при обновлении истории: {e}")
        raise DatabaseError("Ошибка при обновлении истории")

@history_router.delete('/{id}',
                       summary='Удалить историю по ID',
                       status_code=status.HTTP_204_NO_CONTENT,
                       responses=history_delete_responses)
async def delete_history(id: int, user: User = Depends(get_current_user)) -> Response:
    try:
        await get_history_or_error(id=id, user=user)
        await history_manager.delete_obj(id)
        app_logger.info(f"История {id} удалена пользователем {user.login}")
        return Response(status_code=204)
    except (HistoryNotFoundError, OwnershipHistoryError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при удалении истории: {e}")
        raise DatabaseError("Ошибка при удалении истории")
