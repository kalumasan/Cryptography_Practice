"""empty message

Revision ID: b2a91c13f0c4
Revises: 9b022760aaf9
Create Date: 2023-07-25 00:12:16.914099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2a91c13f0c4'
down_revision = '9b022760aaf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('creator_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('filename', sa.String(length=64), nullable=False),
    sa.Column('hash_value', sa.String(length=128), nullable=True),
    sa.Column('shared', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('creator_id', 'filename')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    # ### end Alembic commands ###
