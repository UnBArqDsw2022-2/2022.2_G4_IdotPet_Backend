"""Remove breed constraint

Revision ID: 577e7f054627
Revises: cbff66881778
Create Date: 2023-01-30 03:47:21.802126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '577e7f054627'
down_revision = 'cbff66881778'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('base_users', 'birth_day',
               existing_type=sa.DATE(),
               nullable=True)
    op.drop_constraint('pet_specie_name_breed_name_fkey', 'pet', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('pet_specie_name_breed_name_fkey', 'pet', 'pet_breed', ['specie_name', 'breed_name'], ['specie_name', 'breed_name'])
    op.alter_column('base_users', 'birth_day',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###
