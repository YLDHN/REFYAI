#!/usr/bin/env python3
"""
Script pour créer des projets de test dans la base de données
"""
import asyncio
import sys
sys.path.insert(0, '/Users/yld/Documents/REFYAI/backend')

from app.core.database import AsyncSessionLocal
from app.models.project import Project
from datetime import datetime
import uuid

async def create_test_projects():
    """Crée plusieurs projets de test"""
    async with AsyncSessionLocal() as db:
        
        projects = [
            {
                "name": "Immeuble Haussmannien Paris 8",
                "address": "45 Avenue des Champs-Élysées",
                "city": "Paris",
                "postal_code": "75008",
                "typologie": "IMMEUBLE",
                "surface_totale": 450.0,
                "prix_acquisition": 2500000.0,
                "status": "En cours",
                "tri_avant_is": 0.18,
                "van_avant_is": 350000.0,
                "score_technique": 0.85,
                "score_bloquant": 0,
            },
            {
                "name": "Appartement T3 Lyon",
                "address": "12 Rue de la République",
                "city": "Lyon",
                "postal_code": "69002",
                "typologie": "APPARTEMENT",
                "surface_totale": 85.0,
                "prix_acquisition": 350000.0,
                "status": "En cours",
                "tri_avant_is": 0.12,
                "van_avant_is": 45000.0,
                "score_technique": 0.72,
                "score_bloquant": 1,
            },
            {
                "name": "Commerce Marseille Centre",
                "address": "78 La Canebière",
                "city": "Marseille",
                "postal_code": "13001",
                "typologie": "COMMERCE",
                "surface_totale": 200.0,
                "prix_acquisition": 650000.0,
                "status": "Terminé",
                "tri_avant_is": 0.22,
                "van_avant_is": 180000.0,
                "score_technique": 0.92,
                "score_bloquant": 0,
            },
            {
                "name": "Maison Bordeaux",
                "address": "34 Rue Sainte-Catherine",
                "city": "Bordeaux",
                "postal_code": "33000",
                "typologie": "MAISON",
                "surface_totale": 180.0,
                "prix_acquisition": 580000.0,
                "status": "En cours",
                "tri_avant_is": 0.09,
                "van_avant_is": -20000.0,
                "score_technique": 0.58,
                "score_bloquant": 2,
            },
            {
                "name": "Bureau La Défense",
                "address": "Tour CB21, Esplanade du Général de Gaulle",
                "city": "Courbevoie",
                "postal_code": "92400",
                "typologie": "BUREAU",
                "surface_totale": 750.0,
                "prix_acquisition": 4200000.0,
                "status": "En cours",
                "tri_avant_is": 0.15,
                "van_avant_is": 520000.0,
                "score_technique": 0.88,
                "score_bloquant": 0,
            },
        ]
        
        try:
            from sqlalchemy import select
            
            for project_data in projects:
                # Vérifier si un projet avec le même nom existe déjà
                result = await db.execute(
                    select(Project).filter(Project.name == project_data["name"])
                )
                existing = result.scalar_one_or_none()
                
                if existing:
                    print(f"⏭️  Projet '{project_data['name']}' existe déjà")
                    continue
                
                project = Project(
                    id=str(uuid.uuid4()),
                    created_at=datetime.utcnow(),
                    **project_data
                )
                db.add(project)
                print(f"✅ Projet créé: {project_data['name']}")
            
            await db.commit()
            print(f"\n🎉 Projets de test créés avec succès!")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            await db.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(create_test_projects())
