from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, joinedload, selectinload
from sqlalchemy.engine import Result

from src.database import get_async_session

from core.models.task import Task
from core.models.employee import Employee
from src.tasks.schemas import TaskRead, TaskCreate, TaskUpdate
from src.tasks.services import get_suitable_employee

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


@router.get('/important', response_model=List[TaskRead])
async def get_important_tasks(session: AsyncSession = Depends(get_async_session)) -> list[Task]:
    stmt = select(Task).where(Task.base_task is not None and Task.employee_id is None and Task.base_task.employee_id is not None).options(joinedload(Task.previous_task).joinedload(Task.employee)).order_by(Task.id)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()

    for task in tasks:
        base_task_employee = task.previous_task.employee
        suitable_employee = get_suitable_employee(base_task_employee)
        
    return list(tasks)
