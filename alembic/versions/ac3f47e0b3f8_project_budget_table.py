"""project budget table

Revision ID: ac3f47e0b3f8
Revises: 550a0b5ef168
Create Date: 2022-09-21 21:06:43.422735

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ac3f47e0b3f8'
down_revision = '550a0b5ef168'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("project_budget",
                    sa.Column("uuid", sa.CHAR(36), nullable=False),
                    sa.Column("user_id", sa.CHAR(36), nullable=False),
                    sa.Column("company_id", sa.CHAR(36), nullable=False),
                    sa.Column("budget_item_id", sa.CHAR(36), nullable=False),
                    sa.Column("project_id", sa.CHAR(36), nullable=False),
                    sa.Column("initial_quantity", sa.Float()),
                    sa.Column("initial_cost", sa.Float()),
                    sa.Column("initial_total", sa.Float(), nullable=False),
                    sa.Column("spent_quantity", sa.Float()),
                    sa.Column("spent_total", sa.Float(), nullable=False),
                    sa.Column("to_spend_quantity", sa.Float()),
                    sa.Column("to_spend_cost", sa.Float()),
                    sa.Column("to_spend_total", sa.Float(), nullable=False),
                    sa.Column("updated_budget", sa.Float(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint("uuid"),
                    sa.UniqueConstraint("project_id", "company_id", "budget_item_id"),
                    sa.ForeignKeyConstraint(("company_id",), ["companies.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("user_id",), ["users.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("budget_item_id",), ["budget_items.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("project_id",), ["projects.uuid"], ondelete="RESTRICT"),
                    )
    pass


def downgrade() -> None:
    op.drop_table("project_budget")
    pass
