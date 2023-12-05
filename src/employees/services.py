from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result
from sqlalchemy.sql.functions import func

from core.models.employee import Employee
from core.models.task import Task
from src.employees.schemas import EmployeeCreate, EmployeeUpdate


async def get_all_employees(session: AsyncSession) -> list[Employee]:
    """Получает список всех сотрудников"""
    stmt = select(Employee).options(selectinload(Employee.tasks)).order_by(Employee.id)
    result: Result = await session.execute(stmt)
    employees = result.scalars().all()
    return list(employees)


async def get_employee(employee_id: int, session: AsyncSession) -> Employee | None:
    """Получает данные сотрудника по его id"""
    stmt = select(Employee).where(Employee.id == employee_id).options(selectinload(Employee.tasks))
    result: Result = await session.execute(stmt)
    employee: Employee | None = result.scalar_one_or_none()
    return employee


async def create_employee(new_employee: EmployeeCreate, session: AsyncSession) -> Employee:
    """Создает нового сотрудника"""
    employee = Employee(**new_employee.model_dump())
    session.add(employee)
    await session.commit()
    return employee


async def update_employee(employee_id: int, employee_update: EmployeeUpdate,
                          session: AsyncSession) -> Employee:
    """Обновляет данные сотрудника"""
    stmt = select(Employee).where(Employee.id == employee_id)
    result: Result = await session.execute(stmt)
    employee: Employee | None = result.scalar_one_or_none()
    for key, value in employee_update.model_dump(exclude_none=True).items():
        setattr(employee, key, value)
    await session.commit()
    return employee


async def delete_employee(employee_id: int, session: AsyncSession):
    """Удаляет сотрудника"""
    stmt = select(Employee).where(Employee.id == employee_id)
    result: Result = await session.execute(stmt)
    employee: Employee | None = result.scalar_one_or_none()
    await session.delete(employee)
    await session.commit()
    return {'result': 'success'}


async def get_engaged_employees(session: AsyncSession) -> list[Employee]:
    """Получает список занятых сотрудников, отсортированные по количеству активных задач"""
    stmt = (select(
        Employee,
        func.count(Task.id).label('active_tasks_count')
        ).join(Employee.tasks)
        .filter(Task.is_active)
        .group_by(Employee.id)
        .order_by(desc('active_tasks_count'))
        .options(selectinload(Employee.tasks))
    )

    result: Result = await session.execute(stmt)
    employees = result.scalars().all()
    return list(employees)
