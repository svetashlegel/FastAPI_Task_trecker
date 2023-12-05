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

from src.tasks import services
from src.tasks.dependencies import get_least_busy_employee

router = APIRouter(
    prefix='/task',
    tags=['Tasks']
)


@router.get('/list', response_model=List[TaskRead])
async def get_all_tasks(session: AsyncSession = Depends(get_async_session)):
    return await services.get_all_tasks(session)


@router.get('/detail/{task_id}', response_model=TaskRead)
async def get_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    return await services.get_task(task_id, session)


@router.post('/create', response_model=TaskRead)
async def create_task(new_task: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    return await services.create_task(new_task, session)


@router.patch('/update/{task_id}', response_model=TaskRead)
async def update_task(task_id: int, task_update: TaskUpdate, session: AsyncSession = Depends(get_async_session)):
    return await services.update_task(task_id, task_update, session)


@router.delete('/delete/{task_id}')
async def delete_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    return await services.delete_task(task_id, session)


@router.get('/important')
async def get_important_tasks(least_busy_employee: Employee = Depends(get_least_busy_employee),
                              session: AsyncSession = Depends(get_async_session)):
    tasks = await services.get_important_tasks(session)
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
