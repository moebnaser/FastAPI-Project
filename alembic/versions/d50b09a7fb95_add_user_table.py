"""add user table 

Revision ID: d50b09a7fb95
Revises: 38b09a2cb7e1
Create Date: 2026-02-06 18:38:56.897389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd50b09a7fb95'
down_revision: Union[str, Sequence[str], None] = '38b09a2cb7e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text('now()')
        )
    )


def downgrade() -> None:
    op.drop_table('users')