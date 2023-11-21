"""add summary and address to user

Revision ID: 4674d3ca6276
Revises: 8828386363ef
Create Date: 2023-11-21 11:02:31.561064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4674d3ca6276'
down_revision: Union[str, None] = '8828386363ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('summary', sa.String(), nullable=True))
    op.add_column('users', sa.Column('address', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'address')
    op.drop_column('users', 'summary')
    # ### end Alembic commands ###