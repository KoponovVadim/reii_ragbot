from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from database import Database
import logging

from core.config import settings
from database.connections import database_connection, database_disconnection, get_database
from api.endpoints import contact


logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения...")
    await database_connection()
    logger.info("Подключение к базе данных установлено.")

    yield

    logger.info("Завершение приложения...")
    await database_disconnection()
    logger.info("Подключение к базе данных закрыто.")


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.include_router(contact.router, prefix="/api")

@app.get("/health")
async def health_check(db: Database = Depends(get_database)):
    try:
        await db.fetch_one("SELECT 1")
        return {"status": "ok", "message": "База данных доступна"}
    except Exception as e:
        logger.error(f"Ошибка при проверке подключения к базе данных: {e}")
        return {"status": "error", "message": str(e)}
    