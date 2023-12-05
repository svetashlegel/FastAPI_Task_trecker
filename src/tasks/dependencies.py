from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from sqlalchemy import select, func
from sqlalchemy.engine import Result

from core.models.employee import Employee
from core.models.task import Task


async def get_least_busy_employee(session: AsyncSession = Depends(get_async_session)) -> Employee:
    """Получает сотрудника с наименьшим количеством активных задач"""
    least_busy_employee_q = (
        select(Employee)
        .outerjoin(Employee.tasks)
        .filter(Task.is_active.is_(True))
        .group_by(Employee.id)
        .order_by(func.count(Task.id))
        .limit(1)
    )
    r: Result = await session.execute(least_busy_employee_q)
    least_busy_employee: Employee = r.scalar_one()
    return least_busy_employee
