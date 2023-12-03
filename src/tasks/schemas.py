from typing import Optional

from pydantic import BaseModel, Field
from datetime import date


class TaskBase(BaseModel):
    title: str
    base_task: Optional[int] = Field(default=None, foreign_key='task.id')
    employee_id: Optional[int] = Field(default=None, foreign_key='employee.id')
    deadline: date
    is_active: bool


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskCreate):
    title: str | None = None
    base_task: Optional[int] = Field(default=None, foreign_key='task.id')
    employee_id: Optional[int] = Field(default=None, foreign_key='employee.id')
    deadline: date | None = None
    is_active: bool | None = None


class TaskRead(TaskBase):
    id: int
