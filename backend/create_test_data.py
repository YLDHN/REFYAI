"""
Script pour créer des projets de test
"""
import asyncio
from app.core.database import AsyncSessionLocal
from app.models.project import Project, ProjectStatus, ProjectType
from datetime import datetime, timedelta

async def create_test_projects():
    async with AsyncSessionLocal() as session:
        # Créer un utilisateur test si nécessaire
        from sqlalchemy import select
        from app.models.user import User
        
        result = await session.execute(select(User).where(User.email == "test@example.com"))
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(
                email="test@example.com",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5L2nCkJ3L5gKe",  # "password"
                full_name="Test User",
                is_active=True,
                is_superuser=False
            )
            session.add(user)
            await session.flush()
        
        # Projets de test
        projects = [
            Project(
                user_id=user.id,
                name="Immeuble Haussmannien - Paris 8ème",
                description="Immeuble de standing avec 8 appartements",
                address="45 Avenue des Champs-Élysées",
                city="Paris",
                postal_code="75008",
                project_type="rental",
                status="in_progress",
                strategy="core_plus",
                bp_duration=10,
                asset_type="residential",
                surface=800.0,
                purchase_price=5000000.0,
                renovation_budget=500000.0,
                estimated_value=6000000.0,
                current_rent=300000.0,
                market_rent=350000.0,
                occupancy_rate=95.0,
                walb=3.5,
                walt=5.2,
                acquisition_price=5000000.0,
                notary_fees=250000.0,
                financing_amount=3500000.0,
                ltv=70.0,
                interest_rate=3.5,
                loan_duration=15,
                technical_score=8.5,
                risk_score=6.2
            ),
            Project(
                user_id=user.id,
                name="Bureaux Neuilly-sur-Seine",
                description="Immeuble de bureaux moderne",
                address="12 Rue du Château",
                city="Neuilly-sur-Seine",
                postal_code="92200",
                project_type="rental",
                status="completed",
                strategy="core",
                bp_duration=12,
                asset_type="office",
                surface=1500.0,
                purchase_price=8000000.0,
                renovation_budget=200000.0,
                estimated_value=8500000.0,
                current_rent=500000.0,
                market_rent=520000.0,
                occupancy_rate=100.0,
                walb=4.0,
                walt=6.5,
                acquisition_price=8000000.0,
                notary_fees=400000.0,
                financing_amount=5600000.0,
                ltv=70.0,
                interest_rate=3.2,
                loan_duration=20,
                technical_score=9.2,
                risk_score=4.5
            ),
            Project(
                user_id=user.id,
                name="Entrepôt Logistique Lyon",
                description="Plateforme logistique proche A7",
                address="Zone industrielle Nord",
                city="Lyon",
                postal_code="69007",
                project_type="rental",
                status="in_progress",
                strategy="value_add",
                bp_duration=8,
                asset_type="logistics",
                surface=5000.0,
                purchase_price=3000000.0,
                renovation_budget=800000.0,
                estimated_value=4500000.0,
                current_rent=250000.0,
                market_rent=300000.0,
                occupancy_rate=80.0,
                walb=2.5,
                walt=4.0,
                acquisition_price=3000000.0,
                notary_fees=150000.0,
                financing_amount=2400000.0,
                ltv=80.0,
                interest_rate=4.0,
                loan_duration=12,
                technical_score=7.8,
                risk_score=7.5
            ),
            Project(
                user_id=user.id,
                name="Centre Commercial Bordeaux",
                description="Galerie commerciale rénovée",
                address="Place de la Comédie",
                city="Bordeaux",
                postal_code="33000",
                project_type="rental",
                status="draft",
                strategy="core_plus",
                bp_duration=10,
                asset_type="retail",
                surface=2500.0,
                purchase_price=6000000.0,
                renovation_budget=1000000.0,
                estimated_value=7500000.0,
                current_rent=400000.0,
                market_rent=450000.0,
                occupancy_rate=90.0,
                walb=3.0,
                walt=5.0,
                acquisition_price=6000000.0,
                notary_fees=300000.0,
                financing_amount=4800000.0,
                ltv=75.0,
                interest_rate=3.8,
                loan_duration=15,
                technical_score=8.0,
                risk_score=6.0
            ),
            Project(
                user_id=user.id,
                name="Résidence Mixte Marseille",
                description="Immeuble mixte habitation + commerces",
                address="Cours Julien",
                city="Marseille",
                postal_code="13006",
                project_type="mixed",
                status="in_progress",
                strategy="value_add",
                bp_duration=7,
                asset_type="mixed",
                surface=3000.0,
                purchase_price=4000000.0,
                renovation_budget=600000.0,
                estimated_value=5200000.0,
                current_rent=280000.0,
                market_rent=320000.0,
                occupancy_rate=85.0,
                walb=3.2,
                walt=4.8,
                acquisition_price=4000000.0,
                notary_fees=200000.0,
                financing_amount=3200000.0,
                ltv=80.0,
                interest_rate=4.2,
                loan_duration=12,
                technical_score=7.5,
                risk_score=7.0
            )
        ]
        
        for project in projects:
            session.add(project)
        
        await session.commit()
        print(f"✅ {len(projects)} projets de test créés avec succès!")

if __name__ == "__main__":
    asyncio.run(create_test_projects())
