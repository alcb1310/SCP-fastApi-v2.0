"""add user table

Revision ID: 5f406f94f2d3
Revises: 5cbdfce0654e
Create Date: 2022-09-20 18:49:38.636971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f406f94f2d3'
down_revision = '5cbdfce0654e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("uuid", sa.CHAR(36), nullable=False),
                    sa.Column("company_id", sa.CHAR(36), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("name", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint("uuid"),
                    sa.UniqueConstraint("email"),
                    sa.ForeignKeyConstraint(("company_id",), ["companies.uuid"], ondelete="RESTRICT"),
                )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
