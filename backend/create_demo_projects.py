"""
Script pour créer des projets pour l'utilisateur demo
"""
import asyncio
from app.core.database import AsyncSessionLocal
from app.models.project import Project
from sqlalchemy import select
from app.models.user import User

async def create_demo_projects():
    async with AsyncSessionLocal() as session:
        # Trouver l'utilisateur demo
        result = await session.execute(select(User).where(User.email == "demo@refyai.com"))
        user = result.scalar_one_or_none()
        
        if not user:
            print("❌ Utilisateur demo non trouvé")
            return
        
        print(f"✓ Utilisateur trouvé: {user.email} (ID: {user.id})")
        
        # Projets de démonstration
        projects = [
            Project(
                user_id=user.id,
                name="Tour de Bureaux - La Défense",
                description="Immeuble de bureaux premium avec vue sur Paris",
                address="1 Parvis de La Défense",
                city="Puteaux",
                postal_code="92800",
                project_type="rental",
                status="in_progress",
                strategy="core",
                bp_duration=15,
                asset_type="office",
                surface=3500.0,
                purchase_price=15000000.0,
                renovation_budget=1000000.0,
                estimated_value=17000000.0,
                current_rent=800000.0,
                market_rent=850000.0,
                occupancy_rate=98.0,
                walb=5.5,
                walt=8.2,
                acquisition_price=15000000.0,
                notary_fees=750000.0,
                financing_amount=10500000.0,
                ltv=70.0,
                interest_rate=3.1,
                loan_duration=20,
                technical_score=9.5,
                risk_score=3.8
            ),
            Project(
                user_id=user.id,
                name="Résidence Étudiante Lyon",
                description="Résidence moderne de 120 studios meublés",
                address="Avenue Jean Jaurès",
                city="Lyon",
                postal_code="69007",
                project_type="rental",
                status="completed",
                strategy="core_plus",
                bp_duration=10,
                asset_type="residential",
                surface=2800.0,
                purchase_price=7000000.0,
                renovation_budget=500000.0,
                estimated_value=8000000.0,
                current_rent=450000.0,
                market_rent=480000.0,
                occupancy_rate=100.0,
                walb=1.0,
                walt=1.0,
                acquisition_price=7000000.0,
                notary_fees=350000.0,
                financing_amount=5600000.0,
                ltv=80.0,
                interest_rate=3.6,
                loan_duration=15,
                technical_score=8.8,
                risk_score=5.2
            ),
            Project(
                user_id=user.id,
                name="Centre Commercial Bordeaux",
                description="Galerie commerciale en centre-ville rénové",
                address="Rue Sainte-Catherine",
                city="Bordeaux",
                postal_code="33000",
                project_type="rental",
                status="in_progress",
                strategy="value_add",
                bp_duration=8,
                asset_type="retail",
                surface=4500.0,
                purchase_price=10000000.0,
                renovation_budget=2000000.0,
                estimated_value=13000000.0,
                current_rent=600000.0,
                market_rent=750000.0,
                occupancy_rate=85.0,
                walb=2.8,
                walt=4.5,
                acquisition_price=10000000.0,
                notary_fees=500000.0,
                financing_amount=8000000.0,
                ltv=75.0,
                interest_rate=4.1,
                loan_duration=12,
                technical_score=7.6,
                risk_score=6.8
            ),
        ]
        
        for project in projects:
            session.add(project)
        
        await session.commit()
        print(f"✅ {len(projects)} projets créés pour {user.email}!")

if __name__ == "__main__":
    asyncio.run(create_demo_projects())
