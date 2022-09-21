"""supplier table

Revision ID: c4fc1db04ece
Revises: c6f1d299f680
Create Date: 2022-09-21 15:22:50.651522

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c4fc1db04ece'
down_revision = 'c6f1d299f680'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("suppliers",
                    sa.Column("uuid", sa.CHAR(36), nullable=False),
                    sa.Column("user_id", sa.CHAR(36), nullable=False),
                    sa.Column("company_id", sa.CHAR(36), nullable=False),
                    sa.Column("supplier_id", sa.String(), nullable=False),
                    sa.Column("name", sa.String(), nullable=False),
                    sa.Column("contact_name", sa.String()),
                    sa.Column("contact_phone", sa.String()),
                    sa.Column("contact_email", sa.String()),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint("uuid"),
                    sa.UniqueConstraint("name", "company_id"),
                    sa.ForeignKeyConstraint(("company_id",), ["companies.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("user_id",), ["users.uuid"], ondelete="RESTRICT")
                    )
    pass


def downgrade() -> None:
    op.drop_table("suppliers")
    pass
