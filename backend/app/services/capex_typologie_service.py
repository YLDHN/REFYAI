"""
Extension du service CAPEX pour les 3 typologies spécifiques du Business Plan:
- HABITATION
- BUREAUX
- COMMERCE

Chaque typologie a une liste de postes spécifiques selon le PDF BP.
"""
from typing import Dict, List
from app.services.capex_service import capex_service


class CAPEXTypology:
    """Typologies de projets selon Business Plan"""
    HABITATION = "habitation"
    BUREAUX = "bureaux"
    COMMERCE = "commerce"


# ===== TYPOLOGIE: HABITATION =====
CAPEX_HABITATION_TEMPLATE = [
    # Aménagement du terrain
    {"key": "vrd_raccordement_eau", "label": "Raccordement eau", "default_quantity": 50},
    {"key": "vrd_assainissement", "label": "Raccordement égoût / Redevance", "default_quantity": 50},
    
    # Démolition / Désamiantage
    {"key": "demolition_legere", "label": "Démolition légère", "default_quantity": 100},
    {"key": "desamiantage", "label": "Désamiantage diagnostiqué", "default_quantity": 200},
    
    # VRD
    {"key": "vrd_voirie", "label": "VRD parking et voirie", "default_quantity": 150},
    {"key": "vrd_raccordement_concessionnaires", "label": "Concessionnaires (Electricité, Gaz)", "default_quantity": 1},
    
    # Travaux Gros Œuvre
    {"key": "structure_reprise_fondations", "label": "Reprise fondations si nécessaire", "default_quantity": 10},
    {"key": "structure_reprise_planchers", "label": "Reprise planchers", "default_quantity": 100},
    {"key": "facade_ravalement_pierre", "label": "Ravalement façade", "default_quantity": 300},
    {"key": "toiture_refection_complete", "label": "Réfection toiture", "default_quantity": 200},
    {"key": "isolation_murs_interieurs", "label": "Isolation thermique", "default_quantity": 400},
    
    # Second Œuvre
    {"key": "menuiseries_fenetres_pvc", "label": "Menuiseries extérieures (fenêtres)", "default_quantity": 20},
    {"key": "cloisons_placo", "label": "Cloisons intérieures", "default_quantity": 150},
    {"key": "electricite_renovation_complete", "label": "Electricité (rénovation complète)", "default_quantity": 400},
    {"key": "plomberie_renovation_complete", "label": "Plomberie (rénovation complète)", "default_quantity": 400},
    {"key": "chauffage_pompe_chaleur", "label": "Chauffage (pompe à chaleur)", "default_quantity": 1},
    {"key": "revetements_carrelage", "label": "Revêtements sols (carrelage)", "default_quantity": 200},
    {"key": "revetements_peinture", "label": "Peinture", "default_quantity": 800},
    
    # Cuisine / SdB
    {"key": "cuisine_equipee_standard", "label": "Cuisines équipées", "default_quantity": 15},
    {"key": "salle_bain_complete_standard", "label": "Salles de bain complètes", "default_quantity": 6},
    
    # Equipements communs
    {"key": "ascenseur_installation", "label": "Ascenseur (si applicable)", "default_quantity": 1},
    {"key": "securite_detecteurs", "label": "Sécurité incendie (détecteurs)", "default_quantity": 10},
    {"key": "pmr_rampe_acces", "label": "Accessibilité PMR (rampe)", "default_quantity": 1},
    
    # Aléas travaux
    {"key": "aleas_travaux", "label": "Aléas travaux (10%)", "is_percentage": True, "default_rate": 0.10},
    
    # Honoraires techniques
    {"key": "honoraires_architecte", "label": "Maîtrise d'Œuvre (Architecte)", "is_percentage": True, "default_rate": 0.12},
    {"key": "etudes_structure", "label": "BET Structure", "default_quantity": 1},
    {"key": "etudes_thermique", "label": "Audit énergétique", "default_quantity": 1},
    {"key": "assurances_dommages_ouvrage", "label": "Assurances (Dommages-Ouvrage)", "is_percentage": True, "default_rate": 0.03},
    
    # Honoraires de gestion
    {"key": "hono_gestion_copro", "label": "SAV / Gestion des copropriétés", "default_quantity": 1},
    {" key": "hono_mod", "label": "MOD (honoraires de montage)", "default_quantity": 1},
]


# ===== TYPOLOGIE: BUREAUX =====
CAPEX_BUREAUX_TEMPLATE = [
    # Aménagement du terrain
    {"key": "vrd_raccordement_eau", "label": "Raccordement eau", "default_quantity": 30},
    {"key": "vrd_assainissement", "label": "Raccordement égoût", "default_quantity": 30},
    
    # Commissions et taxes
    {"key": "commission_plu", "label": "Commission PLU", "default_quantity": 1},
    {"key": "taxe_creation_bureaux", "label": "Taxe Création Bureaux", "is_percentage": True, "default_rate": 0.02},
    
    # Démolition
    {"key": "demolition_legere", "label": "Démolition / Curage", "default_quantity": 200},
    {"key": "desamiantage", "label": "Désamiantage (diagnostiqué)", "default_quantity": 150},
    
    # VRD
    {"key": "vrd_voirie", "label": "VRD parking et voirie", "default_quantity": 200},
    {"key": "vrd_raccordement_concessionnaires", "label": "Concessionnaires (puissance augmentée)", "default_quantity": 1},
    
    # Travaux Gros Œuvre
    {"key": "structure_reprise_planchers", "label": "Reprise planchers (charges bureaux)", "default_quantity": 300},
    {"key": "facade_ravalement_simple", "label": "Ravalement façade", "default_quantity": 400},
    {"key": "toiture_refection_complete", "label": "Étanchéité toiture", "default_quantity": 250},
    {"key": "isolation_murs_interieurs", "label": "Isolation thermique ITE/ITI", "default_quantity": 600},
    
    # Second Œuvre
    {"key": "menuiseries_fenetres_alu", "label": "Menuiseries aluminium", "default_quantity": 40},
    {"key": "cloisons_placo", "label": "Cloisons (plateau flexible)", "default_quantity": 200},
    {"key": "electricite_renovation_complete", "label": "Electricité tertiaire", "default_quantity": 600},
    {"key": "plomberie_renovation_complete", "label": "Plomberie (sanitaires communs)", "default_quantity": 600},
    {"key": "chauffage_pompe_chaleur", "label": "CVC (Chauffage/Ventilation/Clim)", "default_quantity": 2},
    {"key": "revetements_carrelage", "label": "Revêtements sols techniques", "default_quantity": 400},
    {"key": "revetements_peinture", "label": "Peinture", "default_quantity": 1200},
    
    # Equipements spécifiques
    {"key": "ascenseur_installation", "label": "Ascenseur(s)", "default_quantity": 2},
    {"key": "securite_incendie_erp", "label": "Sécurité Incendie ERP", "default_quantity": 1},
    {"key": "pmr_sanitaires_adaptes", "label": "Accessibilité PMR", "default_quantity": 2},
    {"key": "cablage_reseau", "label": "Câblage réseau informatique", "default_quantity": 600},
    
    # Aléas
    {"key": "aleas_travaux", "label": "Aléas travaux (10%)", "is_percentage": True, "default_rate": 0.10},
    
    # Honoraires techniques
    {"key": "honoraires_architecte", "label": "Maîtrise d'Œuvre", "is_percentage": True, "default_rate": 0.12},
    {"key": "etudes_structure", "label": "BET Structure", "default_quantity": 1},
    {"key": "etudes_thermique", "label": "BET Fluides/CVC", "default_quantity": 1},
    {"key": "assurances_dommages_ouvrage", "label": "Assurances DO", "is_percentage": True, "default_rate": 0.03},
    
    # Honoraires gestion
    {"key": "hono_mod", "label": "MOD (honoraires de montage)", "default_quantity": 1},
    {"key": "hono_commercialisation", "label": "Honoraires de commercialisation", "is_percentage": True, "default_rate": 0.05},
]


# ===== TYPOLOGIE: COMMERCE =====
CAPEX_COMMERCE_TEMPLATE = [
    # Aménagement du terrain
    {"key": "vrd_raccordement_eau", "label": "Raccordement eau", "default_quantity": 20},
    {"key": "vrd_assainissement", "label": "Raccordement égoût / Redevance", "default_quantity": 20},
    
    # Commissions et taxes
    {"key": "commission_plu", "label": "Commission PLU", "default_quantity": 1},
    {"key": "taxe_creation_bureaux", "label": "Taxe Création Bureaux-Commerces", "is_percentage": True, "default_rate": 0.015},
    
    # Démolition
    {"key": "demolition_depose_enseignes", "label": "Démolition / Dépose d'enseignes et vitrines", "default_quantity": 50},
    {"key": "sondages_accessibilite", "label": "Sondages (accessibilité PMR)", "default_quantity": 1},
    
    # VRD
    {"key": "vrd_voirie", "label": "VRD parkings clients et signalétique", "default_quantity": 100},
    {"key": "vrd_raccordement_concessionnaires", "label": "Concessionnaires (Puissance électrique augmentée)", "default_quantity": 1},
    
    # Travaux
    {"key": "facade_vitrines", "label": "Rénovation façades et vitrines (linéaire marchand)", "default_quantity": 30},
    {"key": "amenagement_brut_beton", "label": "Aménagement intérieur (Brut de béton / Fluides en attente)", "default_quantity": 200},
    {"key": "extraction_technique", "label": "Extraction technique (indispensable pour restauration)", "default_quantity": 1},
    {"key": "mise_normes_pmr", "label": "Mise aux normes Accessibilité PMR", "default_quantity": 200},
    {"key": "securite_incendie_erp", "label": "Sécurité Incendie ERP", "default_quantity": 1},
    {"key": "eclairage_enseignes", "label": "Éclairage enseignes et extérieur", "default_quantity": 10},
    
    # Aléas
    {"key": "aleas_copro", "label": "Aléas travaux (contraintes de copropriété)", "is_percentage": True, "default_rate": 0.12},
    
    # Honoraires techniques
    {"key": "honoraires_architecte_retail", "label": "Maîtrise d'Œuvre (Architecte spécialisé Retail)", "is_percentage": True, "default_rate": 0.10},
    {"key": "etudes_thermique", "label": "Audit énergétique et accessibilité", "default_quantity": 1},
    {"key": "bet_securite", "label": "Contrôleur technique (Solidité et Sécurité Incendie)", "default_quantity": 1},
    {"key": "assurances_dommages_ouvrage", "label": "Assurances (Dommages-Ouvrage)", "is_percentage": True, "default_rate": 0.03},
    {"key": "geometre", "label": "Géomètre (Copro / État descriptif de division)", "default_quantity": 1},
    {"key": "bet_cuisine_extraction", "label": "BET Cuisine / Extraction (si applicable)", "default_quantity": 1},
    
    # Honoraires gestion et commercialisation
    {"key": "hono_gestion_copro", "label": "SAV / Gestion des copropriétés", "default_quantity": 1},
    {"key": "hono_mod", "label": "MOD (honoraires de montage)", "default_quantity": 1},
    {"key": "dossier_enseigne", "label": "Montage des dossiers d'enseigne (Mairie)", "default_quantity": 1},
    {"key": "marketing_lancement", "label": "Publicité et marketing de lancement", "default_quantity": 1},
    {"key": "gestion_evictions", "label": "Gestion des évictions ou renouvellements", "default_quantity": 1},
    {"key": "hono_commercialisation", "label": "Honoraires de commercialisation (Droit au bail)", "is_percentage": True, "default_rate": 0.08},
    {"key": "aides_vente", "label": "Aides à la vente (Franchises travaux)", "is_percentage": True, "default_rate": 0.05},
]


def get_typologie_template(typologie: str) -> List[Dict]:
    """
    Obtenir le template CAPEX pour une typologie
    
    Args:
        typologie: "habitation", "bureaux", ou "commerce"
    
    Returns:
        Liste des postes CAPEX pour cette typologie
    """
    typologie_lower = typologie.lower()
    
    if typologie_lower == CAPEXTypology.HABITATION:
        return CAPEX_HABITATION_TEMPLATE
    elif typologie_lower == CAPEXTypology.BUREAUX:
        return CAPEX_BUREAUX_TEMPLATE
    elif typologie_lower == CAPEXTypology.COMMERCE:
        return CAPEX_COMMERCE_TEMPLATE
    else:
        # Fallback: retourner template générique
        return CAPEX_HABITATION_TEMPLATE


def estimate_capex_by_typologie(
    typologie: str,
    surface: float,
    city_tier: int = 1,
    construction_year: int = 2000,
    project_description: str = ""
) -> Dict:
    """
    Estimation CAPEX automatique selon typologie BP
    
    Args:
        typologie: "habitation", "bureaux", "commerce"
        surface: Surface en m²
        city_tier: Tier ville (1, 2, 3)
        construction_year: Année de construction
        project_description: Description additionnelle
    
    Returns:
        Estimation détaillée par poste
    """
    template = get_typologie_template(typologie)
    
    # Calculer quantités estimées selon surface
    items_with_quantities = []
    
    for poste in template:
        # Ignorer les postes en pourcentage pour l'instant (seront calculés après)
        if poste.get("is_percentage"):
            continue
        
        # Estimer quantité selon surface et type de poste
        quantity = _estimate_quantity(poste, surface)
        
        items_with_quantities.append({
            "key": poste["key"],
            "label": poste["label"],
            "quantity": quantity
        })
    
    # Calculer via service existant
    result = capex_service.calculate_project_capex(
        items_with_quantities,
        city_tier=city_tier,
        contingency_rate=0.10
    )
    
    # Ajouter métadonnées typologie
    result["typologie"] = typologie
    result["surface_m2"] = surface
    result["cost_per_m2"] = result["project_capex"]["total_with_contingency"]["avg"] / surface if surface > 0 else 0
    
    return result


def _estimate_quantity(poste: Dict, surface: float) -> float:
    """Estimer quantité d'un poste selon surface projet"""
    key = poste["key"]
    default_qty = poste.get("default_quantity", 1)
    
    # Logique d'estimation simple (à affiner avec IA)
    if "m2" in key or "surface" in key.lower():
        # Postes au m² = surface totale
        return surface
    elif "ml" in key or "lineaire" in key.lower():
        # Linéaire = périmètre estimé
        return max(surface ** 0.5 * 4, default_qty)
    elif "unite" in key or "installation" in key.lower():
        # Unités = ratio surface / seuil
        if surface < 300:
            return 1
        elif surface < 800:
            return default_qty
        else:
            return default_qty * 2
    else:
        return default_qty
