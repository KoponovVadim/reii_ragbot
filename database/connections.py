from database import Database
from core.config import settings

database = Database(settings.database_url)

async def database_connection():
    await database.connect()
    print("Подключение к базе данных установлено.")

async def database_disconnection():
    await database.disconnect()
    print("Подключение к базе данных закрыто.")

async def get_database():
    return database


logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)
