"""Add field in Evalaution table

Revision ID: 40f285a8695c
Revises: 85d8193b9a8a
Create Date: 2025-02-21 13:49:20.671689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '40f285a8695c'
down_revision: Union[str, None] = '85d8193b9a8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('evaluation_result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('evaluation_id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_submitted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['evaluation_id'], ['evaluation.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['teacher_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_evaluation_result_id'), 'evaluation_result', ['id'], unique=False)
    op.drop_index('ix_evaluationresult_id', table_name='evaluationresult')
    op.drop_table('evaluationresult')
    op.add_column('question', sa.Column('evaluation_result_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'question', 'evaluation_result', ['evaluation_result_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.drop_column('question', 'evaluation_result_id')
    op.create_table('evaluationresult',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('evaluation_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('admin_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_submitted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['evaluation_id'], ['evaluation.id'], name='evaluationresult_evaluation_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['teacher_id'], ['user.id'], name='evaluationresult_teacher_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='evaluationresult_pkey')
    )
    op.create_index('ix_evaluationresult_id', 'evaluationresult', ['id'], unique=False)
    op.drop_index(op.f('ix_evaluation_result_id'), table_name='evaluation_result')
    op.drop_table('evaluation_result')
    # ### end Alembic commands ###
