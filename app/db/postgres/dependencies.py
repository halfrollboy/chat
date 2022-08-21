from functools import lru_cache

from . import config
from . import database
from sqlalchemy.ext.asyncio import AsyncSession

# TODO будет переписано после отладки
async def get_db() -> AsyncSession:
    db = database.SessionLocal()
    print("CON DB Session")
    try:
        print("CON DB")
        yield db
    finally:
        print("final")
        await db.close()


# Возврат существующего экземпляра DBSettings вместо создания нового
@lru_cache
def get_db_settings() -> config.DBSettings:
    return config.DBSettings()
