from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.task import Task


class Employee(Base):
    first_name: Mapped[str] = mapped_column(String(30))
    second_name: Mapped[str] = mapped_column(String(50))
    position: Mapped[str] = mapped_column(String(20))

    tasks: Mapped[list['Task']] = relationship(back_populates='employee')

    def __str__(self):
        return f'{self.first_name} {self.second_name} - {self.position} (id={self.id})'

    def __repr__(self):
        return f'{self.__class__.__name__} (id= {self.id}, name= {self.first_name} {self.second_name})'
