"""budget items table

Revision ID: 550a0b5ef168
Revises: c4fc1db04ece
Create Date: 2022-09-21 20:56:03.533739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '550a0b5ef168'
down_revision = 'c4fc1db04ece'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("budget_items",
                    sa.Column("uuid", sa.CHAR(36), nullable=False),
                    sa.Column("user_id", sa.CHAR(36), nullable=False),
                    sa.Column("company_id", sa.CHAR(36), nullable=False),
                    sa.Column("code", sa.String(), nullable=False),
                    sa.Column("name", sa.String(), nullable=False),
                    sa.Column("accumulates", sa.Boolean(), nullable=False),
                    sa.Column("level", sa.Integer()),
                    sa.Column("parent_id", sa.CHAR(36)),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint("uuid"),
                    sa.UniqueConstraint("name", "company_id"),
                    sa.UniqueConstraint("code", "company_id"),
                    sa.ForeignKeyConstraint(("company_id",), ["companies.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("user_id",), ["users.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("parent_id",), ["budget_items.uuid"], ondelete="RESTRICT")
                    )
    pass


def downgrade() -> None:
    op.drop_table("budget_items")
    pass
