from typing import List
from pydantic import BaseModel, Field
from src.tasks.schemas import TaskRead


class EmployeeBase(BaseModel):
    first_name: str = Field(max_length=100)
    second_name: str = Field(max_length=100)
    position: str = Field(max_length=100)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeCreate):
    first_name: str | None = None
    second_name: str | None = None
    position: str | None = None


class EmployeeRead(EmployeeBase):
    id: int


class EmployeeReadWithTasks(EmployeeRead):
    tasks: List[TaskRead] = []

