from fastapi import (
    APIRouter,
    Response,
    status,
    Depends,
)
from fastapi.responses import JSONResponse

from api.auth_config import JWT_ACCESS_COOKIE_NAME
from api.dependencies.auth import validate_refresh_token

from core.jwt import create_access_token
from core.cookie import set_auth_cookies, clear_auth_cookies
from core.logger import app_logger

from schemas.user import UserCreate, UserAuth

from services.auth_service import register_user, login_user

from exceptions.users import UserAlreadyExistsError, InvalidCredentialsError
from exceptions.base import DatabaseError

from api.docs.auth import (
    auth_login_responses, 
    auth_register_responses, 
    refresh_token_responses, 
    logout_responses,
)

auth_router = APIRouter(prefix='/auth', tags=['Аутентификация'])

@auth_router.post('/register',
                  summary='Создать пользователя',
                  status_code=status.HTTP_201_CREATED,
                  responses=auth_register_responses)
async def create_user(new_user: UserCreate, response: Response) -> Response:
    """Создаёт нового пользователя и выдает токены"""
    try:
        access_token, refresh_token = await register_user(new_user)
        response = JSONResponse(content={"message": "Пользователь успешно создан"})
        set_auth_cookies(response, access_token, refresh_token)
        app_logger.info(f"Пользователь {new_user.login} успешно создан")
    except UserAlreadyExistsError as e:
        raise UserAlreadyExistsError(e.detail)
    except DatabaseError as e:
        raise DatabaseError(e.detail)
    return response

@auth_router.post('/login',
                  summary='Войти в аккаунт',
                  status_code=status.HTTP_200_OK,
                  responses=auth_login_responses)
async def login(user: UserAuth, response: Response) -> Response:
    try:
        access_token, refresh_token = await login_user(user)
        response = JSONResponse(content={"message": "Вы успешно вошли в аккаунт"})
        set_auth_cookies(response, access_token, refresh_token)
        app_logger.info(f"Пользователь {user.login} успешно вошел в аккаунт")
    except InvalidCredentialsError as e:
        raise InvalidCredentialsError(e.detail)
    except DatabaseError as e:
        raise DatabaseError(e.detail)
    return response

@auth_router.post('/refresh',
                  summary='Обновить access токен',
                  status_code=status.HTTP_200_OK,
                  responses=refresh_token_responses)
async def refresh_access_token(response: Response,
                               user_id: int = Depends(validate_refresh_token)) -> Response:
    try:
        access_token = create_access_token({"sub": str(user_id)})
        response = JSONResponse(content={"message": "Access токен обновлен"})
        response.set_cookie(JWT_ACCESS_COOKIE_NAME, access_token, httponly=True)
        app_logger.info(f"Access токен обновлен для пользователя {user_id}")
    except DatabaseError as e:
        raise DatabaseError(e.detail)
    return response

@auth_router.post('/logout',
                  summary='Выйти из аккаунта',
                  status_code=status.HTTP_204_NO_CONTENT,
                  responses=logout_responses)
async def logout(response: Response) -> Response:
    clear_auth_cookies(response)
    app_logger.info(f"Пользователь вышел из аккаунта")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
