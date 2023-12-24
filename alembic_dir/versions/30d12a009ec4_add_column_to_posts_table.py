"""add column to posts table

Revision ID: 30d12a009ec4
Revises: e4edda9fd31a
Create Date: 2023-12-21 23:35:39.063535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30d12a009ec4'
down_revision: Union[str, None] = 'e4edda9fd31a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
