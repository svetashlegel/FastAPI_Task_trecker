from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, joinedload, selectinload
from sqlalchemy.engine import Result
from sqlalchemy.sql.functions import count

from src.database import get_async_session
from core.models.employee import Employee
from core.models.task import Task

from src.employees.schemas import EmployeeCreate, EmployeeUpdate, EmployeeRead, EmployeeReadWithTasks


router = APIRouter(
    prefix='/employee',
    tags=['Employees']
)


@router.get('/list', response_model=List[EmployeeReadWithTasks])
async def get_all_employees(session: AsyncSession = Depends(get_async_session)) -> list[Employee]:
    stmt = select(Employee).options(selectinload(Employee.tasks)).order_by(Employee.id)
    result: Result = await session.execute(stmt)
    employees = result.scalars().all()
    return list(employees)


@router.get('/detail/{employee_id}', response_model=EmployeeReadWithTasks)
async def get_employee(employee_id: int, session: AsyncSession = Depends(get_async_session)) -> Employee | None:
    stmt = select(Employee).where(Employee.id == employee_id).options(selectinload(Employee.tasks))
    result: Result = await session.execute(stmt)
    employee: Employee | None = result.scalar_one_or_none()
    return employee


@router.post('/create', response_model=EmployeeRead)
async def create_employee(new_employee: EmployeeCreate, session: AsyncSession = Depends(get_async_session)):
    employee = Employee(**new_employee.model_dump())
    session.add(employee)
    await session.commit()
    return employee


@router.patch('/update/{employee_id}', response_model=EmployeeRead)
async def update_employee(employee_id: int, employee_update: EmployeeUpdate, session: AsyncSession = Depends(get_async_session)):
    stmt = select(Employee).where(Employee.id == employee_id)
    result: Result = await session.execute(stmt)
    employee: Employee | None = result.scalar_one_or_none()
    for key, value in employee_update.model_dump(exclude_none=True).items():
        setattr(employee, key, value)
    await session.commit()
    return employee


@router.delete('/delete/{employee_id}')
async def delete_employee(employee_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = select(Employee).where(Employee.id == employee_id)
    result: Result = await session.execute(stmt)
    employee: Employee | None = result.scalar_one_or_none()
    await session.delete(employee)
    await session.commit()
    return {'result': 'success'}


@router.get('/engaged', response_model=List[EmployeeReadWithTasks])
async def get_engaged_employees(session: AsyncSession = Depends(get_async_session)) -> list[Employee]:
    stmt = (select(Employee).join(Employee.tasks).options(selectinload(Employee.tasks)).filter(Task.is_active)
            .order_by(count(Task.is_active)))

    result: Result = await session.execute(stmt)
    employees = result.scalars().all()
    return list(employees)
