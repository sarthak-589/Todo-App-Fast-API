"""Create address table

Revision ID: 64f571dab38d
Revises: ab6dbdf1ef69
Create Date: 2024-05-30 11:36:15.079069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
  

# revision identifiers, used by Alembic.
revision: str = '64f571dab38d'
down_revision: Union[str, None] = 'ab6dbdf1ef69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('address', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('pin_code', sa.String(), nullable=False),
                    )


def downgrade() -> None:
    op.drop_table('address')
