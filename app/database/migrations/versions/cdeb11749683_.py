"""empty message

Revision ID: cdeb11749683
Revises: 5e26b8e3087d
Create Date: 2025-11-10 17:11:30.268537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdeb11749683'
down_revision: Union[str, None] = '5e26b8e3087d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('trick', schema=None) as batch_op:
        batch_op.alter_column('video',
                              existing_type=sa.String(),
                              nullable=True)

def downgrade():
    with op.batch_alter_table('trick', schema=None) as batch_op:
        batch_op.alter_column('video',
                              existing_type=sa.String(),
                              nullable=False)