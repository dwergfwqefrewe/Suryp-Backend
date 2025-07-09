from .sockets import socket_app
from main import app
import uvicorn

asgi_app = socket_app(app)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:asgi_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
