"""empty message

Revision ID: 2e7f4d21799a
Revises: 58a99197b048
Create Date: 2018-11-27 19:24:46.662911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e7f4d21799a'
down_revision = '58a99197b048'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activity', 'number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity', sa.Column('number', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
