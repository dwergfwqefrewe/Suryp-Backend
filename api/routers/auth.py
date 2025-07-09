from fastapi import APIRouter, Request, Response, HTTPException, status

from api.auth_config import JWT_ACCESS_COOKIE_NAME, JWT_REFRESH_COOKIE_NAME
from .jwt_auth import create_access_token, create_refresh_token, decode_token

from database.managers.user_manager import UserManager

from models.user import User as _User
from schemas.response import SuccessResponse
from schemas.user import UserCreate, UserAuth


manager = UserManager()

auth_router = APIRouter(prefix='/auth', tags=['Аутентификация'])


def set_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """Устанавливает cookies с токенами"""
    response.set_cookie(
        JWT_ACCESS_COOKIE_NAME, 
        access_token, 
        httponly=True,
        secure=False,  # True для HTTPS
        samesite='lax'
    )
    response.set_cookie(
        JWT_REFRESH_COOKIE_NAME, 
        refresh_token, 
        httponly=True,
        secure=False,  # True для HTTPS
        samesite='lax'
    )


@auth_router.post('/register',
                  summary='Создать пользователя и выдать токен',
                  status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserCreate, response: Response) -> SuccessResponse:
    """Создает нового пользователя и выдает токены"""
    try:
        created_user = manager.create_obj(new_user)
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
def login(user: UserAuth, response: Response) -> SuccessResponse:
    user_id = manager.get_user_id_by_login(login=user.login)

    if manager.check_user_data(user):
        access_token = create_access_token({"sub": str(user_id)})
        refresh_token = create_refresh_token({"sub": str(user_id)})
        set_cookies(response, access_token, refresh_token)
        return SuccessResponse(success=True)

    raise HTTPException(status_code=404, detail='Invalid register data')


@auth_router.post('/refresh',
                  summary='Обновить access токен',
                  status_code=status.HTTP_200_OK)
def refresh_token(request: Request, response: Response) -> SuccessResponse:
    refresh_token = request.cookies.get(JWT_REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Missing refresh token')
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get('sub')
        access_token = create_access_token({"sub": str(user_id)})
        response.set_cookie(JWT_ACCESS_COOKIE_NAME, access_token, httponly=True)
        return SuccessResponse(success=True)
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid refresh token')


@auth_router.post('/logout',
                  summary='Выйти из аккаунта',
                  status_code=status.HTTP_200_OK)
def logout(response: Response) -> SuccessResponse:
    response.delete_cookie(JWT_ACCESS_COOKIE_NAME)
    response.delete_cookie(JWT_REFRESH_COOKIE_NAME)
    return SuccessResponse(success=True)
