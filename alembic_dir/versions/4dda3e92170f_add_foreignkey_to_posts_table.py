"""add foreignkey to posts table

Revision ID: 4dda3e92170f
Revises: 0c6bdf60f752
Create Date: 2023-12-22 00:11:20.632023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dda3e92170f'
down_revision: Union[str, None] = '0c6bdf60f752'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#creates relationship between the users and post table
def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    #links btwn two tables
    #give an fk name,source for foreigh key,referent a remote table,local column in the post table,
    #remote_locs -->covers the users id field
    op.create_foreign_key("post_user_fk",source_table="posts",referent_table="users",
                          local_cols=['owner_id'],remote_cols=["id"],ondelete="CASCADE")
    pass

#drop the foreign common key --=>post_user_fk
def downgrade() -> None:
    op.drop_constraint("post_user_fk",table_name="posts")
    op.drop_column('posts','owner_id')
    pass
