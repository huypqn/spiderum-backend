"""add post thumbnail

Revision ID: 342a43808240
Revises: 674a6c3a68be
Create Date: 2022-11-04 12:09:06.427984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '342a43808240'
down_revision = '674a6c3a68be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('thumbnail', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'thumbnail')
    # ### end Alembic commands ###
