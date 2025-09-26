"""Add courier enhancements and order channels

Revision ID: 02_add_courier_and_channels
Revises: 01_add_vendor_and_vehicle_types
Create Date: 2025-09-25 10:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '02_add_courier_and_channels'
down_revision = '01_add_vendor_and_vehicle_types'
branch_labels = None
depends_on = None

def upgrade():
    # Create VehicleType enum if it doesn't exist
    op.execute("""
        CREATE TYPE vehicletype AS ENUM (
            'bicycle', 'motorcycle', 'car', 'scooter', 'e_bike', 'walking'
        )
    """)

    # Create CourierStatus enum if it doesn't exist
    op.execute("""
        CREATE TYPE courierstatus AS ENUM (
            'offline', 'available', 'busy', 'on_break', 'maintenance'
        )
    """)

    # Add new columns to couriers table
    op.add_column('couriers', sa.Column('active_area', postgresql.JSON(), nullable=True))
    op.add_column('couriers', sa.Column('availability_hours', postgresql.JSON(), nullable=True))
    op.add_column('couriers', sa.Column('rating', sa.Float(), nullable=True, server_default='5.0'))
    op.add_column('couriers', sa.Column('total_deliveries', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('couriers', sa.Column('total_distance', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('couriers', sa.Column('current_load', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('couriers', sa.Column('vehicle_docs', postgresql.JSON(), nullable=True))
    op.add_column('couriers', sa.Column('insurance_info', postgresql.JSON(), nullable=True))
    op.add_column('couriers', sa.Column('delivery_preferences', postgresql.JSON(), nullable=True))
    op.add_column('couriers', sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('couriers', sa.Column('last_maintenance', sa.DateTime(), nullable=True))

    # Create order_channels table
    op.create_table(
        'order_channels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('channel_type', postgresql.ENUM('app', 'whatsapp', 'sms', 'phone', 'ussd', 'web', name='orderchanneltype'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('config', postgresql.JSON(), nullable=True),
        sa.Column('phone_number', sa.String(20), nullable=True),
        sa.Column('api_credentials', postgresql.JSON(), nullable=True),
        sa.Column('webhook_url', sa.String(255), nullable=True),
        sa.Column('rate_limit', sa.Integer(), nullable=True),
        sa.Column('operating_hours', postgresql.JSON(), nullable=True),
        sa.Column('error_messages', postgresql.JSON(), nullable=True),
        sa.Column('success_messages', postgresql.JSON(), nullable=True),
        sa.Column('menu_format', postgresql.JSON(), nullable=True),
        sa.PrimaryKey('id')
    )

def downgrade():
    # Drop order_channels table
    op.drop_table('order_channels')

    # Drop new columns from couriers table
    op.drop_column('couriers', 'last_maintenance')
    op.drop_column('couriers', 'is_verified')
    op.drop_column('couriers', 'delivery_preferences')
    op.drop_column('couriers', 'insurance_info')
    op.drop_column('couriers', 'vehicle_docs')
    op.drop_column('couriers', 'current_load')
    op.drop_column('couriers', 'total_distance')
    op.drop_column('couriers', 'total_deliveries')
    op.drop_column('couriers', 'rating')
    op.drop_column('couriers', 'availability_hours')
    op.drop_column('couriers', 'active_area')

    # Drop enums
    op.execute('DROP TYPE orderchanneltype')
    op.execute('DROP TYPE vehicletype')
    op.execute('DROP TYPE courierstatus')