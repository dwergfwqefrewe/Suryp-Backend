from .sockets import socket_app
from main import app

from core.logger import app_logger

import uvicorn

asgi_app = socket_app(app)

if __name__ == "__main__":
    app_logger.info(f"Socket сервер запущен на порту 8000")
    uvicorn.run(
        "main:asgi_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
