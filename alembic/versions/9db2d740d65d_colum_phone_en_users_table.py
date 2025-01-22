"""colum phone en users table

Revision ID: 9db2d740d65d
Revises: 
Create Date: 2025-01-21 15:07:33.538204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9db2d740d65d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# para actualizar algunos cambios pasamos los datos que queremos actualizar
def upgrade() -> None:
    op.add_column('users', sa.Column('phone', sa.String()))


def downgrade() -> None:
    op.drop_column('users', 'phone')
