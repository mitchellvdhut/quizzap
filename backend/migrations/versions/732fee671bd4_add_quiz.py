"""Add quiz

Revision ID: 732fee671bd4
Revises: ca1950aac03e
Create Date: 2024-11-24 13:43:44.124294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '732fee671bd4'
down_revision: Union[str, None] = 'ca1950aac03e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer')
    op.drop_table('question')
    op.drop_table('quiz')
    # ### end Alembic commands ###
