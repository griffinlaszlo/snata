"""empty message

Revision ID: f9e671113ab7
Revises: bfac3fdfacfd
Create Date: 2022-12-11 19:27:58.094292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9e671113ab7'
down_revision = 'bfac3fdfacfd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sent_received_ratio', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('received_sent_ratio', sa.Integer(), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('random_location', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('random_location')

    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.drop_column('received_sent_ratio')
        batch_op.drop_column('sent_received_ratio')

    # ### end Alembic commands ###
