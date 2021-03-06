"""try to fix customer

Revision ID: bf253509d775
Revises: a3cb3594a772
Create Date: 2021-04-25 14:14:53.318716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf253509d775'
down_revision = 'a3cb3594a772'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('customer_id', sa.Integer(), nullable=False))
    op.drop_constraint('cart__customer_id_fkey', 'cart', type_='foreignkey')
    op.create_foreign_key(None, 'cart', 'customer', ['customer_id'], ['id'])
    op.drop_column('cart', '_customer_id')
    op.add_column('product_photo', sa.Column('product_id', sa.Integer(), nullable=False))
    op.drop_constraint('product_photo__product_id_fkey', 'product_photo', type_='foreignkey')
    op.create_foreign_key(None, 'product_photo', 'product', ['product_id'], ['id'])
    op.drop_column('product_photo', '_product_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_photo', sa.Column('_product_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'product_photo', type_='foreignkey')
    op.create_foreign_key('product_photo__product_id_fkey', 'product_photo', 'product', ['_product_id'], ['id'])
    op.drop_column('product_photo', 'product_id')
    op.add_column('cart', sa.Column('_customer_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.create_foreign_key('cart__customer_id_fkey', 'cart', 'customer', ['_customer_id'], ['id'])
    op.drop_column('cart', 'customer_id')
    # ### end Alembic commands ###
