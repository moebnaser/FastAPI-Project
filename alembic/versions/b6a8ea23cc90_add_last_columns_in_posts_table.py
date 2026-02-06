"""add last columns in posts table

Revision ID: b6a8ea23cc90
Revises: aafd2d237635
Create Date: 2026-02-06 19:21:42.720533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6a8ea23cc90'
down_revision: Union[str, Sequence[str], None] = 'aafd2d237635'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('published', sa.Boolean(), nullable = False, 
                            server_default= 'TRUE'))
    op.add_column('posts', 
                  sa.Column('created_at', sa.TIMESTAMP(timezone= True), nullable = False, 
                            server_default= sa.text('now()')))



def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
