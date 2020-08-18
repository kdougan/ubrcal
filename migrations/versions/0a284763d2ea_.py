"""empty message

Revision ID: 0a284763d2ea
Revises: 2871bb36e1ac
Create Date: 2020-08-17 18:00:54.138727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a284763d2ea'
down_revision = '2871bb36e1ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('queued_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('queue_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('queue_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('state', sa.Enum('requested', 'accepted', 'queued', 'rejected', 'blocked', name='queueduserstate'), nullable=True),
    sa.Column('meta', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['queue_id'], ['queues.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('queued_users')
    # ### end Alembic commands ###
