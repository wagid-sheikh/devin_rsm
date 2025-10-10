"""add_customer_models

Revision ID: 003_1728571800
Revises: 002_1728571699
Create Date: 2025-10-10 16:25:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = '003_1728571800'
down_revision: str | None = '002_1728571699'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'customers',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('company_id', sa.BigInteger(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('phone_primary', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_company_id'), 'customers', ['company_id'], unique=False)
    op.create_index(op.f('ix_customers_code'), 'customers', ['code'], unique=False)
    op.create_index(op.f('ix_customers_name'), 'customers', ['name'], unique=False)
    op.create_index(op.f('ix_customers_phone_primary'), 'customers', ['phone_primary'], unique=False)
    op.create_index(op.f('ix_customers_email'), 'customers', ['email'], unique=False)

    op.create_table(
        'customer_contacts',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('customer_id', sa.BigInteger(), nullable=False),
        sa.Column('contact_person', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_contacts_customer_id'), 'customer_contacts', ['customer_id'], unique=False)

    op.create_table(
        'customer_addresses',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('customer_id', sa.BigInteger(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('is_pickup_default', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_delivery_default', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_addresses_customer_id'), 'customer_addresses', ['customer_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_customer_addresses_customer_id'), table_name='customer_addresses')
    op.drop_table('customer_addresses')
    op.drop_index(op.f('ix_customer_contacts_customer_id'), table_name='customer_contacts')
    op.drop_table('customer_contacts')
    op.drop_index(op.f('ix_customers_email'), table_name='customers')
    op.drop_index(op.f('ix_customers_phone_primary'), table_name='customers')
    op.drop_index(op.f('ix_customers_name'), table_name='customers')
    op.drop_index(op.f('ix_customers_code'), table_name='customers')
    op.drop_index(op.f('ix_customers_company_id'), table_name='customers')
    op.drop_table('customers')
