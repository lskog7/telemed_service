"""upd 1.1

Revision ID: a857e002a396
Revises: 10ae2ea388da
Create Date: 2024-11-13 22:51:56.495314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a857e002a396'
down_revision: Union[str, None] = '10ae2ea388da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('profiles', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('profiles', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
