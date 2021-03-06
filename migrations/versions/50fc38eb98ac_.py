"""empty message

Revision ID: 50fc38eb98ac
Revises: dadef18fc39b
Create Date: 2017-12-13 20:03:27.446626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50fc38eb98ac'
down_revision = 'dadef18fc39b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session_demo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('session_num', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('session_num'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session_demo')
    # ### end Alembic commands ###
