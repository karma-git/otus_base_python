"""fix one-to-one p - pp

Revision ID: 106b9766576f
Revises: fdf620b9f816
Create Date: 2021-04-25 14:48:38.313650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '106b9766576f'
down_revision = 'fdf620b9f816'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_photo', sa.Column('product', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'product_photo', 'product', ['product'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_photo', type_='foreignkey')
    op.drop_column('product_photo', 'product')
    # ### end Alembic commands ###
