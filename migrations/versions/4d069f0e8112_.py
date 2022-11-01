"""empty message

Revision ID: 4d069f0e8112
Revises: 
Create Date: 2022-10-30 16:47:00.505281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d069f0e8112'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('filename', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('data', sa.LargeBinary(), nullable=True))
    op.create_unique_constraint('test', 'users', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'data')
    op.drop_column('users', 'filename')
    # ### end Alembic commands ###
