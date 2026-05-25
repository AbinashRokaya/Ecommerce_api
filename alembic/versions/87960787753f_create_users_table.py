# alembic/versions/87960787753f_create_users_table.py

from alembic import op
import sqlalchemy as sa
# Import postgresql dialect to access ENUM
from sqlalchemy.dialects import postgresql 

# revision identifiers, used by Alembic.
revision = '87960787753f'
down_revision = 'cb4fa6099ec9'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. Create the enum type in the database first
    user_role_enum = postgresql.ENUM('User', 'Admin', name='role_schema')
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # 2. Add the column using the created type
    op.add_column('users', sa.Column('user_role', sa.Enum('User', 'Admin', name='role_schema'), nullable=True))


def downgrade() -> None:
    # 1. Drop the column first
    op.drop_column('users', 'user_role')

    # 2. Drop the custom enum type from the database
    user_role_enum = postgresql.ENUM('User', 'Admin', name='role_schema')
    user_role_enum.drop(op.get_bind(), checkfirst=True)
