"""Add pet

Revision ID: e93f186c5ebd
Revises: 87c4f064386f
Create Date: 2023-01-28 23:52:32.778450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e93f186c5ebd'
down_revision = '87c4f064386f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pet_breed',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=True),
    sa.Column('specie_name', sa.String(length=150), nullable=False),
    sa.Column('breed_name', sa.String(length=150), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('specie_name', 'breed_name')
    )
    op.create_table('pet',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('cep', sa.String(length=20), nullable=True),
    sa.Column('specie_name', sa.String(length=150), nullable=False),
    sa.Column('breed_name', sa.String(length=150), nullable=False),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('size', sa.String(length=150), nullable=False),
    sa.Column('gender', sa.Enum('f', 'm', name='pet_gender'), nullable=False),
    sa.Column('status', sa.Enum('ADOPTED', 'ANNOUNCED', 'AVAILABLE', name='petstatus'), nullable=False),
    sa.Column('vaccine', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['specie_name', 'breed_name'], ['pet_breed.specie_name', 'pet_breed.breed_name'], ),
    sa.ForeignKeyConstraint(['user_id'], ['base_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pet')
    op.drop_table('pet_breed')
    # ### end Alembic commands ###