"""Create post table

Revision ID: e4edda9fd31a
Revises: 
Create Date: 2023-12-21 23:33:18.683811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4edda9fd31a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


#handles the changes
def upgrade() -> None:
    op.create_table("posts",sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                sa.Column("title",sa.String(),nullable=False))
    pass

#handles tables when they arent needed any more
def downgrade() -> None:
    op.drop_table("posts")
    pass
