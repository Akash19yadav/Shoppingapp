import sqlalchemy_utils
"""update

Revision ID: 15d82ae5eb39
Revises: 
Create Date: 2022-08-17 15:42:42.558356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15d82ae5eb39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('slug', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('coupon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=True),
    sa.Column('valid_from', sa.DateTime(), nullable=True),
    sa.Column('valid_to', sa.DateTime(), nullable=True),
    sa.Column('discount', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('phone_number', sa.String(length=10), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=True),
    sa.Column('address', sa.String(length=500), nullable=True),
    sa.Column('postal_code', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=150), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('is_paid', sa.Boolean(), nullable=True),
    sa.Column('coupon_id', sa.Integer(), nullable=True),
    sa.Column('discount', sa.DECIMAL(scale=2), nullable=True),
    sa.Column('total_price', sa.DECIMAL(scale=2), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['coupon_id'], ['coupon.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('url', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.Column('price', sa.DECIMAL(scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('slug', sa.String(length=20), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('orderitem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.DECIMAL(scale=2), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orderitem')
    op.drop_table('product')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('coupon')
    op.drop_table('category')
    # ### end Alembic commands ###
