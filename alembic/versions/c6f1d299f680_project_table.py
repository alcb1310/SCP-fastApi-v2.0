"""project table

Revision ID: c6f1d299f680
Revises: 5f406f94f2d3
Create Date: 2022-09-20 20:39:12.630692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6f1d299f680'
down_revision = '5f406f94f2d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("projects", sa.Column("uuid", sa.CHAR(36), nullable=False),
                    sa.Column("name", sa.String, nullable=False),
                    sa.Column("user_id", sa.CHAR(36), nullable=False),
                    sa.Column("company_id", sa.CHAR(36), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint("uuid"),
                    sa.UniqueConstraint("name", "company_id"),
                    sa.ForeignKeyConstraint(("company_id",), ["companies.uuid"], ondelete="RESTRICT"),
                    sa.ForeignKeyConstraint(("user_id",), ["users.uuid"], ondelete="RESTRICT")
                )
    pass


def downgrade() -> None:
    op.drop_table("projects")
    pass
