from fastapi import (
    APIRouter,
    Response,
    HTTPException,
    status,
    Depends
)

from api.auth_config import JWT_ACCESS_COOKIE_NAME, JWT_REFRESH_COOKIE_NAME
from .jwt_auth import create_access_token, create_refresh_token

from database.managers.user_manager import UserManager

from schemas.response import SuccessResponse
from schemas.user import UserCreate, UserAuth
from models.user import User
from .dependencies import get_current_user, validate_refresh_token

manager = UserManager()

auth_router = APIRouter(prefix='/auth', tags=['Аутентификация'])


def set_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """
    Устанавливает cookies с токенами
    """
    max_age = 3600 * 24 * 7
    response.set_cookie(
        JWT_ACCESS_COOKIE_NAME, 
        access_token, 
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=max_age
    )
    response.set_cookie(
        JWT_REFRESH_COOKIE_NAME, 
        refresh_token, 
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=max_age
    )


@auth_router.post('/register',
                  summary='Создать пользователя и выдать токен',
                  status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserCreate, response: Response) -> SuccessResponse:
    """
    Создаёт нового пользователя и выдает токены
    """
    try:
        created_user = await manager.create_user(new_user)
        access_token = create_access_token({"sub": str(created_user.id)})
        refresh_token = create_refresh_token({"sub": str(created_user.id)})
        set_cookies(response, access_token, refresh_token)
        return SuccessResponse(success=True)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании пользователя: {str(e)}"
        )


@auth_router.post('/login',
                  summary='Войти в аккаунт',
                  status_code=status.HTTP_200_OK)
async def login(user: UserAuth, response: Response) -> SuccessResponse:
    user_obj = await manager.check_user_data(user)
    if user_obj:
        user_id = user_obj.id
        access_token = create_access_token({"sub": str(user_id)})
        refresh_token = create_refresh_token({"sub": str(user_id)})
        set_cookies(response, access_token, refresh_token)
        return SuccessResponse(success=True)
    raise HTTPException(status_code=401, detail='Неверный логин или пароль')


@auth_router.post('/refresh',
                  summary='Обновить access токен',
                  status_code=status.HTTP_200_OK)
async def refresh_access_token(response: Response,
                               user: User = Depends(validate_refresh_token)) -> SuccessResponse:
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(JWT_ACCESS_COOKIE_NAME, access_token, httponly=True)
    return SuccessResponse(success=True)


@auth_router.post('/logout',
                  summary='Выйти из аккаунта',
                  status_code=status.HTTP_200_OK)
async def logout(response: Response, user: User = Depends(get_current_user)) -> SuccessResponse:
    response.delete_cookie(JWT_ACCESS_COOKIE_NAME)
    response.delete_cookie(JWT_REFRESH_COOKIE_NAME)
    return SuccessResponse(success=True)
