from typing import List
from pydantic import parse_obj_as
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from ..models.pydantic.company import Company
from ..repositories.company import CompanyRepository


router_company = APIRouter(
    prefix="/company",
    tags=["company"],
    responses={404: {"company": "Not found"}},
)


# Получение всех работников
@router_company.get("/", response_model=List[Company])
async def list_companys(
    skip: int = 0, max: int = 10, companys: CompanyRepository = Depends()
):
    db_company = companys.all(skip=skip, max=max)
    return parse_obj_as(List[Company], db_company)


# Создание работника
@router_company.post("/", response_model=Company, status_code=status.HTTP_201_CREATED)
async def store_company(company: Company, companys: CompanyRepository = Depends()):
    db_company = companys.find_by_email(email=company.email)

    if db_company:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_company = companys.create(company)
    return Company.from_orm(db_company)


# Получение всех работников
@router_company.get("/ping")
async def list_companys(
    skip: int = 0, max: int = 10, companys: CompanyRepository = Depends()
):
    db_company = companys.all(skip=skip, max=max)
    return parse_obj_as(List[Company], db_company)


# Тестовое пространство получения работника
@router_company.get("/{company_id}", response_model=Company)
async def get_company(company_id: int, companys: CompanyRepository = Depends()):
    db_company = companys.find(company_id)

    if db_company is None:
        raise HTTPException(status_code=404, detail="company not found")

    return Company.from_orm(db_company)
