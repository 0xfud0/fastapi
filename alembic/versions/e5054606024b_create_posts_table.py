"""create posts table

Revision ID: e5054606024b
Revises: 
Create Date: 2025-12-08 11:32:37.302757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5054606024b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
                    sa.Column('title', sa.String(), nullable = False)
                    )
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
