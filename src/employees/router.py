from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.employees import services
from src.employees.schemas import EmployeeCreate, EmployeeUpdate, EmployeeRead, EmployeeReadWithTasks


router = APIRouter(
    prefix='/employee',
    tags=['Employees']
)


@router.get('/list', response_model=List[EmployeeReadWithTasks])
async def get_all_employees(session: AsyncSession = Depends(get_async_session)):
    """Общий список сотрудников"""
    return await services.get_all_employees(session)


@router.get('/detail/{employee_id}', response_model=EmployeeReadWithTasks)
async def get_employee(employee_id: int, session: AsyncSession = Depends(get_async_session)):
    """Данные по одному сотруднику"""
    return await services.get_employee(employee_id, session)


@router.post('/create', response_model=EmployeeRead)
async def create_employee(new_employee: EmployeeCreate, session: AsyncSession = Depends(get_async_session)):
    """Создание сотрудника"""
    return await services.create_employee(new_employee, session)


@router.patch('/update/{employee_id}', response_model=EmployeeRead)
async def update_employee(employee_id: int, employee_update: EmployeeUpdate,
                          session: AsyncSession = Depends(get_async_session)):
    """Обновление сотрудника"""
    return await services.update_employee(employee_id, employee_update, session)


@router.delete('/delete/{employee_id}')
async def delete_employee(employee_id: int, session: AsyncSession = Depends(get_async_session)):
    """Удаление сотрудника"""
    return await services.delete_employee(employee_id, session)


@router.get('/engaged', response_model=List[EmployeeReadWithTasks])
async def get_engaged_employees(session: AsyncSession = Depends(get_async_session)):
    """Список занятых сотрудников, отсортированные по количеству активных задач."""
    return await services.get_engaged_employees(session)
