"""invoice details table

Revision ID: f03d4c5663e2
Revises: 9ef593cc4876
Create Date: 2022-09-21 21:30:15.118226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f03d4c5663e2'
down_revision = '9ef593cc4876'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("invoice_details",
                    sa.Column("uuid", sa.CHAR(36), nullable=False),
                    sa.Column("user_id", sa.CHAR(36), nullable=False),
                    sa.Column("company_id", sa.CHAR(36), nullable=False),
                    sa.Column("invoice_id", sa.CHAR(36), nullable=False),
                    sa.Column("budget_item_id", sa.CHAR(36), nullable=False),
                    sa.Column("quantity", sa.Float(), nullable=False),
                    sa.Column("cost", sa.Float(), nullable=False),
                    sa.Column("total", sa.Float(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint("uuid"),
                    sa.ForeignKeyConstraint(("company_id",), ["companies.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("user_id",), ["users.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("invoice_id",), ["invoices.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("budget_item_id",), ["budget_items.uuid"], ondelete="RESTRICT")
                    )
    pass


def downgrade() -> None:
    op.drop_table("invoice_details")
    pass
