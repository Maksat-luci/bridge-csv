"""Initial migration

Revision ID: 64f50929b27a
Revises: 6b75d3d2e630
Create Date: 2023-06-27 18:57:21.553578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64f50929b27a'
down_revision = '6b75d3d2e630'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('maxsimus')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('maxsimus',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('max1', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('max2', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('max3', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('max4', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['max1'], ['profile.id'], name='maxsimus_max1_fkey'),
    sa.PrimaryKeyConstraint('id', name='maxsimus_pkey')
    )
    # ### end Alembic commands ###
