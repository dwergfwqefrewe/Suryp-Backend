from database.config import engine, Base
from core.logger import app_logger

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 

app_logger.info(f"База данных инициализирована")   
