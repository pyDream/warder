"""create user table

Revision ID: 414e0160cac0
Revises: 
Create Date: 2018-01-02 10:34:52.576471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '414e0160cac0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        u'user',
        sa.Column(u'id', sa.Integer, primary_key=True),
        sa.Column(u'user_id', sa.String(255), nullable=True, unique=True),
        sa.Column(u'name', sa.String(64), nullable=False, unique=True),
        sa.Column(u'gender', sa.String(64), nullable=False),
        sa.Column(u'age', sa.Integer, nullable=False),
        sa.Column(u'email', sa.String(255))
    )


def downgrade():
    pass
