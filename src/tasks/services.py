from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.engine import Result

from core.models.task import Task
from core.models.employee import Employee
from src.tasks.schemas import TaskCreate, TaskUpdate


async def get_all_tasks(session: AsyncSession) -> list[Task]:
    """Получает список всех задач"""
    stmt = select(Task).order_by(Task.id)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


async def get_task(task_id: int, session: AsyncSession) -> Task | None:
    """Получает данные одной задачи по ее id"""
    stmt = select(Task).where(Task.id == task_id)
    result: Result = await session.execute(stmt)
    task: Task | None = result.scalar_one_or_none()
    return task


async def create_task(new_task: TaskCreate, session: AsyncSession) -> Task:
    """Создает новоую задачу"""
    task = Task(**new_task.model_dump())
    session.add(task)
    await session.commit()
    return task


async def update_task(task_id: int, task_update: TaskUpdate, session: AsyncSession) -> Task:
    """Обновляет данные по задаче"""
    stmt = select(Task).where(Task.id == task_id)
    result: Result = await session.execute(stmt)
    task: Task | None = result.scalar_one_or_none()
    for key, value in task_update.model_dump(exclude_none=True).items():
        setattr(task, key, value)
    await session.commit()
    return task


async def delete_task(task_id: int, session: AsyncSession):
    """Удаляет задачу"""
    stmt = select(Task).where(Task.id == task_id)
    result: Result = await session.execute(stmt)
    task: Task | None = result.scalar_one_or_none()
    await session.delete(task)
    await session.commit()
    return {'result': 'success'}


async def get_important_tasks(session: AsyncSession):
    """Получает список важных задач"""
    stmt = select(Task).outerjoin(
        Employee, Task.employee_id == Employee.id
        ).filter(
        Task.employee_id.is_(None),
        Task.parent_task.has(Task.employee_id.isnot(None))
        ).options(joinedload(Task.parent_task).joinedload(Task.employee).joinedload(Employee.tasks))

    result: Result = await session.execute(stmt)
    tasks = result.unique().scalars().all()

    return tasks
