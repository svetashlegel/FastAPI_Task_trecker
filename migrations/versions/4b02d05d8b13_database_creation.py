"""database creation

Revision ID: 4b02d05d8b13
Revises: 
Create Date: 2023-12-01 01:04:01.745196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b02d05d8b13'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('second_name', sa.String(length=50), nullable=False),
    sa.Column('position', sa.String(length=20), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('deadline', sa.TIMESTAMP(), nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), nullable=False),
    sa.Column('base_task', sa.Integer(), nullable=True),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['base_task'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('employees')
    # ### end Alembic commands ###
