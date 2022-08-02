from types import coroutine
from typing import List
from os import environ

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..models.postgres.pg_models import Company
from ..db.postgres.dependencies import get_db

# from ..models.pydantic.company import CompanyCreate
from loguru import logger


class CompanyRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def find(self, id: int) -> Company:
        """Поиск компании по id"""
        query = self.db.query(Company)
        return query.filter(Company.id == id).first()

    def find_by_email(self, email: EmailStr):
        """Поиск компании по email"""
        query = self.db.query(Company)
        return query.filter(Company.email == email).first()

    def all(self, skip: int = 0, max: int = 100) -> List[Company]:
        """Получить все компании"""
        query = self.db.query(Company)
        return query.offset(skip).limit(max).all()

    def create(self, company: Company) -> Company:
        """Создание компании"""

        db_company = Company(
            name=company.name,
            phone=company.phone,
            email=company.email,
            info_id=company.info_id,
            adress=company.adress,
            coordinate=company.coordinate,
        )

        self.db.add(db_company)
        self.db.commit()
        self.db.refresh(db_company)
        logger.debug(f"company {db_company}")
        return db_company
