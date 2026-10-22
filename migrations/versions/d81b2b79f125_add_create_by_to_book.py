"""add create_by to book

Revision ID: d81b2b79f125
Revises: b2c336a06876
Create Date: 2026-10-22 15:30:58.555241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd81b2b79f125'
down_revision: Union[str, Sequence[str], None] = 'b2c336a06876'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_by', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_books_created_by_users',
            'users', ['created_by'], ['id'],
            ondelete='SET NULL'
        )

def downgrade() -> None:
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_constraint('fk_books_created_by_users', type_='foreignkey')
        batch_op.drop_column('created_by')