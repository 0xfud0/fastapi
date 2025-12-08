"""adding user table

Revision ID: 5b62453dbe20
Revises: 5c0630b808b0
Create Date: 2025-12-08 12:59:13.875588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b62453dbe20'
down_revision: Union[str, Sequence[str], None] = '5c0630b808b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable = False),     
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True),
                              server_default = sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
