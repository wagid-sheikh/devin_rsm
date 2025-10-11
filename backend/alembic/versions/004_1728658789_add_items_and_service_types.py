"""add items and service types

Revision ID: 004_1728658789
Revises: 003_1728571800
Create Date: 2024-10-11 04:46:29.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision = '004_1728658789'
down_revision = '003_1728571800'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'service_types',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_service_types_code'), 'service_types', ['code'], unique=True)

    op.create_table(
        'items',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('company_id', sa.BigInteger(), nullable=False),
        sa.Column('sku', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('hsn_sac', sa.String(length=20), nullable=True),
        sa.Column('uom', sa.String(length=20), nullable=False),
        sa.Column('tax_rate', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_company_id'), 'items', ['company_id'], unique=False)
    op.create_index(op.f('ix_items_sku'), 'items', ['sku'], unique=False)
    op.create_index(op.f('ix_items_name'), 'items', ['name'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_items_name'), table_name='items')
    op.drop_index(op.f('ix_items_sku'), table_name='items')
    op.drop_index(op.f('ix_items_company_id'), table_name='items')
    op.drop_table('items')

    op.drop_index(op.f('ix_service_types_code'), table_name='service_types')
    op.drop_table('service_types')
