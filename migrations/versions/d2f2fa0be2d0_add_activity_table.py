"""add activity table

Revision ID: d2f2fa0be2d0
Revises: a4a95dbc7f37
Create Date: 2023-11-14 17:57:55.606696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2f2fa0be2d0'
down_revision: Union[str, None] = 'a4a95dbc7f37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('dog_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activities_id'), 'activities', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_activities_id'), table_name='activities')
    op.drop_table('activities')
    # ### end Alembic commands ###