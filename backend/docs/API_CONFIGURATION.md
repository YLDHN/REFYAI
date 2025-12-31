# Configuration APIs externes

## 1. API DVF (Demande de Valeurs Foncières)

### Endpoint officiel
```
https://api.cquest.org/dvf
```

### Documentation
- https://github.com/cquest/dvf_as_api
- https://app.dvf.etalab.gouv.fr/

### Exemple requête
```bash
# Par commune
GET https://api.cquest.org/dvf?code_commune=75101&type_local=Appartement

# Par coordonnées géographiques
GET https://api.cquest.org/dvf?lat=48.8566&lon=2.3522&dist=1000

# Avec filtres
GET https://api.cquest.org/dvf?code_commune=75101&nature_mutation=Vente&type_local=Appartement
```

### Paramètres disponibles
- `code_commune`: Code INSEE commune (ex: 75101 pour Paris 1er)
- `code_postal`: Code postal
- `lat` / `lon`: Coordonnées GPS
- `dist`: Rayon de recherche en mètres (défaut 500m)
- `type_local`: Appartement, Maison, Local commercial, etc.
- `nature_mutation`: Vente, Vente en l'état futur d'achèvement, etc.
- `date_debut` / `date_fin`: Période (format YYYY-MM-DD)

### Réponse exemple
```json
{
  "resultats": [
    {
      "id_mutation": "2023-12345",
      "date_mutation": "2023-06-15",
      "numero_disposition": "000001",
      "nature_mutation": "Vente",
      "valeur_fonciere": 450000,
      "adresse_numero": "10",
      "adresse_nom_voie": "RUE DE LA PAIX",
      "code_postal": "75001",
      "code_commune": "75101",
      "nom_commune": "PARIS",
      "type_local": "Appartement",
      "surface_reelle_bati": 85,
      "nombre_pieces_principales": 3,
      "surface_terrain": null,
      "longitude": 2.3305,
      "latitude": 48.8698
    }
  ]
}
```

---

## 2. API Euribor (Taux d'intérêt)

### Option 1: API ECB (Banque Centrale Européenne) - GRATUITE
```
https://data-api.ecb.europa.eu/service/data/
```

### Documentation
- https://data.ecb.europa.eu/help/api/overview

### Exemple requête Euribor 3 mois
```bash
GET https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.RT.MM.EURIBOR3MD_.HSTA?format=jsondata&lastNObservations=1
```

### Paramètres
- `D`: Daily (quotidien)
- `U2`: Euro area
- `EUR`: Euro
- `EURIBOR3MD_`: Euribor 3 mois
- `EURIBOR6MD_`: Euribor 6 mois
- `EURIBOR12MD_`: Euribor 12 mois

### Réponse exemple
```json
{
  "dataSets": [{
    "series": {
      "0:0:0:0:0:0:0": {
        "observations": {
          "0": [3.654]
        }
      }
    }
  }],
  "structure": {
    "dimensions": {
      "observation": [{
        "id": "TIME_PERIOD",
        "values": [{
          "id": "2025-12-31",
          "name": "2025-12-31"
        }]
      }]
    }
  }
}
```

### Option 2: API Alternative - Financial Modeling Prep (Freemium)
```
https://financialmodelingprep.com/api/v4/treasury?maturity=3month
```

### Option 3: Scraping fallback (si APIs down)
- https://www.euribor-rates.eu/en/current-euribor-rates/
- Parser la page HTML pour extraire taux actuel

---

## 3. Configuration dans le code

### Fichier .env
```env
# API DVF
DVF_API_URL=https://api.cquest.org/dvf
DVF_API_KEY=  # Pas de clé requise pour API publique

# API Euribor (ECB)
EURIBOR_API_URL=https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.RT.MM
EURIBOR_API_KEY=  # Pas de clé requise

# Fallback taux si API indisponible
EURIBOR_FALLBACK_RATE=3.45
```

### Update dvf_service.py
```python
# Remplacer
DVF_API_URL = "https://api.cquest.org/dvf"

# Dans get_comparable_sales()
url = f"{self.api_url}?code_commune={code_commune}&type_local={property_type}&dist={radius}"
```

### Update interest_rate_service.py
```python
# Remplacer
ECB_API_URL = "https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.RT.MM"

# Dans get_current_euribor()
if maturity == 3:
    url = f"{self.ecb_api_url}.EURIBOR3MD_.HSTA?format=jsondata&lastNObservations=1"
elif maturity == 6:
    url = f"{self.ecb_api_url}.EURIBOR6MD_.HSTA?format=jsondata&lastNObservations=1"
```

---

## 4. Codes INSEE communes principales

```python
INSEE_CODES = {
    "Paris": "75056",
    "Lyon": "69123",
    "Marseille": "13055",
    "Toulouse": "31555",
    "Nice": "06088",
    "Nantes": "44109",
    "Montpellier": "34172",
    "Strasbourg": "67482",
    "Bordeaux": "33063",
    "Lille": "59350"
}
```

---

## 5. Limites et quotas

### API DVF
- ✅ Gratuite et sans limite
- ✅ Données officielles gouvernement
- ⚠️ Données jusqu'à 5 ans en arrière
- ⚠️ Délai de publication ~6 mois

### API ECB
- ✅ Gratuite et sans clé API
- ✅ Données officielles BCE
- ⚠️ Rate limit: 100 req/10 sec
- ✅ Historique complet

---

## 6. Gestion des erreurs

### Stratégie fallback
1. Essayer API principale
2. Si échec, essayer API alternative
3. Si échec, utiliser valeur par défaut en cache
4. Logger l'erreur pour monitoring

### Exemple code
```python
async def get_euribor_with_fallback(self, maturity: int = 3) -> float:
    try:
        # Essayer API ECB
        rate = await self._fetch_from_ecb(maturity)
        if rate:
            return rate
    except Exception as e:
        logger.warning(f"ECB API failed: {e}")
    
    try:
        # Essayer scraping
        rate = await self._scrape_euribor_rates()
        if rate:
            return rate
    except Exception as e:
        logger.warning(f"Scraping failed: {e}")
    
    # Fallback valeur par défaut
    return settings.EURIBOR_FALLBACK_RATE
```

---

## 7. Mise en cache

### Redis recommandé
```python
# Cache DVF 7 jours
@cache(expire=604800)
async def get_comparable_sales(...):
    pass

# Cache Euribor 24h
@cache(expire=86400)
async def get_current_euribor(...):
    pass
```

---

## 8. Tests

### Test DVF
```bash
curl "https://api.cquest.org/dvf?code_commune=75056&type_local=Appartement" | jq
```

### Test Euribor
```bash
curl "https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.RT.MM.EURIBOR3MD_.HSTA?format=jsondata&lastNObservations=1" | jq
```

---

## 9. Prochaines étapes

1. ✅ Ajouter URLs dans .env
2. ✅ Update dvf_service.py avec vraie API
3. ✅ Update interest_rate_service.py avec ECB
4. ✅ Ajouter gestion erreurs + fallback
5. ✅ Implémenter cache Redis
6. ✅ Tests d'intégration
7. ✅ Monitoring + alertes si API down
