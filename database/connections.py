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
