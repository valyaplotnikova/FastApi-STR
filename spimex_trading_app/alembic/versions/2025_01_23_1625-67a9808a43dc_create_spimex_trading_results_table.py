"""create spimex_trading_results table

Revision ID: 67a9808a43dc
Revises: 8d4581f1b499
Create Date: 2025-01-23 16:25:55.143025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '67a9808a43dc'
down_revision: Union[str, None] = '8d4581f1b499'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('spimex_trading_results', 'exchange_product_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('spimex_trading_results', 'exchange_product_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('spimex_trading_results', 'oil_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('spimex_trading_results', 'delivery_basis_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('spimex_trading_results', 'delivery_basis_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('spimex_trading_results', 'delivery_type_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('spimex_trading_results', 'volume',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('spimex_trading_results', 'total',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('spimex_trading_results', 'count',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               nullable=False)
    op.alter_column('spimex_trading_results', 'date',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('spimex_trading_results', 'created_on',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('spimex_trading_results', 'updated_on',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('spimex_trading_results', 'updated_on',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('spimex_trading_results', 'created_on',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('spimex_trading_results', 'date',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('spimex_trading_results', 'count',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               nullable=True)
    op.alter_column('spimex_trading_results', 'total',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('spimex_trading_results', 'volume',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('spimex_trading_results', 'delivery_type_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('spimex_trading_results', 'delivery_basis_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('spimex_trading_results', 'delivery_basis_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('spimex_trading_results', 'oil_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('spimex_trading_results', 'exchange_product_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('spimex_trading_results', 'exchange_product_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
