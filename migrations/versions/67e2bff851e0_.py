"""empty message

Revision ID: 67e2bff851e0
Revises: 530a69f6c355
Create Date: 2023-11-14 22:18:13.307324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67e2bff851e0'
down_revision = '530a69f6c355'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('poke_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('poke_id')
    )
    op.create_table('added_to_team',
    sa.Column('poke_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['poke_id'], ['pokemon.poke_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('added_to_team')
    op.drop_table('pokemon')
    # ### end Alembic commands ###
