from typing import Sequence

from fastapi import APIRouter, Depends, status, Response

from database.managers.history_manager import HistoryManager

from models.user import User
from models.history import History as _History

from schemas.history import HistoryCreate, HistoryUpdate, HistoryOut
from schemas.response import SuccessResponse

from .dependencies import get_current_user, get_history_or_error

history_manager = HistoryManager()

history_router = APIRouter(prefix='/history', tags=['Истории'])


@history_router.post('/',
                     summary='Создать историю',
                     status_code=status.HTTP_201_CREATED)
async def create_history(new_history: HistoryCreate,
                   user: User = Depends(get_current_user)) -> HistoryOut:
    history = _History(**new_history.model_dump(exclude={"author_id"}), author_id=user.id)
    return await history_manager.create_history_with_response(history)


@history_router.get('/',
                    summary='Получить все истории',
                    status_code=status.HTTP_200_OK)
async def get_histories() -> Sequence[HistoryOut]:
    return await history_manager.get_histories_with_authors()


@history_router.get('/{id}',
                    summary='Получить историю по ID',
                    status_code=status.HTTP_200_OK)
async def get_history(id: int, user: User = Depends(get_current_user)) -> HistoryOut:
    history = await get_history_or_error(id=id, user=user)
    return history


@history_router.put('/{id}',
                    summary='Изменить историю по ID',
                    status_code=status.HTTP_200_OK)
async def update_history(id: int,
                   updated_history: HistoryUpdate,
                   user: User = Depends(get_current_user)) -> SuccessResponse:
    await get_history_or_error(id=id, user=user)
    await history_manager.update_obj(id=id, updated_obj=updated_history)
    return SuccessResponse(success=True)


@history_router.delete('/{id}',
                       summary='Удалить историю по ID',
                       status_code=status.HTTP_204_NO_CONTENT)
async def delete_history(id: int, user: User = Depends(get_current_user)) -> Response:
    await get_history_or_error(id=id, user=user)
    await history_manager.delete_history_with_response(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
