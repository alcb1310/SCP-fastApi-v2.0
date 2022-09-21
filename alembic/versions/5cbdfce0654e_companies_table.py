"""companies table

Revision ID: 5cbdfce0654e
Revises: 
Create Date: 2022-09-20 18:24:39.449707

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5cbdfce0654e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("companies",
                    sa.Column("uuid", sa.CHAR(36), nullable=False),
                    sa.Column("ruc", sa.String(), nullable=False),
                    sa.Column("name", sa.String(), nullable=False),
                    sa.Column("employees", sa.Integer(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint("uuid"),
                    sa.UniqueConstraint("ruc"),
                    sa.UniqueConstraint("name")
                    )
    pass


def downgrade() -> None:
    op.drop_table("companies")
    pass
