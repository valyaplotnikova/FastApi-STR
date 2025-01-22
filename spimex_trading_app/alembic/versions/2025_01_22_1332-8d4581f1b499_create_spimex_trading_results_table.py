"""create spimex_trading_results table

Revision ID: 8d4581f1b499
Revises: 
Create Date: 2025-01-22 13:32:27.523017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '8d4581f1b499'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('spimex_trading_results',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('exchange_product_id', sa.String(), nullable=True),
    sa.Column('exchange_product_name', sa.String(), nullable=True),
    sa.Column('oil_id', sa.String(), nullable=True),
    sa.Column('delivery_basis_id', sa.String(), nullable=True),
    sa.Column('delivery_basis_name', sa.String(), nullable=True),
    sa.Column('delivery_type_id', sa.String(), nullable=True),
    sa.Column('volume', sa.Float(), nullable=True),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('created_on', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_on', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_spimex_trading_results'))
    )


def downgrade() -> None:
    op.drop_table('spimex_trading_results')

