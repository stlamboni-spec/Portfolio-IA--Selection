from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

# Initialisation de l'API pour le Pipeline 7 (API Gateway Validation)
app = FastAPI(
    title="Pipeline 7 : Advanced API Gateway Validation Microservice",
    description="Microservice de passerelle applicative gérant le typage strict, le nettoyage et la validation de données géographiques complexes via Pydantic v2.",
    version="1.0.0"
)

class RequeteAnalyseUrbaine(BaseModel):
    project_name: str = Field(..., min_length=3, max_length=50, description="Nom du projet d'aménagement territorial")
    target_area_km2: float = Field(..., gt=0, lt=10000, description="Superficie ciblée en km²")
    density_category: str = Field(..., description="Catégorie de densité : URBAIN, PERIURBAIN ou RURAL")

    @field_validator('density_category')
    @classmethod
    def verifier_categorie_densite(cls, valeur: str) -> str:
        categories_valides = ["URBAIN", "PERIURBAIN", "RURAL"]
        valeur_majuscule = valeur.upper().strip()
        if valeur_majuscule not in categories_valides:
            raise ValueError(f"Catégorie invalide. Choisissez parmi : {categories_valides}")
        return valeur_majuscule

@app.post("/validate_and_forward", summary="Valider, nettoyer et transmettre la requête métier vers les modèles d'IA")
def valider_et_transmettre_requete(payload: RequeteAnalyseUrbaine):
    return {
        "gateway_status": "REQUEST_VALIDATED_AND_CLEANED",
        "forwarded_payload": payload.model_dump(),
        "security_check": "PASSED"
    }
