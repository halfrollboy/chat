from typing import List
from pydantic import parse_obj_as
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from ..models.pydantic.company import Employee, EmployeeCreate
from ..repositories.employee import EmployeeRepository


router_employee = APIRouter(
    prefix="/employee",
    tags=["employee"],
    # dependencies=[Depends(get_token_handler)],
    responses={404: {"employee": "Not found"}},
)

# Получение всех работников
@router_employee.get("/", response_model=List[Employee])
async def list_employees(
    skip: int = 0, max: int = 10, employees: EmployeeRepository = Depends()
):
    db_employee = employees.all(skip=skip, max=max)
    return parse_obj_as(List[Employee], db_employee)


# Создание работника
@router_employee.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def store_employee(
    employee: EmployeeCreate, employees: EmployeeRepository = Depends()
):
    db_employee = employees.find_by_email(email=employee.email)

    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_employee = employees.create(employee)
    return Employee.from_orm(db_employee)


# Тестовое пространство получения работника
@router_employee.get("/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int, employees: EmployeeRepository = Depends()):
    db_employee = employees.find(employee_id)

    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return Employee.from_orm(db_employee)
