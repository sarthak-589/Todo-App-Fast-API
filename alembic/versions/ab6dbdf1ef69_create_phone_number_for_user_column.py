"""Create phone number for user column

Revision ID: ab6dbdf1ef69
Revises: 
Create Date: 2024-05-23 16:17:10.767896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab6dbdf1ef69'
down_revision: Union[str, None] = None  
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
