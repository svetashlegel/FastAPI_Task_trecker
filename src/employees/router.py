from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result
from sqlalchemy.sql.functions import func

from src.database import get_async_session
from core.models.employee import Employee
from core.models.task import Task
from src.employees import services

from src.employees.schemas import EmployeeCreate, EmployeeUpdate, EmployeeRead, EmployeeReadWithTasks


router = APIRouter(
    prefix='/employee',
    tags=['Employees']
)


@router.get('/list', response_model=List[EmployeeReadWithTasks])
async def get_all_employees(session: AsyncSession = Depends(get_async_session)):
    return await services.get_all_employees(session)


@router.get('/detail/{employee_id}', response_model=EmployeeReadWithTasks)
async def get_employee(employee_id: int, session: AsyncSession = Depends(get_async_session)):
    return await services.get_employee(employee_id, session)


@router.post('/create', response_model=EmployeeRead)
async def create_employee(new_employee: EmployeeCreate, session: AsyncSession = Depends(get_async_session)):
    return await services.create_employee(new_employee, session)


@router.patch('/update/{employee_id}', response_model=EmployeeRead)
async def update_employee(employee_id: int, employee_update: EmployeeUpdate,
                          session: AsyncSession = Depends(get_async_session)):
    return await services.update_employee(employee_id, employee_update, session)


@router.delete('/delete/{employee_id}')
async def delete_employee(employee_id: int, session: AsyncSession = Depends(get_async_session)):
    return await services.delete_employee(employee_id, session)


@router.get('/engaged', response_model=List[EmployeeReadWithTasks])
async def get_engaged_employees(session: AsyncSession = Depends(get_async_session)):
    return await services.get_engaged_employees(session)
