from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.engine import Result

from src.database import get_async_session

from core.models.task import Task
from core.models.employee import Employee
from src.tasks.schemas import TaskRead, TaskCreate, TaskUpdate

router = APIRouter(
    prefix='/task',
    tags=['Tasks']
)


@router.get('/list', response_model=List[TaskRead])
async def get_all_tasks(session: AsyncSession = Depends(get_async_session)) -> list[Task]:
    stmt = select(Task).order_by(Task.id)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


@router.get('/detail/{task_id}', response_model=TaskRead)
async def get_task(task_id: int, session: AsyncSession = Depends(get_async_session)) -> Task | None:
    stmt = select(Task).where(Task.id == task_id)
    result: Result = await session.execute(stmt)
    task: Task | None = result.scalar_one_or_none()
    return task


@router.post('/create', response_model=TaskRead)
async def create_task(new_task: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    task = Task(**new_task.model_dump())
    session.add(task)
    await session.commit()
    return task


@router.patch('/update/{task_id}', response_model=TaskRead)
async def update_task(task_id: int, task_update: TaskUpdate, session: AsyncSession = Depends(get_async_session)):
    stmt = select(Task).where(Task.id == task_id)
    result: Result = await session.execute(stmt)
    task: Task | None = result.scalar_one_or_none()
    for key, value in task_update.model_dump(exclude_none=True).items():
        setattr(task, key, value)
    await session.commit()
    return task


@router.delete('/delete/{task_id}')
async def delete_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = select(Task).where(Task.id == task_id)
    result: Result = await session.execute(stmt)
    task: Task | None = result.scalar_one_or_none()
    await session.delete(task)
    await session.commit()
    return {'result': 'success'}


@router.get('/important')
async def get_important_tasks2(session: AsyncSession = Depends(get_async_session)):

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

    stmt = select(Task).outerjoin(
        Employee, Task.employee_id == Employee.id
        ).filter(
        Task.employee_id.is_(None),
        Task.parent_task.has(Task.employee_id.isnot(None))
        ).options(joinedload(Task.parent_task).joinedload(Task.employee).joinedload(Employee.tasks))

    result1: Result = await session.execute(stmt)
    tasks = result1.unique().scalars().all()

    res_tasks = []
    for task in tasks:
        parent_task_employee_task_count = len([t for t in task.parent_task.employee.tasks if t.is_active])
        least_busy_employee_task_count = len([t for t in least_busy_employee.tasks if t.is_active])
        res = parent_task_employee_task_count - least_busy_employee_task_count
        if res <= 2:
            available_employee = task.parent_task.employee
        else:
            available_employee = least_busy_employee

        task_data = {
            'task': TaskRead.model_validate(task, from_attributes=True),
            'available_employee': available_employee.__str__()
        }
        res_tasks.append(task_data)

    return res_tasks
