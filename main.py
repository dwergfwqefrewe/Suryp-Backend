from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import main_router

from config import settings
from database.config import engine, Base
from models import user, history, comments, history_like

# Создаем таблицы при запуске
@asynccontextmanager
async def lifespan(app: FastAPI):   
    # Создаем таблицы при запуске
    Base.metadata.create_all(bind=engine)
    yield
    # Очистка при завершении
    engine.dispose()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(router=main_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.app_name}
