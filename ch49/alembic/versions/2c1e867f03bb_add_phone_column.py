"""add phone column

Revision ID: 2c1e867f03bb
Revises: f100673dccd6
Create Date: 2025-04-29 11:14:46.859490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c1e867f03bb'
down_revision: Union[str, None] = 'f100673dccd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone", sa.Integer()))


def downgrade() -> None:
    op.drop_column("users", "phone")
