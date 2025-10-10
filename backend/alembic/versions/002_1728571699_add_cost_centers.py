"""add cost centers

Revision ID: 002_1728571699
Revises: 001_1760020500
Create Date: 2025-10-08 14:58:19

"""

import sqlalchemy as sa

from alembic import op

revision = "002_1728571699"
down_revision = "001_1760020500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cost_centers",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(
        op.f("ix_cost_centers_code"), "cost_centers", ["code"], unique=True
    )

    op.create_table(
        "company_cost_centers",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.BigInteger(), nullable=False),
        sa.Column("cost_center_id", sa.BigInteger(), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
        ),
        sa.ForeignKeyConstraint(
            ["cost_center_id"],
            ["cost_centers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_company_cost_centers_company_id"),
        "company_cost_centers",
        ["company_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_company_cost_centers_cost_center_id"),
        "company_cost_centers",
        ["cost_center_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_company_cost_centers_cost_center_id"),
        table_name="company_cost_centers",
    )
    op.drop_index(
        op.f("ix_company_cost_centers_company_id"), table_name="company_cost_centers"
    )
    op.drop_table("company_cost_centers")
    op.drop_index(op.f("ix_cost_centers_code"), table_name="cost_centers")
    op.drop_table("cost_centers")
