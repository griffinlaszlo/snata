"""empty message

Revision ID: 71f85978d86a
Revises: ae76d1bd8ee0
Create Date: 2022-12-11 11:32:57.506549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71f85978d86a'
down_revision = 'ae76d1bd8ee0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('recent_snap', sa.String(length=50), nullable=True),
    sa.Column('top3_snappers', sa.String(length=100), nullable=True),
    sa.Column('most_received', sa.Text(), nullable=True),
    sa.Column('total_snaps_sent', sa.Integer(), nullable=True),
    sa.Column('total_snaps_received', sa.Integer(), nullable=True),
    sa.Column('total_snaps_saved', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('recent_snap')
        batch_op.drop_column('total_snaps_sent')
        batch_op.drop_column('total_snaps_saved')
        batch_op.drop_column('most_received')
        batch_op.drop_column('top3_snappers')
        batch_op.drop_column('total_snaps_received')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_snaps_received', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('top3_snappers', sa.VARCHAR(length=50), nullable=True))
        batch_op.add_column(sa.Column('most_received', sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('total_snaps_saved', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('total_snaps_sent', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('recent_snap', sa.VARCHAR(length=50), nullable=True))

    op.drop_table('chats')
    # ### end Alembic commands ###
