"""add foregn key to posts table

Revision ID: aafd2d237635
Revises: d50b09a7fb95
Create Date: 2026-02-06 18:47:32.309442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aafd2d237635'
down_revision: Union[str, Sequence[str], None] = 'd50b09a7fb95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_users_fk', source_table= 'posts', referent_table='users', 
                          local_cols=['owner_id'], remote_cols=['id'], ondelete= 'CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint ('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
