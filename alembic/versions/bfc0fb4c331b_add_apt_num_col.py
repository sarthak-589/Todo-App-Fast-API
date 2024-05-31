"""add apt num col

Revision ID: bfc0fb4c331b
Revises: 95839650807e
Create Date: 2024-05-30 15:40:19.407222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bfc0fb4c331b'
down_revision: Union[str, None] = '95839650807e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("address", sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("address", "apt_num")
