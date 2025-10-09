"""add company_gstin_id foreign key to stores

Revision ID: d995159813bc
Revises: 001_1760020500
Create Date: 2025-10-09 15:35:58.895486

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'd995159813bc'
down_revision: str | None = '001_1760020500'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'stores',
        sa.Column('company_gstin_id', sa.BigInteger(), nullable=True)
    )
    op.create_index(
        op.f('ix_stores_company_gstin_id'),
        'stores',
        ['company_gstin_id'],
        unique=False
    )
    op.create_foreign_key(
        'fk_stores_company_gstin_id',
        'stores',
        'company_gstins',
        ['company_gstin_id'],
        ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    op.drop_constraint('fk_stores_company_gstin_id', 'stores', type_='foreignkey')
    op.drop_index(op.f('ix_stores_company_gstin_id'), table_name='stores')
    op.drop_column('stores', 'company_gstin_id')
