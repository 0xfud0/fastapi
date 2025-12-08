"""add content column to the posts table

Revision ID: 5c0630b808b0
Revises: e5054606024b
Create Date: 2025-12-08 12:37:38.092679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c0630b808b0'
down_revision: Union[str, Sequence[str], None] = 'e5054606024b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content', sa.String(), nullable = False ))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
