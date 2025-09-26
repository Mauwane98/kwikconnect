"""Add vendor types and courier vehicle types

Revision ID: 01_add_vendor_and_vehicle_types
Revises: 93dba145e9cc
Create Date: 2025-09-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '01_add_vendor_and_vehicle_types'
down_revision = '93dba145e9cc'
branch_labels = None
depends_on = None

def upgrade():
    # Create VendorType enum
    op.execute("""
        CREATE TYPE vendortype AS ENUM (
            'spaza', 'supermarket', 'butchery', 'pharmacy', 'fast_food',
            'street_food', 'tavern', 'hardware', 'clothing', 'salon',
            'electronics', 'stationery', 'fruit_and_vegetables', 'bakery',
            'tuckshop', 'cell_phone_shop', 'car_wash', 'laundry',
            'restaurant', 'other'
        )
    """)

    # Add new columns to vendors table
    op.add_column('vendors', sa.Column('vendor_type', postgresql.ENUM('spaza', 'supermarket', 'butchery', 'pharmacy', 'fast_food', 'street_food', 'tavern', 'hardware', 'clothing', 'salon', 'electronics', 'stationery', 'fruit_and_vegetables', 'bakery', 'tuckshop', 'cell_phone_shop', 'car_wash', 'laundry', 'restaurant', 'other', name='vendortype'), nullable=False, server_default='other'))
    op.add_column('vendors', sa.Column('delivery_radius', sa.Float(), nullable=True))
    op.add_column('vendors', sa.Column('minimum_order', sa.Float(), nullable=True))
    op.add_column('vendors', sa.Column('estimated_delivery_time', sa.Integer(), nullable=True))
    op.add_column('vendors', sa.Column('licenses', postgresql.JSON(), nullable=True))
    op.add_column('vendors', sa.Column('features', postgresql.JSON(), nullable=True))
    op.add_column('vendors', sa.Column('payment_methods', postgresql.JSON(), nullable=True))
    
    # Modify operating_hours to JSON type
    op.alter_column('vendors', 'operating_hours',
                    existing_type=sa.String(length=255),
                    type_=postgresql.JSON(),
                    existing_nullable=True)

def downgrade():
    # Drop new columns from vendors table
    op.drop_column('vendors', 'payment_methods')
    op.drop_column('vendors', 'features')
    op.drop_column('vendors', 'licenses')
    op.drop_column('vendors', 'estimated_delivery_time')
    op.drop_column('vendors', 'minimum_order')
    op.drop_column('vendors', 'delivery_radius')
    op.drop_column('vendors', 'vendor_type')
    
    # Revert operating_hours to string
    op.alter_column('vendors', 'operating_hours',
                    existing_type=postgresql.JSON(),
                    type_=sa.String(length=255),
                    existing_nullable=True)
    
    # Drop VendorType enum
    op.execute('DROP TYPE vendortype')