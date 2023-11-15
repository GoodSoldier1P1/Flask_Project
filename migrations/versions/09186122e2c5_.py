"""empty message

Revision ID: 09186122e2c5
Revises: 67e2bff851e0
Create Date: 2023-11-14 23:03:01.727355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09186122e2c5'
down_revision = '67e2bff851e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pokemon', schema=None) as batch_op:
        batch_op.alter_column('poke_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pokemon', schema=None) as batch_op:
        batch_op.alter_column('poke_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
