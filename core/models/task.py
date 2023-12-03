from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String, BOOLEAN, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.employee import Employee


class Task(Base):
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    deadline: Mapped[date] = mapped_column(TIMESTAMP)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True)

    base_task: Mapped[int | None] = mapped_column(ForeignKey('tasks.id'), nullable=True)
    employee_id: Mapped[int | None] = mapped_column(ForeignKey('employees.id'), nullable=True)

    parent_task: Mapped['Task'] = relationship('Task', remote_side='Task.id', backref='subtasks')
    employee: Mapped['Employee'] = relationship(back_populates='tasks')

    def __str__(self):
        return f'{self.title} (id={self.id})'

    def __repr__(self):
        return f'{self.__class__.__name__} (id= {self.id}, title= {self.title})'
