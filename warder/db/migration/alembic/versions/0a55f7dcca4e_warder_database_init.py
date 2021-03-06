"""warder database init

Revision ID: 0a55f7dcca4e
Revises: 
Create Date: 2018-01-03 16:37:43.490376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a55f7dcca4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('gender', sa.String(length=64), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_user_user_id', 'user', ['user_id'], unique=False)
    op.create_table('telephone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telnumber', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('telephone')
    op.drop_index('ix_user_user_id', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
