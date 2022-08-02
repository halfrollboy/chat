from typing import List
from os import environ
from fastapi import HTTPException
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..models.postgres.pg_models import Employee, Company
from ..db.postgres.dependencies import get_db
from ..models.pydantic.company import EmployeeCreate
from loguru import logger


class EmployeeRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db  # внедрение зависимостей

    def find(self, id: int) -> Employee:
        """Поиск пользователя по id"""
        query = self.db.query(Employee)
        return query.filter(Employee.id == id).first()

    def find_by_email(self, email: EmailStr):
        """Поиск ползователя по email"""
        query = self.db.query(Employee)
        return query.filter(Employee.email == email).first()

    def all(self, skip: int = 0, max: int = 100) -> List[Employee]:
        """Получить всех пользователей"""
        query = self.db.query(Employee)
        return query.offset(skip).limit(max).all()

    # Постараться создавать изначально компанию, а потом пользователя
    def add_company(self, id: int, company: Company) -> Employee:
        """Добавление работника в комапнию"""
        self.db.query(Employee).filter(Employee.id == id).update(
            {"company_id": company.id}
        )
        self.db.commit()

    def create(self, employee: EmployeeCreate) -> Employee:
        """Создание пользователя"""
        faked_pass_hash = employee.password + f"{ environ.get('APP_TOKEN') }"

        try:
            db_employee = Employee(
                name=employee.name,
                email=employee.email,
                phone=employee.phone,
                password=faked_pass_hash,
                company_id=employee.company_id,
                gender=employee.gender,
                owner=employee.owner,
                admin=employee.admin,
            )

            self.db.add(db_employee)
            self.db.commit()
            self.db.refresh(db_employee)
        except:
            {"error": employee}
        logger.debug(f"db_employe:{db_employee}, employe:{employee}")
        return db_employee


# def create(self, speedster: SpeedsterCreate) -> Speedster:
#     speedster.password += "__you_must_hash_me"

#     db_speedster = Speedster(**speedster.dict())

#     self.db.add(db_speedster)
#     self.db.commit()
#     self.db.refresh(db_speedster)

#     return db_speedster
