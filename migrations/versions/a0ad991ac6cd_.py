"""empty message

Revision ID: a0ad991ac6cd
Revises: c44591af59b3
Create Date: 2022-11-29 14:55:13.332819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0ad991ac6cd'
down_revision = 'c44591af59b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('top3_snappers', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('top3_snappers')

    # ### end Alembic commands ###
