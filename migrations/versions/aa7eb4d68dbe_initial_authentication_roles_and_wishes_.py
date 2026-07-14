"""Initial authentication, roles, and wishes schema

Revision ID: aa7eb4d68dbe
Revises: 
Create Date: 2026-07-14 05:47:41.952440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa7eb4d68dbe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_roles')),
        sa.UniqueConstraint('slug', name=op.f('uq_roles_slug'))
    )

    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('profile_image', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
        sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )

    op.create_table('user_roles',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_user_roles_role_id_roles'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_roles_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'role_id', name=op.f('pk_user_roles'))
    )

    op.create_table('wishes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('author', sa.String(length=100), nullable=False),
        sa.Column('role', sa.String(length=100), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('likes', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_wishes_user_id_users'), ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_wishes'))
    )

    op.create_table('wish_likes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('wish_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_wish_likes_user_id_users'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['wish_id'], ['wishes.id'], name=op.f('fk_wish_likes_wish_id_wishes'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_wish_likes'))
    )


def downgrade():
    op.drop_table('wish_likes')
    op.drop_table('wishes')
    op.drop_table('user_roles')
    op.drop_table('users')
    op.drop_table('roles')
