"""add session_id to session_logs

Revision ID: 0d61bc7fd937
Revises: 28657c2940ee
Create Date: 2026-09-13 11:24:33.168300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d61bc7fd937'
down_revision: Union[str, Sequence[str], None] = '28657c2940ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "session_logs",
        sa.Column(
            "session_id",
            postgresql.UUID(as_uuid=True),
            nullable=False
        )
    )

    op.create_unique_constraint(
        "uq_session_logs_session_id",
        "session_logs",
        ["session_id"]
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
