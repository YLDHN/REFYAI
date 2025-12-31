"""Add new features tables

Revision ID: 002
Revises: 001
Create Date: 2025-12-31

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Ajouter colonnes manquantes à projects
    op.add_column('projects', sa.Column('questionnaire_data', postgresql.JSON(), nullable=True))
    op.add_column('projects', sa.Column('showstoppers', postgresql.JSON(), nullable=True))
    op.add_column('projects', sa.Column('market_analysis', postgresql.JSON(), nullable=True))
    op.add_column('projects', sa.Column('interest_rate', sa.Float(), nullable=True))
    op.add_column('projects', sa.Column('tender_end_date', sa.DateTime(timezone=True), nullable=True))
    
    # 2. Créer table privacy_shield_status
    op.create_table(
        'privacy_shield_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('tender_end_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('release_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_protected', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('released_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_privacy_shield_status_project_id'), 'privacy_shield_status', ['project_id'], unique=True)
    op.create_index(op.f('ix_privacy_shield_status_release_date'), 'privacy_shield_status', ['release_date'], unique=False)
    
    # 3. Créer table capex_costs (coûts travaux)
    op.create_table(
        'capex_costs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),  # structure, facade, toiture, etc.
        sa.Column('subcategory', sa.String(), nullable=True),
        sa.Column('unit', sa.String(), nullable=False),  # m2, m3, unité
        sa.Column('min_price', sa.Float(), nullable=False),
        sa.Column('avg_price', sa.Float(), nullable=False),
        sa.Column('max_price', sa.Float(), nullable=False),
        sa.Column('city_tier', sa.Integer(), nullable=False, default=1),  # 1=Paris/Lyon, 2=Grandes villes, 3=Province
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('source', sa.String(), nullable=True),  # FFB, CSTB, etc.
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_capex_costs_category'), 'capex_costs', ['category'], unique=False)
    op.create_index(op.f('ix_capex_costs_city_tier'), 'capex_costs', ['city_tier'], unique=False)
    
    # 4. Créer table administrative_delays (délais administratifs)
    op.create_table(
        'administrative_delays',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('postal_code', sa.String(), nullable=True),
        sa.Column('procedure_type', sa.String(), nullable=False),  # PC, DP, AT, etc.
        sa.Column('avg_delay_days', sa.Integer(), nullable=False),
        sa.Column('min_delay_days', sa.Integer(), nullable=True),
        sa.Column('max_delay_days', sa.Integer(), nullable=True),
        sa.Column('complexity_factor', sa.Float(), nullable=True, default=1.0),
        sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('source', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_administrative_delays_city'), 'administrative_delays', ['city'], unique=False)
    op.create_index(op.f('ix_administrative_delays_procedure_type'), 'administrative_delays', ['procedure_type'], unique=False)
    
    # 5. Créer table plu_zones (données PLU préchargées)
    op.create_table(
        'plu_zones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('zone_name', sa.String(), nullable=False),  # UC, UB, N, A, etc.
        sa.Column('zone_type', sa.String(), nullable=False),  # urbain, agricole, naturel
        sa.Column('is_constructible', sa.Boolean(), nullable=False),
        sa.Column('max_height', sa.Float(), nullable=True),
        sa.Column('cos', sa.Float(), nullable=True),  # Coefficient Occupation Sol
        sa.Column('ces', sa.Float(), nullable=True),  # Coefficient Emprise Sol
        sa.Column('constraints', postgresql.JSON(), nullable=True),  # Liste contraintes spécifiques
        sa.Column('permitted_uses', postgresql.JSON(), nullable=True),  # Destinations autorisées
        sa.Column('document_url', sa.String(), nullable=True),
        sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plu_zones_city'), 'plu_zones', ['city'], unique=False)
    op.create_index(op.f('ix_plu_zones_zone_name'), 'plu_zones', ['zone_name'], unique=False)
    
    # 6. Créer table technical_norms (normes techniques)
    op.create_table(
        'technical_norms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('norm_type', sa.String(), nullable=False),  # ERP, incendie, PMR, structure, etc.
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('requirement', sa.String(), nullable=False),
        sa.Column('regulation_reference', sa.String(), nullable=True),  # Code Construction, AT, etc.
        sa.Column('applies_to', postgresql.JSON(), nullable=True),  # Types de bâtiments concernés
        sa.Column('severity', sa.String(), nullable=True),  # obligatoire, recommandé
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_technical_norms_norm_type'), 'technical_norms', ['norm_type'], unique=False)
    op.create_index(op.f('ix_technical_norms_category'), 'technical_norms', ['category'], unique=False)


def downgrade():
    # Supprimer les tables dans l'ordre inverse
    op.drop_index(op.f('ix_technical_norms_category'), table_name='technical_norms')
    op.drop_index(op.f('ix_technical_norms_norm_type'), table_name='technical_norms')
    op.drop_table('technical_norms')
    
    op.drop_index(op.f('ix_plu_zones_zone_name'), table_name='plu_zones')
    op.drop_index(op.f('ix_plu_zones_city'), table_name='plu_zones')
    op.drop_table('plu_zones')
    
    op.drop_index(op.f('ix_administrative_delays_procedure_type'), table_name='administrative_delays')
    op.drop_index(op.f('ix_administrative_delays_city'), table_name='administrative_delays')
    op.drop_table('administrative_delays')
    
    op.drop_index(op.f('ix_capex_costs_city_tier'), table_name='capex_costs')
    op.drop_index(op.f('ix_capex_costs_category'), table_name='capex_costs')
    op.drop_table('capex_costs')
    
    op.drop_index(op.f('ix_privacy_shield_status_release_date'), table_name='privacy_shield_status')
    op.drop_index(op.f('ix_privacy_shield_status_project_id'), table_name='privacy_shield_status')
    op.drop_table('privacy_shield_status')
    
    # Supprimer colonnes ajoutées à projects
    op.drop_column('projects', 'tender_end_date')
    op.drop_column('projects', 'interest_rate')
    op.drop_column('projects', 'market_analysis')
    op.drop_column('projects', 'showstoppers')
    op.drop_column('projects', 'questionnaire_data')
