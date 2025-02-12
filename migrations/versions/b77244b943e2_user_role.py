"""User role

Revision ID: b77244b943e2
Revises: ed244e802c39
Create Date: 2025-01-17 10:47:55.005370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from models import UserRoleType

# revision identifiers, used by Alembic.
revision: str = 'b77244b943e2'
down_revision: Union[str, None] = 'ed244e802c39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    UserRoleType.create(op.get_bind(), checkfirst=True)
    op.add_column('user_account', sa.Column("role", UserRoleType, nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_account', 'role')
    UserRoleType.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
