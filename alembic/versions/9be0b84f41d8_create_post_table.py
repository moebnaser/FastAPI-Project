"""create post table

Revision ID: 9be0b84f41d8
Revises: 
Create Date: 2026-02-06 18:24:18.128402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9be0b84f41d8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
                            sa.Column('title', sa.String(), nullable = False)),
    pass


def downgrade() -> None:
    op.drop_table ('posts')
    pass
