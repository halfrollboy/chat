from functools import lru_cache

from . import config
from . import database
from sqlalchemy.orm import Session

# Вызывается во время внедрения зависимости
def get_db() -> Session:
    db = database.SessionLocal()
    try:
        print("CON DB")
        yield db
    finally:
        db.close()


# Возврат существующего экземпляра DBSettings вместо создания нового
@lru_cache
def get_db_settings() -> config.DBSettings:
    return config.DBSettings()
