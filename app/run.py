import uvicorn

from core.config import settings

if __name__ == '__main__':
    uvicorn.run(
        'sockets.main:asgi_app',
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )
