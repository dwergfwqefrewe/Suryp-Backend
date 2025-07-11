from fastapi import APIRouter

from api.routers.history import history_router
from api.routers.user import user_router
from api.routers.auth import auth_router
from api.routers.comment import comment_router
from api.routers.like import like_router
from api.routers.message import message_router


main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(auth_router)
main_router.include_router(history_router)
main_router.include_router(comment_router)
main_router.include_router(like_router)
main_router.include_router(message_router)
