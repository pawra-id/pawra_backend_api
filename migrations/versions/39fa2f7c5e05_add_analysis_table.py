"""add analysis table

Revision ID: 39fa2f7c5e05
Revises: f608cf175fdd
Create Date: 2023-11-21 12:32:49.626605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39fa2f7c5e05'
down_revision: Union[str, None] = 'f608cf175fdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('analysis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('prediction', sa.String(), nullable=False),
    sa.Column('is_shared', sa.Boolean(), nullable=False, server_default='FALSE'),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('dog_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dog_id'], ['dogs.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_id'), 'analysis', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_analysis_id'), table_name='analysis')
    op.drop_table('analysis')
    # ### end Alembic commands ###
