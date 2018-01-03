"""create telephone table

Revision ID: 60cc99926b3a
Revises: 414e0160cac0
Create Date: 2018-01-02 10:35:26.507981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60cc99926b3a'
down_revision = '414e0160cac0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        u'telephone',
        sa.Column(u'id', sa.Integer, primary_key=True),
        sa.Column(u'telnumber', sa.String(255), nullable=True, unique=True),
        sa.Column(u'user_id', sa.Integer, sa.ForeignKey('user.id')),
    )


def downgrade():
    pass
