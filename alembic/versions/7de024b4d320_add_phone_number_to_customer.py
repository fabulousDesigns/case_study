"""Add phone_number to Customer

Revision ID: 7de024b4d320
Revises: b926f7a80b01
Create Date: 2024-07-18 17:13:36.449790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7de024b4d320'
down_revision: Union[str, None] = 'b926f7a80b01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('phone_number', sa.String(), nullable=True))
    op.create_index(op.f('ix_customers_phone_number'), 'customers', ['phone_number'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_customers_phone_number'), table_name='customers')
    op.drop_column('customers', 'phone_number')
    # ### end Alembic commands ###