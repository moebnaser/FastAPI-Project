"""add content column to posts table

Revision ID: 38b09a2cb7e1
Revises: 9be0b84f41d8
Create Date: 2026-02-06 18:34:43.197266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38b09a2cb7e1'
down_revision: Union[str, Sequence[str], None] = '9be0b84f41d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String, nullable= False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
