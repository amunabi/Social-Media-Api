"""add few columns to post table

Revision ID: ac7ad269f1f6
Revises: 4dda3e92170f
Create Date: 2023-12-22 00:28:29.640783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac7ad269f1f6'
down_revision: Union[str, None] = '4dda3e92170f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("published",sa.Boolean(),server_default="True",nullable=False),)
    op.add_column("posts",sa.Column("create_at",sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),)
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','create_at')
    pass
