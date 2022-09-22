"""invoice table

Revision ID: 9ef593cc4876
Revises: ac3f47e0b3f8
Create Date: 2022-09-21 21:20:12.088775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ef593cc4876'
down_revision = 'ac3f47e0b3f8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("invoices",
                    sa.Column("uuid", sa.CHAR(36), nullable=False),
                    sa.Column("user_id", sa.CHAR(36), nullable=False),
                    sa.Column("company_id", sa.CHAR(36), nullable=False),
                    sa.Column("project_id", sa.CHAR(36), nullable=False),
                    sa.Column("supplier_id", sa.CHAR(36), nullable=False),
                    sa.Column("invoice_number", sa.String(), nullable=False),
                    sa.Column("invoice_date", sa.Date(), nullable=False),
                    sa.Column("invoice_total", sa.Float(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint("uuid"),
                    sa.UniqueConstraint("project_id", "company_id", "supplier_id", "invoice_number"),
                    sa.ForeignKeyConstraint(("company_id",), ["companies.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("user_id",), ["users.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("supplier_id",), ["suppliers.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("project_id",), ["projects.uuid"], ondelete="RESTRICT")
                    )
    pass


def downgrade() -> None:
    op.drop_table("invoices")
    pass
