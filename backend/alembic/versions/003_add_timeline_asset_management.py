"""Add timeline and asset management models

Revision ID: 003
Revises: 002
Create Date: 2025-01-03

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # === 1. Créer table project_timelines ===
    op.create_table(
        'project_timelines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        
        # Phases dates
        sa.Column('studies_start', sa.Date(), nullable=True),
        sa.Column('studies_end', sa.Date(), nullable=True),
        sa.Column('permit_start', sa.Date(), nullable=True),
        sa.Column('permit_end', sa.Date(), nullable=True),
        sa.Column('construction_start', sa.Date(), nullable=True),
        sa.Column('construction_end', sa.Date(), nullable=True),
        sa.Column('commercialization_start', sa.Date(), nullable=True),
        sa.Column('commercialization_end', sa.Date(), nullable=True),
        
        # Budgets phases
        sa.Column('studies_budget', sa.Float(), nullable=True),
        sa.Column('permit_budget', sa.Float(), nullable=True),
        sa.Column('construction_budget', sa.Float(), nullable=True),
        sa.Column('commercialization_budget', sa.Float(), nullable=True),
        
        # CAPEX curve
        sa.Column('capex_curve_type', sa.String(), nullable=True, default='S_CURVE'),
        sa.Column('cashflow_schedule', postgresql.JSON(), nullable=True),
        
        # Mode exécution
        sa.Column('execution_mode', sa.String(), nullable=True, default='sequential'),
        
        # Métadonnées
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_project_timelines_project_id', 'project_timelines', ['project_id'], unique=True)
    
    
    # === 2. Ajouter colonnes Asset Management à projects ===
    op.add_column('projects', sa.Column('rent_free_months', sa.Integer(), nullable=True, default=0))
    op.add_column('projects', sa.Column('tenant_improvements', sa.Float(), nullable=True, default=0))
    op.add_column('projects', sa.Column('indexation_type', sa.String(), nullable=True, default='NONE'))
    op.add_column('projects', sa.Column('indexation_rate', sa.Float(), nullable=True, default=0.0))
    op.add_column('projects', sa.Column('indexation_start_year', sa.Integer(), nullable=True, default=1))
    op.add_column('projects', sa.Column('last_indexation_date', sa.Date(), nullable=True))
    
    
    # === 3. Ajouter colonnes typologie et autres ===
    op.add_column('projects', sa.Column('typologie', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('zip_code', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('estimated_budget', sa.Float(), nullable=True))
    op.add_column('projects', sa.Column('equity', sa.Float(), nullable=True))
    op.add_column('projects', sa.Column('loan_amount', sa.Float(), nullable=True))
    op.add_column('projects', sa.Column('ltv', sa.Float(), nullable=True))
    op.add_column('projects', sa.Column('tri', sa.Float(), nullable=True))
    op.add_column('projects', sa.Column('van', sa.Float(), nullable=True))


def downgrade():
    # Supprimer colonnes projects
    op.drop_column('projects', 'van')
    op.drop_column('projects', 'tri')
    op.drop_column('projects', 'ltv')
    op.drop_column('projects', 'loan_amount')
    op.drop_column('projects', 'equity')
    op.drop_column('projects', 'estimated_budget')
    op.drop_column('projects', 'zip_code')
    op.drop_column('projects', 'typologie')
    op.drop_column('projects', 'last_indexation_date')
    op.drop_column('projects', 'indexation_start_year')
    op.drop_column('projects', 'indexation_rate')
    op.drop_column('projects', 'indexation_type')
    op.drop_column('projects', 'tenant_improvements')
    op.drop_column('projects', 'rent_free_months')
    
    # Supprimer table timelines
    op.drop_index('ix_project_timelines_project_id', table_name='project_timelines')
    op.drop_table('project_timelines')
