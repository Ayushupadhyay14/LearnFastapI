"""create users table

Revision ID: f100673dccd6
Revises: 
Create Date: 2025-04-29 11:01:13.100563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f100673dccd6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
    "users",
    sa.Column("id", sa.INTEGER, primary_key=True),
    sa.Column("name", sa.String(50), nullable=False),
    sa.Column("email", sa.String, nullable=False),
)

def downgrade() -> None:
    op.drop_table('users')
