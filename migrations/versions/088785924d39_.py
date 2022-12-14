"""empty message

Revision ID: 088785924d39
Revises: f9e671113ab7
Create Date: 2022-12-13 18:58:29.610471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '088785924d39'
down_revision = 'f9e671113ab7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sent_top10_text', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('sent_breakdown', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('received_top10_text', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('received_breakdown', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('received_breakdown')
        batch_op.drop_column('received_top10_text')
        batch_op.drop_column('sent_breakdown')
        batch_op.drop_column('sent_top10_text')

    # ### end Alembic commands ###
